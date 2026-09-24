mod api;
mod core;
mod db;

use axum::{
    routing::{get, post},
    Router,
};
use std::net::SocketAddr;
use tower_http::cors::CorsLayer;
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use sqlx::{Pool, Postgres};

#[derive(Clone)]
pub struct AppState {
    pub db: Pool<Postgres>,
}

#[tokio::main]
async fn main() {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "data_service=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let db_pool = db::establish_connection().await;
    let state = AppState { db: db_pool };

    // Setup routes
    let app = Router::new()
        .route("/health", get(|| async { "Data Service OK" }))
        .route("/api/v1/data/upload", post(api::routes::upload_dataset))
        .route("/api/v1/data/schema/:dataset_id", get(api::routes::get_schema))
        .route("/api/v1/data/clean/:dataset_id", post(api::routes::clean_data))
        .route("/api/v1/data/preview/:dataset_id", get(api::routes::get_preview))
        .route("/api/v1/data/columns/:dataset_id", post(api::routes::get_columns))
        .with_state(state)
        .layer(TraceLayer::new_for_http())
        .layer(CorsLayer::permissive());

    // Bind and serve
    let port: u16 = std::env::var("PORT").ok().and_then(|p| p.parse().ok()).unwrap_or(8001);
    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    tracing::info!("listening on {}", addr);
    
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
