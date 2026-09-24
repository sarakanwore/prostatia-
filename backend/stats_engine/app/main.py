from fastapi import FastAPI
from app.api import routes

app = FastAPI(
    title="STATIA Stats Engine",
    description="Deterministic mathematical computation service for STATIA",
    version="1.0.0",
)

app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "stats_engine"}
