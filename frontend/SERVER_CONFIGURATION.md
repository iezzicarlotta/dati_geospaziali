# Frontend Server Configuration

## 🚀 Serving Static Files

### Option 1: Python (Simple HTTP Server)

```bash
# Navigate to project root
cd c:\Users\net.SIS-03\Desktop\dati_geospaziali

# Start server on port 3000
python -m http.server 3000 --directory frontend/public

# Access at http://localhost:3000
```

**Pros:**
- No installation needed (Python built-in)
- Simple one-liner
- Good for development

**Cons:**
- Single-threaded
- No caching headers
- No compression

---

### Option 2: Node.js HTTP Server

```bash
# Install globally (one time)
npm install -g http-server

# Navigate to public folder
cd frontend/public

# Start server on port 3000
http-server -p 3000 -c-1

# Access at http://localhost:3000
```

**Pros:**
- Better performance
- Caching support
- Compression available

**Cons:**
- Requires Node.js installation
- Extra package needed

---

### Option 3: Flask (Python Micro-framework)

**File:** `frontend/server.py`

```python
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, 
    static_folder='public',
    static_url_path='',
    template_folder='public')

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

@app.errorhandler(404)
def not_found(error):
    return send_from_directory('public', 'index.html'), 404

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=3000,
        static_folder='public'
    )
```

**Usage:**
```bash
# Install Flask
pip install flask

# Run server
cd frontend
python server.py

# Access at http://localhost:3000
```

---

### Option 4: Express.js (Node.js)

**File:** `frontend/server.js`

```javascript
const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Gzip compression
app.use(express.static(path.join(__dirname, 'public'), {
  maxAge: '1d',
  etag: false
}));

// SPA fallback - return index.html for all routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
```

**Usage:**
```bash
# Install dependencies
npm install express

# Run server
node server.js

# Access at http://localhost:3000
```

---

## 🔗 Integration with Backend

### CORS Configuration

The backend FastAPI app should have CORS enabled:

```python
# backend/fastapi_app/main.py

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Calls from Frontend

```javascript
// frontend/src/js/utils/api-client.js

const API_BASE_URL = process.env.API_URL || 'http://localhost:8000/api/v1';

// All API calls will use this base URL
// Example: GET http://localhost:8000/api/v1/fountains/nils/dropdown
```

---

## 📁 Directory Structure

### For Static Serving

```
frontend/
├── public/                    # ← Serve this directory
│   ├── index.html            # Main HTML file
│   ├── css/                  # CSS files
│   │   ├── design-system.css
│   │   ├── components.css
│   │   └── pages/
│   │       └── home.css
│   └── js/                   # Compiled JS files
│       ├── utils/
│       ├── components/
│       └── pages/
│
└── src/                      # Source files (not served)
    ├── js/                   # Source JavaScript
    ├── styles/               # Source CSS
    └── main.js
```

### For SPA (Single Page Application)

If using a bundler (Webpack, Vite), the structure would be:

```
frontend/
├── src/
│   ├── index.html           # Template
│   ├── main.js              # Entry point
│   ├── components/
│   ├── pages/
│   ├── styles/
│   └── utils/
│
├── dist/                    # Built files (generated)
│   ├── index.html
│   ├── css/
│   └── js/
│
└── vite.config.js          # Build config (if using Vite)
```

---

## 🔒 Security Headers

### Express.js with Helmet

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "http://localhost:8000"]
    }
  }
}));
```

### Flask with Security Headers

```python
from flask_cors import CORS
from flask_talisman import Talisman

app = Flask(__name__)
CORS(app)
Talisman(app)
```

---

## 🚀 Development Workflow

### Quick Start with Python

```bash
# Terminal 1: Start backend (already running)
cd c:\Users\net.SIS-03\Desktop\dati_geospaziali
python -m uvicorn backend.fastapi_app.main:app --reload --port 8000

# Terminal 2: Start frontend
cd c:\Users\net.SIS-03\Desktop\dati_geospaziali
python -m http.server 3000 --directory frontend/public

# Terminal 3 (optional): File watcher for CSS changes
cd frontend
# Watch CSS files and auto-copy to public/css/
```

### Access URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs

---

## 🛠️ Build Tools Configuration

### Vite Configuration (if needed)

**File:** `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'

export default defineConfig({
  root: 'src',
  build: {
    outDir: '../public',
    emptyOutDir: true,
    rollupOptions: {
      input: 'src/index.html',
      output: {
        entryFileNames: 'js/[name].[hash].js',
        chunkFileNames: 'js/[name].[hash].js',
        assetFileNames: ({ name }) => {
          if (/\.(css)$/.test(name ?? '')) {
            return 'css/[name].[hash][extname]';
          }
          return '[name].[hash][extname]';
        }
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api/v1')
      }
    }
  }
})
```

**Usage:**
```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🌐 Environment Configuration

### Environment Variables

**File:** `frontend/.env.development`

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=Fontanelle Milano
```

**File:** `frontend/.env.production`

```
VITE_API_BASE_URL=https://api.fontanellemilano.it/api/v1
VITE_APP_TITLE=Fontanelle Milano
```

### Access in JavaScript

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
```

---

## 📊 Deployment Checklist

### Pre-deployment
- [ ] All CSS files compiled and minified
- [ ] All JavaScript files bundled and minified
- [ ] Images optimized
- [ ] HTML validated
- [ ] Links checked (internal and external)
- [ ] Forms tested
- [ ] API endpoints verified
- [ ] Performance tested (PageSpeed Insights)
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Environment variables set
- [ ] Error pages created (404, 500)

### Production Server

**Nginx Configuration Example:**

```nginx
server {
    listen 80;
    server_name fontanellemilano.it www.fontanellemilano.it;

    root /var/www/frontend/public;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_minlength 1000;

    # Caching
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🧪 Testing

### Manual Testing Checklist

```
Desktop Testing
[ ] Chrome latest
[ ] Firefox latest
[ ] Safari latest
[ ] Edge latest

Mobile Testing
[ ] iPhone SE (small)
[ ] iPhone 12 (medium)
[ ] iPad (tablet)
[ ] Android (Chrome/Firefox)

Features
[ ] All buttons clickable
[ ] Forms submit correctly
[ ] API calls work
[ ] Results render properly
[ ] Responsive layout works
[ ] Touch interactions work
[ ] Keyboard navigation works
[ ] Screen reader works
```

### Automated Testing (Optional)

**With Playwright:**

```javascript
// tests/homepage.spec.js
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  const title = await page.locator('h1').textContent();
  expect(title).toContain('Fontanelle Milano');
});

test('search form submits', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Click search tab
  await page.click('[data-tab="tab-search-nil"]');
  
  // Select NIL
  await page.selectOption('#nil-select', '1');
  
  // Submit
  await page.click('button:has-text("Cerca")');
  
  // Wait for results
  await page.waitForSelector('.result-item');
});
```

---

## 📈 Performance Tips

### 1. CSS Optimization
```bash
# Install PurgeCSS (remove unused CSS)
npm install purge-css --save-dev

# Run before deployment
npx purge-css --css src/styles/*.css \
               --content public/index.html \
               --output public/css/
```

### 2. Image Optimization
```bash
# Install ImageMagick or use online tool
# Optimize all images
convert image.jpg -quality 85 image-optimized.jpg
```

### 3. Minification
```bash
# Install csso (CSS minifier)
npm install csso-cli --save-dev

# Minify CSS
csso src/styles/design-system.css -o public/css/design-system.min.css
```

### 4. Lazy Loading
```html
<!-- For map and heavy components -->
<div id="map-canvas" data-src="/js/map-component.js"></div>

<script>
  // Load only when needed
  document.addEventListener('scroll', () => {
    const mapCanvas = document.getElementById('map-canvas');
    if (mapCanvas.getBoundingClientRect().top < window.innerHeight) {
      // Load map component
    }
  });
</script>
```

---

## 🐛 Troubleshooting

### Issue: CORS errors

**Solution:** Ensure backend has CORS enabled:
```python
# backend/fastapi_app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: 404 errors on page refresh

**Solution:** Configure server to serve `index.html` for all routes:
```javascript
app.get('*', (res, req) => {
  req.sendFile('index.html');
});
```

### Issue: Styles not loading

**Solution:** Check CSS file paths and ensure they're being served:
```bash
# Check that CSS files exist in public/css/
ls -la frontend/public/css/

# Check browser Network tab for failed requests
# Verify paths in <link> tags match actual files
```

---

## 📚 Resources

- [MDN: HTTP Server Configuration](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Express.js Guide](https://expressjs.com/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Vite Documentation](https://vitejs.dev/)

---

**Last Updated:** 2026-04-15
**Status:** ✅ Configuration guides ready
