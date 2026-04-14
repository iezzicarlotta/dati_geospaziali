"""Bootstrap FastAPI application (skeleton only)."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Fontanelle Milano API", version="0.1.0")
    return app


app = create_app()
