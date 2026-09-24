# Ingestion des Données

Le Stats Engine intègre un service d'ingestion capable de convertir différentes sources de données en DataFrames `pandas` prêts pour l'analyse statistique ou les pipelines de prétraitement.

---

## Formats et Connecteurs pris en charge

### 1. Fichiers CSV (`ingest_csv`)

Le format CSV peut être lu directement depuis une chaîne brute ou un chemin de fichier.

- **Fonction** : `app.services.data_ingestion.ingest_csv(content: str)`
- **Paramètres** :
    - `content` : Chaîne de caractères formatée au format CSV (ou fichier uploadé).
- **Séparateur par défaut** : Détection automatique ou virgule `,`.

### 2. Fichiers Parquet (`ingest_parquet`)

Le format Parquet permet des lectures binaires column-oriented rapides et compactes via `pyarrow`.

- **Fonction** : `app.services.data_ingestion.ingest_parquet(content: bytes)`
- **Paramètres** :
    - `content` : Données binaires du fichier Parquet.

### 3. Bases relationnelles SQL (`ingest_sql`)

Connexion dynamique via `SQLAlchemy` pour exécuter des requêtes d'extraction SQL sur PostgreSQL, MySQL, SQLite, etc.

- **Fonction** : `app.services.data_ingestion.ingest_sql(connection_string: str, query: str)`
- **Paramètres** :
    - `connection_string` : Chaîne de connexion SQLAlchemy (ex : `postgresql://user:password@localhost:5432/prostatia_db`).
    - `query` : Requête SQL d'extraction (ex : `SELECT * FROM observations WHERE valide = true`).

### 4. Bases NoSQL MongoDB (`ingest_mongodb`)

Extraction de documents JSON depuis une collection MongoDB via `pymongo`.

- **Fonction** : `app.services.data_ingestion.ingest_mongodb(connection_string: str, database: str, collection: str, query: dict)`
- **Paramètres** :
    - `connection_string` : URI MongoDB (ex : `mongodb://localhost:27017`).
    - `database` : Nom de la base.
    - `collection` : Nom de la collection.
    - `query` : Filtre BSON / JSON de sélection.

---

## Endpoint d'Ingestion de l'API

L'API expose le point d'entrée suivant :

```http
POST /api/v1/ingest
Content-Type: application/json
```

### Exemple de charge utile (Payload)

```json
{
  "source_type": "csv",
  "csv_string": "age,taille,poids\n25,175,70\n30,180,82\n45,168,65"
}
```

### Réponse

```json
{
  "status": "success",
  "rows": 3,
  "columns": ["age", "taille", "poids"]
}
```
