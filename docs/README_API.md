# Backend API - Complete Documentation Index

## 📑 Documentation Structure

### Quick References
- **[API_SUMMARY.txt](API_SUMMARY.txt)** ⭐ START HERE
  - Visual overview of all endpoints
  - Architecture diagram
  - Quick start (3 minutes)
  - Response format examples

### Implementation Guides
- **[API_QUICK_START.md](API_QUICK_START.md)**
  - Step-by-step setup (5 minutes)
  - Copy-paste test commands
  - Troubleshooting
  - Frontend integration examples
  - Leaflet.js code examples

- **[API_ENDPOINTS.md](API_ENDPOINTS.md)**
  - Complete endpoint reference (8 endpoints)
  - Request/response examples
  - Query parameters
  - Error codes
  - Frontend integration patterns
  - cURL, Python, JavaScript examples

- **[API_IMPLEMENTATION.md](API_IMPLEMENTATION.md)**
  - Implementation details
  - Test cases for each endpoint
  - Files created/modified
  - Data flow diagram
  - Performance metrics
  - Known limitations
  - Next steps

### Architecture & Patterns
- **[DATA_LAYER.md](DATA_LAYER.md)**
  - Data layer architecture
  - Package structure
  - Repository pattern details
  - Query builders
  - Service layer examples
  - Usage patterns
  - Testing strategy
  - Database indexes

## 🎯 Use Cases by Endpoint

### 1. Search Fountains by NIL (Text Input)
- **File**: [API_ENDPOINTS.md → Endpoint 1](API_ENDPOINTS.md#1-search-fountains-by-nil-id)
- **Method**: POST `/fountains/search/by-nil`
- **Request**: `{"nil_id": "1", "page": 1}`
- **Response**: Paginated fountain list
- **Test**: See [API_QUICK_START.md → Test 1](API_QUICK_START.md#1-health-check)

### 2. Select NIL from Dropdown
- **Get Options**:
  - File: [API_ENDPOINTS.md → Endpoint 2a](API_ENDPOINTS.md#2a-get-nil-dropdown-options)
  - Method: GET `/fountains/nils/dropdown`
  
- **Search by Selection**:
  - File: [API_ENDPOINTS.md → Endpoint 2b](API_ENDPOINTS.md#2b-search-fountains-by-nil-dropdown-selection)
  - Method: POST `/fountains/search/by-nil-dropdown`

### 3. Search Near Coordinates (User Input)
- **File**: [API_ENDPOINTS.md → Endpoint 3](API_ENDPOINTS.md#3-search-fountains-near-location-text-input)
- **Method**: POST `/fountains/search/nearby`
- **Request**: `{"latitude": 45.464, "longitude": 9.190, "radius_meters": 500}`
- **Response**: Fountains with distances

### 4. Find Fountains Near User (GPS)
- **File**: [API_ENDPOINTS.md → Endpoint 4](API_ENDPOINTS.md#4-search-fountains-near-user-geolocation)
- **Method**: POST `/fountains/search/nearby/geolocation`
- **JavaScript**: See [API_QUICK_START.md → Geolocation](API_QUICK_START.md#🌐-quick-test-in-browser-console)

### 5. Show Fountains per NIL (Table)
- **File**: [API_ENDPOINTS.md → Endpoint 5](API_ENDPOINTS.md#5-get-nil-statistics-table)
- **Method**: GET `/fountains/statistics/nils`
- **Response**: Sorted statistics with color classes
- **Example**: See [API_QUICK_START.md → Display Table](API_QUICK_START.md#📊-display-statistics-table)

### 6. Show Choropleth Map
- **File**: [API_ENDPOINTS.md → Endpoint 6](API_ENDPOINTS.md#6-get-choropleth-map-data)
- **Method**: GET `/fountains/choropleth`
- **Response**: GeoJSON FeatureCollection with colors
- **Example**: See [API_QUICK_START.md → Choropleth](API_QUICK_START.md#display-choropleth-map)

## 🚀 Setup & Running

1. **Start API Server**
   - See: [API_QUICK_START.md → Start API Server](API_QUICK_START.md#-start-api-server-5-minutes)
   - Command: `uvicorn main:app --reload --port 8000`

2. **Access Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - OpenAPI: http://localhost:8000/openapi.json

3. **Test Endpoints**
   - Swagger (recommended): See [API_QUICK_START.md → Test](API_QUICK_START.md#🧪-quick-test-with-curl)
   - cURL: See [API_QUICK_START.md → cURL](API_QUICK_START.md#🧪-quick-test-with-curl)
   - Python: See [API_QUICK_START.md → Python](API_QUICK_START.md#🧪-quick-test-with-python)

## 📊 Response Formats

### Fountain Object
```json
{
  "id": "507f1f77bcf86cd799439011",
  "nil_id": 1,
  "coordinate": {"longitude": 9.190, "latitude": 45.464},
  "name": "Fontanella Centro",
  "municipio": "Milano",
  "cap": "20100"
}
```

### Paginated Response
```json
{
  "items": [...],
  "total_count": 45,
  "page": 1,
  "total_pages": 3,
  "has_next": true
}
```

### Statistics Entry
```json
{
  "nil_id": 1,
  "nil_name": "Centro Storico",
  "fountain_count": 127,
  "density_fountains_per_km2": 50.8,
  "color_class": "VERY_HIGH"
}
```

### Choropleth Feature
```json
{
  "type": "Feature",
  "geometry": {"type": "Polygon", "coordinates": [...]},
  "properties": {
    "nil_id": 1,
    "fountain_count": 127,
    "color_class": "VERY_HIGH"
  }
}
```

## 🧪 Testing Checklist

- [ ] API server running on port 8000
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] Health check returns 200 OK
- [ ] Can get NIL dropdown (3+ options)
- [ ] Can search by NIL (returns results)
- [ ] Can search nearby (with distances)
- [ ] Can get statistics (sorted desc)
- [ ] Can get choropleth (GeoJSON valid)

## 📝 Files Created

### Source Code
- `backend/fastapi_app/api/v1/routes/fountains.py` (750+ lines, 8 endpoints)
- `backend/fastapi_app/main.py` (updated with CORS, router)

### Documentation
- `docs/API_SUMMARY.txt` (visual overview)
- `docs/API_QUICK_START.md` (quick reference)
- `docs/API_ENDPOINTS.md` (complete reference)
- `docs/API_IMPLEMENTATION.md` (implementation details)
- `docs/DATA_LAYER.md` (architecture)

## 🔗 Code File Locations

### API Routes
- **Fountains Endpoints**: `backend/fastapi_app/api/v1/routes/fountains.py`
  - Search by NIL
  - Get dropdown options
  - Search nearby
  - Get statistics
  - Get choropleth
  - Advanced search
  - Health check

### Services (Business Logic)
- **Fountain Service**: `backend/fastapi_app/services/fontanella_service.py`
- **NIL Service**: `backend/fastapi_app/services/fontanella_service.py`

### Data Access (Repositories)
- **Repositories**: `backend/fastapi_app/repositories/fontanella.py`
  - FontanellaRepository
  - NILRepository

### Query Building
- **Query Builders**: `backend/fastapi_app/queries/builder.py`
  - GeospatialQueryBuilder
  - AggregationBuilder

### Domain Models
- **Models**: `backend/fastapi_app/models/fontanella.py`
  - Coordinate, Fontanella, NIL
  - Statistics, Results, Filters

### Data Transfer Objects
- **DTOs**: `backend/fastapi_app/mappers/fontanella_mapper.py`
  - All response models
  - DTOMapper utility

## 🎓 Learning Path

1. **Start Here**: [API_SUMMARY.txt](API_SUMMARY.txt)
   - Get visual overview
   - Understand architecture

2. **Quick Setup**: [API_QUICK_START.md](API_QUICK_START.md)
   - Start server
   - Run tests
   - See examples

3. **Endpoint Details**: [API_ENDPOINTS.md](API_ENDPOINTS.md)
   - Read each endpoint
   - Copy request examples
   - Understand responses

4. **Implementation**: [API_IMPLEMENTATION.md](API_IMPLEMENTATION.md)
   - See test cases
   - Understand flow
   - Check file structure

5. **Architecture**: [DATA_LAYER.md](DATA_LAYER.md)
   - Understand patterns
   - Learn about repositories
   - See design decisions

## 🔗 External Resources

### Frameworks & Libraries
- **FastAPI**: https://fastapi.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/
- **MongoDB**: https://docs.mongodb.com/

### Frontend Integration
- **Leaflet.js**: https://leafletjs.com/
- **GeoJSON**: https://geojson.org/
- **Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

## ❓ FAQ

### Q: How do I start the API server?
**A**: See [API_QUICK_START.md → Start API Server](API_QUICK_START.md#-start-api-server-5-minutes)

### Q: Where can I test endpoints?
**A**: Use Swagger UI at http://localhost:8000/docs (recommended)

### Q: How do I display fountains on a map?
**A**: See [API_QUICK_START.md → Display Fountains](API_QUICK_START.md#mapping-use-case-examples)

### Q: What does color_class mean?
**A**: Density classification: LOW (green), MEDIUM (yellow), HIGH (orange), VERY_HIGH (red)

### Q: How are distances calculated?
**A**: Using Haversine formula from WGS84 coordinates

### Q: Can I search by multiple filters?
**A**: Yes, use `/fountains/search/advanced` endpoint

### Q: What's the default search radius?
**A**: 500 meters (configurable in request)

## ✅ Status

- ✅ All 6 use cases implemented
- ✅ 8 endpoints fully functional
- ✅ Input validation complete
- ✅ Error handling in place
- ✅ Documentation comprehensive
- ✅ Examples for all integration methods
- ✅ Ready for frontend development

---

**Last Updated**: April 15, 2026

**Version**: 1.0 - Production Ready

**Next Step**: Begin frontend implementation using these API endpoints!
