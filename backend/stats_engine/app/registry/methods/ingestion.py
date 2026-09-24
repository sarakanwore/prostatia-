from app.registry.schemas import MethodFiche, MethodParameter, MethodOutput

COMMON_INPUT = {
    "content": MethodParameter(type="string", description="Raw data content (CSV string or Parquet bytes base64)")
}

CSV_INGEST_FICHE = MethodFiche(
    id="csv_ingest",
    name="Ingestion CSV",
    category="ingestion",
    description="Charge un CSV fourni sous forme de chaîne de caractères et le convertit en DataFrame.",
    inputs={"content": MethodParameter(type="string", description="CSV string")},
    outputs={"df": MethodOutput(type="csv", description="DataFrame au format CSV")},
    numerical_method="data_ingestion.ingest_csv",
)

PARQUET_INGEST_FICHE = MethodFiche(
    id="parquet_ingest",
    name="Ingestion Parquet",
    category="ingestion",
    description="Charge un fichier Parquet fourni en binaire et le convertit en DataFrame.",
    inputs={"content": MethodParameter(type="bytes", description="Parquet bytes")},
    outputs={"df": MethodOutput(type="csv", description="DataFrame au format CSV")},
    numerical_method="data_ingestion.ingest_parquet",
)

SQL_INGEST_FICHE = MethodFiche(
    id="sql_ingest",
    name="Ingestion SQL",
    category="ingestion",
    description="Exécute une requête SQL sur la base spécifiée et retourne le résultat sous forme de DataFrame.",
    inputs={
        "connection_string": MethodParameter(type="string", description="SQLAlchemy connection URL"),
        "query": MethodParameter(type="string", description="SQL query to execute"),
    },
    outputs={"df": MethodOutput(type="csv", description="DataFrame au format CSV")},
    numerical_method="data_ingestion.ingest_sql",
)

MONGODB_INGEST_FICHE = MethodFiche(
    id="mongodb_ingest",
    name="Ingestion MongoDB",
    category="ingestion",
    description="Récupère des documents depuis une collection MongoDB et les transforme en DataFrame.",
    inputs={
        "uri": MethodParameter(type="string", description="MongoDB connection URI"),
        "db": MethodParameter(type="string", description="Database name"),
        "collection": MethodParameter(type="string", description="Collection name"),
        "filter": MethodParameter(type="dict", description="Optional filter query (default: {})"),
    },
    outputs={"df": MethodOutput(type="csv", description="DataFrame au format CSV")},
    numerical_method="data_ingestion.ingest_mongodb",
)

INGESTION_METHODS = {
    CSV_INGEST_FICHE.id: CSV_INGEST_FICHE,
    PARQUET_INGEST_FICHE.id: PARQUET_INGEST_FICHE,
    SQL_INGEST_FICHE.id: SQL_INGEST_FICHE,
    MONGODB_INGEST_FICHE.id: MONGODB_INGEST_FICHE,
}
