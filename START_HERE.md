# ✓ Setup MongoDB Completato - Prossimi Passi

## Cosa è stato fatto

Tutto il layer di database è pronto per lavorare con i dati reali già presenti in MongoDB remoto:

✓ **Connessione MongoDB** - Client singleton riutilizzabile
✓ **Schemas Pydantic** - Supporto formato GeoJSON Feature (dati reali)
✓ **Indici Geospaziali** - 2dsphere su geometry field + compound indexes
✓ **FastAPI Integration** - Lifecycle events (startup/shutdown)
✓ **Setup Script** - Preserva dati, crea solo indici
✓ **Test Script** - Verifica connessione e query
✓ **Documentazione** - Complete + Quick start guide

---

## Struttura Dati Reale

**Database**: `dbSpaziali`

### Collection: fontanelle
```json
{
  "type": "Feature",
  "properties": {
    "objectID": "5407",
    "ID_NIL": "53",
    "NIL": "LORENTEGGIO",
    "MUNICIPIO": "6",
    "CAP": "20152",
    "LONG_X_4326": 9.104075763359273,
    "LAT_Y_4326": 45.45100463400172
  },
  "geometry": {
    "type": "Point",
    "coordinates": [9.104075763359273, 45.45100463400172]
  }
}
```
- **1847+ documenti** con geometrie Point
- **Indici**: geometry (2dsphere), ID_NIL, MUNICIPIO, CAP

### Collection: nil
```json
{
  "_id": ObjectId("..."),
  "type": "Feature",
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
- **93+ documenti** con geometrie Polygon
- **Indici**: geometry (2dsphere), ID_NIL, NIL

---

## Come Avviare il Progetto

### 1️⃣ Configura il Database

```bash
# Vai in directory
cd c:\Users\net.LABXX-XX.000\Desktop\dati_geospaziali

# Copia configurazione (se non esiste)
copy .env.example .env

# Modifica .env con connection string MongoDB remota
# Es: MONGODB_URL=mongodb://host:27017
```

### 2️⃣ Installa Dipendenze

```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Database (Crea indici, preserva dati!)

```bash
python -m backend.fastapi_app.scripts.setup_db
```

Output atteso:
```
✓ Collection fontanelle already exists
✓ Collection nil already exists
✓ Created geospatial index on fontanelle.geometry
✓ Created index on fontanelle.properties.ID_NIL
...
NIL documents: 93
Fontanelle documents: 1847
✓ Setup completed successfully!
```

### 4️⃣ Verifica Connessione (Opzionale)

```bash
python -m backend.fastapi_app.scripts.test_connection
```

### 5️⃣ Avvia FastAPI

```bash
uvicorn backend.fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

Accedi: **http://localhost:8000/health**

Risposta attesa:
```json
{
  "status": "ok",
  "application": "Fontanelle Milano API",
  "database": "dbSpaziali"
}
```

---

## File Chiave

| File | Descrizione |
|------|-------------|
| `backend/fastapi_app/core/database.py` | Client MongoDB (singleton) |
| `backend/fastapi_app/core/config.py` | Configurazione da `.env` |
| `backend/fastapi_app/core/indexes.py` | Definizione indici geospaziali |
| `backend/fastapi_app/schemas/fontanella.py` | Models Pydantic (GeoJSON Feature) |
| `backend/fastapi_app/scripts/setup_db.py` | Setup indici (preserva dati) |
| `.env` | Variables ambiente (MongoDB URL) |
| `requirements.txt` | Dipendenze Python |
| `docs/DATABASE.md` | Riferimento schema database |
| `docs/QUICK_START.md` | Guida rapida |

---

## Esempi Query Python

### Fontanelle entro 1km da Duomo

```python
from backend.fastapi_app.core.database import MongoDBConnection

db = MongoDBConnection.get_database()

fontanelle = list(db.fontanelle.find({
    "geometry": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": [9.1845, 45.4642]  # Duomo
            },
            "$maxDistance": 1000  # 1 km
        }
    }
}).limit(10))

for f in fontanelle:
    print(f['properties']['NIL'])

MongoDBConnection.disconnect()
```

### NIL contenente il Duomo

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

### Conteggio fontanelle per NIL

```python
result = list(db.fontanelle.aggregate([
    {
        "$group": {
            "_id": "$properties.ID_NIL",
            "count": { "$sum": 1 },
            "nil_name": { "$first": "$properties.NIL" }
        }
    },
    {
        "$sort": { "count": -1 }
    },
    {
        "$limit": 10
    }
]))

for r in result:
    print(f"{r['nil_name']}: {r['count']} fontanelle")
```

---

## Prossimi Step (Fuori Scope di Questo Task)

1. **Rotte API** - Implementare endpoints CRUD per fontanelle/NIL
2. **Query Avanzate** - Aggregation pipeline complesse
3. **Frontend** - UI con mappa interattiva (Leaflet/Mapbox)
4. **Autenticazione** - JWT o sessioni
5. **Caching** - Redis per query frequenti
6. **Deployment** - Docker + Cloud

---

## Troubleshooting

### ❌ "ConnectionFailure: could not connect"
- Verifica `.env` con URL MongoDB corretto
- Testa manuale: `python -c "from pymongo import MongoClient; MongoClient('mongodb://...').admin.command('ping')"`

### ❌ "Indici non creati"
- Esegui di nuovo: `python -m backend.fastapi_app.scripts.setup_db`
- Verifica in mongosh: `db.fontanelle.getIndexes()`

### ❌ "Query geospaziale non funziona"
- Controlla che indice esista: `db.fontanelle.find({}).explain()` (vedi stage `GEO_2DSPHERE`)
- Assicurati di usare il campo `geometry` (non `coordinate`)

### ❌ "ModuleNotFoundError" durante import
- Installa dipendenze: `pip install -r requirements.txt`
- Controlla che sei nella directory giusta
- Usa: `python -m backend.fastapi_app.scripts.setup_db` (non `python setup_db.py`)

---

## Comandi Utili

```bash
# Installa dipendenze
pip install -r requirements.txt

# Setup database (crea indici)
python -m backend.fastapi_app.scripts.setup_db

# Test connessione
python -m backend.fastapi_app.scripts.test_connection

# Avvia FastAPI
uvicorn backend.fastapi_app.main:app --reload

# Connetti a MongoDB (bash)
mongosh "mongodb://host:27017/dbSpaziali"
```

---

## Documentazione Completa

Vedi questi file per dettagli:

- **Setup Rapido**: [QUICK_START.md](QUICK_START.md)
- **Schema Database**: [docs/DATABASE.md](docs/DATABASE.md)
- **Best Practices**: [docs/MONGODB_ARCHITECTURE.md](docs/MONGODB_ARCHITECTURE.md)
- **Modello Concettuale**: [docs/CONCEPTUAL_MODEL.md](docs/CONCEPTUAL_MODEL.md)

---

**Status**: ✅ Database Layer Pronto per l'Uso

Il progetto è configurato per lavorare con i dati reali in MongoDB remoto.
Pronto per implementare rotte API e frontend!
