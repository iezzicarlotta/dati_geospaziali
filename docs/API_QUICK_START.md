# API Quick Start Guide

## 🚀 Start API Server (5 minutes)

### Step 1: Ensure MongoDB is Running

```bash
# Check MongoDB status
mongosh --eval "db.adminCommand('ping')"

# Output should show: { ok: 1 }
```

### Step 2: Start FastAPI Server

```bash
# From workspace root
cd backend/fastapi_app

# Start API with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
✓ FastAPI started with MongoDB connection
```

### Step 3: Open Swagger Documentation

Visit: http://localhost:8000/docs

You should see interactive API documentation with all endpoints.

---

## 📌 Core Endpoints (Copy-Paste Ready)

### 1. Health Check
```
GET http://localhost:8000/api/v1/fountains/health
```

**Response**:
```json
{
  "status": "healthy",
  "message": "API is running and database is accessible",
  "total_fountains": 2847
}
```

---

### 2. Get NIL Dropdown (for select component)
```
GET http://localhost:8000/api/v1/fountains/nils/dropdown
```

**Response**:
```json
[
  {"id": "507f1f...", "name": "Centro Storico"},
  {"id": "507f1f...", "name": "Navigli"},
  {"id": "507f1f...", "name": "Porta Romana"}
]
```

---

### 3. Search Fountains by NIL (Use Case 1 & 2)
```
POST http://localhost:8000/api/v1/fountains/search/by-nil

Request Body:
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
      "nil_id": 1,
      "coordinate": {"longitude": 9.190, "latitude": 45.464},
      "name": "Fontanella Centro"
    }
  ],
  "total_count": 45,
  "page": 1,
  "page_size": 20,
  "total_pages": 3,
  "has_next": true
}
```

---

### 4. Search Nearby (Use Case 3)
```
POST http://localhost:8000/api/v1/fountains/search/nearby

Request Body:
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
```

---

### 5. Search Near User's Location (Use Case 4)
```
POST http://localhost:8000/api/v1/fountains/search/nearby/geolocation?latitude=45.464&longitude=9.190&radius_meters=500
```

**Response**: Same as endpoint 4

---

### 6. Get Statistics Table (Use Case 5)
```
GET http://localhost:8000/api/v1/fountains/statistics/nils
```

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
    }
  ],
  "total_nils": 99,
  "total_fountains": 2847,
  "max_density": 50.8,
  "min_density": 0.24
}
```

---

### 7. Get Choropleth Map Data (Use Case 6)
```
GET http://localhost:8000/api/v1/fountains/choropleth
```

**Response** (200 OK) - GeoJSON FeatureCollection:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[9.1, 45.4], [9.2, 45.4], [9.2, 45.5], [9.1, 45.5], [9.1, 45.4]]]
      },
      "properties": {
        "nil_id": 1,
        "nil_name": "Centro Storico",
        "fountain_count": 127,
        "density_fountains_per_km2": 50.8,
        "color_class": "VERY_HIGH"
      }
    }
  ],
  "statistics": [],
  "bounds": {"north": 45.5, "south": 45.4, "east": 9.3, "west": 9.1},
  "min_density": 0.24,
  "max_density": 50.8,
  "total_fountains": 2847
}
```

---

## 🧪 Quick Test with cURL

Copy-paste in terminal:

```bash
# Test 1: Health check
curl http://localhost:8000/api/v1/fountains/health | jq

# Test 2: Get dropdown
curl http://localhost:8000/api/v1/fountains/nils/dropdown | jq '.[:3]'

# Test 3: Search by NIL
curl -X POST http://localhost:8000/api/v1/fountains/search/by-nil \
  -H "Content-Type: application/json" \
  -d '{"nil_id":"1","page":1,"page_size":5}' | jq '.total_count, .items[0].name'

# Test 4: Search nearby
curl -X POST http://localhost:8000/api/v1/fountains/search/nearby \
  -H "Content-Type: application/json" \
  -d '{"latitude":45.464,"longitude":9.190}' | jq '.total_count'

# Test 5: Get statistics
curl http://localhost:8000/api/v1/fountains/statistics/nils | jq '.statistics[:3]'

# Test 6: Get choropleth
curl http://localhost:8000/api/v1/fountains/choropleth | jq '.type, .features | length'
```

---

## 🧪 Quick Test with Python

```python
import requests
import json

BASE = "http://localhost:8000/api/v1"

def test():
    # 1. Health
    print("Health:", requests.get(f"{BASE}/fountains/health").json()["status"])
    
    # 2. Dropdown
    nils = requests.get(f"{BASE}/fountains/nils/dropdown").json()
    print(f"NILs: {len(nils)} options")
    
    # 3. Search by NIL
    res = requests.post(f"{BASE}/fountains/search/by-nil",
                        json={"nil_id":"1","page":1}).json()
    print(f"NIL 1: {res['total_count']} fountains found, showing {len(res['items'])}")
    
    # 4. Nearby
    res = requests.post(f"{BASE}/fountains/search/nearby",
                        json={"latitude":45.464,"longitude":9.190}).json()
    print(f"Nearby: {res['total_count']} fountains within 500m")
    
    # 5. Stats
    res = requests.get(f"{BASE}/fountains/statistics/nils").json()
    print(f"Stats: {res['total_fountains']} fountains in {res['total_nils']} NILs")
    
    # 6. Choropleth
    res = requests.get(f"{BASE}/fountains/choropleth").json()
    print(f"Choropleth: {len(res['features'])} GeoJSON features")

test()
```

Save as `quick_test.py` and run: `python quick_test.py`

---

## 🌐 Quick Test in Browser Console

Open http://localhost:8000/docs, then paste in browser console:

```javascript
const BASE = "http://localhost:8000/api/v1";

// Test all endpoints
Promise.all([
  fetch(`${BASE}/fountains/health`).then(r => r.json()),
  fetch(`${BASE}/fountains/nils/dropdown`).then(r => r.json()),
  fetch(`${BASE}/fountains/search/by-nil`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({nil_id: "1", page: 1})
  }).then(r => r.json()),
  fetch(`${BASE}/fountains/statistics/nils`).then(r => r.json()),
  fetch(`${BASE}/fountains/choropleth`).then(r => r.json())
]).then(([h, nils, search, stats, choropleth]) => {
  console.log("✓ Health:", h.status);
  console.log("✓ NILs:", nils.length, "options");
  console.log("✓ Search:", search.total_count, "fountains");
  console.log("✓ Stats:", stats.total_fountains, "fountains");
  console.log("✓ Choropleth:", choropleth.features.length, "features");
});
```

---

## 🎯 Mapping Use Case Examples

### Display Fountains on Map (Leaflet.js)

```javascript
const map = L.map('map').setView([45.464, 9.190], 11);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Search and display
fetch("http://localhost:8000/api/v1/fountains/search/by-nil", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({nil_id: "1", page: 1, page_size: 100})
})
.then(r => r.json())
.then(data => {
  data.items.forEach(fountain => {
    L.circleMarker(
      [fountain.coordinate.latitude, fountain.coordinate.longitude],
      {radius: 5, fillColor: "blue"}
    )
    .bindPopup(fountain.name)
    .addTo(map);
  });
});
```

### Display Choropleth Map

```javascript
const map = L.map('map').setView([45.464, 9.190], 11);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Color mapping
const colorMap = {
  "LOW": "#2ecc71",
  "MEDIUM": "#f39c12",
  "HIGH": "#e74c3c",
  "VERY_HIGH": "#c0392b"
};

// Load choropleth
fetch("http://localhost:8000/api/v1/fountains/choropleth")
.then(r => r.json())
.then(data => {
  L.geoJSON(data, {
    style: f => ({
      fillColor: colorMap[f.properties.color_class],
      fillOpacity: 0.7,
      weight: 2
    })
  }).addTo(map);
});
```

---

## 📊 Display Statistics Table

```javascript
// Get stats and create table
fetch("http://localhost:8000/api/v1/fountains/statistics/nils")
.then(r => r.json())
.then(data => {
  const tbody = document.getElementById("table-body");
  data.statistics.forEach(stat => {
    const row = tbody.insertRow();
    row.innerHTML = `
      <td>${stat.nil_name}</td>
      <td>${stat.fountain_count}</td>
      <td>${stat.density_fountains_per_km2.toFixed(2)}</td>
      <td><span class="badge ${stat.color_class}">${stat.color_class}</span></td>
    `;
  });
});
```

---

## ⚡ API Performance Notes

| Endpoint | Typical Response Time | Notes |
|----------|----------------------|-------|
| Search by NIL | 50-200ms | Paginated, index on ID_NIL |
| Nearby search | 100-300ms | Geospatial index required |
| Statistics | 200-500ms | Aggregation pipeline |
| Choropleth | 300-800ms | Largest response, includes geometries |

All times measured with MongoDB locally.

---

## 🔧 Troubleshooting

### API won't start: "Address already in use"
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### "Cannot connect to MongoDB"
```bash
# Check MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# If fails, start MongoDB
# (Platform-specific: brew services start mongodb-community, etc.)
```

### "No results returned"
- Check NIL ID is valid (1-999)
- Check coordinates are within Milan area (~45.4-45.5 lat, ~9.1-9.3 lon)
- Check database has data: `mongosh dbSpaziali --eval "db.fontanelle.countDocuments()"`

### CORS errors in browser
- Ensure FastAPI server has CORS middleware enabled (already done in main.py)
- Frontend and API should have different ports (frontend: 3000, API: 8000)

---

## 📚 Full Documentation

- **API Details**: `docs/API_ENDPOINTS.md` (complete endpoint reference)
- **Data Layer**: `docs/DATA_LAYER.md` (architecture and patterns)
- **Implementation**: `docs/API_IMPLEMENTATION.md` (test cases and integration)

---

## ✅ Checklist

- [ ] MongoDB running
- [ ] FastAPI server started on port 8000
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] Health endpoint returns 200 OK
- [ ] Can see NILs in dropdown
- [ ] Search by NIL returns results
- [ ] Nearby search returns fountains with distance
- [ ] Statistics table loads
- [ ] Choropleth GeoJSON has features

**Once all checked**: Ready to start frontend development! 🎉

---

## 🚀 Next: Frontend Development

Now that API is ready:

1. **Setup Frontend Project**
   ```bash
   mkdir frontend
   cd frontend
   npm init -y
   npm install leaflet axios
   ```

2. **Create HTML with Map**
   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
   </head>
   <body>
     <div id="map" style="height: 600px;"></div>
   </body>
   </html>
   ```

3. **Use API to Display Data**
   - Follow examples above for map display
   - Implement search forms
   - Add error handling

4. **Deploy**
   - Frontend: Netlify/Vercel
   - API: AWS/Heroku/DigitalOcean
   - Database: MongoDB Atlas

---

**Status**: ✅ Backend API is production-ready for frontend integration.
