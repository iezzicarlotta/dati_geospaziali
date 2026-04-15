"""
Query builder for complex MongoDB geospatial operations.

This module provides a clean, type-safe interface for building
sophisticated MongoDB queries, especially geospatial operations,
without exposing raw MongoDB syntax to business logic.
"""

from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
from backend.fastapi_app.models.fontanella import (
    Coordinate,
    BoundingBox,
)


class SortDirection(Enum):
    """Sort direction for query results."""
    ASCENDING = 1
    DESCENDING = -1


class GeospatialQueryBuilder:
    """
    Builder for geospatial MongoDB queries.
    
    Provides a fluent interface for constructing complex spatial queries
    while hiding MongoDB's GeoJSON and query syntax.
    """
    
    def __init__(self):
        """Initialize an empty query builder."""
        self._query: Dict[str, Any] = {}
        self._sort: List[Tuple[str, int]] = []
        self._skip: int = 0
        self._limit: Optional[int] = None
    
    def near_point(
        self,
        center: Coordinate,
        max_distance_meters: int,
        min_distance_meters: int = 0
    ) -> "GeospatialQueryBuilder":
        """
        Add a proximity search constraint (within a radius).
        
        Args:
            center: Search center point
            max_distance_meters: Maximum distance in meters
            min_distance_meters: Minimum distance in meters (default: 0)
            
        Returns:
            self for method chaining
        """
        self._query["geometry"] = {
            "$near": {
                "$geometry": center.to_geojson_point(),
                "$maxDistance": max_distance_meters,
                "$minDistance": min_distance_meters,
            }
        }
        return self
    
    def within_box(self, bbox: BoundingBox) -> "GeospatialQueryBuilder":
        """
        Add a bounding box constraint.
        
        Args:
            bbox: BoundingBox defining search area
            
        Returns:
            self for method chaining
        """
        self._query["geometry"] = {
            "$geoWithin": {
                "$geometry": bbox.to_geojson_polygon(),
            }
        }
        return self
    
    def within_polygon(self, coordinates: List[List[float]]) -> "GeospatialQueryBuilder":
        """
        Add a polygon boundary constraint.
        
        Args:
            coordinates: List of [lon, lat] pairs defining polygon
            
        Returns:
            self for method chaining
        """
        polygon = {
            "type": "Polygon",
            "coordinates": [coordinates],
        }
        self._query["geometry"] = {
            "$geoWithin": {
                "$geometry": polygon,
            }
        }
        return self
    
    def equals(self, field: str, value: Any) -> "GeospatialQueryBuilder":
        """
        Add an exact match constraint.
        
        Args:
            field: Document field name
            value: Value to match
            
        Returns:
            self for method chaining
        """
        self._query[field] = value
        return self
    
    def in_array(self, field: str, values: List[Any]) -> "GeospatialQueryBuilder":
        """
        Add an "in array" constraint.
        
        Args:
            field: Document field name
            values: Array of values to match against
            
        Returns:
            self for method chaining
        """
        self._query[field] = {"$in": values}
        return self
    
    def text_search(self, search_text: str) -> "GeospatialQueryBuilder":
        """
        Add a text search constraint.
        
        Searches across indexed text fields (usually name, description).
        
        Args:
            search_text: Text to search for
            
        Returns:
            self for method chaining
        """
        self._query["$text"] = {"$search": search_text}
        return self
    
    def regex_search(self, field: str, pattern: str, case_insensitive: bool = True) -> "GeospatialQueryBuilder":
        """
        Add a regex pattern search constraint.
        
        Args:
            field: Document field name
            pattern: Regex pattern
            case_insensitive: Whether to ignore case
            
        Returns:
            self for method chaining
        """
        options = "i" if case_insensitive else ""
        self._query[field] = {"$regex": pattern, "$options": options}
        return self
    
    def sort_by(
        self,
        field: str,
        direction: SortDirection = SortDirection.ASCENDING
    ) -> "GeospatialQueryBuilder":
        """
        Add a sort constraint.
        
        Args:
            field: Document field to sort by
            direction: Sort direction
            
        Returns:
            self for method chaining
        """
        self._sort.append((field, direction.value))
        return self
    
    def sort_by_distance(self) -> "GeospatialQueryBuilder":
        """
        Sort results by distance (only valid after near_point).
        
        Returns:
            self for method chaining
        """
        return self.sort_by("geometry", SortDirection.ASCENDING)
    
    def skip(self, num: int) -> "GeospatialQueryBuilder":
        """
        Add a skip constraint (for pagination).
        
        Args:
            num: Number of documents to skip
            
        Returns:
            self for method chaining
        """
        self._skip = max(0, num)
        return self
    
    def limit(self, num: int) -> "GeospatialQueryBuilder":
        """
        Add a limit constraint (for pagination).
        
        Args:
            num: Maximum number of documents to return
            
        Returns:
            self for method chaining
        """
        self._limit = max(1, num)
        return self
    
    def build(self) -> Dict[str, Any]:
        """
        Build the final MongoDB query dict.
        
        Returns:
            Dictionary with 'filter', 'sort', 'skip', 'limit' keys
        """
        query_spec = {
            "filter": self._query or {},
            "sort": self._sort or None,
            "skip": self._skip,
            "limit": self._limit,
        }
        return query_spec


class AggregationBuilder:
    """
    Builder for MongoDB aggregation pipeline queries.
    
    Provides a fluent interface for building aggregation pipelines
    for complex analytics like choropleth statistics.
    """
    
    def __init__(self):
        """Initialize an empty aggregation pipeline."""
        self._pipeline: List[Dict[str, Any]] = []
    
    def match(self, filter_dict: Dict[str, Any]) -> "AggregationBuilder":
        """
        Add a $match stage to filter documents early.
        
        Args:
            filter_dict: MongoDB match criteria
            
        Returns:
            self for method chaining
        """
        self._pipeline.append({"$match": filter_dict})
        return self
    
    def group_by(
        self,
        group_id: str,
        accumulators: Dict[str, Dict[str, Any]]
    ) -> "AggregationBuilder":
        """
        Add a $group stage for aggregation.
        
        Example:
            builder.group_by(
                "$properties.ID_NIL",
                {
                    "count": {"$sum": 1},
                    "names": {"$push": "$properties.Nome"},
                }
            )
        
        Args:
            group_id: Field to group by (can use $ prefix for field reference)
            accumulators: Dict of accumulator expressions
            
        Returns:
            self for method chaining
        """
        group_doc = {"_id": group_id}
        group_doc.update(accumulators)
        self._pipeline.append({"$group": group_doc})
        return self
    
    def sort(
        self,
        sort_spec: Dict[str, int]
    ) -> "AggregationBuilder":
        """
        Add a $sort stage.
        
        Args:
            sort_spec: Dict mapping field names to 1 (asc) or -1 (desc)
            
        Returns:
            self for method chaining
        """
        self._pipeline.append({"$sort": sort_spec})
        return self
    
    def skip(self, num: int) -> "AggregationBuilder":
        """
        Add a $skip stage.
        
        Args:
            num: Number of documents to skip
            
        Returns:
            self for method chaining
        """
        self._pipeline.append({"$skip": num})
        return self
    
    def limit(self, num: int) -> "AggregationBuilder":
        """
        Add a $limit stage.
        
        Args:
            num: Maximum documents to return
            
        Returns:
            self for method chaining
        """
        self._pipeline.append({"$limit": num})
        return self
    
    def project(self, projection: Dict[str, Any]) -> "AggregationBuilder":
        """
        Add a $project stage to reshape documents.
        
        Args:
            projection: Dict specifying which fields to include/exclude/transform
            
        Returns:
            self for method chaining
        """
        self._pipeline.append({"$project": projection})
        return self
    
    def lookup(
        self,
        from_collection: str,
        local_field: str,
        foreign_field: str,
        as_name: str
    ) -> "AggregationBuilder":
        """
        Add a $lookup stage for joining collections.
        
        Args:
            from_collection: Collection to join with
            local_field: Field from current collection
            foreign_field: Field from other collection
            as_name: Output array field name
            
        Returns:
            self for method chaining
        """
        self._pipeline.append({
            "$lookup": {
                "from": from_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_name,
            }
        })
        return self
    
    def unwind(self, field: str, preserve_null: bool = True) -> "AggregationBuilder":
        """
        Add an $unwind stage to deconstruct arrays.
        
        Args:
            field: Array field to unwind (include $ prefix)
            preserve_null: Whether to keep docs with missing/null arrays
            
        Returns:
            self for method chaining
        """
        unwind_spec = {
            "path": field,
            "preserveNullAndEmptyArrays": preserve_null,
        }
        self._pipeline.append({"$unwind": unwind_spec})
        return self
    
    def build(self) -> List[Dict[str, Any]]:
        """
        Build the final aggregation pipeline.
        
        Returns:
            List of pipeline stages
        """
        return self._pipeline


class CountAggregationBuilder:
    """
    Specialized builder for count queries with grouping.
    
    Used for statistics like "count fountains per NIL".
    """
    
    @staticmethod
    def count_by_group(
        group_field: str,
        match_criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Build aggregation pipeline to count documents by group.
        
        Args:
            group_field: Field to group by (with $ prefix, e.g., "$properties.ID_NIL")
            match_criteria: Optional filter before grouping
            
        Returns:
            Aggregation pipeline
        """
        pipeline = []
        
        if match_criteria:
            pipeline.append({"$match": match_criteria})
        
        pipeline.append({
            "$group": {
                "_id": group_field,
                "count": {"$sum": 1},
            }
        })
        
        pipeline.append({"$sort": {"count": -1}})
        
        return pipeline
    
    @staticmethod
    def count_with_properties(
        group_field: str,
        property_fields: List[str],
        match_criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Build aggregation to count documents and preserve properties.
        
        Args:
            group_field: Field to group by
            property_fields: Fields to preserve in output
            match_criteria: Optional filter
            
        Returns:
            Aggregation pipeline
        """
        pipeline = []
        
        if match_criteria:
            pipeline.append({"$match": match_criteria})
        
        # Add sort before group to get deterministic "first" document
        pipeline.append({"$sort": {"_id": 1}})
        
        # Group and take first value of each property
        group_stage = {
            "_id": group_field,
            "count": {"$sum": 1},
        }
        for field in property_fields:
            group_stage[field] = {"$first": f"${field}"}
        
        pipeline.append({"$group": group_stage})
        pipeline.append({"$sort": {"count": -1}})
        
        return pipeline
