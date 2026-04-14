# Database Directory Structure

## Cartella: `database/`

Questa cartella contiene le risorse e documentazione relative alla gestione del database MongoDB.

### Sottocartelle

#### `mongodb/`
- **Descrizione**: Configurazioni specifiche per MongoDB
- **Sottodirectory**:
  - `init/` - Script di inizializzazione (da popolare)
  - `indexes/` - Documentazione indici (da popolare)

---

## Actual Database Configuration

**Nota**: La configurazione effettiva di MongoDB si trova in:

```
backend/fastapi_app/
├── core/
│   ├── config.py           → Settings (MONGODB_URL, database name)
│   ├── database.py         → Connection management
│   └── indexes.py          → Index definitions
│
└── scripts/
    ├── init_db.py          → Database initialization
    └── test_connection.py  → Connection testing
```

---

## Database Name: `dbSpaziali`

### Collections
1. **`fontanelle`** - Geospatial points for public fountains
2. **`nil`** - Geospatial areas (Nuclei di Identità Locale)

### Indexes
Vedi `docs/MONGODB_ARCHITECTURE.md` per dettagli completi.

---

## Utilizzo

### Inizializzazione
```bash
python -m backend.fastapi_app.scripts.init_db
```

### Test
```bash
python -m backend.fastapi_app.scripts.test_connection
```

### Query Manuale
```bash
mongosh mongodb://localhost:27017/dbSpaziali
```

---

## File di Riferimento

- [DATABASE.md](../DATABASE.md) - Struttura collection e query
- [MONGODB_ARCHITECTURE.md](../MONGODB_ARCHITECTURE.md) - Best practices
- [SETUP_MONGODB_COMPLETE.md](../SETUP_MONGODB_COMPLETE.md) - Quick start completo
