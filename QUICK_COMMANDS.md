# ⚡ QUICK COMMANDS - NEXT STEPS

Dopo la revisione, ecco i comandi utili per procedere:

---

## 🧪 TEST & VERIFICA (Fai adesso)

```bash
# Verifica connessione MongoDB
python -m backend.fastapi_app.scripts.test_connection

# Aspettati: ✓ All tests passed!
```

```bash
# Setup database (se non già fatto)
python -m backend.fastapi_app.scripts.setup_db

# Aspettati: ✓ Setup completed successfully!
```

---

## 🚀 AVVIA IL PROGETTO (Fai adesso)

### FastAPI (porta 8000)
```bash
cd c:\Users\net.SIS-03\Desktop\dati_geospaziali
uvicorn backend.fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

**Test endpoint**:
```bash
curl http://localhost:8000/health
```

**Expected output**:
```json
{
  "status": "ok",
  "application": "Fontanelle Milano API",
  "database": "dbSpaziali"
}
```

### Flask (porta 5000) - OPZIONALE
```bash
python -m flask --app backend.flask_app.app run --port 5000
```

**Test**:
```bash
curl http://localhost:5000/
```

---

## 📚 LEGGI I DOCUMENTI (Fai adesso)

```bash
# Sommario veloce (2 min)
type QUICK_REFERENCE.md

# Sommario italiano (5 min)
type RISULTATI_REVISIONE.md

# Per stakeholder (5-10 min)
type REVIEW_EXECUTIVE_SUMMARY.md

# Analisi completa (30-45 min)
type REVIEW_STEP1_STEP2.md

# Prossimi passi STEP 3 (20-30 min)
type STEP3_INSTRUCTIONS.md
```

---

## 🔧 SVILUPPO STEP 3 (Prossimamente)

Creare file:
```bash
# API endpoint
touch backend/fastapi_app/api/v1/routes/fontanelle.py

# Frontend components
touch frontend/src/components/Map.js
touch frontend/src/pages/MapPage.js

# Test
touch tests/integration/test_geospatial.py
```

---

## 🐳 DOCKER (Opzionale)

```bash
# Build
docker build -t fontanelle-milano .

# Run with Docker Compose
docker-compose -f infra/docker-compose.yml up -d

# Stop
docker-compose -f infra/docker-compose.yml down
```

---

## 📊 VERIFICARE I FIX (Opzionale)

```bash
# Vedere test script aggiornato
type backend/fastapi_app/scripts/test_connection.py | findstr "idx_fontanelle_geometry"

# Vedere Flask integrata
type backend/fastapi_app/main:app | findstr "register_blueprint"

# Vedere type hints
type backend/fastapi_app/core/database.py | findstr "-> Database"
```

---

## 🗂️ FILE PRINCIPALI MODIFICATI

```bash
# View file modificati
dir backend/fastapi_app/scripts/test_connection.py
dir backend/flask_app/app.py
dir backend/flask_app/blueprints/web.py
dir backend/fastapi_app/core/database.py
dir backend/fastapi_app/schemas/fontanella.py
```

---

## 📍 IMPORTANTE

**Prima di procedere con STEP 3**:
1. ✅ Esegui `test_connection.py` → deve passare
2. ✅ Avvia FastAPI → deve funzionare
3. ✅ Testa `/health` endpoint → deve rispondere
4. ✅ Leggi STEP3_INSTRUCTIONS.md → per proseguire

---

## 🆘 TROUBLESHOOTING

### Se test_connection.py fallisce:
```bash
# Verifica MongoDB è running
mongosh "mongodb://localhost:27017"
use dbSpaziali
db.fontanelle.count()
db.nil.count()
```

### Se FastAPI non avvia:
```bash
# Verifiche Python
python --version  # Deve essere >= 3.11
pip list | grep -E "fastapi|pymongo|pydantic"

# Verifica import
python -c "from backend.fastapi_app.main import app; print(app)"
```

### Se Flask non funziona:
```bash
python -c "from backend.flask_app.app import app; print(app)"
```

---

## 📞 SUPPORT DOCS

| Problema | Documento |
|----------|-----------|
| Cosa fare adesso? | STEP3_INSTRUCTIONS.md |
| Come funziona il progetto? | REVIEW_STEP1_STEP2.md |
| Quali fix sono stati applicati? | FIXES_APPLIED.md |
| Sono pronto per STEP 3? | REVIEW_EXECUTIVE_SUMMARY.md |
| Voglio solo TL;DR | QUICK_REFERENCE.md |

---

## 🎯 TIMELINE CONSIGLIATO

```
OGGI
├─ Leggi RISULTATI_REVISIONE.md (5 min)
├─ Esegui test_connection.py (5 min)
└─ Avvia FastAPI (2 min)

DOMANI
├─ Leggi STEP3_INSTRUCTIONS.md (30 min)
└─ Setup ambiente STEP 3 (1-2 ore)

GIORNO 3-7
├─ Implementa API endpoints (1-2 giorni)
├─ Crea frontend Leaflet (1-2 giorni)
├─ Testing (1 giorno)
└─ Deploy (1 giorno)
```

---

## ✅ CHECKLIST PRIMA DI INIZIARE

- [ ] Letto RISULTATI_REVISIONE.md
- [ ] Eseguito test_connection.py ✓
- [ ] FastAPI avvia ✓
- [ ] Endpoint /health risponde ✓
- [ ] Database verificato (dbSpaziali) ✓
- [ ] Collection (fontanelle, nil) verificate ✓
- [ ] Letto STEP3_INSTRUCTIONS.md
- [ ] Pronto per STEP 3 🚀

---

## 🎉 PRONTO?

Quando sei pronto:
1. Esegui i test
2. Leggi STEP3_INSTRUCTIONS.md
3. Inizia lo sviluppo di STEP 3

**Buona fortuna! 🚀**

