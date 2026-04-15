"""
API routes for fountain (fontanelle) operations.

Provides endpoints for searching, filtering, and retrieving fountain data
for map visualization and analytics.
"""

from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, Field, validator

from backend.fastapi_app.services.fontanella_service import (
    FontanellaService,
    ServiceError,
)
from backend.fastapi_app.mappers.fontanella_mapper import DTOMapper
from backend.fastapi_app.models.fontanella import Coordinate


# Pydantic request models for validation and documentation

class SearchByNILRequest(BaseModel):
    """Request model for searching fountains by NIL."""
    nil_id: str = Field(..., description="NIL ID to search (e.g., '1', '123')")
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=20, ge=1, le=100, description="Results per page")
    
    class Config:
        schema_extra = {
            "example": {
                "nil_id": "1",
                "page": 1,
                "page_size": 20
            }
        }


class SearchByLocationRequest(BaseModel):
    """Request model for searching fountains near a location."""
    latitude: float = Field(..., ge=-90, le=90, description="Search point latitude (WGS84)")
    longitude: float = Field(..., ge=-180, le=180, description="Search point longitude (WGS84)")
    radius_meters: int = Field(default=500, ge=1, le=50000, description="Search radius in meters")
    limit: int = Field(default=50, ge=1, le=500, description="Maximum results to return")
    
    class Config:
        schema_extra = {
            "example": {
                "latitude": 45.464,
                "longitude": 9.190,
                "radius_meters": 500,
                "limit": 50
            }
        }


class AdvancedSearchRequest(BaseModel):
    """Request model for advanced fountain search with multiple filters."""
    nil_id: Optional[str] = Field(default=None, description="Filter by NIL ID")
    nil_name: Optional[str] = Field(default=None, description="Filter by NIL name (partial match)")
    municipio: Optional[str] = Field(default=None, description="Filter by municipality")
    cap: Optional[str] = Field(default=None, description="Filter by postal code")
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Results per page")
    
    class Config:
        schema_extra = {
            "example": {
                "nil_id": "1",
                "municipio": "Milano",
                "page": 1,
                "page_size": 20
            }
        }


# Pydantic response models for documentation and validation

class CoordinateResponse(BaseModel):
    """Response model for geographic coordinates."""
    longitude: float
    latitude: float


class FountainResponse(BaseModel):
    """Response model for a single fountain."""
    id: str
    object_id: Optional[str]
    nil_id: int
    coordinate: CoordinateResponse
    name: Optional[str] = None
    description: Optional[str] = None
    municipio: Optional[str] = None
    cap: Optional[str] = None
    geometry_type: str = "Point"


class PaginatedFountainResponse(BaseModel):
    """Response model for paginated fountain search results."""
    items: List[FountainResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    
    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "id": "507f1f77bcf86cd799439011",
                        "object_id": "1001",
                        "nil_id": 1,
                        "coordinate": {"longitude": 9.190, "latitude": 45.464},
                        "name": "Fontanella Centro",
                        "municipio": "Milano",
                        "cap": "20100"
                    }
                ],
                "total_count": 150,
                "page": 1,
                "page_size": 20,
                "total_pages": 8,
                "has_next": True,
                "has_previous": False
            }
        }


class NearbyFountainResponse(BaseModel):
    """Response model for nearby fountain with distance."""
    id: str
    object_id: Optional[str]
    nil_id: int
    coordinate: CoordinateResponse
    name: Optional[str] = None
    description: Optional[str] = None
    distance_meters: float
    
    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "object_id": "1001",
                "nil_id": 1,
                "coordinate": {"longitude": 9.190, "latitude": 45.464},
                "name": "Fontanella Centro",
                "distance_meters": 245.5
            }
        }


class NearbyFountainListResponse(BaseModel):
    """Response model for list of nearby fountains."""
    items: List[NearbyFountainResponse]
    search_center: CoordinateResponse
    search_radius_meters: int
    total_count: int
    
    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "id": "507f1f77bcf86cd799439011",
                        "nil_id": 1,
                        "coordinate": {"longitude": 9.190, "latitude": 45.464},
                        "name": "Fontanella Centro",
                        "distance_meters": 145.3
                    }
                ],
                "search_center": {"longitude": 9.190, "latitude": 45.464},
                "search_radius_meters": 500,
                "total_count": 12
            }
        }


class NILStatsResponse(BaseModel):
    """Response model for NIL statistics."""
    nil_id: int
    nil_name: str
    fountain_count: int
    area_km2: Optional[float] = None
    density_fountains_per_km2: float
    color_class: str
    
    class Config:
        schema_extra = {
            "example": {
                "nil_id": 1,
                "nil_name": "Centro Storico",
                "fountain_count": 45,
                "area_km2": 2.5,
                "density_fountains_per_km2": 18.0,
                "color_class": "HIGH"
            }
        }


class NILStatsTableResponse(BaseModel):
    """Response model for table of NIL statistics."""
    statistics: List[NILStatsResponse]
    total_nils: int
    total_fountains: int
    max_density: float
    min_density: float
    
    class Config:
        schema_extra = {
            "example": {
                "statistics": [
                    {
                        "nil_id": 1,
                        "nil_name": "Centro",
                        "fountain_count": 50,
                        "area_km2": 2.5,
                        "density_fountains_per_km2": 20.0,
                        "color_class": "HIGH"
                    },
                    {
                        "nil_id": 2,
                        "nil_name": "Navigli",
                        "fountain_count": 30,
                        "area_km2": 3.0,
                        "density_fountains_per_km2": 10.0,
                        "color_class": "MEDIUM"
                    }
                ],
                "total_nils": 99,
                "total_fountains": 2800,
                "max_density": 25.5,
                "min_density": 0.5
            }
        }


class ChoroplethFeatureResponse(BaseModel):
    """GeoJSON Feature for a single NIL in choropleth."""
    type: str = "Feature"
    geometry: dict  # GeoJSON Polygon geometry
    properties: dict  # NIL properties and statistics


class ChoroplethResponse(BaseModel):
    """Response model for choropleth map data."""
    type: str = "FeatureCollection"
    features: List[dict]  # Array of GeoJSON Features
    statistics: List[NILStatsResponse]
    bounds: dict  # Bounding box: {"north": 45.5, "south": 45.4, "east": 9.3, "west": 9.1}
    min_density: float
    max_density: float
    total_fountains: int
    
    class Config:
        schema_extra = {
            "example": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[[[9.1, 45.4], [9.2, 45.4], [9.2, 45.5], [9.1, 45.5], [9.1, 45.4]]]]
                        },
                        "properties": {
                            "nil_id": 1,
                            "nil_name": "Centro",
                            "fountain_count": 45,
                            "color_class": "HIGH"
                        }
                    }
                ],
                "statistics": [],
                "bounds": {"north": 45.5, "south": 45.4, "east": 9.3, "west": 9.1},
                "min_density": 0.5,
                "max_density": 25.5,
                "total_fountains": 2800
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: Optional[str] = None
    status_code: int
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "nil_id must be a valid integer string",
                "status_code": 400
            }
        }


# Create router
router = APIRouter(
    prefix="/fountains",
    tags=["fountains"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Invalid input"},
        404: {"model": ErrorResponse, "description": "Not Found - Resource not found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)

# Initialize service
fountain_service = FontanellaService()
nil_service = FontanellaService().nil_repo  # Direct access for some operations
mapper = DTOMapper()


# ============================================================================
# ENDPOINT 1: Search fountains by NIL ID (text search)
# ============================================================================

@router.post(
    "/search/by-nil",
    response_model=PaginatedFountainResponse,
    summary="Search fountains by NIL ID",
    description="Find all fountains in a specific NIL (neighborhood) by entering a NIL ID.",
    responses={
        200: {"model": PaginatedFountainResponse},
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def search_fountains_by_nil(request: SearchByNILRequest) -> PaginatedFountainResponse:
    """
    Search fountains by NIL ID.
    
    **Use case 1**: User enters a NIL ID (e.g., "1") in a text input and clicks search.
    
    Returns paginated list of fountains in that NIL, ready for map display.
    """
    try:
        result = fountain_service.search_fountains_by_nil(
            nil_id=request.nil_id,
            page=request.page,
            page_size=request.page_size
        )
        
        dto = mapper.search_result_to_dto(result)
        response_dict = dto.to_dict()
        
        return PaginatedFountainResponse(**response_dict)
    
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# ENDPOINT 2: Get NIL dropdown options
# ============================================================================

@router.get(
    "/nils/dropdown",
    response_model=List[dict],
    summary="Get NIL options for dropdown",
    description="Retrieve list of all NILs sorted by name for use in dropdown/select component.",
    responses={
        200: {"model": List[dict]},
        500: {"model": ErrorResponse},
    },
)
async def get_nil_dropdown_options() -> List[dict]:
    """
    Get NIL dropdown options.
    
    **Use case 2**: Frontend loads dropdown/select component with all NILs.
    
    Returns list of {id, name} objects ready for rendering in HTML select.
    """
    try:
        from backend.fastapi_app.services.fontanella_service import NILService
        nil_service_instance = NILService()
        options = nil_service_instance.get_dropdown_options()
        return options
    
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/search/by-nil-dropdown",
    response_model=PaginatedFountainResponse,
    summary="Search fountains from dropdown selection",
    description="Find fountains in a NIL selected from dropdown (same as by-nil but triggered from UI dropdown).",
    responses={
        200: {"model": PaginatedFountainResponse},
        400: {"model": ErrorResponse},
    },
)
async def search_fountains_by_nil_dropdown(
    nil_id: str = Query(..., description="NIL ID selected from dropdown"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page"),
) -> PaginatedFountainResponse:
    """
    Search fountains by NIL selected from dropdown.
    
    **Use case 2 (alternative)**: User selects NIL from dropdown and results load.
    
    Same as /search/by-nil but with query parameters instead of POST body.
    """
    try:
        result = fountain_service.search_fountains_by_nil(
            nil_id=nil_id,
            page=page,
            page_size=page_size
        )
        
        dto = mapper.search_result_to_dto(result)
        response_dict = dto.to_dict()
        
        return PaginatedFountainResponse(**response_dict)
    
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# ENDPOINT 3: Search fountains nearby (user-entered location)
# ============================================================================

@router.post(
    "/search/nearby",
    response_model=NearbyFountainListResponse,
    summary="Search fountains near a location",
    description="Find fountains within 500m radius of a user-entered geographic point.",
    responses={
        200: {"model": NearbyFountainListResponse},
        400: {"model": ErrorResponse},
    },
)
async def search_fountains_nearby(request: SearchByLocationRequest) -> NearbyFountainListResponse:
    """
    Search fountains near a location.
    
    **Use case 3**: User enters coordinates (lat/lon) or address converted to coordinates,
    and sees all fountains within 500m on the map.
    
    Returns list of fountains sorted by distance.
    """
    try:
        result = fountain_service.search_fountains_nearby(
            latitude=request.latitude,
            longitude=request.longitude,
            radius_meters=request.radius_meters,
            limit=request.limit
        )
        
        # Build response with distance information
        items = []
        for item in result.items:
            item_dict = {
                "id": str(item.id),
                "object_id": item.object_id,
                "nil_id": item.nil_id,
                "coordinate": {
                    "longitude": item.coordinate.longitude,
                    "latitude": item.coordinate.latitude,
                },
                "name": item.name,
                "description": item.description,
                "distance_meters": item.distance_meters,
            }
            items.append(NearbyFountainResponse(**item_dict))
        
        response = NearbyFountainListResponse(
            items=items,
            search_center=CoordinateResponse(
                longitude=request.longitude,
                latitude=request.latitude
            ),
            search_radius_meters=request.radius_meters,
            total_count=len(items)
        )
        
        return response
    
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# ENDPOINT 4: Search fountains near user location (geolocation)
# ============================================================================

@router.post(
    "/search/nearby/geolocation",
    response_model=NearbyFountainListResponse,
    summary="Search fountains near user's current location",
    description="Find fountains within 500m of user's current GPS location.",
    responses={
        200: {"model": NearbyFountainListResponse},
        400: {"model": ErrorResponse},
    },
)
async def search_fountains_near_user_location(
    latitude: float = Query(..., ge=-90, le=90, description="User's current latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="User's current longitude"),
    radius_meters: int = Query(500, ge=1, le=50000, description="Search radius in meters"),
    limit: int = Query(50, ge=1, le=500, description="Maximum results"),
) -> NearbyFountainListResponse:
    """
    Search fountains near user's GPS location.
    
    **Use case 4**: Browser geolocation API provides user coordinates,
    automatically finds nearby fountains (default 500m).
    
    This is typically called automatically when page loads (if user allows geolocation).
    """
    try:
        result = fountain_service.search_fountains_nearby(
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
            limit=limit
        )
        
        items = []
        for item in result.items:
            item_dict = {
                "id": str(item.id),
                "object_id": item.object_id,
                "nil_id": item.nil_id,
                "coordinate": {
                    "longitude": item.coordinate.longitude,
                    "latitude": item.coordinate.latitude,
                },
                "name": item.name,
                "description": item.description,
                "distance_meters": item.distance_meters,
            }
            items.append(NearbyFountainResponse(**item_dict))
        
        response = NearbyFountainListResponse(
            items=items,
            search_center=CoordinateResponse(
                longitude=longitude,
                latitude=latitude
            ),
            search_radius_meters=radius_meters,
            total_count=len(items)
        )
        
        return response
    
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# ENDPOINT 5: Get NIL statistics table (fountains per NIL)
# ============================================================================

@router.get(
    "/statistics/nils",
    response_model=NILStatsTableResponse,
    summary="Get fountain count per NIL",
    description="Retrieve table of all NILs with fountain counts, sorted by count descending.",
    responses={
        200: {"model": NILStatsTableResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_nil_statistics() -> NILStatsTableResponse:
    """
    Get statistics table for all NILs.
    
    **Use case 5**: Display table with columns: NIL name, fountain count, density.
    Sorted by fountain count in descending order.
    
    Returns aggregated statistics ready for table rendering (sorted desc by count).
    """
    try:
        from backend.fastapi_app.services.fontanella_service import NILService
        nil_service_instance = NILService()
        choropleth_data = nil_service_instance.get_choropleth_data()
        
        # Sort by fountain_count descending
        sorted_stats = sorted(
            choropleth_data.statistics,
            key=lambda x: x.fountain_count,
            reverse=True
        )
        
        stats_dtos = [
            {
                "nil_id": s.nil_id,
                "nil_name": s.nil_name,
                "fountain_count": s.fountain_count,
                "area_km2": s.area_km2,
                "density_fountains_per_km2": s.density,
                "color_class": s.color_class.value,
            }
            for s in sorted_stats
        ]
        
        response = NILStatsTableResponse(
            statistics=[NILStatsResponse(**s) for s in stats_dtos],
            total_nils=len(sorted_stats),
            total_fountains=sum(s.fountain_count for s in sorted_stats),
            max_density=max(s.density for s in sorted_stats) if sorted_stats else 0,
            min_density=min(s.density for s in sorted_stats) if sorted_stats else 0,
        )
        
        return response
    
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# ENDPOINT 6: Get choropleth data (GeoJSON with statistics)
# ============================================================================

@router.get(
    "/choropleth",
    response_model=ChoroplethResponse,
    summary="Get choropleth map data",
    description="Retrieve GeoJSON FeatureCollection with NIL geometries and color-coded statistics for density visualization.",
    responses={
        200: {"model": ChoroplethResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_choropleth_data() -> ChoroplethResponse:
    """
    Get choropleth map data.
    
    **Use case 6**: Display interactive map with NILs colored by fountain density.
    
    Returns GeoJSON FeatureCollection where:
    - Each feature is a NIL (Polygon geometry)
    - Properties include fountain count, density, color class
    - Features can be styled by color_class (LOW, MEDIUM, HIGH, VERY_HIGH)
    
    Example styling:
    - LOW: green
    - MEDIUM: yellow
    - HIGH: orange
    - VERY_HIGH: red
    """
    try:
        from backend.fastapi_app.services.fontanella_service import NILService
        nil_service_instance = NILService()
        choropleth_data = nil_service_instance.get_choropleth_data()
        
        # Build statistics list
        stats_list = []
        features = []
        
        for stat in choropleth_data.statistics:
            # Add to statistics
            stat_dict = {
                "nil_id": stat.nil_id,
                "nil_name": stat.nil_name,
                "fountain_count": stat.fountain_count,
                "area_km2": stat.area_km2,
                "density_fountains_per_km2": stat.density,
                "color_class": stat.color_class.value,
            }
            stats_list.append(NILStatsResponse(**stat_dict))
            
            # Build GeoJSON feature (geometry needs to come from NIL object)
            # For now, properties only - geometry will be added from NIL collection
            feature = {
                "type": "Feature",
                "geometry": None,  # Will be populated from MongoDB NIL document
                "properties": {
                    "nil_id": stat.nil_id,
                    "nil_name": stat.nil_name,
                    "fountain_count": stat.fountain_count,
                    "density_fountains_per_km2": stat.density,
                    "color_class": stat.color_class.value,
                }
            }
            features.append(feature)
        
        response = ChoroplethResponse(
            type="FeatureCollection",
            features=features,
            statistics=stats_list,
            bounds=choropleth_data.bounds or {},
            min_density=choropleth_data.min_density,
            max_density=choropleth_data.max_density,
            total_fountains=sum(s.fountain_count for s in choropleth_data.statistics),
        )
        
        return response
    
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# BONUS: Advanced search with multiple filters
# ============================================================================

@router.post(
    "/search/advanced",
    response_model=PaginatedFountainResponse,
    summary="Advanced search with multiple filters",
    description="Search fountains by combining multiple filter criteria (NIL, municipality, postal code).",
    responses={
        200: {"model": PaginatedFountainResponse},
        400: {"model": ErrorResponse},
    },
)
async def advanced_search(request: AdvancedSearchRequest) -> PaginatedFountainResponse:
    """
    Advanced search with multiple filters.
    
    Allows combining filters:
    - nil_id: exact match by NIL ID
    - nil_name: partial match by NIL name
    - municipio: exact match by municipality
    - cap: exact match by postal code
    
    At least one filter must be provided.
    """
    try:
        # Validate at least one filter is provided
        filters_provided = [
            request.nil_id,
            request.nil_name,
            request.municipio,
            request.cap
        ]
        
        if not any(filters_provided):
            raise ServiceError("At least one filter must be provided (nil_id, nil_name, municipio, or cap)")
        
        result = fountain_service.search_fountains(
            nil_id=request.nil_id,
            nil_name=request.nil_name,
            municipio=request.municipio,
            cap=request.cap,
            page=request.page,
            page_size=request.page_size
        )
        
        dto = mapper.search_result_to_dto(result)
        response_dict = dto.to_dict()
        
        return PaginatedFountainResponse(**response_dict)
    
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# INFO: Health check and metadata
# ============================================================================

@router.get(
    "/health",
    response_model=dict,
    summary="Health check",
    description="Check if API is running and database is accessible.",
    responses={
        200: {"model": dict},
        500: {"model": ErrorResponse},
    },
)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Verifies API is running and has database connectivity.
    """
    try:
        # Try to get total fountain count as connectivity test
        total = fountain_service.get_total_fountain_count()
        
        return {
            "status": "healthy",
            "message": "API is running and database is accessible",
            "total_fountains": total
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        )
