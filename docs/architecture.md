# Architettura iniziale (Step 0)

## Obiettivo
Definire una base ordinata, estendibile e testabile per integrare progressivamente:
- backend FastAPI,
- backend Flask,
- frontend HTML/JS,
- MongoDB.

## Scelte architetturali (sintesi)
1. **Separazione per responsabilità**
   - `backend/fastapi_app`: API e dominio applicativo lato servizi.
   - `backend/flask_app`: entrypoint web e gestione template/static server-side.
   - `frontend/`: asset e codice UI evolutivo indipendente.
   - `database/`: bootstrap MongoDB, script di inizializzazione e indici futuri.
   - `shared/`: elementi condivisi cross-layer (costanti, helper, componenti riutilizzabili).

2. **Versionamento API sin da subito**
   - Presenza di `api/v1/` in FastAPI per garantire evoluzione backward-compatible.

3. **Configurazione centralizzata**
   - Cartella `config/` e file ambiente in `environments/` per evitare hardcode.

4. **Testability by design**
   - Cartella `tests/` separata in unit/integration per crescita progressiva.

5. **Deployment-ready**
   - `infra/` contiene basi per containerizzazione/orchestrazione futura.

## Responsabilità dei moduli
- `backend/fastapi_app/main.py`: bootstrap app FastAPI (senza rotte complete).
- `backend/fastapi_app/core/config.py`: gestione configurazione e variabili ambiente.
- `backend/fastapi_app/api/v1/routes/`: namespace rotte (stub).
- `backend/fastapi_app/schemas/`: modelli di input/output (stub).
- `backend/fastapi_app/services/`: logica business futura (stub).
- `backend/flask_app/app.py`: bootstrap Flask app.
- `backend/flask_app/blueprints/`: blueprint modulari Flask (stub).
- `backend/flask_app/templates/`: template HTML base.
- `backend/flask_app/static/`: static CSS/JS serviti da Flask.
- `frontend/src/`: codice JS/CSS/componenti lato client.
- `frontend/public/`: file statici pubblici e HTML di ingresso.
- `database/mongodb/init/`: script iniziali database (placeholder).
- `database/mongodb/indexes/`: definizioni indici (placeholder).
- `shared/components/`: componenti riutilizzabili.
- `shared/utils/`: utility condivise.
- `scripts/`: comandi operativi (setup/dev/test, placeholder).
- `tests/`: suite di test.
- `infra/`: file di infrastruttura (compose, dockerfile, ecc.).

## File iniziali consigliati
- Bootstrap applicazioni: `backend/fastapi_app/main.py`, `backend/flask_app/app.py`
- Config: `config/settings.toml`, `environments/.env.example`
- Frontend base: `frontend/public/index.html`, `frontend/src/main.js`, `frontend/src/styles/base.css`
- DB bootstrap: `database/mongodb/init/README.md`, `database/mongodb/indexes/README.md`
- Operatività: `scripts/bootstrap.sh`, `infra/docker-compose.yml`
- QA: `tests/unit/test_placeholder.py`, `tests/integration/test_placeholder.py`
