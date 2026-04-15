# API Endpoints Documentation

## Overview

FastAPI backend provides 8 endpoints (6 main + 1 bonus + 1 health check) supporting all required web app functionality:

```
BASE_URL = http://localhost:8000/api/v1
```

## Endpoints Summary

| # | Endpoint | Method | Purpose | Use Case |
|---|----------|--------|---------|----------|
| 1 | `/fountains/search/by-nil` | POST | Search by NIL ID (text input) | User enters NIL ID |
| 2 | `/fountains/nils/dropdown` | GET | Get NIL options | Load dropdown |
| 2b | `/fountains/search/by-nil-dropdown` | POST | Search by NIL (dropdown) | User selects from dropdown |
| 3 | `/fountains/search/nearby` | POST | Search near coordinates | User enters location |
| 4 | `/fountains/search/nearby/geolocation` | POST | Search near user's location | Browser geolocation API |
| 5 | `/fountains/statistics/nils` | GET | Get fountains per NIL table | Display statistics table |
| 6 | `/fountains/choropleth` | GET | Get GeoJSON for choropleth map | Display colored map |
| 7 | `/fountains/search/advanced` | POST | Advanced multi-filter search | BONUS: Complex queries |
| 8 | `/fountains/health` | GET | API health check | Monitor connectivity |

---

## Endpoint Details

### 1. Search Fountains by NIL ID

**Endpoint**: `POST /api/v1/fountains/search/by-nil`

**Use Case**: User enters a NIL ID (e.g., "1") in a text input field and clicks search.

**Request**:
```json
{
  "nil_id": "1",
  "page": 1,
  "page_size": 20
}
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "object_id": "1001",
      "nil_id": 1,
      "coordinate": {
        "longitude": 9.190,
        "latitude": 45.464
      },
      "name": "Fontanella Centro",
      "description": "Fountain in historic center",
      "municipio": "Milano",
      "cap": "20100",
      "geometry_type": "Point"
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "object_id": "1002",
      "nil_id": 1,
      "coordinate": {
        "longitude": 9.191,
        "latitude": 45.465
      },
      "name": "Fontanella Duomo",
      "description": null,
      "municipio": "Milano",
      "cap": "20100",
      "geometry_type": "Point"
    }
  ],
  "total_count": 45,
  "page": 1,
  "page_size": 20,
  "total_pages": 3,
  "has_next": true,
  "has_previous": false
}
```

**Error** (400 Bad Request):
```json
{
  "detail": "NIL ID not found or invalid"
}
```

**Query Parameters**:
- `nil_id` (string, required): NIL ID to search (e.g., "1", "123")
- `page` (integer, optional, default=1): Page number (1-indexed)
- `page_size` (integer, optional, default=20, max=100): Results per page

**Frontend Integration**:
```javascript
// Example: User enters "1" in text input and clicks search
const nilId = document.getElementById("nil-input").value;
const response = await fetch("/api/v1/fountains/search/by-nil", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    nil_id: nilId,
    page: 1,
    page_size: 20
  })
});
const data = await response.json();
displayFountainsOnMap(data.items);  // Plot on map
displayPagination(data.page, data.total_pages);  // Show page controls
```

---

### 2a. Get NIL Dropdown Options

**Endpoint**: `GET /api/v1/fountains/nils/dropdown`

**Use Case**: Frontend loads dropdown/select component on page load.

**Request**: No body (GET request)

**Response** (200 OK):
```json
[
  {
    "id": "507f1f77bcf86cd799439001",
    "name": "Centro Storico"
  },
  {
    "id": "507f1f77bcf86cd799439002",
    "name": "Navigli"
  },
  {
    "id": "507f1f77bcf86cd799439003",
    "name": "Porta Romana"
  }
]
```

**Frontend Integration**:
```javascript
// On page load, populate dropdown
const response = await fetch("/api/v1/fountains/nils/dropdown");
const nils = await response.json();

const select = document.getElementById("nil-select");
nils.forEach(nil => {
  const option = document.createElement("option");
  option.value = nil.id;
  option.textContent = nil.name;
  select.appendChild(option);
});
```

---

### 2b. Search Fountains by NIL (Dropdown Selection)

**Endpoint**: `POST /api/v1/fountains/search/by-nil-dropdown`

**Use Case**: User selects a NIL from dropdown and results are automatically loaded.

**Request** (Query Parameters):
```
POST /api/v1/fountains/search/by-nil-dropdown?nil_id=1&page=1&page_size=20
```

**Response** (200 OK): Same as endpoint 1

**Frontend Integration**:
```javascript
// When dropdown selection changes
document.getElementById("nil-select").addEventListener("change", async (e) => {
  const nilId = e.target.value;
  const response = await fetch(
    `/api/v1/fountains/search/by-nil-dropdown?nil_id=${nilId}&page=1&page_size=20`,
    { method: "POST" }
  );
  const data = await response.json();
  clearMap();
  displayFountainsOnMap(data.items);
});
```

---

### 3. Search Fountains Near Location (Text Input)

**Endpoint**: `POST /api/v1/fountains/search/nearby`

**Use Case**: User enters coordinates or an address (converted to lat/lon), and sees all fountains within 500m.

**Request**:
```json
{
  "latitude": 45.464,
  "longitude": 9.190,
  "radius_meters": 500,
  "limit": 50
}
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "object_id": "1001",
      "nil_id": 1,
      "coordinate": {
        "longitude": 9.190,
        "latitude": 45.464
      },
      "name": "Fontanella Centro",
      "description": "Fountain in historic center",
      "distance_meters": 145.3
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "object_id": "1002",
      "nil_id": 1,
      "coordinate": {
        "longitude": 9.191,
        "latitude": 45.465
      },
      "name": "Fontanella Duomo",
      "description": null,
      "distance_meters": 287.5
    }
  ],
  "search_center": {
    "longitude": 9.190,
    "latitude": 45.464
  },
  "search_radius_meters": 500,
  "total_count": 12
}
```

**Query Parameters**:
- `latitude` (float, required): Search point latitude (-90 to 90)
- `longitude` (float, required): Search point longitude (-180 to 180)
- `radius_meters` (integer, optional, default=500): Search radius in meters (1-50000)
- `limit` (integer, optional, default=50): Maximum results to return

**Frontend Integration**:
```javascript
// User clicks "Find fountains near" and enters coordinates
document.getElementById("search-nearby-btn").addEventListener("click", async () => {
  const latitude = parseFloat(document.getElementById("lat-input").value);
  const longitude = parseFloat(document.getElementById("lon-input").value);
  
  const response = await fetch("/api/v1/fountains/search/nearby", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      latitude,
      longitude,
      radius_meters: 500,
      limit: 50
    })
  });
  
  const data = await response.json();
  clearMap();
  displaySearchCenter(data.search_center);  // Mark search point
  displayFountainsWithDistance(data.items);  // Show fountains with distances
});
```

---

### 4. Search Fountains Near User (Geolocation)

**Endpoint**: `POST /api/v1/fountains/search/nearby/geolocation`

**Use Case**: Browser geolocation API provides user's current location, automatically finds nearby fountains.

**Request** (Query Parameters):
```
POST /api/v1/fountains/search/nearby/geolocation?latitude=45.464&longitude=9.190&radius_meters=500&limit=50
```

**Response** (200 OK): Same format as endpoint 3

**Frontend Integration**:
```javascript
// On page load, request user geolocation
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(async (position) => {
    const { latitude, longitude } = position.coords;
    
    const response = await fetch(
      `/api/v1/fountains/search/nearby/geolocation?latitude=${latitude}&longitude=${longitude}&radius_meters=500&limit=50`,
      { method: "POST" }
    );
    
    const data = await response.json();
    clearMap();
    displayUserLocation(data.search_center, "blue");  // Mark user in blue
    displayFountains(data.items);  // Show fountains
    showMessage(`Found ${data.total_count} fountains within 500m`);
  });
}
```

---

### 5. Get NIL Statistics Table

**Endpoint**: `GET /api/v1/fountains/statistics/nils`

**Use Case**: Display table with NIL statistics (name, fountain count, density) sorted by count descending.

**Request**: No body (GET request)

**Response** (200 OK):
```json
{
  "statistics": [
    {
      "nil_id": 1,
      "nil_name": "Centro Storico",
      "fountain_count": 127,
      "area_km2": 2.5,
      "density_fountains_per_km2": 50.8,
      "color_class": "VERY_HIGH"
    },
    {
      "nil_id": 2,
      "nil_name": "Navigli",
      "fountain_count": 89,
      "area_km2": 3.2,
      "density_fountains_per_km2": 27.8,
      "color_class": "HIGH"
    },
    {
      "nil_id": 3,
      "nil_name": "Porta Romana",
      "fountain_count": 45,
      "area_km2": 4.1,
      "density_fountains_per_km2": 11.0,
      "color_class": "MEDIUM"
    },
    {
      "nil_id": 99,
      "nil_name": "Periferia Nord",
      "fountain_count": 3,
      "area_km2": 12.5,
      "density_fountains_per_km2": 0.24,
      "color_class": "LOW"
    }
  ],
  "total_nils": 99,
  "total_fountains": 2847,
  "max_density": 50.8,
  "min_density": 0.24
}
```

**Frontend Integration**:
```javascript
// Load statistics table on page load
async function loadStatisticsTable() {
  const response = await fetch("/api/v1/fountains/statistics/nils");
  const data = await response.json();
  
  const tbody = document.getElementById("stats-tbody");
  tbody.innerHTML = "";
  
  data.statistics.forEach(stat => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${stat.nil_name}</td>
      <td>${stat.fountain_count}</td>
      <td>${stat.density_fountains_per_km2.toFixed(2)}</td>
      <td><span class="badge ${stat.color_class.toLowerCase()}">${stat.color_class}</span></td>
    `;
    tbody.appendChild(tr);
  });
  
  document.getElementById("stats-summary").innerHTML = `
    Total: ${data.total_fountains} fountains in ${data.total_nils} NILs
  `;
}

loadStatisticsTable();
```

---

### 6. Get Choropleth Map Data

**Endpoint**: `GET /api/v1/fountains/choropleth`

**Use Case**: Display interactive map with NILs colored by fountain density.

**Request**: No body (GET request)

**Response** (200 OK):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [9.1, 45.4],
          [9.2, 45.4],
          [9.2, 45.5],
          [9.1, 45.5],
          [9.1, 45.4]
        ]]
      },
      "properties": {
        "nil_id": 1,
        "nil_name": "Centro Storico",
        "fountain_count": 127,
        "density_fountains_per_km2": 50.8,
        "color_class": "VERY_HIGH"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [9.2, 45.4],
          [9.3, 45.4],
          [9.3, 45.5],
          [9.2, 45.5],
          [9.2, 45.4]
        ]]
      },
      "properties": {
        "nil_id": 2,
        "nil_name": "Navigli",
        "fountain_count": 89,
        "density_fountains_per_km2": 27.8,
        "color_class": "HIGH"
      }
    }
  ],
  "statistics": [
    {
      "nil_id": 1,
      "nil_name": "Centro Storico",
      "fountain_count": 127,
      "area_km2": 2.5,
      "density_fountains_per_km2": 50.8,
      "color_class": "VERY_HIGH"
    }
  ],
  "bounds": {
    "north": 45.5,
    "south": 45.4,
    "east": 9.3,
    "west": 9.1
  },
  "min_density": 0.24,
  "max_density": 50.8,
  "total_fountains": 2847
}
```

**Frontend Integration** (with Leaflet.js):
```javascript
// Load and render choropleth map
async function loadChoropleth() {
  const response = await fetch("/api/v1/fountains/choropleth");
  const data = await response.json();
  
  // Define colors by density class
  const colorMap = {
    "LOW": "#2ecc71",      // Green
    "MEDIUM": "#f39c12",   // Yellow
    "HIGH": "#e74c3c",     // Orange
    "VERY_HIGH": "#c0392b" // Red
  };
  
  // Create Leaflet GeoJSON layer
  const geojsonLayer = L.geoJSON(data, {
    style: (feature) => ({
      fillColor: colorMap[feature.properties.color_class],
      weight: 2,
      opacity: 0.8,
      color: "#666",
      fillOpacity: 0.7
    }),
    onEachFeature: (feature, layer) => {
      const props = feature.properties;
      const popup = `
        <strong>${props.nil_name}</strong><br>
        Fountains: ${props.fountain_count}<br>
        Density: ${props.density_fountains_per_km2.toFixed(2)} fountains/km²
      `;
      layer.bindPopup(popup);
    }
  });
  
  // Add to map
  const map = L.map("map").setView([45.464, 9.190], 11);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
  geojsonLayer.addTo(map);
  
  // Add legend
  const legend = L.control({ position: "bottomright" });
  legend.onAdd = () => {
    const div = L.DomUtil.create("div", "legend");
    Object.entries(colorMap).forEach(([cls, color]) => {
      div.innerHTML += `
        <div>
          <span style="background-color: ${color}; display: inline-block; width: 20px; height: 20px; margin-right: 5px;"></span>
          ${cls}
        </div>
      `;
    });
    return div;
  };
  legend.addTo(map);
}

loadChoropleth();
```

---

### 7. Advanced Multi-Filter Search (Bonus)

**Endpoint**: `POST /api/v1/fountains/search/advanced`

**Use Case**: Complex queries combining multiple filter criteria.

**Request**:
```json
{
  "nil_id": "1",
  "nil_name": "Centro",
  "municipio": "Milano",
  "cap": "20100",
  "page": 1,
  "page_size": 20
}
```

**Response** (200 OK): Same as endpoint 1

**Notes**:
- At least one filter must be provided
- All filters are optional but at least one required
- `nil_name` is partial match (contains), others are exact match

---

### 8. Health Check

**Endpoint**: `GET /api/v1/fountains/health`

**Use Case**: Monitor API and database connectivity.

**Request**: No body (GET request)

**Response** (200 OK):
```json
{
  "status": "healthy",
  "message": "API is running and database is accessible",
  "total_fountains": 2847
}
```

**Response** (500 Error):
```json
{
  "detail": "Database connection failed"
}
```

---

## Error Handling

All endpoints follow consistent error response format:

### 400 Bad Request
```json
{
  "detail": "Invalid input - description of validation error"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error - check server logs"
}
```

---

## Response Codes Summary

| Status | Meaning | Endpoint |
|--------|---------|----------|
| 200 | Success | All GET/POST |
| 400 | Bad Request - validation error | All |
| 404 | Not Found - resource missing | Search endpoints |
| 500 | Internal Server Error | All |

---

## Testing Endpoints

### Using cURL

```bash
# 1. Search by NIL ID
curl -X POST http://localhost:8000/api/v1/fountains/search/by-nil \
  -H "Content-Type: application/json" \
  -d '{"nil_id":"1","page":1,"page_size":20}'

# 2. Get NIL dropdown
curl http://localhost:8000/api/v1/fountains/nils/dropdown

# 3. Search nearby (text input)
curl -X POST http://localhost:8000/api/v1/fountains/search/nearby \
  -H "Content-Type: application/json" \
  -d '{"latitude":45.464,"longitude":9.190,"radius_meters":500}'

# 4. Search nearby (geolocation)
curl -X POST "http://localhost:8000/api/v1/fountains/search/nearby/geolocation?latitude=45.464&longitude=9.190"

# 5. Get statistics table
curl http://localhost:8000/api/v1/fountains/statistics/nils

# 6. Get choropleth data
curl http://localhost:8000/api/v1/fountains/choropleth

# 8. Health check
curl http://localhost:8000/api/v1/fountains/health
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Search by NIL
response = requests.post(
    f"{BASE_URL}/fountains/search/by-nil",
    json={"nil_id": "1", "page": 1, "page_size": 20}
)
print(response.json())

# Get dropdown options
response = requests.get(f"{BASE_URL}/fountains/nils/dropdown")
print(response.json())

# Search nearby
response = requests.post(
    f"{BASE_URL}/fountains/search/nearby",
    json={"latitude": 45.464, "longitude": 9.190, "radius_meters": 500}
)
print(response.json())

# Get statistics
response = requests.get(f"{BASE_URL}/fountains/statistics/nils")
print(response.json())

# Get choropleth
response = requests.get(f"{BASE_URL}/fountains/choropleth")
print(response.json())

# Health check
response = requests.get(f"{BASE_URL}/fountains/health")
print(response.json())
```

### Using Postman

1. Import collection from OpenAPI/Swagger: `http://localhost:8000/openapi.json`
2. Or manually create requests for each endpoint
3. All endpoints are documented in Swagger UI at: `http://localhost:8000/docs`

---

## Swagger/OpenAPI Documentation

Once the API is running, access interactive documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

All endpoints, request/response models, and example values are documented in the interactive UI.

---

## Input Validation

All inputs are validated:

### Coordinate Validation
- **latitude**: Must be -90 to 90
- **longitude**: Must be -180 to 180

### Pagination Validation
- **page**: Must be >= 1
- **page_size**: Must be 1-100 (default 20)

### Search Radius
- **radius_meters**: Must be 1-50000 (default 500)

### NIL ID
- **nil_id**: Must be a valid numeric string (e.g., "1", "123")

Validation errors return 400 with detailed error messages.

---

## Next Steps for Frontend

1. **Map Display**: Use Leaflet.js or similar to display fountain markers
2. **Pagination**: Implement page controls for result sets
3. **Search Forms**: Create input forms for each search type
4. **Error Handling**: Display user-friendly error messages
5. **Loading States**: Show loading indicators during API calls
6. **Distance Display**: Format distances in meters/km for display
7. **Color Styling**: Apply color classes to map features and table rows
8. **Responsive Design**: Ensure maps and tables work on mobile

All API responses are JSON-formatted and ready for direct JavaScript consumption.
