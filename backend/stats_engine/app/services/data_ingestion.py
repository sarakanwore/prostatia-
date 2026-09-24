"""Data ingestion service for PROSTATIA Stats Engine.

Provides utility functions to load data from various sources (CSV, Parquet, SQL, MongoDB)
and return a :class:`pandas.DataFrame`. These helpers are used by the Stats Engine's
``ingest`` registry method.

All functions accept simple parameters (strings, bytes, or connection strings) and
raise ``ValueError`` on failure.
"""

from typing import Dict, Any
import pandas as pd
import io
import sqlalchemy
from pymongo import MongoClient
import pyarrow.parquet as pq


def ingest_csv(content: str) -> pd.DataFrame:
    """Ingest CSV data from a raw string.

    Args:
        content: CSV formatted string.

    Returns:
        pandas.DataFrame containing the parsed CSV data.
    """
    return pd.read_csv(io.StringIO(content))


def ingest_parquet(content: bytes) -> pd.DataFrame:
    """Ingest Parquet data from raw bytes.

    Args:
        content: Binary representation of a Parquet file.

    Returns:
        pandas.DataFrame with the parquet table content.
    """
    buffer = io.BytesIO(content)
    table = pq.read_table(buffer)
    return table.to_pandas()


def ingest_sql(connection_string: str, query: str) -> pd.DataFrame:
    """Ingest data from a SQL database using SQLAlchemy.

    Args:
        connection_string: SQLAlchemy connection URL (e.g. ``postgresql://user:pwd@host/db``).
        query: SQL query to execute.

    Returns:
        pandas.DataFrame with the query result.
    """
    engine = sqlalchemy.create_engine(connection_string)
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df


def ingest_mongodb(uri: str, db: str, collection: str, filter: Dict[str, Any] | None = None) -> pd.DataFrame:
    """Ingest data from a MongoDB collection.

    Args:
        uri: MongoDB connection URI.
        db: Database name.
        collection: Collection name.
        filter: Optional MongoDB filter dictionary; defaults to an empty filter.

    Returns:
        pandas.DataFrame built from the documents. The automatic ``_id`` field is removed.
    """
    client = MongoClient(uri)
    coll = client[db][collection]
    docs = list(coll.find(filter or {}))
    if not docs:
        return pd.DataFrame()
    for doc in docs:
        doc.pop("_id", None)
    return pd.DataFrame(docs)


def ingest(method_id: str, payload: Dict[str, Any]) -> pd.DataFrame:
    """Dispatch ingestion based on a method identifier.

    Supported ``method_id`` values are:
        - ``csv_ingest``
        - ``parquet_ingest``
        - ``sql_ingest``
        - ``mongodb_ingest``

    The ``payload`` dictionary must contain the required keys for each method.

    Args:
        method_id: Identifier of the ingestion method.
        payload: Dictionary of parameters required by the selected method.

    Returns:
        pandas.DataFrame loaded from the specified source.

    Raises:
        ValueError: If an unsupported ``method_id`` is provided.
    """
    if method_id == "csv_ingest":
        return ingest_csv(payload["content"])
    if method_id == "parquet_ingest":
        return ingest_parquet(payload["content"])
    if method_id == "sql_ingest":
        return ingest_sql(payload["connection_string"], payload["query"])
    if method_id == "mongodb_ingest":
        return ingest_mongodb(
            payload["uri"], payload["db"], payload["collection"], payload.get("filter")
        )
    raise ValueError(f"Unsupported ingestion method: {method_id}")
