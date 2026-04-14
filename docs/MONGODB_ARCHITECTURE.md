# MongoDB - Architettura e Best Practices

## Struttura della Connessione

### File: `core/database.py`
Gestisce una **singola istanza di connessione riutilizzabile** (pattern Singleton):

```
MongoDBConnection
├── connect()          → Stabilisce connessione (una sola volta)
├── disconnect()       → Chiude connessione
├── get_database()     → Accesso al database `dbSpaziali`
├── get_collection()   → Accesso diretto a collection
└── _client (singleton) → Mantiene la connessione viva
```

**Vantaggi:**
- Una sola connessione per tutta l'applicazione
- Connection pooling automatico di PyMongo
- Facile da testare e debuggare

---

## Lifecycle Integrazione FastAPI

### File: `main.py`
```python
@app.on_event("startup")
async def startup():
    MongoDBConnection.connect()

@app.on_event("shutdown")
async def shutdown():
    MongoDBConnection.disconnect()
```

**Comportamento:**
1. All'avvio di FastAPI: connessioni a MongoDB
2. Durante le richieste: le rotte usano `MongoDBConnection.get_database()`
3. All'arresto: chiude la connessione

---

## Uso in Rotte (Template)

```python
from fastapi import APIRouter, HTTPException
from backend.fastapi_app.core.database import MongoDBConnection
from backend.fastapi_app.schemas.fontanella import Fontanella, FontanellaCreate

router = APIRouter()

@router.get("/fontanelle")
async def list_fontanelle():
    db = MongoDBConnection.get_database()
    fontanelle = list(db.fontanelle.find({}, {"_id": 1, "nome": 1}))
    return fontanelle

@router.post("/fontanelle")
async def create_fontanella(fontanella: FontanellaCreate):
    db = MongoDBConnection.get_database()
    result = db.fontanelle.insert_one(fontanella.dict())
    return {"id": str(result.inserted_id)}
```

---

## Schemi Pydantic

### File: `schemas/fontanella.py`

**Perché Pydantic?**
1. **Validazione** - Verifica tipi e vincoli prima di inserire in DB
2. **Serializzazione** - Converte ObjectId in string per JSON
3. **Documentazione** - Genera schema OpenAPI automaticamente

**Flusso Dati:**
```
Request JSON
    ↓
Pydantic Model (FontanellaCreate)
    ↓
Conversione in dict per MongoDB
    ↓
MongoDB INSERT
    ↓
Documento con _id
    ↓
Pydantic Model (Fontanella) con alias
    ↓
Response JSON
```

**Custom PyObjectId:**
```python
class PyObjectId(ObjectId):
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)
```
Permette a Pydantic di usare e validare ObjectId in schema.

---

## Indici Geospaziali

### File: `core/indexes.py`

**Perché gli indici?**
- Query su milioni di fontanelle senza indice = scan completo (lentissimo)
- Indice 2dsphere = query geospaziale in millisecondi

**Tipi di Indici Creati:**

1. **2dsphere** (Geospatiale)
   ```javascript
   db.fontanelle.createIndex({ "coordinate": "2dsphere" })
   ```
   - Abilita: `$near`, `$geoWithin`, `$geoIntersects`
   - Usa coordinate del mondo reale (WGS84)
   - ESSENZIALE

2. **Compound Index** (Query combinate)
   ```javascript
   db.fontanelle.createIndex({ "quartiere": 1, "stato": 1 })
   ```
   - Velocizza: `find({"quartiere": "...", "stato": "..."})`
   - In ordine dei campi più filtrati

3. **Unique Index** (Vincolo di business)
   ```javascript
   db.nil.createIndex({ "numero": 1 }, { unique: true })
   ```
   - Garanzia che numero NIL sia univoco
   - Previene duplicati a livello DB

---

## Dati GeoJSON

### Coordinate: [longitude, latitude]
```javascript
// ❌ SBAGLIATO
"coordinate": [45.4642, 9.1845]  // [lat, lon]

// ✓ CORRETTO
"coordinate": [9.1845, 45.4642]  // [lon, lat]
```

### Formato Punto
```json
{
  "type": "Point",
  "coordinates": [9.1845, 45.4642]
}
```

### Formato Poligono (NIL)
```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [9.17, 45.45],   // Primo punto
      [9.19, 45.45],
      [9.19, 45.47],
      [9.17, 45.47],
      [9.17, 45.45]    // Chiude il poligono
    ]
  ]
}
```

> **Nota**: Primo e ultimo punto devono coincidere!

---

## Query Ottimizzate

### 1. Fontanelle Vicine (Raggio)
```python
db.fontanelle.find({
    "coordinate": {
        "$near": {
            "$geometry": { "type": "Point", "coordinates": [9.1845, 45.4642] },
            "$maxDistance": 1000  # metri
        }
    }
}).limit(10)
```
**Indice usato:** `idx_fontanelle_coordinate_geospatial` ✓ Veloce

### 2. Fontanelle in un'Area
```python
db.fontanelle.find({
    "coordinate": {
        "$geoWithin": {
            "$geometry": { "type": "Polygon", "coordinates": [...] }
        }
    }
})
```
**Indice usato:** `idx_fontanelle_coordinate_geospatial` ✓ Veloce

### 3. Fontanelle per Stato + Quartiere
```python
db.fontanelle.find({
    "quartiere": "Centro",
    "stato": "attiva"
})
```
**Indice usato:** `idx_fontanelle_quartiere_stato` ✓ Veloce

### 4. NIL Contienen un Punto
```python
db.nil.find({
    "geometria": {
        "$geoIntersects": {
            "$geometry": { "type": "Point", "coordinates": [9.1845, 45.4642] }
        }
    }
})
```
**Indice usato:** `idx_nil_geometria_geospatial` ✓ Veloce

---

## Aggregation Pipeline (Analisi Avanzate)

### Fontanelle più Vicine con Distanze
```python
db.fontanelle.aggregate([
    {
        "$geoNear": {
            "near": { "type": "Point", "coordinates": [9.1845, 45.4642] },
            "maxDistance": 5000,
            "distanceField": "distanza_metri",
            "spherical": True
        }
    },
    {
        "$limit": 10
    },
    {
        "$project": {
            "nome": 1,
            "quartiere": 1,
            "distanza_km": { "$divide": ["$distanza_metri", 1000] }
        }
    }
])
```

### Fontanelle per NIL con Conteggi
```python
db.fontanelle.aggregate([
    {
        "$group": {
            "_id": "$nil_id",
            "total": { "$sum": 1 },
            "attive": {
                "$sum": { "$cond": [{ "$eq": ["$stato", "attiva"] }, 1, 0] }
            },
            "accessibili": {
                "$sum": { "$cond": ["$accessibilita", 1, 0] }
            }
        }
    },
    {
        "$lookup": {
            "from": "nil",
            "localField": "_id",
            "foreignField": "_id",
            "as": "nil_info"
        }
    }
])
```

---

## Gestione Errori

### Connessione Fallita
```python
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

try:
    MongoDBConnection.connect()
except (ConnectionFailure, ServerSelectionTimeoutError):
    # MongoDB non disponibile
    # → Fallback a cache locale o risposta di errore
    pass
```

### Validazione Pydantic
```python
from pydantic import ValidationError

try:
    fontanella = FontanellaCreate(**data)
except ValidationError as e:
    # Dati non validi
    return {"errors": e.errors()}
```

### Operazione DB Fallita
```python
from pymongo.errors import DuplicateKeyError

try:
    db.nil.insert_one({"numero": 1, ...})
except DuplicateKeyError:
    # Numero NIL già esiste
    raise HTTPException(status_code=409, detail="NIL number already exists")
```

---

## Testing Connessione

### 1. Via Script
```bash
python -m backend.fastapi_app.scripts.init_db
```

### 2. Via Python REPL
```python
from backend.fastapi_app.core.database import MongoDBConnection

db = MongoDBConnection.get_database()
print(f"Connesso a: {db.name}")
print(f"Fontanelle: {db.fontanelle.count_documents({})}")
print(f"Indici su fontanelle: {[i['name'] for i in db.fontanelle.list_indexes()]}")
MongoDBConnection.disconnect()
```

### 3. Via mongosh
```bash
mongosh mongodb://localhost:27017/dbSpaziali

# Nel prompt mongosh:
db.fontanelle.countDocuments()
db.nil.countDocuments()
db.fontanelle.getIndexes()
db.nil.getIndexes()
```

---

## Troubleshooting

| Problema | Causa | Soluzione |
|----------|-------|-----------|
| `ConnectionFailure` | MongoDB non running | `mongod` avviare MongoDB |
| Indici non vengono creati | Nomi troppo lunghi | Ridurre nomi o usare MongoDB 4.4+ |
| Query geospaziale lenta | Indice 2dsphere mancante | Eseguire `init_db.py` |
| ObjectId parsing error | Formato string non valido | Validare hex string 24 caratteri |
| Duplicate key error | Numero NIL duplicato | Incrementare numero o verificare DB |

---

## Prossimi Step

1. ✓ Connessione MongoDB configurata
2. ✓ Collection e indici creati
3. ✓ Pydantic schemas definiti
4. ✗ PROSSIMO: Rotte CRUD per fontanelle/NIL
5. ✗ Poi: Query avanzate geospaziali
6. ✗ Frontend con mappa interattiva
