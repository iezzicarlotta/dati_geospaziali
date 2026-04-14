# Modello Concettuale Database - Dati Geospaziali

## Diagramma ER (Entity-Relationship)

```
┌─────────────────────────────────────────────────────────────────┐
│                       NIL (Nuclei Identità)                      │
├─────────────────────────────────────────────────────────────────┤
│ PK: _id (ObjectId)                                               │
│                                                                  │
│ numero (Integer, Unique) ──────────┐                             │
│ nome (String)                       │                             │
│ zona (String)                       │                             │
│ geometria (GeoJSON Polygon)         │ 1                           │
│ descrizione (String)                │                             │
│ popolazione (Integer)               │                             │
│ area_kmq (Float)                    │                             │
│ comuni_interessati (Array<String>)  │                             │
│ fontanelle_count (Integer) ◄────────┼─────┐                      │
│ createdAt (DateTime)                │     │                      │
│ updatedAt (DateTime)                │     │ aggregazione         │
│                                      │     │                      │
└──────────────┬───────────────────────────────────────────────────┘
               │
               │ 1:N (una NIL contiene molte fontanelle)
               │
┌──────────────▼───────────────────────────────────────────────────┐
│                      FONTANELLE (Fontanelle)                     │
├─────────────────────────────────────────────────────────────────┤
│ PK: _id (ObjectId)                                               │
│                                                                  │
│ FK: nil_id (ObjectId) ────────────────┐                          │
│ nome (String)                         │                          │
│ descrizione (String)                  │                          │
│ coordinate (GeoJSON Point)            │ N                        │
│ indirizzo (String)                    │                          │
│ quartiere (String)                    │ 1                        │
│ consorzio (String)                    │                          │
│ data_installazione (DateTime)         │                          │
│ stato (Enum: attiva|manutenzione|...) │                          │
│ accessibilita (Boolean)               │                          │
│ note (String)                         │                          │
│ createdAt (DateTime)                  │                          │
│ updatedAt (DateTime)                  │                          │
│                                       │                          │
└───────────────────────────────────────┴──────────────────────────┘
```

---

## Tabella Compariativa con DB Relazionale

| Aspetto | SQL Relazionale | MongoDB (nostro) |
|---------|-----------------|------------------|
| **Tabella** | `nil`, `fontanelle` | Collection `nil`, `fontanelle` |
| **Riga** | Record | Document (JSON) |
| **Colonna** | Field | Field |
| **Id Primaria** | `id INT PRIMARY KEY` | `_id ObjectId` |
| **Relazione 1:N** | Foreign Key | Soft reference (nil_id) |
| **Indice Spaziale** | SPATIAL INDEX | 2dsphere |
| **Join** | SQL JOIN | MongoDB lookup / aggregation |
| **Schema** | Rigido (CREATE TABLE) | Flessibile (Pydantic valida) |

---

## Flusso di Dati

### 1. Creazione Fontanella

```
HTTP POST /fontanelle
         ↓
  Request JSON Body
         ↓
Validazione Pydantic (FontanellaCreate)
         ↓
  Conversione a Dict
         ↓
  MongoDB INSERT
         ↓
  _id generato da MongoDB
         ↓
HTTP 201 + JSON response
```

### 2. Query Geospaziale

```
HTTP GET /fontanelle?lat=45.46&lon=9.18&max_distance_m=1000
         ↓
Parsing parametri
         ↓
Geometria GeoJSON Point
         ↓
MongoDB $near query con indice 2dsphere
         ↓
  Risultati ordinati per distanza
         ↓
Pydantic serialization (ObjectId → string)
         ↓
HTTP 200 + JSON array response
```

### 3. Query di Intersezione Area

```
HTTP GET /fontanelle?nil_id=507f1f77bcf86cd799439011
         ↓
 Lookup NIL per geometria
         ↓
MongoDB $geoWithin query
         ↓
Fontanelle entro perimetro
         ↓
HTTP 200 + JSON array response
```

---

## Struttura JSON Document

### FONTANELLA Document
```json
{
  "_id": {
    "$oid": "507f1f77bcf86cd799439011"
  },
  "nome": "Fontanella Piazza Duomo",
  "descrizione": "Fontanella storica in Piazza Duomo",
  "coordinate": {
    "type": "Point",
    "coordinates": [
      9.1845,
      45.4642
    ]
  },
  "indirizzo": "Piazza Duomo, Milano",
  "quartiere": "Centro Storico",
  "nil_id": {
    "$oid": "507f1f77bcf86cd799439012"
  },
  "consorzio": "Consortium A",
  "data_installazione": {
    "$date": "2010-06-15T00:00:00.000Z"
  },
  "stato": "attiva",
  "accessibilita": true,
  "note": "Fontanella ben mantenuta",
  "createdAt": {
    "$date": "2024-01-15T10:30:00.000Z"
  },
  "updatedAt": {
    "$date": "2024-01-15T10:30:00.000Z"
  }
}
```

### NIL Document
```json
{
  "_id": {
    "$oid": "507f1f77bcf86cd799439012"
  },
  "nome": "NIL 1 - Centro Storico",
  "numero": 1,
  "zona": "Centro",
  "geometria": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          9.17,
          45.45
        ],
        [
          9.19,
          45.45
        ],
        [
          9.19,
          45.47
        ],
        [
          9.17,
          45.47
        ],
        [
          9.17,
          45.45
        ]
      ]
    ]
  },
  "descrizione": "Area centrale di Milano",
  "popolazione": 15000,
  "area_kmq": 2.5,
  "comuni_interessati": [
    "Milano"
  ],
  "fontanelle_count": 5,
  "createdAt": {
    "$date": "2024-01-01T00:00:00.000Z"
  },
  "updatedAt": {
    "$date": "2024-01-01T00:00:00.000Z"
  }
}
```

---

## Cardinalità Relazioni

### NIL ↔ FONTANELLE

| NIL | Fontanelle | Descrizione |
|-----|-----------|-------------|
| 0..1 | 0..* | Un NIL può non avere fontanelle (nuovo), o avere molte |
| 1 | 0 | Una fontanella in manutenzione potrebbe riferire a NIL inesistente (soft FK) |
| 1 | 1..* | Normalmente 1+ fontanelle per NIL |

**Tipo relazione**: 1 to Many (1:N)  
**Implementazione**: Soft Foreign Key via `nil_id` in fontanella

---

## Indici - Analisi Performance

### Senza Indici
```
Query: db.fontanelle.find({coordinate: {$near: {$geometry: ..., $maxDistance: 1000}}})
Result: Collection Scan (scansiona TUTTI i 1M di documenti) → 10+ secondi ❌
```

### Con Indice 2dsphere
```
Query: (stessa query)
Result: Uses 2dsphere index → 10-50 millisecondi ✓
```

---

## Vincoli di Business Logic

### Unicità
- `nil.numero` - Ogni NIL deve avere un numero univoco (1-999)
- `fontanelle._id` - MongoDB garantisce unicità _id

### Obbligatorietà
- `fontanelle.nome` - Sempre obbligatorio
- `fontanelle.coordinate` - Sempre obbligatorio (dati geospaziali)
- `fontanelle.indirizzo` - Sempre obbligatorio
- `nil.numero` - Sempre obbligatorio
- `nil.nome` - Sempre obbligatorio
- `nil.geometria` - Sempre obbligatorio

### Intervalità
- `fontanella.stato` - Enum: `attiva | manutenzione | disattiva`
- `fontanella.accessibilita` - Boolean
- `nil.numero` - Integer 1-999

---

## Denormalizzazione: `fontanelle_count`

In NIL aggiungiamo `fontanelle_count` per velocizzare query analitiche:

```javascript
// Senza denormalizzazione
db.fontanelle.aggregate([
  {$group: {_id: "$nil_id", count: {$sum: 1}}}
])
// → Scann Aggregate necessario

// Con denormalizzazione
db.nil.find({}, {fontanelle_count: 1})
// → Query diretta, istantanea ✓
```

**Trade-off**: Coerenza vs Performance
- Su UPDATE fontanella: aggiornare conta in NIL (trigger o app logic)
- Rischio: conta desincronizzata se errore
- Beneficio: Query rapide

---

## Scalabilità Future

### Se dati crescono (10M+ fontanelle):
1. ✓ Indici 2dsphere ottimizzano ricerche spaziali
2. ✓ Indici composti (quartiere, stato) per filtri veloci
3. ✓ Aggregation pipeline per analitiche
4. Possibile sharding su `nil_id` o `quartiere`
5. Possibile replica set per alta disponibilità

### Se complesso cresce:
1. ✓ Pydantic per validazione
2. Possibile cache Redis per query frequenti
3. Possibile search full-text (MongoDB Text Indexes)
4. Possibile graph per relazioni NIL-NIL

---

## Conclusione

Attualmente il modello supporta:
- ✓ Query geospaziali per vicinanza
- ✓ Query per area/intersezione
- ✓ Aggregazioni NIL per statistiche
- ✓ Filtri by status/quartiere
- ✓ Relazioni 1:N tra NIL e fontanelle

Struttura è **pronta per production-grade geospatial queries**.
