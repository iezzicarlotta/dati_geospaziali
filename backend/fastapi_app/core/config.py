"""Centralized application settings (placeholder)."""

from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = "Fontanelle Milano"
    environment: str = "development"


settings = Settings()
