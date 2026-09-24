use axum::{
    extract::{Multipart, Path, State},
    http::{StatusCode, HeaderMap},
    response::IntoResponse,
    Json,
};
use serde_json::json;
use std::fs;
use uuid::Uuid;

use crate::core::dataframe::{
    extract_schema_from_csv, clean_dataset, convert_xlsx_to_csv,
    get_dataset_preview_json, extract_columns_json,
};

// Directory to store uploaded files temporarily (would use S3/Blob storage in prod)
const UPLOAD_DIR: &str = "./uploads";

pub async fn upload_dataset(
    State(state): State<crate::AppState>,
    headers: HeaderMap,
    mut multipart: Multipart,
) -> impl IntoResponse {
    // Extract user_id from headers (set by Gateway)
    let user_id_str = match headers.get("X-User-Id").and_then(|v| v.to_str().ok()) {
        Some(uid) => uid,
        None => return (StatusCode::UNAUTHORIZED, Json(json!({"error": "Missing X-User-Id"}))).into_response(),
    };
    
    let user_id = match Uuid::parse_str(user_id_str) {
        Ok(uid) => uid,
        Err(_) => return (StatusCode::BAD_REQUEST, Json(json!({"error": "Invalid user ID"}))).into_response(),
    };

    // Create uploads directory if it doesn't exist
    fs::create_dir_all(UPLOAD_DIR).unwrap_or_default();

    let mut dataset_id = String::new();
    let mut file_path = String::new();
    let mut original_name = String::new();
    let mut is_xlsx = false;

    while let Some(field) = multipart.next_field().await.unwrap_or(None) {
        if field.name() == Some("file") {
            original_name = field.file_name().unwrap_or("dataset.csv").to_string();
            let file_name = original_name.to_lowercase();
            let data = field.bytes().await.unwrap();
            
            let id = Uuid::new_v4().to_string();
            dataset_id = id.clone();
            
            is_xlsx = file_name.ends_with(".xlsx");
            let ext = if is_xlsx { ".xlsx" } else { ".csv" };
            file_path = format!("{}/{}{}", UPLOAD_DIR, id, ext);
            
            fs::write(&file_path, &data).unwrap();
            break;
        }
    }

    if dataset_id.is_empty() {
        return (
            StatusCode::BAD_REQUEST,
            Json(json!({"error": "No file field found in multipart form"})),
        ).into_response();
    }

    let csv_path = if is_xlsx {
        let converted_path = format!("{}/{}.csv", UPLOAD_DIR, dataset_id);
        if let Err(e) = convert_xlsx_to_csv(&file_path, &converted_path) {
            return (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(json!({"error": format!("Failed to convert XLSX to CSV: {}", e)})),
            ).into_response();
        }
        converted_path
    } else {
        file_path.clone()
    };

    // Attempt to parse schema immediately
    match extract_schema_from_csv(&csv_path, &dataset_id) {
        Ok(schema) => {
            let schema_json = serde_json::to_value(&schema).unwrap();
            let d_id = Uuid::parse_str(&dataset_id).unwrap();
            
            // Save to PostgreSQL
            let result = sqlx::query(
                "INSERT INTO datasets (id, user_id, original_name, storage_path, schema) VALUES ($1, $2, $3, $4, $5)"
            )
            .bind(d_id)
            .bind(user_id)
            .bind(&original_name)
            .bind(&csv_path)
            .bind(&schema_json)
            .execute(&state.db)
            .await;
            
            if let Err(e) = result {
                return (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    Json(json!({"error": format!("Failed to save dataset metadata: {}", e)})),
                ).into_response();
            }

            (
                StatusCode::OK,
                Json(json!({
                    "status": "success",
                    "dataset_id": dataset_id,
                    "schema": schema
                })),
            ).into_response()
        },
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(json!({"error": format!("Failed to parse CSV: {}", e)})),
        ).into_response()
    }
}

pub async fn get_schema(Path(dataset_id): Path<String>) -> impl IntoResponse {
    let file_path = format!("{}/{}.csv", UPLOAD_DIR, dataset_id);
    
    if !std::path::Path::new(&file_path).exists() {
        return (
            StatusCode::NOT_FOUND,
            Json(json!({"error": "Dataset not found"})),
        );
    }

    match extract_schema_from_csv(&file_path, &dataset_id) {
        Ok(schema) => (
            StatusCode::OK,
            Json(json!({"status": "success", "schema": schema})),
        ),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(json!({"error": format!("Failed to parse CSV schema: {}", e)})),
        )
    }
}

pub async fn clean_data(Path(dataset_id): Path<String>) -> impl IntoResponse {
    let file_path = format!("{}/{}.csv", UPLOAD_DIR, dataset_id);
    let out_path = format!("{}/{}_cleaned.csv", UPLOAD_DIR, dataset_id);
    
    if !std::path::Path::new(&file_path).exists() {
        return (
            StatusCode::NOT_FOUND,
            Json(json!({"error": "Dataset not found"})),
        );
    }

    match clean_dataset(&file_path, &out_path) {
        Ok(rows) => (
            StatusCode::OK,
            Json(json!({"status": "success", "cleaned_rows": rows, "new_dataset_id": format!("{}_cleaned", dataset_id)})),
        ),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(json!({"error": format!("Failed to clean CSV: {}", e)})),
        )
    }
}

#[derive(serde::Deserialize)]
pub struct PreviewQuery {
    pub limit: Option<usize>,
}

#[derive(serde::Deserialize)]
pub struct ColumnsPayload {
    pub columns: Vec<String>,
}

pub async fn get_preview(
    Path(dataset_id): Path<String>,
    axum::extract::Query(query): axum::extract::Query<PreviewQuery>,
) -> impl IntoResponse {
    let file_path = format!("{}/{}.csv", UPLOAD_DIR, dataset_id);
    
    if !std::path::Path::new(&file_path).exists() {
        return (
            StatusCode::NOT_FOUND,
            Json(json!({"error": "Dataset not found"})),
        );
    }

    let limit = query.limit.unwrap_or(100);
    match get_dataset_preview_json(&file_path, limit) {
        Ok(records) => (
            StatusCode::OK,
            Json(json!({"status": "success", "data": records})),
        ),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(json!({"error": format!("Failed to read preview: {}", e)})),
        )
    }
}

pub async fn get_columns(
    Path(dataset_id): Path<String>,
    Json(payload): Json<ColumnsPayload>,
) -> impl IntoResponse {
    let file_path = format!("{}/{}.csv", UPLOAD_DIR, dataset_id);
    
    if !std::path::Path::new(&file_path).exists() {
        return (
            StatusCode::NOT_FOUND,
            Json(json!({"error": "Dataset not found"})),
        );
    }

    match extract_columns_json(&file_path, &payload.columns) {
        Ok(columns_data) => (
            StatusCode::OK,
            Json(json!({"status": "success", "data": columns_data})),
        ),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(json!({"error": format!("Failed to extract columns: {}", e)})),
        )
    }
}

