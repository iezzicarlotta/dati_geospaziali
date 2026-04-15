"""
Data Transfer Objects and mappers for API responses.

This module handles conversion between domain models and API response DTOs,
ensuring clean separation between internal models and external API contracts.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from backend.fastapi_app.models.fontanella import (
    Fontanella,
    Coordinate,
    NIL,
    NILStatistics,
    FontanellaSearchResult,
    ChoroplethData,
)


@dataclass
class CoordinateDTO:
    """DTO for geographic coordinate (GeoJSON Point)."""
    longitude: float
    latitude: float
    
    @classmethod
    def from_domain(cls, coord: Coordinate) -> "CoordinateDTO":
        """Convert from domain Coordinate."""
        return cls(longitude=coord.longitude, latitude=coord.latitude)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class FontanellaDTO:
    """DTO for Fountain response."""
    id: str
    object_id: Optional[str]
    nil_id: int
    coordinate: CoordinateDTO
    name: Optional[str] = None
    description: Optional[str] = None
    municipio: Optional[str] = None
    cap: Optional[str] = None
    geometry_type: str = "Point"
    
    @classmethod
    def from_domain(cls, fountain: Fontanella) -> "FontanellaDTO":
        """Convert from domain Fontanella model."""
        return cls(
            id=str(fountain.id),
            object_id=fountain.object_id,
            nil_id=fountain.nil_id,
            coordinate=CoordinateDTO.from_domain(fountain.coordinate),
            name=fountain.name,
            description=fountain.description,
            municipio=fountain.municipio,
            cap=fountain.cap,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Flatten nested coordinate
        data["coordinate"] = self.coordinate.to_dict()
        return data


@dataclass
class NILStatisticsDTO:
    """DTO for NIL statistics (used in choropleth)."""
    nil_id: int
    nil_name: str
    fountain_count: int
    area_km2: Optional[float]
    density_fountains_per_km2: float
    color_class: str
    
    @classmethod
    def from_domain(cls, stats: NILStatistics) -> "NILStatisticsDTO":
        """Convert from domain NILStatistics."""
        return cls(
            nil_id=stats.nil_id,
            nil_name=stats.nil_name,
            fountain_count=stats.fountain_count,
            area_km2=stats.area_km2,
            density_fountains_per_km2=stats.density,
            color_class=stats.color_class.value,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class NILDTO:
    """DTO for NIL (neighborhood) response."""
    id: str
    nil_id: int
    name: str
    municipio: Optional[str] = None
    geometry_type: str = "Polygon"
    
    @classmethod
    def from_domain(cls, nil: NIL) -> "NILDTO":
        """Convert from domain NIL model."""
        return cls(
            id=str(nil.id),
            nil_id=nil.nil_id,
            name=nil.name,
            municipio=nil.municipio,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class FontanellaSearchResultDTO:
    """DTO for paginated fountain search results."""
    items: List[FontanellaDTO]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    
    @classmethod
    def from_domain(cls, domain_result: FontanellaSearchResult) -> "FontanellaSearchResultDTO":
        """Convert from domain FontanellaSearchResult."""
        items = [FontanellaDTO.from_domain(f) for f in domain_result.items]
        
        total_pages = (domain_result.total_count + domain_result.page_size - 1) // domain_result.page_size
        page = (domain_result.skip // domain_result.page_size) + 1
        
        return cls(
            items=items,
            total_count=domain_result.total_count,
            page=page,
            page_size=domain_result.page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "items": [item.to_dict() for item in self.items],
            "total_count": self.total_count,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
            "has_next": self.has_next,
            "has_previous": self.has_previous,
        }


@dataclass
class ChoroplethDataDTO:
    """DTO for choropleth map data."""
    statistics: List[NILStatisticsDTO]
    bounds: Dict[str, float]
    min_density: float
    max_density: float
    total_fountains: int
    
    @classmethod
    def from_domain(cls, data: ChoroplethData) -> "ChoroplethDataDTO":
        """Convert from domain ChoroplethData."""
        stats_dtos = [NILStatisticsDTO.from_domain(s) for s in data.statistics]
        
        return cls(
            statistics=stats_dtos,
            bounds=data.bounds or {},
            min_density=data.min_density,
            max_density=data.max_density,
            total_fountains=sum(s.fountain_count for s in data.statistics),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "statistics": [s.to_dict() for s in self.statistics],
            "bounds": self.bounds,
            "min_density": self.min_density,
            "max_density": self.max_density,
            "total_fountains": self.total_fountains,
        }


class DTOMapper:
    """Utility mapper for converting domain models to DTOs."""
    
    @staticmethod
    def fountain_to_dto(fountain: Fontanella) -> FontanellaDTO:
        """Convert Fountain to DTO."""
        return FontanellaDTO.from_domain(fountain)
    
    @staticmethod
    def fountains_to_dto_list(fountains: List[Fontanella]) -> List[FontanellaDTO]:
        """Convert list of Fountains to DTO list."""
        return [FontanellaDTO.from_domain(f) for f in fountains]
    
    @staticmethod
    def search_result_to_dto(result: FontanellaSearchResult) -> FontanellaSearchResultDTO:
        """Convert search result to DTO."""
        return FontanellaSearchResultDTO.from_domain(result)
    
    @staticmethod
    def nil_to_dto(nil: NIL) -> NILDTO:
        """Convert NIL to DTO."""
        return NILDTO.from_domain(nil)
    
    @staticmethod
    def nils_to_dto_list(nils: List[NIL]) -> List[NILDTO]:
        """Convert list of NILs to DTO list."""
        return [NILDTO.from_domain(n) for n in nils]
    
    @staticmethod
    def choropleth_to_dto(data: ChoroplethData) -> ChoroplethDataDTO:
        """Convert choropleth data to DTO."""
        return ChoroplethDataDTO.from_domain(data)
