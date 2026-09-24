FROM rust:1.76-slim AS builder

WORKDIR /usr/src/app

COPY Cargo.toml Cargo.lock* ./
COPY src/ ./src/

RUN cargo build --release

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /usr/src/app/target/release/gateway .
COPY migrations/ ./migrations/

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["./gateway"]
