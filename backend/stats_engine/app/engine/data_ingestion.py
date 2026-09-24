from typing import Dict, Any
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Optional imports for database connections – they will be lazily imported when needed

def _csv_ingest(payload: Dict[str, Any]) -> pd.DataFrame:
    """Ingest CSV data.

    Expected payload keys:
    - ``file_path`` (optional): path to a CSV file on the container.
    - ``csv_string`` (optional): raw CSV content as a string.
    - ``separator`` (optional): column separator, default ",".
    Returns a pandas DataFrame.
    """
    if "file_path" in payload:
        return pd.read_csv(payload["file_path"], sep=payload.get("separator", ","))
    if "csv_string" in payload:
        from io import StringIO
        return pd.read_csv(StringIO(payload["csv_string"]), sep=payload.get("separator", ","))
    raise ValueError("Either 'file_path' or 'csv_string' must be provided for CSV ingestion.")


def _parquet_ingest(payload: Dict[str, Any]) -> pd.DataFrame:
    """Ingest Parquet data.

    Expected payload keys:
    - ``file_path``: path to a Parquet file.
    Returns a pandas DataFrame.
    """
    if "file_path" not in payload:
        raise ValueError("'file_path' is required for Parquet ingestion.")
    return pd.read_parquet(payload["file_path"])


def _sql_ingest(payload: Dict[str, Any]) -> pd.DataFrame:
    """Ingest data from a SQL database using SQLAlchemy.

    Expected payload keys:
    - ``connection_string``: SQLAlchemy URL (e.g. ``postgresql://user:pwd@host/db``).
    - ``query``: SQL query string returning a result set.
    Returns a pandas DataFrame.
    """
    try:
        from sqlalchemy import create_engine
    except ImportError as exc:
        raise ImportError("SQLAlchemy is required for SQL ingestion.") from exc

    if "connection_string" not in payload or "query" not in payload:
        raise ValueError("Both 'connection_string' and 'query' are required for SQL ingestion.")
    engine = create_engine(payload["connection_string"])
    with engine.connect() as conn:
        return pd.read_sql_query(payload["query"], conn)


def _mongodb_ingest(payload: Dict[str, Any]) -> pd.DataFrame:
    """Ingest data from a MongoDB collection.

    Expected payload keys:
    - ``uri``: MongoDB connection URI.
    - ``database``: Database name.
    - ``collection``: Collection name.
    - ``filter`` (optional): MongoDB filter dict, default ``{}``.
    Returns a pandas DataFrame.
    """
    try:
        from pymongo import MongoClient
    except ImportError as exc:
        raise ImportError("pymongo is required for MongoDB ingestion.") from exc

    required = {"uri", "database", "collection"}
    if not required.issubset(payload):
        missing = required - payload.keys()
        raise ValueError(f"Missing required fields for MongoDB ingestion: {missing}")

    client = MongoClient(payload["uri"])
    db = client[payload["database"]]
    coll = db[payload["collection"]]
    docs = list(coll.find(payload.get("filter", {})))
    # Remove the automatic _id field for cleaner output
    for doc in docs:
        doc.pop("_id", None)
    return pd.DataFrame(docs)


def ingest(method_id: str, payload: Dict[str, Any]) -> pd.DataFrame:
    """Dispatcher for ingestion methods.

    ``method_id`` must be one of ``csv_ingest``, ``parquet_ingest``, ``sql_ingest`` or ``mongodb_ingest``.
    The function forwards the ``payload`` to the appropriate internal helper and returns a DataFrame.
    """
    dispatch = {
        "csv_ingest": _csv_ingest,
        "parquet_ingest": _parquet_ingest,
        "sql_ingest": _sql_ingest,
        "mongodb_ingest": _mongodb_ingest,
    }
    if method_id not in dispatch:
        raise ValueError(f"Unsupported ingestion method: {method_id}")
    return dispatch[method_id](payload)


def ingest_csv(payload: Dict[str, Any]) -> pd.DataFrame:
    """Wrapper for CSV ingestion used by registry."""
    return _csv_ingest(payload)

def ingest_parquet(payload: Dict[str, Any]) -> pd.DataFrame:
    """Wrapper for Parquet ingestion used by registry."""
    return _parquet_ingest(payload)

def ingest_sql(payload: Dict[str, Any]) -> pd.DataFrame:
    """Wrapper for SQL ingestion used by registry."""
    return _sql_ingest(payload)

def ingest_mongodb(payload: Dict[str, Any]) -> pd.DataFrame:
    """Wrapper for MongoDB ingestion used by registry."""
    return _mongodb_ingest(payload)
