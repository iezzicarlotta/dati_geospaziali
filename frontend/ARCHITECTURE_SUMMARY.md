# Frontend Architecture Summary

## 🎯 Quick Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FONTANELLE MILANO WEB APP                    │
│                    Frontend Architecture                         │
└─────────────────────────────────────────────────────────────────┘

┌─ HTML STRUCTURE ──────────────────────────────────────────────┐
│                                                                 │
│  index.html (Semantic, semantic HTML5, ARIA roles)            │
│  ├── Header (sticky nav)                                       │
│  ├── Hero Section                                              │
│  ├── Search Section (3 tabs)                                   │
│  ├── Map Section                                               │
│  ├── Statistics Section                                        │
│  ├── About Section                                             │
│  └── Footer                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────┘

┌─ CSS LAYERS ──────────────────────────────────────────────────┐
│                                                                 │
│  1. design-system.css       (CSS custom properties)            │
│     └─ Colors, Typography, Spacing, Shadows                   │
│                                                                 │
│  2. components.css          (Component styles)                 │
│     ├─ Header, Nav, Sections                                   │
│     ├─ Tabs, Forms, Cards, Alerts                              │
│     ├─ Buttons, Badges, Tables                                 │
│     ├─ Map, Statistics, Footer                                 │
│     └─ Loading, Toast, Info lists                              │
│                                                                 │
│  3. pages/home.css          (Page-specific styles)             │
│     ├─ Responsive breakpoints                                  │
│     ├─ Form layouts                                            │
│     ├─ Result rendering                                        │
│     ├─ Accessibility enhancements                              │
│     └─ Print styles                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────┘

┌─ JAVASCRIPT MODULES ──────────────────────────────────────────┐
│                                                                 │
│  utils/                                                         │
│  ├─ api-client.js          (API request wrapper)               │
│  │  └─ Centralized HTTP client, error handling                │
│  │                                                              │
│  └─ toast.js               (Toast notifications)               │
│     └─ Success, error, warning, info toasts                   │
│                                                                 │
│  components/                                                    │
│  └─ tabs.js                (Tab switcher component)            │
│     └─ Tab navigation logic, state management                 │
│                                                                 │
│  pages/                                                         │
│  └─ home.js                (Home page main logic)              │
│     ├─ Form handling                                           │
│     ├─ API integration                                         │
│     ├─ Results rendering                                       │
│     ├─ Statistics loading                                      │
│     ├─ Geolocation                                             │
│     └─ Pagination                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────┘

┌─ API ENDPOINTS (Backend) ──────────────────────────────────────┐
│                                                                 │
│  POST   /fountains/search/by-nil           (NIL search)       │
│  GET    /fountains/nils/dropdown           (NIL options)      │
│  POST   /fountains/search/nearby           (Location search)   │
│  POST   /fountains/search/advanced         (Filter search)    │
│  GET    /fountains/statistics/nils         (Stats)            │
│  GET    /fountains/choropleth              (Choropleth data)  │
│  GET    /fountains/health                  (Health check)     │
│                                                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Component Hierarchy

```
┌─ HEADER (sticky) ────────────────────┐
│  ├─ Logo + Tagline                   │
│  └─ Navigation (Mappa, Ricerca, etc) │
└──────────────────────────────────────┘
         ↓
┌─ HERO SECTION ──────────────────────┐
│  ├─ Title                            │
│  ├─ Subtitle                         │
│  └─ CTA Buttons                      │
└──────────────────────────────────────┘
         ↓
┌─ SEARCH SECTION ────────────────────┐
│  ├─ Tabs (3 types)                   │
│  │  ├─ Tab 1: By NIL                │
│  │  ├─ Tab 2: By Location            │
│  │  └─ Tab 3: Advanced Filters       │
│  ├─ Forms                            │
│  └─ Results Container                │
└──────────────────────────────────────┘
         ↓
┌─ MAP SECTION ───────────────────────┐
│  ├─ Interactive Map                  │
│  └─ Density Legend                   │
└──────────────────────────────────────┘
         ↓
┌─ STATISTICS SECTION ────────────────┐
│  ├─ 3 Stat Cards                     │
│  ├─ Statistics Table                 │
│  └─ Pagination                       │
└──────────────────────────────────────┘
         ↓
┌─ ABOUT SECTION ─────────────────────┐
│  ├─ Project Info                     │
│  ├─ Data Sources                     │
│  └─ Usage Instructions               │
└──────────────────────────────────────┘
         ↓
┌─ FOOTER ────────────────────────────┐
│  ├─ Branding                         │
│  ├─ Quick Links                      │
│  └─ Resources                        │
└──────────────────────────────────────┘
```

---

## 🎨 Design Token Categories

### 1. **Colors**
- Primary (Blue): `#2563eb`
- Secondary (Green): `#10b981`
- Danger (Red): `#ef4444`
- Neutral palette (9 levels)
- Choropleth colors (5 density levels)

### 2. **Typography**
- Family: System stack (San Francisco, Segoe UI, etc)
- Sizes: 7 scale levels (12px → 36px)
- Weights: 4 levels (400 → 700)
- Line heights: 3 levels (1.2 → 1.75)

### 3. **Spacing**
- Base unit: 8px
- Scale: 12 levels (4px → 96px)
- Applied to margins, padding, gaps

### 4. **Radius**
- 6 levels: 0, 4px, 6px, 8px, 12px, 16px, full

### 5. **Shadows**
- 5 levels from subtle to prominent
- Used for depth and emphasis

### 6. **Transitions**
- Fast: 150ms
- Base: 200ms
- Slow: 300ms

---

## 📱 Responsive Breakpoints

```
Mobile     ─────────────────────┐
(< 640px)  Single column layout │
           Full-width inputs    │
           Card-style tables    │
                              ↓
Tablet     ─────────────────────┐
(640-768)  2 column grid        │
           Form rows: 2 cols    │
           Hamburger nav        │
                              ↓
Desktop    ─────────────────────┐
(768px+)   3-4 column grid      │
           Full navigation      │
           Side-by-side layouts │
```

---

## 🧩 Reusable Components

### Buttons
- Primary, Secondary, Outline, Danger, Success
- Sizes: sm, normal, lg
- States: normal, hover, active, disabled, loading

### Forms
- Text, number, select, textarea inputs
- Form groups with labels
- Form rows (multi-column layouts)
- Validation feedback

### Cards
- Header, body, footer sections
- Hover effects
- Compact variant

### Alerts
- Info, Success, Warning, Error
- Icon + title + message
- Dismissible

### Badges
- Color variants
- Density levels (for choropleth)
- Inline or block display

### Tables
- Sticky headers
- Hover rows
- Responsive (card layout on mobile)
- Pagination support

---

## 🔄 Data Flow

```
┌─────────────┐
│  User Input │  Form submission / Button click / Geolocation
└──────┬──────┘
       │
       ↓
┌─────────────────────────────────────┐
│  Validation & Data Collection       │  Check input values
└──────┬──────────────────────────────┘
       │
       ↓
┌─────────────────────────────────────┐
│  Show Loading Overlay               │  Visual feedback
└──────┬──────────────────────────────┘
       │
       ↓
┌─────────────────────────────────────┐
│  API Request (api-client.js)        │  POST/GET to backend
└──────┬──────────────────────────────┘
       │
       ├─→ Success → Parse Response → Update DOM
       │               ↓
       │            Render Results
       │            Show Toast (success)
       │
       └─→ Error → Show Toast (error) → User can retry
       │
       ↓
┌─────────────────────────────────────┐
│  Hide Loading Overlay               │  Remove visual feedback
└─────────────────────────────────────┘
```

---

## 🎯 User Flows

### Search by NIL
```
User clicks tab → Dropdown loads → User selects NIL → Submits
                  ↓
            Results render with pagination
                  ↓
            User can page through results
```

### Search by Location
```
User clicks tab → Enters coordinates (or uses geolocation)
                  ↓
            Sets radius, page size → Submits
                  ↓
            Results render with distance from query point
                  ↓
            Each result shows distance badge
```

### Advanced Search
```
User clicks tab → Enters Municipio/CAP → Submits
                  ↓
            Results render filtered by parameters
                  ↓
            User can refine filters and search again
```

### Statistics
```
Page loads → Statistics auto-load
                  ↓
            Stat cards populate (total, count, avg density)
                  ↓
            Table loads with all NILs
                  ↓
            Density badges color-coded
                  ↓
            User can sort, filter, paginate (future)
```

---

## 🎨 CSS Utility Class Reference

### Spacing
```
mt-1, mt-2, mt-4, mt-6, mt-8      (margin-top)
mb-1, mb-2, mb-4, mb-6, mb-8      (margin-bottom)
p-2, p-4, p-6                      (padding all sides)
px-4                               (padding left-right)
py-2, py-4                         (padding top-bottom)
```

### Layout
```
d-flex                             (display: flex)
d-grid                             (display: grid)
d-block, d-inline                  (display: block/inline)
flex-row, flex-col                 (flex direction)
flex-center                        (centered flex)
flex-between                       (space-between flex)
gap-2, gap-4, gap-6                (flex gap)
```

### Grid
```
grid                               (display: grid)
grid-cols-1, grid-cols-2, etc      (grid columns)
grid-cols-2-md                     (2 cols on medium+)
grid-cols-3-md                     (3 cols on medium+)
```

### Text
```
text-center, text-left, text-right (text alignment)
text-muted, text-secondary         (text color)
font-medium, font-semibold, font-bold (font weight)
text-xs, text-sm                   (font size)
```

### Visibility
```
hidden                             (display: none)
visible                            (display: block)
sr-only                            (screen reader only)
hide-mobile                        (hidden on mobile)
show-mobile                        (visible on mobile only)
```

---

## 🧪 Component States

### Form Input States
- ✅ Normal
- 🔵 Focus (blue outline)
- ❌ Disabled (reduced opacity)
- ⚠️ Error (red border, error message)

### Button States
- ✅ Normal
- 🔵 Hover (darker shade)
- 🎯 Active (pressed look)
- ❌ Disabled (reduced opacity)
- ⏳ Loading (spinner, disabled)

### Result Item States
- ✅ Default
- 🔵 Hover (shadow increases)
- 🎯 Focus (focus outline)
- ⏳ Loading (opacity reduced)

### Tab States
- ✅ Inactive (gray text)
- 🔵 Active (blue text + underline)
- 🎯 Hover (lighter blue)

---

## 📝 File Checklist

### CSS Files ✅
- ✅ `design-system.css` (1000+ lines)
  - CSS variables for all design tokens
  - Global styles and resets
  - Typography system
  - Utility classes
  - Base component styles
  - Responsive breakpoints

- ✅ `components.css` (1200+ lines)
  - Header and navigation
  - Buttons (all variants)
  - Forms and inputs
  - Cards and alerts
  - Badges and tables
  - Tabs and results
  - Map and statistics
  - Footer
  - Loading and toasts

- ✅ `pages/home.css` (800+ lines)
  - Page layout structure
  - Responsive adjustments
  - Form-specific styles
  - Results rendering
  - Geolocation UI
  - Accessibility features
  - Print styles
  - Animations

### HTML Files ✅
- ✅ `index.html` (500+ lines)
  - Semantic HTML5 structure
  - Proper heading hierarchy
  - ARIA attributes
  - All page sections
  - Placeholder content
  - Script references

### Documentation ✅
- ✅ `FRONTEND_DESIGN_SYSTEM.md` (800+ lines)
  - Design tokens reference
  - Component documentation
  - Usage examples
  - Responsive guide
  - Naming conventions
  - Implementation checklist

- ✅ `JS_IMPLEMENTATION_GUIDE.md` (600+ lines)
  - JavaScript architecture
  - Module descriptions
  - Function signatures
  - Code examples
  - Error handling
  - Implementation roadmap

---

## 🚀 Getting Started

### 1. Static File Serving
```bash
# Copy CSS files to public/css/ directory
# Copy HTML to public/ directory
# Configure web server to serve from public/

# Example with Python:
# python -m http.server 3000 --directory frontend/public
```

### 2. HTML Integration
```html
<!DOCTYPE html>
<html lang="it">
<head>
  <link rel="stylesheet" href="/css/design-system.css">
  <link rel="stylesheet" href="/css/components.css">
  <link rel="stylesheet" href="/css/pages/home.css">
</head>
<body>
  <!-- Main content -->
  <script src="/js/utils/api-client.js"></script>
  <script src="/js/utils/toast.js"></script>
  <script src="/js/components/tabs.js"></script>
  <script src="/js/pages/home.js"></script>
</body>
</html>
```

### 3. Development Workflow
1. Modify CSS → Refresh browser (live reload)
2. Modify HTML → Refresh browser
3. Implement JS → Test in console
4. Add form handlers → Test submissions
5. Call API endpoints → Verify responses

### 4. Testing Checklist
- [ ] All pages responsive on mobile/tablet/desktop
- [ ] Form validation working
- [ ] API calls successful
- [ ] Results render correctly
- [ ] Toast notifications appear
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Performance acceptable

---

## 📊 File Statistics

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| design-system.css | ~50KB | 1000+ | Design tokens & globals |
| components.css | ~60KB | 1200+ | Component styles |
| pages/home.css | ~40KB | 800+ | Page-specific styles |
| index.html | ~25KB | 500+ | Main HTML page |
| FRONTEND_DESIGN_SYSTEM.md | ~80KB | 800+ | System documentation |
| JS_IMPLEMENTATION_GUIDE.md | ~70KB | 600+ | JS development guide |
| **TOTAL** | **~325KB** | **~4900+** | Complete frontend stack |

---

## ✨ Key Features

### Design System
- ✅ Professional color palette
- ✅ Comprehensive typography scale
- ✅ 8px base spacing system
- ✅ Consistent shadows and borders
- ✅ Smooth transitions

### Components
- ✅ 20+ reusable components
- ✅ Clear variant patterns
- ✅ Consistent styling
- ✅ Hover/active states
- ✅ Disabled states

### Accessibility
- ✅ Semantic HTML5
- ✅ ARIA roles and labels
- ✅ Keyboard navigation
- ✅ WCAG AA contrast ratios
- ✅ Screen reader support

### Responsiveness
- ✅ Mobile-first design
- ✅ Multiple breakpoints
- ✅ Flexible layouts
- ✅ Touch-friendly targets
- ✅ Responsive typography

### Developer Experience
- ✅ CSS custom properties
- ✅ Utility-first helpers
- ✅ Clear naming conventions
- ✅ Comprehensive documentation
- ✅ Easy to extend

---

## 🎯 Current Status

✅ **COMPLETE:**
- HTML structure (semantic, accessible)
- Design system (colors, typography, spacing)
- Component styles (forms, buttons, cards, etc)
- Page layout (header to footer)
- Responsive design (mobile to desktop)
- Documentation (2 comprehensive guides)

⏳ **PENDING:**
- JavaScript implementation (forms, API calls)
- Map library integration
- Advanced features (search history, favorites, etc)
- Testing and optimization

---

**Last Updated:** 2026-04-15
**Status:** ✅ Frontend structure and design system COMPLETE
**Next:** JavaScript implementation (see JS_IMPLEMENTATION_GUIDE.md)
