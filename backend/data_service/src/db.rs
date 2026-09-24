use sqlx::{postgres::PgPoolOptions, Pool, Postgres};
use std::env;

pub async fn establish_connection() -> Pool<Postgres> {
    let database_url = env::var("DATABASE_URL").unwrap_or_else(|_| {
        "postgres://prostatia_user:prostatia_password@localhost:5432/prostatia_db".to_string()
    });

    PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Failed to connect to Postgres")
}
