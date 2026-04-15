"""Data access layer with Repository pattern."""

from backend.fastapi_app.repositories.fontanella import (
    FontanellaRepository,
    NILRepository,
    RepositoryError,
)

__all__ = [
    "FontanellaRepository",
    "NILRepository",
    "RepositoryError",
]
