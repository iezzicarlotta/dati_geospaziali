# 🎯 Frontend Quick Reference

## 📌 File Locations

```
Design System Files (Copy to public/css/)
├── design-system.css    → CSS custom properties + global styles
├── components.css       → Reusable component styles  
└── pages/home.css       → Page-specific styles

HTML Files (Serve from public/)
└── index.html          → Main page (500+ lines, semantic HTML)

Documentation Files (For reference)
├── README.md                        → Overview
├── FRONTEND_DESIGN_SYSTEM.md        → Design tokens & components
├── JS_IMPLEMENTATION_GUIDE.md       → JavaScript guide
├── ARCHITECTURE_SUMMARY.md          → Architecture overview
└── SERVER_CONFIGURATION.md          → Server setup
```

---

## 🚀 Quick Start Commands

### Start Frontend Server
```bash
# Python (simple, no dependencies)
python -m http.server 3000 --directory frontend/public

# Node.js (better performance)
npm install -g http-server
http-server frontend/public -p 3000

# Flask (with Python)
pip install flask
python frontend/server.py

# Access at http://localhost:3000
```

### Parallel with Backend
```bash
# Terminal 1: Backend (port 8000)
python -m uvicorn backend.fastapi_app.main:app --reload --port 8000

# Terminal 2: Frontend (port 3000)
python -m http.server 3000 --directory frontend/public

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/v1
# Swagger UI: http://localhost:8000/docs
```

---

## 🎨 CSS File Organization

### design-system.css (1000+ lines)
```
├─ CSS Custom Properties (Colors, Typography, Spacing, Shadows, etc)
├─ Global Styles (Reset, body, headings, links, paragraphs)
├─ Typography (h1-h6, p, small, links, utilities)
├─ Utility Classes (Spacing, Display, Flexbox, Text, Visibility)
└─ Basic Components (btn, form, card, alert, badge, table, grid)
```

### components.css (1200+ lines)
```
├─ Header (sticky nav, branding, navigation)
├─ Sections (hero, section-hero, section-alt)
├─ Tabs (tab navigation and content)
├─ Forms (form-row, search-form, input enhancements)
├─ Results (result-item, result-info, result-footer)
├─ Map (map-container, map-canvas, map-legend)
├─ Statistics (stat-card, table-wrapper)
├─ Footer (multi-section, links, bottom)
├─ Loading (loading-overlay, spinner)
├─ Toast (toast-container, toast variants, animations)
└─ Info Lists (info-list items, borders, spacing)
```

### pages/home.css (800+ lines)
```
├─ Layout (body flex, main-content)
├─ Responsive Containers (media queries for grid layout)
├─ Forms (form-row, input appearance, select styling)
├─ Results Section (empty states, animations)
├─ Coordinates (coordinates display, badges)
├─ Geolocation (status indicators)
├─ Table Responsive (mobile card layout)
├─ Hero Responsive (font size, button layout)
├─ Section Responsive (padding, margins)
├─ Accessibility (skip links, focus-visible)
├─ Print Styles (print layout)
├─ Animations (fadeIn, slideDown, pulse)
└─ States (loading, error, success, disabled)
```

---

## 🧩 Component Classes Reference

### Buttons
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-outline">Outline</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-success">Success</button>

<!-- Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-lg">Large</button>

<!-- States -->
<button class="btn btn-primary btn-block">Full width</button>
<button class="btn btn-primary btn-icon">⚙️</button>
<button class="btn btn-primary" disabled>Disabled</button>
```

### Forms
```html
<div class="form-group">
  <label for="field">Label</label>
  <input type="text" id="field" placeholder="...">
</div>

<!-- Two columns -->
<div class="form-row">
  <div class="form-group">...</div>
  <div class="form-group">...</div>
</div>

<!-- Select with custom arrow -->
<select id="nil-select">
  <option value="">-- Scegli --</option>
  <option value="1">NIL 1</option>
</select>
```

### Cards
```html
<div class="card">
  <div class="card-header">
    <h3>Title</h3>
  </div>
  <div class="card-body">
    Content here...
  </div>
  <div class="card-footer">
    Footer...
  </div>
</div>

<!-- Compact variant -->
<div class="card card-compact">...</div>
```

### Alerts
```html
<div class="alert alert-info">
  <div class="alert-icon">ℹ️</div>
  <div class="alert-content">
    <div class="alert-title">Title</div>
    <div class="alert-message">Message</div>
  </div>
</div>

<!-- Variants: alert-success, alert-warning, alert-error -->
```

### Badges
```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-danger">Danger</span>

<!-- Density levels (for choropleth) -->
<span class="badge badge-density-very-low">Very Low</span>
<span class="badge badge-density-high">High</span>
```

### Tables
```html
<div class="table-wrapper">
  <table class="table">
    <thead>
      <tr>
        <th>Header</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td data-label="Header">Data</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Compact variant -->
<table class="table table-compact">...</table>
```

### Tabs
```html
<div class="tabs">
  <button class="tab-btn active" data-tab="tab-1">Tab 1</button>
  <button class="tab-btn" data-tab="tab-2">Tab 2</button>
</div>

<div class="tabs-content">
  <div class="tab-content active" id="tab-1">Content 1</div>
  <div class="tab-content" id="tab-2">Content 2</div>
</div>
```

### Empty State
```html
<div class="empty-state">
  <div class="empty-icon">🔍</div>
  <div class="empty-title">No Results</div>
  <div class="empty-message">Try different search terms</div>
</div>
```

### Loading
```html
<!-- Overlay -->
<div id="loading-overlay" class="loading-overlay hidden">
  <div class="spinner"></div>
  <p>Loading...</p>
</div>

<!-- Inline -->
<div class="loading">
  <div class="spinner"></div>
  <span>Loading...</span>
</div>
```

### Toast
```html
<div id="toast-container" class="toast-container">
  <!-- Toasts appended here -->
</div>

<!-- Toast structure (created by JS) -->
<div class="toast toast-success">
  <span>Message</span>
  <button class="toast-close">✕</button>
</div>
```

---

## 🌍 CSS Custom Properties (Design Tokens)

### Colors
```css
--color-primary: #2563eb
--color-secondary: #10b981
--color-danger: #ef4444
--color-warning: #f59e0b
--color-info: #3b82f6

--color-neutral-50: #f9fafb
--color-neutral-100: #f3f4f6
--color-neutral-200: #e5e7eb
--color-neutral-400: #9ca3af
--color-neutral-600: #4b5563
--color-neutral-700: #374151
--color-neutral-900: #111827

--color-background: #ffffff
--color-surface: #f9fafb
--color-border: #e5e7eb
--color-text: #1f2937
--color-text-secondary: #6b7280
```

### Typography
```css
--font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', ...
--font-family-mono: 'Monaco', 'Menlo', ...

--font-size-xs: 0.75rem
--font-size-sm: 0.875rem
--font-size-base: 1rem
--font-size-lg: 1.125rem
--font-size-xl: 1.25rem
--font-size-2xl: 1.5rem
--font-size-3xl: 1.875rem
--font-size-4xl: 2.25rem

--font-weight-regular: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700
```

### Spacing
```css
--spacing-1: 0.25rem (4px)
--spacing-2: 0.5rem (8px)
--spacing-3: 0.75rem (12px)
--spacing-4: 1rem (16px)
--spacing-6: 1.5rem (24px)
--spacing-8: 2rem (32px)
--spacing-12: 3rem (48px)
--spacing-20: 5rem (80px)
```

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1)
```

### Radius
```css
--radius-lg: 0.5rem (8px)
--radius-xl: 0.75rem (12px)
--radius-full: 9999px
```

---

## 🎯 Utility Classes Cheat Sheet

### Spacing (margin/padding)
```
mt-1, mt-2, mt-4, mt-6, mt-8      margin-top
mb-1, mb-2, mb-4, mb-6, mb-8      margin-bottom
p-2, p-4, p-6                      padding
px-4                               padding-left/right
py-2, py-4                         padding-top/bottom
```

### Display
```
d-flex                             display: flex
d-grid                             display: grid
d-block                            display: block
d-none                             display: none
hidden                             display: none
```

### Flexbox
```
flex-row                           flex-direction: row
flex-col                           flex-direction: column
flex-center                        center items
flex-between                       space-between
flex-wrap                          flex-wrap: wrap
gap-2, gap-4, gap-6               gap between items
```

### Grid
```
grid                               display: grid
grid-cols-1, 2, 3, 4              grid-template-columns
grid-cols-2-md                     2 cols on tablet+
```

### Text
```
text-center, text-left, text-right text-align
text-muted                         color: #9ca3af
text-secondary                     color: #6b7280
text-xs, text-sm                   font-size
font-medium, semibold, bold        font-weight
```

### Visibility
```
hidden                             display: none
visible                            display: block
sr-only                            screen reader only
hide-mobile                        hide on mobile
show-mobile                        show only on mobile
```

---

## 📱 Responsive Breakpoints

```css
/* Mobile < 640px */
@media (max-width: 640px) {
  /* Single column, full-width */
}

/* Tablet 640px - 768px */
@media (min-width: 641px) and (max-width: 768px) {
  /* Two columns, flexible */
}

/* Desktop > 768px */
@media (min-width: 769px) {
  /* Full grid layout */
}
```

---

## 🎨 Color Swatches

| Color | Value | Usage |
|-------|-------|-------|
| Primary | `#2563eb` | Buttons, links, focus |
| Primary Dark | `#1e40af` | Hover states |
| Primary 50 | `#eff6ff` | Light backgrounds |
| Secondary | `#10b981` | Success, confirmations |
| Danger | `#ef4444` | Errors, delete |
| Warning | `#f59e0b` | Cautions, alerts |
| Surface | `#f9fafb` | Alt backgrounds |
| Border | `#e5e7eb` | Dividers |
| Text | `#1f2937` | Primary text |
| Muted | `#9ca3af` | Secondary text |

---

## ⚡ Performance Tips

1. **CSS:** Only 3 files, ~4000 lines total
2. **Minify:** Remove unused CSS before production
3. **Caching:** Configure browser caching for static files
4. **Images:** Optimize images for web
5. **Lazy Load:** Load map/heavy components on demand

---

## 🧪 Testing Checklist

### Desktop
- [ ] Chrome/Firefox/Safari/Edge
- [ ] All buttons clickable
- [ ] Forms submit
- [ ] Hover effects work

### Mobile
- [ ] iPhone SE (small)
- [ ] iPhone 12 (medium)
- [ ] iPad (tablet)
- [ ] Android

### Features
- [ ] Responsive layout
- [ ] Touch interactions
- [ ] Keyboard navigation
- [ ] Screen reader compatible
- [ ] Print layout works

---

## 📚 Documentation Links

| Document | Purpose |
|----------|---------|
| `README.md` | Overview & quick start |
| `FRONTEND_DESIGN_SYSTEM.md` | Design tokens & components |
| `JS_IMPLEMENTATION_GUIDE.md` | JavaScript development |
| `ARCHITECTURE_SUMMARY.md` | Architecture & structure |
| `SERVER_CONFIGURATION.md` | Server setup & deployment |

---

## 🆘 Troubleshooting

### Issue: Styles not loading
```
✓ Check CSS files in public/css/
✓ Verify <link> paths in index.html
✓ Check browser Network tab for 404s
✓ Clear browser cache
```

### Issue: Form inputs not styled
```
✓ Check form-group wrapper
✓ Verify label has id/for attributes
✓ Ensure input has name attribute
```

### Issue: Responsive not working
```
✓ Check viewport meta tag in HTML
✓ Verify media queries in CSS
✓ Check breakpoint pixel values
✓ Test with browser dev tools
```

---

## 📞 Contact & Support

For questions about specific areas:
- **Design System** → See `FRONTEND_DESIGN_SYSTEM.md`
- **JavaScript** → See `JS_IMPLEMENTATION_GUIDE.md`
- **Architecture** → See `ARCHITECTURE_SUMMARY.md`
- **Server Setup** → See `SERVER_CONFIGURATION.md`

---

**Last Updated:** 2026-04-15 | **Status:** ✅ COMPLETE
