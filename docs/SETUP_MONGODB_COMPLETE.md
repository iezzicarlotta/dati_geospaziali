# MongoDB Setup - Riepilogo Completo

## 📊 Deliverables Completati

### ✓ 1. Configurazione Connessione
- **File**: `backend/fastapi_app/core/config.py`
- **Contenuto**: Classe `Settings` con variabili di ambiente per MongoDB
- **Uso**: Carica URL database, nome database, timeout da `.env`

### ✓ 2. Client MongoDB Riutilizzabile
- **File**: `backend/fastapi_app/core/database.py`
- **Contenuto**: Classe `MongoDBConnection` (Singleton pattern)
- **Metodi**:
  - `connect()` - Stabilisce connessione
  - `disconnect()` - Chiude connessione
  - `get_database()` - Accesso a `dbSpaziali`
  - `get_collection(name)` - Accesso diretto a collection

### ✓ 3. Schemas Pydantic con GeoJSON
- **File**: `backend/fastapi_app/schemas/fontanella.py`
- **Modelli**:
  - `Point` - GeoJSON Point (coordinate geospaziali)
  - `Polygon` - GeoJSON Polygon (aree NIL)
  - `FontanellaCreate` - Schema di creazione fontanella
  - `Fontanella` - Schema completo da database
  - `NILCreate` - Schema di creazione NIL
  - `NIL` - Schema completo da database
- **Supporto**: ObjectId custom + validazione Pydantic

### ✓ 4. Gestione Indici Geospaziali
- **File**: `backend/fastapi_app/core/indexes.py`
- **Indexes Creati**:
  
  **Fontanelle:**
  - `idx_fontanelle_coordinate_geospatial` (2dsphere) - Query per distanza
  - `idx_fontanelle_nil_id` - Join veloce con NIL
  - `idx_fontanelle_stato` - Filtri per stato
  - `idx_fontanelle_createdAt` - Sorting temporale
  - `idx_fontanelle_quartiere_stato` - Compound filter
  
  **NIL:**
  - `idx_nil_geometria_geospatial` (2dsphere) - Query di area
  - `idx_nil_numero_unique` (Unique) - Garanzia unicità numero
  - `idx_nil_nome` - Lookup per nome
  - `idx_nil_createdAt` - Sorting temporale

### ✓ 5. Script Inizializzazione Database
- **File**: `backend/fastapi_app/scripts/init_db.py`
- **Funzioni**:
  - `create_collections_and_indexes()` - Crea collection e indici
  - `seed_sample_data()` - Inserisce 2 NIL + 3 fontanelle di test
  - `verify_setup()` - Verifica corretta configurazione
- **Esecuzione**: `python -m backend.fastapi_app.scripts.init_db`

### ✓ 6. Script Test Connessione
- **File**: `backend/fastapi_app/scripts/test_connection.py`
- **Test**:
  - Connessione MongoDB
  - Accesso collection
  - Presenza indici
  - Query geospaziale
  - Validazione Pydantic
- **Esecuzione**: `python -m backend.fastapi_app.scripts.test_connection`

### ✓ 7. Integrazione FastAPI Lifecycle
- **File**: `backend/fastapi_app/main.py`
- **Aggiunto**:
  - `@app.on_event("startup")` - Connessione database all'avvio
  - `@app.on_event("shutdown")` - Disconnessione all'arresto
  - Endpoint `/health` per health check

### ✓ 8. Configurazione Ambiente
- **File**: `.env.example`
- **Variables**:
  ```
  MONGODB_URL=mongodb://localhost:27017
  MONGODB_DATABASE=dbSpaziali
  MONGODB_TIMEOUT=30
  ```

### ✓ 9. Documentazione Database
- **File**: `docs/DATABASE.md`
- **Contenuto**:
  - Struttura collection fontanelle/NIL
  - Dettagli campi e tipi
  - Query geospaziali di esempio
  - Istruzioni setup e testing
  - Coordinate di riferimento Milano

### ✓ 10. Architettura e Best Practices
- **File**: `docs/MONGODB_ARCHITECTURE.md`
- **Contenuto**:
  - Pattern Singleton connessione
  - Lifecycle FastAPI
  - Template di integrazione rotte
  - GeoJSON best practices
  - Query ottimizzate con indici
  - Aggregation pipeline examples
  - Error handling
  - Troubleshooting

---

## 🚀 Quick Start

### 1. Dipendenze
```bash
cd c:\Users\net.LABXX-XX.000\Desktop\dati_geospaziali
pip install pymongo pydantic pydantic-settings python-dotenv fastapi
```

### 2. Configurazione
```bash
# Copiare template .env
copy .env.example .env

# Editare .env se MongoDB non è su localhost:27017
```

### 3. MongoDB
```bash
# Assicurarsi che MongoDB sia in esecuzione
# Windows: 
#   mongod.exe (nella cartella bin di MongoDB)
# Linux/Mac:
#   mongod
```

### 4. Inizializzazione Database
```bash
python -m backend.fastapi_app.scripts.init_db
```

Output atteso:
```
==================================================
MongoDB Database Initialization
Database: dbSpaziali
==================================================

✓ Created collection: fontanelle
✓ Created collection: nil

=== Setting up MongoDB Indexes ===
...
✓ All indexes configured successfully

=== Seeding Sample Data ===
✓ Inserted 2 NIL records
✓ Inserted 3 fontanelle records

=== Verification ===
Collections: ['fontanelle', 'nil']
...
✓ Database initialization completed successfully!
```

### 5. Test Connessione
```bash
python -m backend.fastapi_app.scripts.test_connection
```

Output atteso:
```
============================================================
MongoDB Connection and Data Integrity Tests
============================================================

=== Testing MongoDB Connection ===
✓ Connected to database: dbSpaziali
✓ Ping successful

=== Testing Collections ===
✓ Fontanelle documents: 3
✓ NIL documents: 2

=== Testing Indexes ===
✓ All fontanelle indexes present
✓ All NIL indexes present

=== Testing Geospatial Query ===
✓ Found 3 fontanelle within 2km of Duomo
  - Fontanella Piazza Duomo
  - Fontanella Via Torino
  - Fontanella Navigli
✓ Found NIL containing Duomo point: NIL 1 - Centro Storico

=== Testing Pydantic Schemas ===
✓ Point schema: {'type': 'Point', 'coordinates': (9.1845, 45.4642)}
✓ FontanellaCreate schema validated: Test Fontanella

============================================================
Test Results Summary
============================================================
✓ PASS - Connection
✓ PASS - Collections
✓ PASS - Indexes
✓ PASS - Geospatial Query
✓ PASS - Schemas

✓ All tests passed! Database is ready.
```

### 6. Avvio FastAPI
```bash
uvicorn backend.fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoint disponibile: `http://localhost:8000/health`

---

## 📁 Struttura File Aggiunta

```
backend/fastapi_app/
├── core/
│   ├── __init__.py
│   ├── config.py              ← Settings MongoDB
│   ├── database.py            ← Connection singleton
│   ├── indexes.py             ← Gestione indici
│   └── (config.py)            ← Aggiornato
│
├── schemas/
│   └── fontanella.py          ← GeoJSON + Pydantic models
│
├── scripts/
│   ├── __init__.py
│   ├── init_db.py             ← Init database + seed
│   └── test_connection.py     ← Test connessione
│
└── main.py                    ← Aggiornato lifecycle

files/
├── DATABASE.md                ← Struttura collection
├── MONGODB_ARCHITECTURE.md    ← Best practices
└── .env.example               ← Template configurazione
```

---

## 🔍 Query Geospaziali - Esempi Pratici

### Fontanelle entro 1km da un punto
```python
from backend.fastapi_app.core.database import MongoDBConnection

db = MongoDBConnection.get_database()
point = [9.1845, 45.4642]  # Duomo Milano

fontanelle = list(db.fontanelle.find({
    "coordinate": {
        "$near": {
            "$geometry": {"type": "Point", "coordinates": point},
            "$maxDistance": 1000  # 1 km
        }
    }
}).limit(10))
```

### NIL contenente un punto
```python
point = [9.1845, 45.4642]

nil = db.nil.find_one({
    "geometria": {
        "$geoIntersects": {
            "$geometry": {"type": "Point", "coordinates": point}
        }
    }
})
```

### Fontanelle per quartiere + stato
```python
fontanelle = list(db.fontanelle.find({
    "quartiere": "Centro Storico",
    "stato": "attiva"
}))
```

---

## ⚠️ Troubleshooting

### ❌ "ConnectionFailure: could not connect to any servers"
**Soluzione**: Avviare MongoDB
```bash
# Windows
mongod.exe

# Linux/Mac
mongod
```

### ❌ "DuplicateKeyError: E11000"
**Soluzione**: Database già ha dati - commentare `delete_many()` in `init_db.py` oppure cancellare e ricreare database

### ❌ "ObjectId is not JSON serializable"
**Soluzione**: Usare sempre `PyObjectId` negli schemas Pydantic (già fatto)

### ❌ Geospatial queries lente
**Soluzione**: Verificare che indice 2dsphere esisu
```bash
python -m backend.fastapi_app.scripts.test_connection
```

---

## ✗ Cose NON Fatto Ancora (PROSSIMI STEP)

1. **Rotte CRUD** - POST/GET/PUT/DELETE fontanelle e NIL
2. **Autenticazione** - JWT o sessioni
3. **Validazione Business Logic** - Regole di business
4. **Aggregation Queries** - Query complesse multi-stage
5. **Caching** - Redis per query frequenti
6. **API Documentation** - Swagger/OpenAPI
7. **Frontend** - UI con mappa interattiva
8. **E2E Tests** - Test con dati reali
9. **Deployment** - Docker, K8s
10. **Monitoring** - Logging, metriche

---

## ✓ Checklist Setup Completato

- [x] MongoDB configurato in `core/config.py`
- [x] Client riutilizzabile creato (`core/database.py`)
- [x] Schemas Pydantic con GeoJSON (`schemas/fontanella.py`)
- [x] Indici geospaziali definiti (`core/indexes.py`)
- [x] Script init database creato (`scripts/init_db.py`)
- [x] Script test creato (`scripts/test_connection.py`)
- [x] FastAPI lifecycle integrato (`main.py`)
- [x] `.env.example` preparato
- [x] Documentazione database (`docs/DATABASE.md`)
- [x] Best practices documentate (`docs/MONGODB_ARCHITECTURE.md`)
- [x] Dipendenze aggiornate (`pyproject.toml`)

**Status**: ✓ Database Layer Pronto per l'Uso

---

## 📞 Supporto Errori

Se durante il setup incontri errori, verifica in ordine:

1. **MongoDB running?** → `mongosh` o `mongo` deve connettersi
2. **Python env?** → `python --version` >= 3.11
3. **Dipendenze?** → `pip list | grep pymongo`
4. **Porta MongoDB?** → Default 27017, verificare in `.env`
5. **Indici?** → `test_connection.py` dovrebbe mostrare tutti gli indici
6. **GeoJSON valido?** → Sempre [lon, lat]!

Tutti gli step sono testabili singolarmente. Ogni file contiene doc-string esplicative.
