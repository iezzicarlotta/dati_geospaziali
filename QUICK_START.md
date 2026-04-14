# Avvio Progetto con MongoDB Remoto (Dati Reali)

## Setup Rapido

### 1. Configura `.env`

```bash
# Se non existe, copia da .env.example
copy .env.example .env
```

Modifica `.env` con la **connection string MongoDB remota**:

```env
# MongoDB remoto (Atlas o self-hosted)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
# oppure
# MONGODB_URL=mongodb://user:pass@remote-host:27017

MONGODB_DATABASE=dbSpaziali
MONGODB_TIMEOUT=30
```

### 2. Installa dipendenze

```bash
pip install -r requirements.txt
```

### 3. Setup indexes (NON modifica i dati!)

Il tuo database ha già:
- Collection `fontanelle` con documenti GeoJSON Feature (formato reale)
- Collection `nil` con geometrie Polygon (formato reale)

Crea gli indici geospaziali:

```bash
python -m backend.fastapi_app.scripts.setup_db
```

Output atteso:
```
============================================================
MongoDB Database Setup
Database: dbSpaziali
============================================================

ℹ Collection fontanelle already exists
ℹ Collection nil already exists

=== Setting up MongoDB Indexes ===

Setting up fontanelle indexes...
✓ Created geospatial index on fontanelle.geometry
✓ Created index on fontanelle.properties.ID_NIL
...

✓ All indexes configured successfully

============================================================
Database Status
============================================================
NIL documents: 2
Fontanelle documents: 2

Fontanelle indexes:
  ✓ idx_fontanelle_geometry_geospatial
  ✓ _id_
  ...
```

### 4. Test connessione

```bash
python -m backend.fastapi_app.scripts.test_connection
```

### 5. Avvia FastAPI

```bash
uvicorn backend.fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

Accedi: **`http://localhost:8000/health`**

---

## Formato Dati Reali (GeoJSON Feature)

### Fontanelle

```json
{
  "type": "Feature",
  "properties": {
    "objectID": "5407",
    "CAP": "20152",
    "MUNICIPIO": "6",
    "ID_NIL": "53",
    "NIL": "LORENTEGGIO",
    "LONG_X_4326": 9.104075763359273,
    "LAT_Y_4326": 45.45100463400172,
    "Location": "(45.45100463400172, 9.104075763359273)"
  },
  "geometry": {
    "type": "Point",
    "coordinates": [9.104075763359273, 45.45100463400172]
  }
}
```

### NIL

```json
{
  "_id": ObjectId("..."),
  "type": "Feature",
  "id": 89,
  "properties": {
    "ID_NIL": 48,
    "NIL": "RONCHETTO SUL NAVIGLIO",
    "Valido_dal": "05/02/2020",
    "Valido_al": "Vigente",
    "Shape_Area": 2406306.0789698716
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [...]
  }
}
```

---

## Query Geospaziali con Dati Reali

### Fontanelle entro 1km da un punto

```python
from backend.fastapi_app.core.database import MongoDBConnection

db = MongoDBConnection.get_database()

# Query con il campo "geometry" reale
fontanelle = db.fontanelle.find({
    "geometry": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": [9.1845, 45.4642]  # Duomo
            },
            "$maxDistance": 1000  # 1 km
        }
    }
}).limit(10)

for f in fontanelle:
    print(f"Fontanella: {f['properties']['NIL']}")
```

### NIL contenente un punto

```python
nil = db.nil.find_one({
    "geometry": {
        "$geoIntersects": {
            "$geometry": {
                "type": "Point",
                "coordinates": [9.1845, 45.4642]
            }
        }
    }
})

if nil:
    print(f"NIL: {nil['properties']['NIL']}")
```

---

## Differenze da Schema Iniziale

| Aspetto | Schema Proposto | Dati Reali |
|---------|-----------------|-----------|
| **Fontanella** | Nome, address, stato | GeoJSON Feature con properties |
| **Coordinate** | Campo `coordinate` | Dentro `geometry` (GeoJSON) |
| **NIL** | Campi propri | `properties` + `geometry` |
| **ID NIL** | `numero` (1-999) | `ID_NIL` (stringa o int) |

---

## Troubleshooting

### ❌ "ConnectionFailure" durante setup_db
- Verifica `.env` con connection string corretta
- Test manuale:
  ```python
  from pymongo import MongoClient
  client = MongoClient("mongodb://...")
  client.admin.command("ping")
  ```

### ❌ "No indexes created"
- Indici potrebbero essere duplicati. Esegui di nuovo:
  ```bash
  python -m backend.fastapi_app.scripts.setup_db
  ```

### ❌ Query Geospaziale non funziona
- Verifica che leggi da `geometry` (non `coordinate`)
- Controlla che indice 2dsphere esista:
  ```bash
  mongosh your_connection_string/dbSpaziali
  db.fontanelle.getIndexes()
  ```

---

## Prossimi Step

1. ✓ Database e indici configurati
2. **Creare rotte API** per CRUD fontanelle/NIL
3. **Query avanzate** geospaziali
4. **Frontend** con mappa interattiva
5. **Autenticazione** e autorizzazione
