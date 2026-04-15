"""Domain models for Fontanelle Milano application."""

from backend.fastapi_app.models.fontanella import (
    Coordinate,
    BoundingBox,
    Fontanella,
    NIL,
    NILStatistics,
    FontanellaSearchResult,
    NearbyFountainsResult,
    FontanellaFilters,
    GeospatialFilters,
    ChoroplethData,
)

__all__ = [
    "Coordinate",
    "BoundingBox",
    "Fontanella",
    "NIL",
    "NILStatistics",
    "FontanellaSearchResult",
    "NearbyFountainsResult",
    "FontanellaFilters",
    "GeospatialFilters",
    "ChoroplethData",
]
