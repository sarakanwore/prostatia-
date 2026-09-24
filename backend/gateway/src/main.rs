mod auth;
mod db;
mod routes_auth;

use axum::{
    routing::{get, post, any},
    Router,
    extract::{Request, State},
    response::IntoResponse,
    body::Body,
};
use std::net::SocketAddr;
use tower_http::cors::CorsLayer;
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use reqwest::Client;
use sqlx::{Pool, Postgres};

use crate::auth::AuthenticatedUser;
use crate::routes_auth::{register, login};

fn get_service_url(var: &str, default: &str) -> String {
    std::env::var(var).unwrap_or_else(|_| default.to_string())
}

#[derive(Clone)]
pub struct AppState {
    pub db: Pool<Postgres>,
    pub client: Client,
}

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "gateway=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let db_pool = db::establish_connection().await;

    // Run migrations automatically at startup (graceful if already initialized)
    if let Err(e) = sqlx::migrate!("./migrations").run(&db_pool).await {
        tracing::warn!("Database migration notice: {}. Continuing startup.", e);
    }

    let ai_url   = get_service_url("AI_ORCHESTRATOR_URL", "http://localhost:8002");
    let data_url = get_service_url("DATA_SERVICE_URL",    "http://localhost:8001");
    let stats_url = get_service_url("STATS_ENGINE_URL",   "http://localhost:8000");
    let viz_url   = get_service_url("VIZ_SERVICE_URL",    "http://localhost:8003");
    let geo_url   = get_service_url("GEO_SERVICE_URL",    "http://localhost:8004");

    let client = Client::new();
    let state = AppState { db: db_pool, client };

    let app = Router::new()
        .route("/health", get(|| async { "API Gateway OK" }))
        .route("/api/v1/auth/register", post(register))
        .route("/api/v1/auth/login", post(login))
        // Protect remaining routes with Authentication
        .route("/api/v1/analyze", post({
            let url = ai_url.clone();
            move |user: AuthenticatedUser, State(state): State<AppState>, req: Request| 
                proxy_request(req, url, state.client, user)
        }))
        .route("/api/v1/detective", post({
            let url = ai_url.clone();
            move |user: AuthenticatedUser, State(state): State<AppState>, req: Request| 
                proxy_request(req, url, state.client, user)
        }))
        .route("/api/v1/data/*path", any({
            let url = data_url.clone();
            move |user: AuthenticatedUser, State(state): State<AppState>, req: Request| 
                proxy_request(req, url, state.client, user)
        }))
        .route("/api/v1/stats/*path", any({
            let url = stats_url.clone();
            move |user: AuthenticatedUser, State(state): State<AppState>, req: Request| 
                proxy_request(req, url, state.client, user)
        }))
        .route("/api/v1/viz/*path", any({
            let url = viz_url.clone();
            move |user: AuthenticatedUser, State(state): State<AppState>, req: Request| 
                proxy_request(req, url, state.client, user)
        }))
        .route("/api/v1/geo/*path", any({
            let url = geo_url.clone();
            move |user: AuthenticatedUser, State(state): State<AppState>, req: Request| 
                proxy_request(req, url, state.client, user)
        }))
        .with_state(state)
        .layer(TraceLayer::new_for_http())
        .layer(CorsLayer::permissive());

    let port: u16 = std::env::var("PORT").ok().and_then(|p| p.parse().ok()).unwrap_or(8080);
    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    tracing::info!("Gateway listening on {}", addr);
    
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn proxy_request(req: Request<axum::body::Body>, target_base_url: String, client: Client, user: AuthenticatedUser) -> impl IntoResponse {
    let path = req.uri().path();
    let query = req.uri().query().map(|q| format!("?{}", q)).unwrap_or_default();
    
    let target_url = format!("{}{}{}", target_base_url.trim_end_matches('/'), path, query);
    
    let mut proxy_req = client.request(req.method().clone(), &target_url);
    
    // Pass user_id to internal services
    proxy_req = proxy_req.header("X-User-Id", user.0);
    
    for (name, value) in req.headers() {
        if name != axum::http::header::HOST && name != axum::http::header::AUTHORIZATION {
            proxy_req = proxy_req.header(name, value);
        }
    }
    
    let bytes = axum::body::to_bytes(req.into_body(), usize::MAX).await.unwrap();
    proxy_req = proxy_req.body(bytes);
    
    let res = proxy_req.send().await.unwrap();
    
    let mut axum_res = axum::response::Response::builder()
        .status(res.status());
        
    for (name, value) in res.headers() {
        axum_res = axum_res.header(name, value);
    }
    
    let bytes = res.bytes().await.unwrap();
    axum_res.body(Body::from(bytes)).unwrap()
}
