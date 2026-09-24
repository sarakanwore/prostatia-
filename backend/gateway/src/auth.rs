use axum::{
    async_trait,
    extract::FromRequestParts,
    http::{request::Parts, StatusCode},
};
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};
use chrono::{Utc, Duration};

const JWT_SECRET: &str = "SUPER_SECRET_KEY_PROSTATIA_2026"; // In prod, load from env

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub sub: String, // User ID
    pub exp: usize,
}

pub fn create_token(user_id: &str) -> Result<String, jsonwebtoken::errors::Error> {
    let expiration = Utc::now()
        .checked_add_signed(Duration::hours(24))
        .expect("valid timestamp")
        .timestamp() as usize;

    let claims = Claims {
        sub: user_id.to_owned(),
        exp: expiration,
    };

    encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(JWT_SECRET.as_ref()),
    )
}

pub struct AuthenticatedUser(pub String);

#[async_trait]
impl<S> FromRequestParts<S> for AuthenticatedUser
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, &'static str);

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        let auth_header = parts
            .headers
            .get("Authorization")
            .and_then(|value| value.to_str().ok())
            .filter(|value| value.starts_with("Bearer "));

        if let Some(auth_header) = auth_header {
            let token = &auth_header[7..];

            match decode::<Claims>(
                token,
                &DecodingKey::from_secret(JWT_SECRET.as_ref()),
                &Validation::default(),
            ) {
                Ok(token_data) => Ok(AuthenticatedUser(token_data.claims.sub)),
                Err(_) => Err((StatusCode::UNAUTHORIZED, "Invalid Token")),
            }
        } else {
            Err((StatusCode::UNAUTHORIZED, "Missing Authorization Header"))
        }
    }
}
