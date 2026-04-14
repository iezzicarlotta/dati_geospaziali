# MongoDB Database Setup - Dati Geospaziali

## Panoramica Struttura

Il database **`dbSpaziali`** contiene due collection principali con **formato GeoJSON Feature**:
- **`fontanelle`** - Punti geografici di fontanelle pubbliche a Milano
- **`nil`** - Aree geografiche (Nuclei di Identità Locale)

---

## Collection: FONTANELLE (GeoJSON Feature Format)

### Documento di Esempio
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

### Campi
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `type` | String | Sempre "Feature" (GeoJSON standard) |
| `properties.objectID` | String | ID univoco della fontanella |
| `properties.CAP` | String | Codice postale |
| `properties.MUNICIPIO` | String | Numero municipio Milano |
| `properties.ID_NIL` | String | ID del NIL contenente |
| `properties.NIL` | String | Nome dell'area NIL |
| `properties.LONG_X_4326` | Number | Longitudine WGS84 |
| `properties.LAT_Y_4326` | Number | Latitudine WGS84 |
| `properties.Location` | String | Formato testo coordinate |
| `geometry.type` | String | Sempre "Point" |
| `geometry.coordinates` | Array | [longitude, latitude] |

### Indici
1. **`idx_fontanelle_geometry_geospatial`** (2dsphere su `geometry`)
   - Abilita query geospaziali: ricerca per distanza, entro area, etc.
   - ESSENZIALE per le query di vicinanza

2. **`idx_fontanelle_nil_id`** (ascendente su `properties.ID_NIL`)
   - Velocizza join con collection NIL
   - Ricerca fontanelle per NIL

3. **`idx_fontanelle_municipio`** (ascendente su `properties.MUNICIPIO`)
   - Filtri per municipio operativo

4. **`idx_fontanelle_cap`** (ascendente su `properties.CAP`)
   - Filtri per codice postale

---

## Collection: NIL (GeoJSON Feature Format)

### Documento di Esempio
```json
{
  "_id": ObjectId("69de005fd8c4381cc41d186d"),
  "type": "Feature",
  "id": 89,
  "properties": {
    "ID_NIL": 48,
    "NIL": "RONCHETTO SUL NAVIGLIO - Q.RE LODOVICO IL MORO",
    "Valido_dal": "05/02/2020",
    "Valido_al": "Vigente",
    "Fonte": "Milano 2030 - PGT Approvato",
    "Shape_Length": 8723.368714059716,
    "Shape_Area": 2406306.0789698716,
    "OBJECTID": 89
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [[...coordinate_array...]]
  }
}
```

### Campi
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `_id` | ObjectId | ID univoco del documento MongoDB |
| `type` | String | Sempre "Feature" (GeoJSON standard) |
| `id` | Integer | ID feature progressivo |
| `properties.ID_NIL` | Integer | Numero univoco del NIL (1-999) |
| `properties.NIL` | String | Nome dell'area NIL |
| `properties.Valido_dal` | String | Data inizio validità |
| `properties.Valido_al` | String | Data fine validità (o "Vigente") |
| `properties.Fonte` | String | Fonte dati (PGT) |
| `properties.Shape_Length` | Float | Perimetro in unità geografiche |
| `properties.Shape_Area` | Float | Area in unità geografiche |
| `properties.OBJECTID` | Integer | ID originario |
| `geometry.type` | String | Sempre "Polygon" |
| `geometry.coordinates` | Array | Array di linear rings (confini) |

### Indici
1. **`idx_nil_geometry_geospatial`** (2dsphere su `geometry`)
   - Abilita query di intersezione e containment
   - ESSENZIALE per ricerche di aree

2. **`idx_nil_id_unique`** (ascendente su `properties.ID_NIL`)
   - Lookup diretto per ID NIL

3. **`idx_nil_name`** (ascendente su `properties.NIL`)
   - Lookup per nome NIL

---

## Query Geospaziali Supportate

### 1. Fontanelle entro distanza da coordinates
```javascript
db.fontanelle.find({
  "geometry": {
    "$near": {
      "$geometry": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      },
      "$maxDistance": 1000  // 1 km in metri
    }
  }
}).limit(10)
```

### 2. Fontanelle entro un'area (NIL)
```javascript
db.fontanelle.find({
  "geometry": {
    "$geoWithin": {
      "$geometry": {
        "type": "Polygon",
        "coordinates": [...polygon_coordinates...]
      }
    }
  }
})
```

### 3. NIL contenente un punto
```javascript
db.nil.find({
  "geometry": {
    "$geoIntersects": {
      "$geometry": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      }
    }
  }
})
```

### 4. Fontanelle in un municipio specifico
```javascript
db.fontanelle.find({
  "properties.MUNICIPIO": "6"
})
```

### 5. Aggregazione: fontanelle per NIL
```javascript
db.fontanelle.aggregate([
  {
    "$group": {
      "_id": "$properties.ID_NIL",
      "count": { "$sum": 1 },
      "cap_list": { "$addToSet": "$properties.CAP" }
    }
  }
])
```

---

## Setup e Testing

### 1. Prerequisiti
- MongoDB connesso e accessibile
- Database `dbSpaziali` con dati già caricati
- Python 3.11+ 
- Dipendenze installate: `pip install -r requirements.txt`

### 2. Configurazione
Copiare `.env.example` in `.env`:
```bash
cp .env.example .env
```

Editare `.env` con MongoDB remoto:
```env
MONGODB_URL=mongodb://host:port
MONGODB_DATABASE=dbSpaziali
MONGODB_TIMEOUT=30
```

### 3. Setup Database (Crea indici, preserva dati!)
```bash
python -m backend.fastapi_app.scripts.setup_db
```

Output atteso - **preserva i dati esistenti, crea solo indici**:
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

============================================================
Database Status
============================================================
NIL documents: 93
Fontanelle documents: 1847

Fontanelle indexes:
  ✓ idx_fontanelle_geometry_geospatial
  ✓ idx_fontanelle_nil_id
  ✓ _id_
  ...

✓ Setup completed successfully!
```

### 4. Test Query Geospaziale (Python)
```python
from backend.fastapi_app.core.database import MongoDBConnection

db = MongoDBConnection.get_database()

# Tutte le fontanelle entro 1km da Duomo
fontanelle = list(db.fontanelle.find({
    "geometry": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": [9.1845, 45.4642]
            },
            "$maxDistance": 1000
        }
    }
}).limit(10))

print(f"Found {len(fontanelle)} fontanelle")
for f in fontanelle:
    print(f"- {f['properties']['NIL']}")

MongoDBConnection.disconnect()
```

### 5. Integrazione FastAPI
Nel main.py:
```python
from fastapi import FastAPI
from backend.fastapi_app.core.database import MongoDBConnection

app = FastAPI()

@app.on_event("startup")
async def startup():
    MongoDBConnection.connect()

@app.on_event("shutdown")
async def shutdown():
    MongoDBConnection.disconnect()

# Le rotte potranno accedere al database:
# db = MongoDBConnection.get_database()
# fontanelle = db.fontanelle.find({...})
```

### 6. Test Query Geospaziali in MongoDB Shell
```bash
mongo mongodb://localhost:27017/dbSpaziali
```

```javascript
// Fontanelle entro 1 km da Duomo
db.fontanelle.find({
  "geometry": {
    "$near": {
      "$geometry": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      },
      "$maxDistance": 1000
    }
  }
}).limit(5)

// NIL contenente il Duomo
db.nil.find({
  "geometry": {
    "$geoIntersects": {
      "$geometry": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      }
    }
  }
})

// Conteggio fontanelle per NIL
db.fontanelle.aggregate([
  {
    "$group": {
      "_id": "$properties.ID_NIL",
      "count": { "$sum": 1 }
    }
  },
  {
    "$sort": { "count": -1 }
  }
])
```

---

## Coordinate di Riferimento (Milano)
- Duomo: [9.1845, 45.4642]
- Navigli: [9.1620, 45.4410]
- Castello Sforzesco: [9.1749, 45.4704]
- Centrale: [9.2041, 45.4858]

> Nota: Usa sempre [longitude, latitude] in GeoJSON!

---

## Prossimi Step (NON IN QUESTO TASK)
1. ✗ Rotte API per CRUD fontanelle/NIL
2. ✗ Query avanzate geospaziali
3. ✗ Frontend con mappa interattiva
4. ✗ Autenticazione/autorizzazione

```json
{
  "_id": ObjectId("..."),
  "nome": "Fontanella Piazza Duomo",
  "descrizione": "Fontanella storica in Piazza Duomo",
  "coordinate": {
    "type": "Point",
    "coordinates": [9.1845, 45.4642]
  },
  "indirizzo": "Piazza Duomo, Milano",
  "quartiere": "Centro Storico",
  "nil_id": ObjectId("..."),
  "consorzio": "Consortium A",
  "data_installazione": ISODate("2010-06-15"),
  "stato": "attiva",
  "accessibilita": true,
  "note": "Fontanella ben mantenuta",
  "createdAt": ISODate("2024-01-15T10:30:00Z"),
  "updatedAt": ISODate("2024-01-15T10:30:00Z")
}
```

### Campi
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `_id` | ObjectId | ID univoco del documento |
| `nome` | String | Nome della fontanella |
| `descrizione` | String (opt) | Breve descrizione |
| `coordinate` | GeoJSON Point | Posizione geografica [lon, lat] - **GEOSPATIAL** |
| `indirizzo` | String | Indirizzo completo |
| `quartiere` | String (opt) | Quartiere/Zona di Milano |
| `nil_id` | ObjectId (opt) | Riferimento al NIL contenente |
| `consorzio` | String (opt) | Nome del consorzio gestore |
| `data_installazione` | Date (opt) | Data di installazione |
| `stato` | Enum | `attiva \| manutenzione \| disattiva` |
| `accessibilita` | Boolean | Se accessibile a persone disabili |
| `note` | String (opt) | Note aggiuntive |
| `createdAt` | DateTime | Timestamp di creazione |
| `updatedAt` | DateTime | Timestamp ultimo aggiornamento |

### Indici
1. **`idx_fontanelle_coordinate_geospatial`** (2dsphere su `coordinate`)
   - Abilita query geospaziali: ricerca per distanza, entro area, etc.
   - ESSENZIALE per le query di vicinanza

2. **`idx_fontanelle_nil_id`** (ascendente su `nil_id`)
   - Velocizza join con collection NIL
   - Ricerca fontanelle per NIL

3. **`idx_fontanelle_stato`** (ascendente su `stato`)
   - Filtri per stato operativo

4. **`idx_fontanelle_createdAt`** (discendente su `createdAt`)
   - Sorting chronologico

5. **`idx_fontanelle_quartiere_stato`** (composto: `quartiere`, `stato`)
   - Query filtrate per quartiere + stato

---

## Collection: NIL

### Documento di Esempio
```json
{
  "_id": ObjectId("..."),
  "nome": "NIL 1 - Centro Storico",
  "numero": 1,
  "zona": "Centro",
  "geometria": {
    "type": "Polygon",
    "coordinates": [
      [
        [9.17, 45.45],
        [9.19, 45.45],
        [9.19, 45.47],
        [9.17, 45.47],
        [9.17, 45.45]
      ]
    ]
  },
  "descrizione": "Area centrale di Milano",
  "popolazione": 15000,
  "area_kmq": 2.5,
  "comuni_interessati": ["Milano"],
  "createdAt": ISODate("2024-01-01T00:00:00Z"),
  "updatedAt": ISODate("2024-01-01T00:00:00Z"),
  "fontanelle_count": 5
}
```

### Campi
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `_id` | ObjectId | ID univoco del documento |
| `nome` | String | Nome del NIL |
| `numero` | Integer | Numero univoco del NIL (1-999) - **Unique** |
| `zona` | String (opt) | Zona di Milano |
| `geometria` | GeoJSON Polygon | Confini dell'area - **GEOSPATIAL** |
| `descrizione` | String (opt) | Descrizione dell'area |
| `popolazione` | Integer (opt) | Abitanti stimati |
| `area_kmq` | Float (opt) | Superficie in km² |
| `comuni_interessati` | Array (opt) | Comuni interessati |
| `createdAt` | DateTime | Timestamp di creazione |
| `updatedAt` | DateTime | Timestamp ultimo aggiornamento |
| `fontanelle_count` | Integer (opt) | Conteggio fontanelle (denormalizzato) |

### Indici
1. **`idx_nil_geometria_geospatial`** (2dsphere su `geometria`)
   - Abilita query di intersezione e containment
   - ESSENZIALE per ricerche di aree

2. **`idx_nil_numero_unique`** (ascendente su `numero`, **Unique**)
   - Garanzia di unicità del numero NIL

3. **`idx_nil_nome`** (ascendente su `nome`)
   - Lookup diretto per nome

4. **`idx_nil_createdAt`** (discendente su `createdAt`)
   - Sorting chronologico

---

## Query Geospaziali Supportate

### 1. Fontanelle entro distanza da coordinates
```javascript
db.fontanelle.find({
  "coordinate": {
    "$near": {
      "$geometry": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      },
      "$maxDistance": 1000  // 1 km in metri
    }
  }
}).limit(10)
```

### 2. Fontanelle entro un'area (NIL)
```javascript
db.fontanelle.find({
  "coordinate": {
    "$geoWithin": {
      "$geometry": {
        "type": "Polygon",
        "coordinates": [...polygon_coordinates...]
      }
    }
  }
})
```

### 3. NIL contenente un punto
```javascript
db.nil.find({
  "geometria": {
    "$geoIntersects": {
      "$geometry": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      }
    }
  }
})
```

### 4. Aggregazione: fontanelle per NIL con distanza media
```javascript
db.fontanelle.aggregate([
  {
    "$geoNear": {
      "near": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      },
      "maxDistance": 5000,
      "distanceField": "distanza_metri",
      "spherical": true
    }
  },
  {
    "$group": {
      "_id": "$nil_id",
      "count": { "$sum": 1 },
      "distanza_media": { "$avg": "$distanza_metri" }
    }
  }
])
```

---

## Setup e Testing

### 1. Prerequisiti
- MongoDB installato e in ascolto su `mongodb://localhost:27017`
- Python 3.11+ 
- Dipendenze installate: `pip install pymongo pydantic pydantic-settings python-dotenv`

### 2. Configurazione
Copiare `.env.example` in `.env`:
```bash
cp .env.example .env
```

Editare `.env` se MongoDB è in una posizione diversa.

### 3. Inizializzazione Database
Eseguire lo script di init:
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

Setting up fontanelle indexes...
✓ Created geospatial index on fontanelle.coordinate
✓ Created index on fontanelle.nil_id
✓ Created index on fontanelle.stato
✓ Created index on fontanelle.createdAt
✓ Created compound index on fontanelle (quartiere, stato)

Setting up NIL indexes...
✓ Created geospatial index on nil.geometria
✓ Created unique index on nil.numero
✓ Created index on nil.nome
✓ Created index on nil.createdAt

✓ All indexes configured successfully

=== Seeding Sample Data ===

✓ Inserted 2 NIL records
✓ Inserted 3 fontanelle records

=== Verification ===

Collections: ['fontanelle', 'nil']
NIL documents: 2
Fontanelle documents: 3

...

✓ Database initialization completed successfully!
==================================================
```

### 4. Test di Connessione Manual (Python)
```python
from backend.fastapi_app.core.database import MongoDBConnection

# Connessione
db = MongoDBConnection.get_database()
print(f"Database connesso: {db.name}")

# Query semplice
fontanelle = db.fontanelle.find_one()
print(f"Fontanella trovata: {fontanelle['nome']}")

# Query geospatiale
result = list(db.fontanelle.aggregate([
    {
        "$geoNear": {
            "near": {
                "type": "Point",
                "coordinates": [9.1845, 45.4642]
            },
            "maxDistance": 1000,
            "distanceField": "distanza",
            "spherical": True
        }
    },
    {"$limit": 5}
]))
print(f"Fontanelle entro 1km: {len(result)}")

MongoDBConnection.disconnect()
```

### 5. Integrazione FastAPI
Nel main.py:
```python
from fastapi import FastAPI
from backend.fastapi_app.core.database import MongoDBConnection

app = FastAPI()

@app.on_event("startup")
async def startup():
    MongoDBConnection.connect()

@app.on_event("shutdown")
async def shutdown():
    MongoDBConnection.disconnect()

# Le rotte potranno accedere al database:
# db = MongoDBConnection.get_database()
```

### 6. Test Query Geospaziali in MongoDB Shell
```bash
mongo mongodb://localhost:27017/dbSpaziali
```

```javascript
// Fontanelle entro 1 km da un punto
db.fontanelle.find({
  "coordinate": {
    "$near": {
      "$geometry": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      },
      "$maxDistance": 1000
    }
  }
})

// NIL contenente un punto
db.nil.find({
  "geometria": {
    "$geoIntersects": {
      "$geometry": {
        "type": "Point",
        "coordinates": [9.1845, 45.4642]
      }
    }
  }
})
```

---

## Coordinate di Riferimento (Milano)
- Duomo: [9.1845, 45.4642]
- Navigli: [9.1620, 45.4410]
- Castello Sforzesco: [9.1749, 45.4704]
- Centrale: [9.2041, 45.4858]

> Nota: Usa sempre [longitude, latitude] in GeoJSON!

---

## Prossimi Step (NON IN QUESTO TASK)
1. ✗ Rotte API per CRUD fontanelle/NIL
2. ✗ Query avanzate geospaziali
3. ✗ Frontend con mappa interattiva
4. ✗ Autenticazione/autorizzazione
