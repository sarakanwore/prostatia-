from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="STATIA Geospatial & Cartography Service",
    description="Service de cartographie et d'analyse territoriale spécialisé pour le Togo et l'Afrique de l'Ouest",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "geo_service", "version": "1.0.0"}
