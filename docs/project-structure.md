# Albero progetto (bootstrap)

```text
.
├── README.md
├── backend/
│   ├── fastapi_app/
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       └── routes/
│   │   │           ├── __init__.py
│   │   │           └── fontanelle.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── fontanella.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── fontanelle_service.py
│   └── flask_app/
│       ├── app.py
│       ├── blueprints/
│       │   ├── __init__.py
│       │   └── web.py
│       ├── templates/
│       │   ├── base.html
│       │   └── home.html
│       └── static/
│           ├── css/
│           │   └── app.css
│           └── js/
│               └── app.js
├── config/
│   └── settings.toml
├── environments/
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── main.js
│       ├── components/
│       │   └── README.md
│       ├── pages/
│       │   └── README.md
│       └── styles/
│           └── base.css
├── database/
│   └── mongodb/
│       ├── init/
│       │   └── README.md
│       └── indexes/
│           └── README.md
├── shared/
│   ├── components/
│   │   ├── __init__.py
│   │   └── README.md
│   └── utils/
│       ├── __init__.py
│       └── README.md
├── scripts/
│   └── bootstrap.sh
├── tests/
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_placeholder.py
│   └── unit/
│       ├── __init__.py
│       └── test_placeholder.py
├── infra/
│   └── docker-compose.yml
├── pyproject.toml
└── .gitignore
```

Tutti i file sono volutamente impostati come placeholder per evitare implementazione anticipata di logica applicativa, query o UI completa.
