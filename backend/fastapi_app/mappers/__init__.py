"""Data Transfer Objects and mappers for API responses."""

from backend.fastapi_app.mappers.fontanella_mapper import (
    FontanellaDTO,
    CoordinateDTO,
    NILDTO,
    NILStatisticsDTO,
    FontanellaSearchResultDTO,
    ChoroplethDataDTO,
    DTOMapper,
)

__all__ = [
    "FontanellaDTO",
    "CoordinateDTO",
    "NILDTO",
    "NILStatisticsDTO",
    "FontanellaSearchResultDTO",
    "ChoroplethDataDTO",
    "DTOMapper",
]
