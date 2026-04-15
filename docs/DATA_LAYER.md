# Data Layer Architecture

## Overview

The data layer provides a clean, testable abstraction over MongoDB with complete separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│ API Layer (FastAPI Routes)                          │
├─────────────────────────────────────────────────────┤
│ DTOs & Mappers (API Response Contracts)             │
├─────────────────────────────────────────────────────┤
│ Service Layer (Business Logic)                      │
├─────────────────────────────────────────────────────┤
│ Repository Pattern (Query Interface)                │
├─────────────────────────────────────────────────────┤
│ Query Builders (Geospatial Operations)              │
├─────────────────────────────────────────────────────┤
│ Domain Models (Coordinate, Fontanella, NIL, etc)    │
├─────────────────────────────────────────────────────┤
│ MongoDB (Persistence Layer)                         │
└─────────────────────────────────────────────────────┘
```

## Package Structure

```
backend/fastapi_app/
├── models/
│   ├── __init__.py
│   └── fontanella.py          # Domain models: Coordinate, Fontanella, NIL, etc.
├── repositories/
│   ├── __init__.py
│   └── fontanella.py          # Repository pattern: FontanellaRepository, NILRepository
├── queries/
│   ├── __init__.py
│   └── builder.py             # Query builders: GeospatialQueryBuilder, AggregationBuilder
├── services/
│   ├── __init__.py
│   └── fontanella_service.py  # Business logic: FontanellaService, NILService
├── mappers/
│   ├── __init__.py
│   └── fontanella_mapper.py   # DTOs and mappers: FontanellaDTO, ChoroplethDataDTO
├── core/
│   └── database.py            # MongoDB connection singleton
└── api/
    └── v1/
        └── routes/
            └── fontanelle.py  # (Next: FastAPI routes using services)
```

## Layers

### 1. Domain Models (`models/fontanella.py`)

Pure Python dataclasses representing business entities:

- **`Coordinate`**: WGS84 (EPSG:4326) geographic point
  - `to_geojson_point()` - convert to GeoJSON Point
  - `from_geojson_point()` - create from GeoJSON
  - `distance_to()` - Haversine distance calculation

- **`BoundingBox`**: Geographic rectangular area
  - `to_geojson_polygon()` - convert to GeoJSON Polygon

- **`Fontanella`**: Fountain domain model
  - Fields: id, nil_id, coordinate, name, description, municipio, cap
  - Validation on creation

- **`NIL`**: Neighborhood area domain model
  - Fields: id, nil_id, name, municipio, geometry
  - Statistics support

- **`NILStatistics`**: Aggregated data for analytics
  - Fountain count, area, density
  - Color classification for choropleth

- **`FontanellaSearchResult`**: Paginated results
- **`NearbyFountainsResult`**: Geospatial results sorted by distance
- **`ChoroplethData`**: Complete data for map visualization

### 2. Repository Pattern (`repositories/fontanella.py`)

Data access abstraction layer that handles all MongoDB interactions:

#### FontanellaRepository

**Lookup Methods:**
```python
find_by_id(fountain_id: str) -> Optional[Fontanella]
find_by_object_id(object_id: str) -> Optional[Fontanella]
```

**Search Methods:**
```python
find_all(skip=0, limit=20) -> FontanellaSearchResult
search_with_filters(filters, skip=0, limit=20) -> FontanellaSearchResult
find_by_nil_id(nil_id: str, skip=0, limit=20) -> FontanellaSearchResult
find_nearby(center: Coordinate, max_distance_meters=500, limit=50) -> NearbyFountainsResult
```

**Aggregation Methods:**
```python
count_by_nil_id(nil_id: str) -> int
count_all() -> int
```

#### NILRepository

**Lookup Methods:**
```python
find_by_id(nil_id: str) -> Optional[NIL]
find_by_nil_id(nil_id: int) -> Optional[NIL]
```

**Search Methods:**
```python
find_all() -> List[NIL]
find_by_name(name: str) -> List[NIL]
```

**Aggregation Methods:**
```python
get_statistics() -> List[NILStatistics]
get_nil_dropdown_options() -> List[Dict[str, Any]]
```

### 3. Query Builders (`queries/builder.py`)

Fluent interface for building complex MongoDB queries:

#### GeospatialQueryBuilder

```python
builder = GeospatialQueryBuilder()
query = (builder
    .near_point(center, max_distance_meters=500)
    .sort_by_distance()
    .limit(50)
    .build())
```

Supports:
- Proximity searches: `.near_point()`
- Bounding box: `.within_box()`
- Polygon containment: `.within_polygon()`
- Exact match: `.equals(field, value)`
- Array membership: `.in_array(field, values)`
- Text search: `.text_search(text)`
- Regex: `.regex_search(field, pattern)`
- Sorting and pagination

#### AggregationBuilder

```python
pipeline = (AggregationBuilder()
    .match({"properties.ID_NIL": nil_id})
    .group_by("$properties.ID_NIL", {"count": {"$sum": 1}})
    .sort({"count": -1})
    .build())
```

#### CountAggregationBuilder

Specialized builders for counting operations.

### 4. Service Layer (`services/fontanella_service.py`)

Business logic orchestration and validation:

#### FontanellaService

```python
service = FontanellaService()

# Direct lookups
fountain = service.get_fountain_by_id(fountain_id)

# Paginated listing
results = service.list_all_fountains(page=1, page_size=20)

# Filtered search
results = service.search_fountains(
    nil_id="1",
    municipio="Milano",
    page=1
)

# Location-based search
nearby = service.search_fountains_nearby(
    latitude=45.464,
    longitude=9.190,
    radius_meters=500
)

# Statistics
count = service.count_fountains_in_nil("1")
total = service.get_total_fountain_count()
```

#### NILService

```python
service = NILService()

# Lookups
nil = service.get_nil_by_number(1)

# Search
nils = service.search_nils_by_name("centro")

# UI utilities
options = service.get_dropdown_options()  # For <select>

# Analytics
choropleth_data = service.get_choropleth_data()
```

### 5. Data Transfer Objects (`mappers/fontanella_mapper.py`)

Clean API response contracts independent of internal models:

```python
# Convert domain models to DTOs
dto = FontanellaDTO.from_domain(fountain)
json_data = dto.to_dict()

# Batch conversions
mapper = DTOMapper()
dtos = mapper.fountains_to_dto_list(fountains)
```

DTOs available:
- `CoordinateDTO` - geographic point
- `FontanellaDTO` - fountain response
- `NILDTO` - neighborhood response
- `NILStatisticsDTO` - statistics for choropleth
- `FontanellaSearchResultDTO` - paginated results
- `ChoroplethDataDTO` - complete visualization data

## Usage Patterns

### Pattern 1: Simple Fountain Lookup

```python
from backend.fastapi_app.services.fontanella_service import FontanellaService
from backend.fastapi_app.mappers.fontanella_mapper import DTOMapper

service = FontanellaService()
mapper = DTOMapper()

fountain = service.get_fountain_by_id(fountain_id)
if fountain:
    dto = mapper.fountain_to_dto(fountain)
    response = dto.to_dict()
```

### Pattern 2: Paginated Search

```python
results = service.search_fountains(
    nil_id="1",
    page=page_num,
    page_size=20
)

result_dto = mapper.search_result_to_dto(results)
return result_dto.to_dict()  # Includes pagination metadata
```

### Pattern 3: Geospatial Query

```python
nearby = service.search_fountains_nearby(
    latitude=45.464,
    longitude=9.190,
    radius_meters=500
)

fountains_dto = mapper.fountains_to_dto_list(nearby.items)
```

### Pattern 4: Choropleth Data

```python
choropleth = service.get_choropleth_data()
dto = mapper.choropleth_to_dto(choropleth)
return dto.to_dict()  # Includes all stats for map visualization
```

## Database Indexes Required

Ensure these MongoDB indexes exist for optimal performance:

```javascript
// Geospatial index (required for $near queries)
db.fontanelle.createIndex({ "geometry": "2dsphere" })
db.nil.createIndex({ "geometry": "2dsphere" })

// Lookup indexes
db.fontanelle.createIndex({ "properties.ID_NIL": 1 })
db.fontanelle.createIndex({ "properties.OBJECTID": 1 })
db.nil.createIndex({ "properties.ID_NIL": 1 })

// Search indexes
db.fontanelle.createIndex({ "properties.Nome": "text" })
db.nil.createIndex({ "properties.NIL_NAME": "text" })
```

See `backend/fastapi_app/scripts/setup_db.py` for index setup automation.

## Error Handling

All layers provide specific error types:

```python
from backend.fastapi_app.repositories.fontanella import RepositoryError
from backend.fastapi_app.services.fontanella_service import ServiceError

try:
    fountain = service.get_fountain_by_id(fountain_id)
except ServiceError as e:
    # Handle business logic error
    log.error(f"Service error: {e}")
except RepositoryError as e:
    # Handle database error
    log.error(f"Database error: {e}")
```

## Testing Strategy

### Unit Tests (Domain Models)

Test Coordinate calculations, validations:

```python
def test_coordinate_distance():
    coord1 = Coordinate(longitude=9.190, latitude=45.464)
    coord2 = Coordinate(longitude=9.191, latitude=45.465)
    distance = coord1.distance_to(coord2)
    assert 100 < distance < 200  # ~150m expected
```

### Unit Tests (Repository Query Building)

Mock MongoDB, test query construction:

```python
def test_fontanella_repository_filters():
    repo = FontanellaRepository()
    query = repo._build_filter_query(
        filters=FontanellaFilters(nil_id="1")
    )
    assert "properties.ID_NIL" in query
```

### Integration Tests

Test with real MongoDB instance:

```python
@pytest.mark.integration
def test_fountain_search_with_real_db():
    service = FontanellaService()
    results = service.search_fountains(nil_id="1", page=1)
    assert len(results.items) > 0
```

## Next Steps

1. **Unit Tests** - Add comprehensive tests for models and repositories
2. **Integration Tests** - Test with real MongoDB
3. **API Routes** - Implement FastAPI endpoints using services
4. **Caching** - Optional Redis layer for frequently accessed data
5. **Monitoring** - Query performance logging and optimization
