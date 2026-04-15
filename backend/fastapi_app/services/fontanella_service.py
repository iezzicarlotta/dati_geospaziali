"""
Service layer for business logic.

This module contains application-specific business logic that orchestrates
repository operations, applies business rules, and prepares data for API responses.
"""

from typing import Optional, List, Dict, Any
from backend.fastapi_app.models.fontanella import (
    Fontanella,
    NIL,
    Coordinate,
    FontanellaFilters,
    FontanellaSearchResult,
    NearbyFountainsResult,
    ChoroplethData,
)
from backend.fastapi_app.repositories.fontanella import (
    FontanellaRepository,
    NILRepository,
    RepositoryError,
)


class FontanellaService:
    """
    Business logic service for fountain operations.
    
    Orchestrates repository operations and applies business rules
    for fountain search and filtering.
    """
    
    def __init__(self):
        """Initialize service with repositories."""
        self.fontanella_repo = FontanellaRepository()
        self.nil_repo = NILRepository()
    
    def get_fountain_by_id(self, fountain_id: str) -> Optional[Fontanella]:
        """
        Get a single fountain by ID.
        
        Args:
            fountain_id: MongoDB ObjectId as string
            
        Returns:
            Fontanella object or None
            
        Raises:
            ServiceError: If operation fails
        """
        try:
            return self.fontanella_repo.find_by_id(fountain_id)
        except RepositoryError as e:
            raise ServiceError(f"Failed to get fountain: {e}")
    
    def list_all_fountains(
        self,
        page: int = 1,
        page_size: int = 20
    ) -> FontanellaSearchResult:
        """
        List all fountains with pagination.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of fountains per page
            
        Returns:
            FontanellaSearchResult with pagination metadata
            
        Raises:
            ServiceError: If page < 1 or invalid parameters
        """
        try:
            if page < 1:
                raise ValueError("Page must be >= 1")
            if page_size < 1 or page_size > 100:
                raise ValueError("Page size must be between 1 and 100")
            
            skip = (page - 1) * page_size
            return self.fontanella_repo.find_all(skip=skip, limit=page_size)
        except (ValueError, RepositoryError) as e:
            raise ServiceError(f"Failed to list fountains: {e}")
    
    def search_fountains_by_nil(
        self,
        nil_id: str,
        page: int = 1,
        page_size: int = 50
    ) -> FontanellaSearchResult:
        """
        Search fountains by NIL ID.
        
        This is the primary way users find fountains by neighborhood.
        
        Args:
            nil_id: The NIL ID to search in
            page: Page number for pagination
            page_size: Results per page
            
        Returns:
            FontanellaSearchResult with fountains in the NIL
            
        Raises:
            ServiceError: If search fails
        """
        try:
            if page < 1:
                raise ValueError("Page must be >= 1")
            
            skip = (page - 1) * page_size
            result = self.fontanella_repo.find_by_nil_id(
                nil_id=nil_id,
                skip=skip,
                limit=page_size
            )
            
            # Add context about the NIL
            nil = self.nil_repo.find_by_nil_id(int(nil_id))
            if nil:
                result.filters_applied = {"nil_name": nil.name}
            
            return result
        except (ValueError, RepositoryError) as e:
            raise ServiceError(f"Failed to search fountains by NIL: {e}")
    
    def search_fountains_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int = 500,
        limit: int = 50
    ) -> NearbyFountainsResult:
        """
        Search fountains near a geographic point.
        
        This enables location-based discovery, e.g., "find fountains
        near my current location".
        
        Args:
            latitude: Search point latitude (WGS84)
            longitude: Search point longitude (WGS84)
            radius_meters: Search radius in meters (default: 500m)
            limit: Maximum results to return
            
        Returns:
            NearbyFountainsResult with fountains sorted by distance
            
        Raises:
            ServiceError: If coordinates invalid or search fails
        """
        try:
            if not (-90 <= latitude <= 90):
                raise ValueError("Latitude must be between -90 and 90")
            if not (-180 <= longitude <= 180):
                raise ValueError("Longitude must be between -180 and 180")
            if radius_meters < 1 or radius_meters > 50000:
                raise ValueError("Radius must be between 1 and 50000 meters")
            
            center = Coordinate(longitude=longitude, latitude=latitude)
            return self.fontanelle_repo.find_nearby(
                center=center,
                max_distance_meters=radius_meters,
                limit=limit
            )
        except (ValueError, RepositoryError) as e:
            raise ServiceError(f"Failed to search nearby fountains: {e}")
    
    def search_fountains(
        self,
        nil_id: Optional[str] = None,
        nil_name: Optional[str] = None,
        municipio: Optional[str] = None,
        cap: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> FontanellaSearchResult:
        """
        Advanced search with multiple filter criteria.
        
        Allows users to combine filters for refined searches.
        
        Args:
            nil_id: Filter by NIL ID
            nil_name: Filter by NIL name (partial match)
            municipio: Filter by municipality
            cap: Filter by postal code
            page: Page number for pagination
            page_size: Results per page
            
        Returns:
            FontanellaSearchResult with filtered fountains
            
        Raises:
            ServiceError: If search fails
        """
        try:
            if page < 1:
                raise ValueError("Page must be >= 1")
            
            filters = FontanellaFilters(
                nil_id=nil_id,
                nil_name=nil_name,
                municipio=municipio,
                cap=cap
            )
            
            skip = (page - 1) * page_size
            return self.fontanella_repo.search_with_filters(
                filters=filters,
                skip=skip,
                limit=page_size
            )
        except (ValueError, RepositoryError) as e:
            raise ServiceError(f"Failed to search fountains: {e}")
    
    def count_fountains_in_nil(self, nil_id: str) -> int:
        """
        Count fountains in a specific NIL.
        
        Useful for statistics and choropleth data.
        
        Args:
            nil_id: The NIL ID to count
            
        Returns:
            Number of fountains in the NIL
            
        Raises:
            ServiceError: If count fails
        """
        try:
            return self.fontanella_repo.count_by_nil_id(nil_id)
        except RepositoryError as e:
            raise ServiceError(f"Failed to count fountains: {e}")
    
    def get_total_fountain_count(self) -> int:
        """
        Get total count of all fountains.
        
        Returns:
            Total number of fountains in database
            
        Raises:
            ServiceError: If count fails
        """
        try:
            return self.fontanella_repo.count_all()
        except RepositoryError as e:
            raise ServiceError(f"Failed to count all fountains: {e}")


class NILService:
    """
    Business logic service for NIL (neighborhood) operations.
    
    Manages NIL data access and provides utilities for UI components
    like dropdowns and choropleth visualization.
    """
    
    def __init__(self):
        """Initialize service with repositories."""
        self.nil_repo = NILRepository()
        self.fontanella_repo = FontanellaRepository()
    
    def get_nil_by_id(self, nil_id: str) -> Optional[NIL]:
        """
        Get a NIL by MongoDB ObjectId.
        
        Args:
            nil_id: MongoDB ObjectId as string
            
        Returns:
            NIL object or None
            
        Raises:
            ServiceError: If lookup fails
        """
        try:
            return self.nil_repo.find_by_id(nil_id)
        except RepositoryError as e:
            raise ServiceError(f"Failed to get NIL: {e}")
    
    def get_nil_by_number(self, nil_id: int) -> Optional[NIL]:
        """
        Get a NIL by numeric ID (1-999).
        
        Args:
            nil_id: Numeric NIL ID
            
        Returns:
            NIL object or None
            
        Raises:
            ServiceError: If lookup fails
        """
        try:
            if not (0 < nil_id < 1000):
                raise ValueError("NIL ID must be between 1 and 999")
            return self.nil_repo.find_by_nil_id(nil_id)
        except (ValueError, RepositoryError) as e:
            raise ServiceError(f"Failed to get NIL by number: {e}")
    
    def list_all_nils(self) -> List[NIL]:
        """
        Get all NILs.
        
        Returns:
            List of all NIL objects
            
        Raises:
            ServiceError: If listing fails
        """
        try:
            return self.nil_repo.find_all()
        except RepositoryError as e:
            raise ServiceError(f"Failed to list NILs: {e}")
    
    def search_nils_by_name(self, name: str) -> List[NIL]:
        """
        Search NILs by name (partial, case-insensitive).
        
        Useful for autocomplete/search input in UI.
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching NIL objects
            
        Raises:
            ServiceError: If search fails
        """
        try:
            if len(name) < 2:
                raise ValueError("Search term must be at least 2 characters")
            return self.nil_repo.find_by_name(name)
        except (ValueError, RepositoryError) as e:
            raise ServiceError(f"Failed to search NILs: {e}")
    
    def get_dropdown_options(self) -> List[Dict[str, Any]]:
        """
        Get NIL options for dropdown/select component.
        
        Returns a sorted list of {id, name} objects ready for UI rendering.
        
        Returns:
            List of dicts with 'id' and 'name' keys
            
        Raises:
            ServiceError: If operation fails
        """
        try:
            return self.nil_repo.get_nil_dropdown_options()
        except RepositoryError as e:
            raise ServiceError(f"Failed to get NIL dropdown options: {e}")
    
    def get_choropleth_data(self) -> ChoroplethData:
        """
        Get data for choropleth map visualization.
        
        Aggregates statistics from all NILs including fountain counts
        and density calculations for color-coding.
        
        Returns:
            ChoroplethData object with all statistics
            
        Raises:
            ServiceError: If aggregation fails
        """
        try:
            statistics = self.nil_repo.get_statistics()
            
            choropleth = ChoroplethData(statistics=statistics)
            choropleth.compute_bounds()
            
            return choropleth
        except RepositoryError as e:
            raise ServiceError(f"Failed to get choropleth data: {e}")


class ServiceError(Exception):
    """Exception raised by service operations."""
    pass
