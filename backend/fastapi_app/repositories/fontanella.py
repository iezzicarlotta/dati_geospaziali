"""
Repository layer for data access.

This module handles all interactions with MongoDB, converting between
database documents and domain models.
"""

from typing import Optional, List, Dict, Any
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from backend.fastapi_app.models.fontanella import (
    Fontanella,
    NIL,
    Coordinate,
    FontanellaFilters,
    GeospatialFilters,
    FontanellaSearchResult,
    NearbyFountainsResult,
    NILStatistics,
)
from backend.fastapi_app.core.database import MongoDBConnection


class FontanellaRepository:
    """
    Repository for Fontanella (fountain) data access.
    
    Handles all database operations for fountains, including search,
    geospatial queries, and aggregations.
    """
    
    def __init__(self):
        """Initialize repository with database connection."""
        self.collection: Collection = MongoDBConnection.get_collection("fontanelle")
    
    def find_by_id(self, fountain_id: str) -> Optional[Fontanella]:
        """
        Find a fountain by MongoDB ObjectId.
        
        Args:
            fountain_id: MongoDB ObjectId as string
            
        Returns:
            Fontanella object or None if not found
        """
        try:
            from bson import ObjectId
            
            doc = self.collection.find_one({"_id": ObjectId(fountain_id)})
            return self._doc_to_model(doc) if doc else None
        except Exception as e:
            raise RepositoryError(f"Error finding fountain by id: {e}")
    
    def find_by_object_id(self, object_id: str) -> Optional[Fontanella]:
        """
        Find a fountain by objectID (original source ID).
        
        Args:
            object_id: Source object ID
            
        Returns:
            Fontanella object or None if not found
        """
        try:
            doc = self.collection.find_one({"properties.objectID": object_id})
            return self._doc_to_model(doc) if doc else None
        except Exception as e:
            raise RepositoryError(f"Error finding fountain by object_id: {e}")
    
    def find_all(
        self,
        skip: int = 0,
        limit: int = 20
    ) -> FontanellaSearchResult:
        """
        Find all fountains with pagination.
        
        Args:
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            
        Returns:
            FontanellaSearchResult with pagination metadata
        """
        try:
            total = self.collection.count_documents({})
            
            docs = list(
                self.collection.find()
                    .skip(skip)
                    .limit(limit)
            )
            
            fountains = [self._doc_to_model(doc) for doc in docs if doc]
            
            return FontanellaSearchResult(
                fountains=fountains,
                total=total,
                skip=skip,
                limit=limit
            )
        except Exception as e:
            raise RepositoryError(f"Error finding all fountains: {e}")
    
    def search_with_filters(
        self,
        filters: FontanellaFilters,
        skip: int = 0,
        limit: int = 20
    ) -> FontanellaSearchResult:
        """
        Search fountains with filter criteria.
        
        Args:
            filters: FontanellaFilters object with search criteria
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            
        Returns:
            FontanellaSearchResult with matching fountains
        """
        try:
            query = self._build_filter_query(filters)
            
            total = self.collection.count_documents(query)
            
            docs = list(
                self.collection.find(query)
                    .skip(skip)
                    .limit(limit)
            )
            
            fountains = [self._doc_to_model(doc) for doc in docs if doc]
            
            return FontanellaSearchResult(
                fountains=fountains,
                total=total,
                skip=skip,
                limit=limit,
                filters_applied=filters.__dict__
            )
        except Exception as e:
            raise RepositoryError(f"Error searching fountains: {e}")
    
    def find_by_nil_id(
        self,
        nil_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> FontanellaSearchResult:
        """
        Find all fountains in a specific NIL.
        
        Args:
            nil_id: The NIL ID to search for
            skip: Pagination skip
            limit: Pagination limit
            
        Returns:
            FontanellaSearchResult with fountains in the NIL
        """
        filters = FontanellaFilters(nil_id=nil_id)
        return self.search_with_filters(filters, skip, limit)
    
    def find_nearby(
        self,
        center: Coordinate,
        max_distance_meters: int = 500,
        limit: int = 50
    ) -> NearbyFountainsResult:
        """
        Find fountains within a certain distance from a point.
        
        Uses MongoDB geospatial indexing for performance.
        
        Args:
            center: Center coordinate for search
            max_distance_meters: Maximum distance in meters (default: 500m)
            limit: Maximum number of results
            
        Returns:
            NearbyFountainsResult with fountains sorted by distance
        """
        try:
            query = {
                "geometry": {
                    "$near": {
                        "$geometry": center.to_geojson_point(),
                        "$maxDistance": max_distance_meters
                    }
                }
            }
            
            docs = list(
                self.collection.find(query).limit(limit)
            )
            
            fountains = [self._doc_to_model(doc) for doc in docs if doc]
            
            return NearbyFountainsResult(
                center_coordinate=center,
                radius_meters=max_distance_meters,
                fountains=fountains
            )
        except Exception as e:
            raise RepositoryError(f"Error finding nearby fountains: {e}")
    
    def count_by_nil_id(self, nil_id: str) -> int:
        """
        Count fountains in a specific NIL.
        
        Args:
            nil_id: The NIL ID to count
            
        Returns:
            Number of fountains in the NIL
        """
        try:
            return self.collection.count_documents(
                {"properties.ID_NIL": nil_id}
            )
        except Exception as e:
            raise RepositoryError(f"Error counting fountains by NIL: {e}")
    
    def count_all(self) -> int:
        """Get total count of all fountains."""
        try:
            return self.collection.count_documents({})
        except Exception as e:
            raise RepositoryError(f"Error counting all fountains: {e}")
    
    def _build_filter_query(self, filters: FontanellaFilters) -> Dict[str, Any]:
        """Build MongoDB query from filters."""
        query = {}
        
        if filters.nil_id:
            query["properties.ID_NIL"] = filters.nil_id
        
        if filters.nil_name:
            query["properties.NIL"] = {"$regex": filters.nil_name, "$options": "i"}
        
        if filters.municipio:
            query["properties.MUNICIPIO"] = filters.municipio
        
        if filters.cap:
            query["properties.CAP"] = filters.cap
        
        return query
    
    def _doc_to_model(self, doc: Dict[str, Any]) -> Fontanella:
        """Convert MongoDB document to Fontanella domain model."""
        if not doc:
            return None
        
        props = doc.get("properties", {})
        geometry = doc.get("geometry", {})
        
        coordinate = None
        if geometry.get("type") == "Point":
            try:
                coordinate = Coordinate.from_geojson_point(geometry)
            except Exception:
                pass
        
        return Fontanella(
            id=str(doc.get("_id")) if doc.get("_id") else None,
            object_id=props.get("objectID", ""),
            nil_id=props.get("ID_NIL"),
            nil_name=props.get("NIL"),
            coordinate=coordinate,
            cap=props.get("CAP"),
            municipio=props.get("MUNICIPIO")
        )


class NILRepository:
    """
    Repository for NIL (neighborhood area) data access.
    
    Handles operations on NIL data, including lookups and statistics.
    """
    
    def __init__(self):
        """Initialize repository with database connection."""
        self.collection: Collection = MongoDBConnection.get_collection("nil")
        self.fontanelle_repo = FontanellaRepository()
    
    def find_all(self) -> List[NIL]:
        """
        Get all NILs.
        
        Returns:
            List of NIL objects
        """
        try:
            docs = list(self.collection.find())
            return [self._doc_to_model(doc) for doc in docs if doc]
        except Exception as e:
            raise RepositoryError(f"Error finding all NILs: {e}")
    
    def find_by_id(self, nil_id: str) -> Optional[NIL]:
        """
        Find NIL by MongoDB ObjectId.
        
        Args:
            nil_id: MongoDB ObjectId as string
            
        Returns:
            NIL object or None if not found
        """
        try:
            from bson import ObjectId
            
            doc = self.collection.find_one({"_id": ObjectId(nil_id)})
            return self._doc_to_model(doc) if doc else None
        except Exception as e:
            raise RepositoryError(f"Error finding NIL by id: {e}")
    
    def find_by_nil_id(self, nil_id: int) -> Optional[NIL]:
        """
        Find NIL by numeric NIL ID (1-999).
        
        Args:
            nil_id: Numeric NIL ID
            
        Returns:
            NIL object or None if not found
        """
        try:
            doc = self.collection.find_one({"properties.ID_NIL": nil_id})
            return self._doc_to_model(doc) if doc else None
        except Exception as e:
            raise RepositoryError(f"Error finding NIL by nil_id: {e}")
    
    def find_by_name(self, name: str) -> List[NIL]:
        """
        Find NILs by name (case-insensitive partial match).
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching NIL objects
        """
        try:
            query = {
                "properties.NIL": {"$regex": name, "$options": "i"}
            }
            docs = list(self.collection.find(query))
            return [self._doc_to_model(doc) for doc in docs if doc]
        except Exception as e:
            raise RepositoryError(f"Error finding NILs by name: {e}")
    
    def get_statistics(self) -> List[NILStatistics]:
        """
        Get statistics for all NILs including fountain counts.
        
        This aggregates data from both nil and fontanelle collections
        to compute density information for choropleth visualization.
        
        Returns:
            List of NILStatistics objects
        """
        try:
            nils = self.find_all()
            statistics = []
            
            for nil in nils:
                if nil.nil_id is None:
                    continue
                
                # Count fountains in this NIL
                count = self.fontanelle_repo.count_by_nil_id(str(nil.nil_id))
                
                # Compute density
                density = None
                if nil.area and nil.area > 0:
                    density = (count / nil.area) * 1_000_000  # per km²
                
                stat = NILStatistics(
                    nil_id=nil.nil_id,
                    nil_name=nil.name,
                    fountain_count=count,
                    area=nil.area,
                    perimeter=nil.perimeter,
                    density=density
                )
                statistics.append(stat)
            
            return statistics
        except Exception as e:
            raise RepositoryError(f"Error computing NIL statistics: {e}")
    
    def get_nil_dropdown_options(self) -> List[Dict[str, Any]]:
        """
        Get options for NIL dropdown selector.
        
        Returns a list of {id, name} tuples sorted by name.
        
        Returns:
            List of dicts with 'id' and 'name' keys
        """
        try:
            nils = self.find_all()
            options = [
                {
                    "id": str(nil.nil_id),
                    "name": nil.name
                }
                for nil in nils
                if nil.nil_id is not None
            ]
            # Sort by name
            options.sort(key=lambda x: x["name"])
            return options
        except Exception as e:
            raise RepositoryError(f"Error getting NIL dropdown options: {e}")
    
    def _doc_to_model(self, doc: Dict[str, Any]) -> NIL:
        """Convert MongoDB document to NIL domain model."""
        if not doc:
            return None
        
        props = doc.get("properties", {})
        
        return NIL(
            id=str(doc.get("_id")) if doc.get("_id") else None,
            nil_id=props.get("ID_NIL"),
            name=props.get("NIL", ""),
            valid_from=props.get("Valido_dal"),
            valid_to=props.get("Valido_al"),
            area=props.get("Shape_Area"),
            perimeter=props.get("Shape_Length"),
            fountain_count=0  # Will be computed by statistics
        )


class RepositoryError(Exception):
    """Exception raised by repository operations."""
    pass
