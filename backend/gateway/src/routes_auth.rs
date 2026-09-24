use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use serde::{Deserialize, Serialize};
use sqlx::FromRow;
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2,
};
use uuid::Uuid;

use crate::auth::create_token;

#[derive(Deserialize)]
pub struct AuthPayload {
    pub email: String,
    pub password: String,
}

#[derive(Serialize)]
pub struct AuthResponse {
    pub token: String,
    pub user_id: String,
}

#[derive(FromRow)]
struct UserRecord {
    id: Uuid,
    password_hash: String,
}

pub async fn register(
    State(state): State<crate::AppState>,
    Json(payload): Json<AuthPayload>,
) -> impl IntoResponse {
    let pool = state.db;
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    let password_hash = match argon2.hash_password(payload.password.as_bytes(), &salt) {
        Ok(hash) => hash.to_string(),
        Err(_) => return (StatusCode::INTERNAL_SERVER_ERROR, "Failed to hash password").into_response(),
    };

    let user_id = Uuid::new_v4();

    let result = sqlx::query(
        "INSERT INTO users (id, email, password_hash) VALUES ($1, $2, $3)"
    )
    .bind(user_id)
    .bind(&payload.email)
    .bind(&password_hash)
    .execute(&pool)
    .await;

    match result {
        Ok(_) => {
            let token = create_token(&user_id.to_string()).unwrap();
            (StatusCode::CREATED, Json(AuthResponse { token, user_id: user_id.to_string() })).into_response()
        }
        Err(e) => {
            tracing::error!("Database insertion error: {:?}", e);
            if e.to_string().contains("duplicate key value") {
                (StatusCode::CONFLICT, "Email already exists").into_response()
            } else {
                (StatusCode::INTERNAL_SERVER_ERROR, format!("Database error: {}", e)).into_response()
            }
        }
    }
}

pub async fn login(
    State(state): State<crate::AppState>,
    Json(payload): Json<AuthPayload>,
) -> impl IntoResponse {
    let pool = state.db;
    let record = sqlx::query_as::<_, UserRecord>(
        "SELECT id, password_hash FROM users WHERE email = $1"
    )
    .bind(&payload.email)
    .fetch_optional(&pool)
    .await;

    match record {
        Ok(Some(user)) => {
            let parsed_hash = PasswordHash::new(&user.password_hash).unwrap();
            if Argon2::default().verify_password(payload.password.as_bytes(), &parsed_hash).is_ok() {
                let token = create_token(&user.id.to_string()).unwrap();
                (StatusCode::OK, Json(AuthResponse { token, user_id: user.id.to_string() })).into_response()
            } else {
                (StatusCode::UNAUTHORIZED, "Invalid password").into_response()
            }
        }
        Ok(None) => (StatusCode::UNAUTHORIZED, "User not found").into_response(),
        Err(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Database error").into_response(),
    }
}
