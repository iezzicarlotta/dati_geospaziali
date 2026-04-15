"""
Domain models for Fontanella application.

These models represent the business logic layer between persistence (MongoDB)
and the application logic. They are independent from HTTP schemas.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ========================== VALUE OBJECTS ==========================

@dataclass
class Coordinate:
    """Represents a geographic point in WGS84 (EPSG:4326)."""
    
    longitude: float
    latitude: float
    
    def to_geojson_point(self) -> Dict[str, Any]:
        """Convert to GeoJSON Point format."""
        return {
            "type": "Point",
            "coordinates": [self.longitude, self.latitude]
        }
    
    @classmethod
    def from_geojson_point(cls, point: Dict[str, Any]) -> "Coordinate":
        """Create from GeoJSON Point."""
        if point.get("type") != "Point":
            raise ValueError("Invalid GeoJSON Point")
        coords = point.get("coordinates", [])
        if len(coords) != 2:
            raise ValueError("Coordinates must have [longitude, latitude]")
        return cls(longitude=coords[0], latitude=coords[1])


@dataclass
class BoundingBox:
    """Represents a geographic bounding box."""
    
    min_longitude: float
    min_latitude: float
    max_longitude: float
    max_latitude: float
    
    def to_geojson_polygon(self) -> Dict[str, Any]:
        """Convert to GeoJSON Polygon."""
        coords = [
            [self.min_longitude, self.min_latitude],
            [self.max_longitude, self.min_latitude],
            [self.max_longitude, self.max_latitude],
            [self.min_longitude, self.max_latitude],
            [self.min_longitude, self.min_latitude]
        ]
        return {
            "type": "Polygon",
            "coordinates": [coords]
        }


# ========================== DOMAIN MODELS ==========================

@dataclass
class Fontanella:
    """
    Domain model for a public fountain (Fontanella).
    
    Represents a single fountain with geographic and administrative information.
    
    Attributes:
        id: Unique identifier from MongoDB ObjectId
        object_id: Original object ID from source data
        nil_id: ID of the NIL (neighborhood area) containing this fountain
        nil_name: Name of the NIL
        coordinate: Geographic location (longitude, latitude)
        cap: Postal code
        municipio: Municipality number (Milan district)
    """
    
    id: Optional[str] = None  # MongoDB ObjectId as string
    object_id: str = ""
    nil_id: Optional[str] = None
    nil_name: Optional[str] = None
    coordinate: Optional[Coordinate] = None
    cap: Optional[str] = None
    municipio: Optional[str] = None
    
    def is_valid(self) -> bool:
        """Check if fontanella has required fields."""
        return (
            self.object_id and
            self.coordinate is not None and
            self.nil_id is not None
        )
    
    def distance_to(self, other_coord: Coordinate) -> float:
        """
        Estimate distance to another coordinate in meters (Haversine).
        
        Note: This is an approximation. For precise geospatial queries,
        use MongoDB's geospatial operators.
        """
        if self.coordinate is None:
            raise ValueError("Fontanella has no coordinate")
        
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Earth radius in meters
        
        lat1, lon1 = radians(self.coordinate.latitude), radians(self.coordinate.longitude)
        lat2, lon2 = radians(other_coord.latitude), radians(other_coord.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return R * c


@dataclass
class NIL:
    """
    Domain model for a NIL (Nucleo di Identità Locale - Local Identity Nucleus).
    
    Represents a geographic area/neighborhood in Milan with administrative
    information.
    
    Attributes:
        id: Unique identifier from MongoDB ObjectId
        nil_id: Numeric ID of the NIL (1-999)
        name: Full name of the NIL
        valid_from: Start date of validity
        valid_to: End date of validity (or "Vigente" if still valid)
        area: Area in square meters (from geodata)
        perimeter: Perimeter in meters (from geodata)
        fountain_count: Number of fountains in this NIL (computed)
    """
    
    id: Optional[str] = None  # MongoDB ObjectId as string
    nil_id: Optional[int] = None
    name: str = ""
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    area: Optional[float] = None
    perimeter: Optional[float] = None
    fountain_count: int = 0
    
    @property
    def is_valid(self) -> bool:
        """Check if NIL is currently valid."""
        return self.valid_to in ["Vigente", None]
    
    @property
    def density(self) -> Optional[float]:
        """Fountains per square kilometer."""
        if self.area and self.area > 0:
            return (self.fountain_count / self.area) * 1_000_000
        return None


@dataclass
class NILStatistics:
    """
    Aggregated statistics for a NIL.
    
    Used for choropleth map data and analytics.
    """
    
    nil_id: int
    nil_name: str
    fountain_count: int
    area: Optional[float] = None
    perimeter: Optional[float] = None
    density: Optional[float] = None
    
    @property
    def color_class(self) -> str:
        """
        Classify density for choropleth coloring.
        
        Returns: "very_low", "low", "medium", "high", "very_high"
        """
        if self.density is None:
            return "unknown"
        
        if self.density < 1:
            return "very_low"
        elif self.density < 5:
            return "low"
        elif self.density < 10:
            return "medium"
        elif self.density < 20:
            return "high"
        else:
            return "very_high"


@dataclass
class FontanellaSearchResult:
    """
    Result of a search for fountains.
    
    Includes pagination and filtering metadata.
    """
    
    fountains: List[Fontanella]
    total: int
    skip: int = 0
    limit: int = 20
    filters_applied: Dict[str, Any] = None
    
    @property
    def page(self) -> int:
        """Compute current page number."""
        return (self.skip // self.limit) + 1 if self.limit > 0 else 1
    
    @property
    def total_pages(self) -> int:
        """Compute total number of pages."""
        return (self.total + self.limit - 1) // self.limit if self.limit > 0 else 1
    
    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        return self.skip + self.limit < self.total
    
    @property
    def has_previous(self) -> bool:
        """Check if there's a previous page."""
        return self.skip > 0


@dataclass
class NearbyFountainsResult:
    """
    Result of a nearby search (geospatial query).
    
    Fountains are sorted by distance from the search point.
    """
    
    center_coordinate: Coordinate
    radius_meters: int
    fountains: List[Fontanella]
    
    @property
    def count(self) -> int:
        """Number of fountains found."""
        return len(self.fountains)


# ========================== SEARCH FILTERS ==========================

@dataclass
class FontanellaFilters:
    """
    Filters for searching fountains.
    
    Supports multiple filtering criteria that can be combined.
    """
    
    nil_id: Optional[str] = None
    nil_name: Optional[str] = None  # For text search
    municipio: Optional[str] = None
    cap: Optional[str] = None
    
    def has_filters(self) -> bool:
        """Check if any filters are active."""
        return any([
            self.nil_id,
            self.nil_name,
            self.municipio,
            self.cap
        ])


@dataclass
class GeospatialFilters:
    """
    Geospatial filters for searching fountains by location.
    """
    
    center: Coordinate
    max_distance_meters: int = 500


# ========================== CHOROPLETH DATA ==========================

@dataclass
class ChoroplethData:
    """
    Data structure for choropleth map visualization.
    
    Contains statistics for all NILs to enable density-based coloring.
    """
    
    statistics: List[NILStatistics]
    min_density: float = 0.0
    max_density: float = 1.0
    
    def get_stats_by_nil_id(self, nil_id: int) -> Optional[NILStatistics]:
        """Get statistics for a specific NIL."""
        for stat in self.statistics:
            if stat.nil_id == nil_id:
                return stat
        return None
    
    def compute_bounds(self) -> None:
        """Compute min/max density from statistics."""
        densities = [s.density for s in self.statistics if s.density is not None]
        if densities:
            self.min_density = min(densities)
            self.max_density = max(densities)
