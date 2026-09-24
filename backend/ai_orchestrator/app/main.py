from fastapi import FastAPI
from app.api import routes

from app.db import Base, engine

# Lifespan context manager for FastAPI (to replace deprecated on_event)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if database is available
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"[AI Orchestrator] Database connection note: {e}. Running without persistent history.")
    yield
    # Cleanup on shutdown (if needed)

app = FastAPI(
    title="STATIA AI Orchestrator",
    description="Translates natural language to strict execution plans for the Stats Engine",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai_orchestrator"}
