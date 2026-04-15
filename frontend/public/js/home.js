/**
 * Home Page Logic - Fontanelle Milano
 * Gestisce tutte le interazioni della pagina principale
 */

class HomePage {
  constructor() {
    this.loadingOverlay = document.getElementById('loading-overlay');
    this.nilDropdown = document.getElementById('nil-select');
    this.formSearchNil = document.getElementById('form-search-nil');
    this.formSearchNearby = document.getElementById('form-search-nearby');
    this.formSearchAdvanced = document.getElementById('form-search-advanced');
    this.btnGeolocation = document.getElementById('btn-use-geolocation');
    this.statisticsTable = document.getElementById('statistics-tbody');

    this.nilsList = []; // Cache NIL list
    this.currentSearchResults = null;
    this.currentStatistics = null;

    this.init();
  }

  /**
   * Inizializza la pagina
   */
  async init() {
    try {
      // Carica lista NIL
      await this.loadNilList();

      // Carica statistiche iniziali
      await this.loadStatistics();

      // Setup event listeners
      this.setupEventListeners();

      toast.success('Applicazione caricata');
    } catch (error) {
      console.error('Error initializing page:', error);
      toast.error('Errore nel caricamento della pagina');
    }
  }

  /**
   * Carica lista NIL dal file JSON
   */
  async loadNilList() {
    try {
      const response = await fetch('/data/nils.json');
      if (!response.ok) throw new Error('Failed to load NILs');

      this.nilsList = await response.json();
      this.populateNilDropdown();
    } catch (error) {
      console.error('Error loading NIL list:', error);
      toast.warning('Impossibile caricare lista dei NIL');
    }
  }

  /**
   * Popola il dropdown dei NIL
   */
  populateNilDropdown() {
    this.nilDropdown.innerHTML = '<option value="">-- Scegli un NIL --</option>';

    this.nilsList.forEach(nil => {
      const option = document.createElement('option');
      option.value = nil.id;
      option.textContent = `${nil.nome} (${nil.id})`;
      this.nilDropdown.appendChild(option);
    });
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Form NIL
    if (this.formSearchNil) {
      this.formSearchNil.addEventListener('submit', (e) => this.handleSearchNil(e));
    }

    // Form Nearby
    if (this.formSearchNearby) {
      this.formSearchNearby.addEventListener('submit', (e) => this.handleSearchNearby(e));
    }

    // Button Geolocation
    if (this.btnGeolocation) {
      this.btnGeolocation.addEventListener('click', () => this.handleGeolocation());
    }

    // Form Advanced
    if (this.formSearchAdvanced) {
      this.formSearchAdvanced.addEventListener('submit', (e) => this.handleSearchAdvanced(e));
    }
  }

  /**
   * Gestisci ricerca per NIL
   */
  async handleSearchNil(event) {
    event.preventDefault();

    const formData = new FormData(this.formSearchNil);
    const nilId = formData.get('nil_id');
    const pageSize = parseInt(formData.get('page_size') || 10);

    if (!nilId) {
      toast.warning('Seleziona un NIL');
      return;
    }

    this.showLoading();

    try {
      const results = await ApiClient.searchByNil(nilId, pageSize);
      this.currentSearchResults = results;
      this.renderNilResults(results);
      toast.success(`${results.total} fontanelle trovate`);
    } catch (error) {
      console.error('Error searching by NIL:', error);
      toast.error('Errore nella ricerca');
      this.renderErrorResults('tab-search-nil');
    } finally {
      this.hideLoading();
    }
  }

  /**
   * Gestisci ricerca per posizione
   */
  async handleSearchNearby(event) {
    event.preventDefault();

    const formData = new FormData(this.formSearchNearby);
    const latitude = parseFloat(formData.get('latitude'));
    const longitude = parseFloat(formData.get('longitude'));
    const radius = parseInt(formData.get('radius') || 500);
    const pageSize = parseInt(formData.get('page_size') || 10);

    if (!latitude || !longitude) {
      toast.warning('Inserisci coordinate valide');
      return;
    }

    if (radius < 100 || radius > 5000) {
      toast.warning('Raggio deve essere tra 100 e 5000 metri');
      return;
    }

    this.showLoading();

    try {
      const results = await ApiClient.searchNearby(latitude, longitude, radius, pageSize);
      this.currentSearchResults = results;
      this.renderNearbyResults(results);
      toast.success(`${results.total} fontanelle trovate entro ${radius}m`);
    } catch (error) {
      console.error('Error searching nearby:', error);
      toast.error('Errore nella ricerca');
      this.renderErrorResults('tab-search-nearby');
    } finally {
      this.hideLoading();
    }
  }

  /**
   * Gestisci ricerca con filtri avanzati
   */
  async handleSearchAdvanced(event) {
    event.preventDefault();

    const formData = new FormData(this.formSearchAdvanced);
    const filters = {
      municipio: formData.get('municipio'),
      cap: formData.get('cap'),
    };
    const pageSize = parseInt(formData.get('page_size') || 10);

    if (!filters.municipio && !filters.cap) {
      toast.warning('Inserisci almeno un filtro');
      return;
    }

    this.showLoading();

    try {
      const results = await ApiClient.searchAdvanced(filters, pageSize);
      this.currentSearchResults = results;
      this.renderAdvancedResults(results);
      toast.success(`${results.total} fontanelle trovate`);
    } catch (error) {
      console.error('Error searching advanced:', error);
      toast.error('Errore nella ricerca');
      this.renderErrorResults('tab-search-advanced');
    } finally {
      this.hideLoading();
    }
  }

  /**
   * Gestisci geolocalizzazione
   */
  handleGeolocation() {
    if (!navigator.geolocation) {
      toast.error('Geolocalizzazione non supportata dal browser');
      return;
    }

    this.showLoading();
    this.btnGeolocation.disabled = true;

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const accuracy = position.coords.accuracy;

        document.getElementById('lat-input').value = lat.toFixed(6);
        document.getElementById('lon-input').value = lon.toFixed(6);

        toast.success(`Posizione trovata (precisione: ±${Math.round(accuracy)}m)`);
        this.hideLoading();
        this.btnGeolocation.disabled = false;
      },
      (error) => {
        let message = 'Errore nella geolocalizzazione';
        switch (error.code) {
          case error.PERMISSION_DENIED:
            message = 'Permesso di geolocalizzazione negato';
            break;
          case error.POSITION_UNAVAILABLE:
            message = 'Posizione non disponibile';
            break;
          case error.TIMEOUT:
            message = 'Timeout nella geolocalizzazione';
            break;
        }
        toast.error(message);
        this.hideLoading();
        this.btnGeolocation.disabled = false;
      }
    );
  }

  /**
   * Renderizza risultati ricerca per NIL
   */
  renderNilResults(results) {
    const container = document.getElementById('results-nil');

    if (!results.fountains || results.fountains.length === 0) {
      container.innerHTML = this.getEmptyResultsHtml('Nessuna fontanella trovata');
      return;
    }

    let html = `
      <div class="results-summary">
        <p><strong>Totale:</strong> ${results.total} fontanelle | <strong>Visualizzate:</strong> ${results.fountains.length}</p>
      </div>
      <div class="results-list">
    `;

    results.fountains.forEach(fountain => {
      html += this.getResultItemHtml(fountain);
    });

    html += '</div>';
    container.innerHTML = html;
    this.updateMapResults(results.fountains);
  }

  /**
   * Renderizza risultati ricerca per posizione
   */
  renderNearbyResults(results) {
    const container = document.getElementById('results-nearby');

    if (!results.fountains || results.fountains.length === 0) {
      container.innerHTML = this.getEmptyResultsHtml('Nessuna fontanella trovata in questa area');
      return;
    }

    let html = `
      <div class="results-summary">
        <p><strong>Totale:</strong> ${results.total} fontanelle | <strong>Visualizzate:</strong> ${results.fountains.length}</p>
      </div>
      <div class="results-list">
    `;

    results.fountains.forEach(fountain => {
      const distance = fountain.distance ? ` (${(fountain.distance / 1000).toFixed(2)} km)` : '';
      const html_item = this.getResultItemHtml(fountain);
      // Aggiungi distanza al risultato se disponibile
      html += html_item.replace('</div></div>', `<div class="result-distance">${distance}</div></div></div>`);
    });

    html += '</div>';
    container.innerHTML = html;
    this.updateMapResults(results.fountains);
  }

  /**
   * Renderizza risultati ricerca avanzata
   */
  renderAdvancedResults(results) {
    const container = document.getElementById('results-advanced');

    if (!results.fountains || results.fountains.length === 0) {
      container.innerHTML = this.getEmptyResultsHtml('Nessuna fontanella trovata con questi filtri');
      return;
    }

    let html = `
      <div class="results-summary">
        <p><strong>Totale:</strong> ${results.total} fontanelle | <strong>Visualizzate:</strong> ${results.fountains.length}</p>
      </div>
      <div class="results-list">
    `;

    results.fountains.forEach(fountain => {
      html += this.getResultItemHtml(fountain);
    });

    html += '</div>';
    container.innerHTML = html;
    this.updateMapResults(results.fountains);
  }

  /**
   * HTML di un singolo risultato
   */
  getResultItemHtml(fountain) {
    return `
      <div class="result-item">
        <div class="result-header">
          <div class="result-title">${this.escapeHtml(fountain.indirizzo || 'Fontanella')}</div>
          <div class="result-nil-badge">${this.escapeHtml(fountain.nil || 'N/A')}</div>
        </div>
        <div class="result-details">
          <div class="detail-row">
            <span class="detail-label">CAP:</span>
            <span class="detail-value">${this.escapeHtml(fountain.cap || 'N/A')}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Municipio:</span>
            <span class="detail-value">${this.escapeHtml(fountain.municipio || 'N/A')}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Coordinate:</span>
            <span class="detail-value">${fountain.latitude?.toFixed(6) || 'N/A'}, ${fountain.longitude?.toFixed(6) || 'N/A'}</span>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * HTML per risultati vuoti
   */
  getEmptyResultsHtml(message) {
    return `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <div class="empty-title">Nessun risultato</div>
        <div class="empty-message">${this.escapeHtml(message)}</div>
      </div>
    `;
  }

  /**
   * HTML per errore
   */
  renderErrorResults(tabId) {
    const containerId = `results-${tabId.split('-')[2]}`;
    const container = document.getElementById(containerId);
    container.innerHTML = `
      <div class="alert alert-error">
        <strong>Errore:</strong> Impossibile effettuare la ricerca. Riprova più tardi.
      </div>
    `;
  }

  /**
   * Aggiorna la mappa con i risultati
   */
  updateMapResults(fountains) {
    try {
      const mapCanvas = document.getElementById('map-canvas');
      
      // Se non ci sono fontanelle, mostra messaggio
      if (!fountains || fountains.length === 0) {
        mapCanvas.innerHTML = `
          <div class="map-empty">
            <p>Nessuna fontanella da visualizzare</p>
          </div>
        `;
        return;
      }

      // Crea/pulisci container mappa
      mapCanvas.innerHTML = `
        <div id="leaflet-map" style="width: 100%; height: 100%; border-radius: var(--radius-xl);"></div>
      `;

      // Inizializza Leaflet map
      const mapElement = document.getElementById('leaflet-map');
      
      // Calcola bounds dalle fontanelle
      let minLat = Infinity, maxLat = -Infinity;
      let minLon = Infinity, maxLon = -Infinity;
      
      fountains.forEach(f => {
        if (f.coordinate) {
          const lat = f.coordinate.latitude || f.coordinate.lat;
          const lon = f.coordinate.longitude || f.coordinate.lon;
          if (lat && lon) {
            minLat = Math.min(minLat, lat);
            maxLat = Math.max(maxLat, lat);
            minLon = Math.min(minLon, lon);
            maxLon = Math.max(maxLon, lon);
          }
        }
      });

      // Fallback to Milano if no valid coordinates
      if (!isFinite(minLat)) {
        minLat = maxLat = 45.4642;
        minLon = maxLon = 9.1900;
      }

      // Crea mappa Leaflet
      const map = L.map(mapElement).fitBounds(
        [[minLat, minLon], [maxLat, maxLon]],
        { padding: [50, 50] }
      );

      // Aggiungi tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(map);

      // Aggiungi marker per ogni fontanella
      fountains.forEach((fountain, index) => {
        try {
          const lat = fountain.coordinate?.latitude || fountain.coordinate?.lat;
          const lon = fountain.coordinate?.longitude || fountain.coordinate?.lon;
          
          if (lat && lon) {
            const marker = L.marker([lat, lon], {
              title: fountain.indirizzo || fountain.name || `Fontanella ${index + 1}`,
            }).addTo(map);

            // Popup con informazioni
            const popupContent = `
              <div class="map-popup">
                <strong>${this.escapeHtml(fountain.indirizzo || fountain.name || 'Fontanella')}</strong><br>
                <small>
                  NIL: ${this.escapeHtml(String(fountain.nil || 'N/A'))}<br>
                  CAP: ${this.escapeHtml(fountain.cap || 'N/A')}<br>
                  Municipio: ${this.escapeHtml(fountain.municipio || 'N/A')}<br>
                  Lat: ${lat.toFixed(4)}, Lon: ${lon.toFixed(4)}
                </small>
              </div>
            `;
            
            marker.bindPopup(popupContent);
          }
        } catch (e) {
          console.warn('Error adding marker:', e);
        }
      });

      // Aggiungi legenda
      const legend = L.control({ position: 'bottomright' });
      legend.onAdd = function() {
        const div = L.DomUtil.create('div', 'map-legend');
        div.innerHTML = `
          <div style="background: white; padding: 10px; border-radius: 5px; box-shadow: 0 0 15px rgba(0,0,0,0.2);">
            <p style="margin: 0 0 5px 0; font-weight: bold;">Fontanelle: ${fountains.length}</p>
            <small>Clicca su un marker per dettagli</small>
          </div>
        `;
        return div;
      };
      legend.addTo(map);

    } catch (error) {
      console.error('Error updating map:', error);
      const mapCanvas = document.getElementById('map-canvas');
      mapCanvas.innerHTML = `
        <div class="map-error">
          <p>Errore nel caricamento della mappa</p>
          <small>${error.message}</small>
        </div>
      `;
    }
  }

  /**
   * Carica e renderizza statistiche
   */
  async loadStatistics() {
    try {
      const stats = await ApiClient.getStatistics();
      this.currentStatistics = stats;
      this.renderStatistics(stats);
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  }

  /**
   * Renderizza statistiche
   */
  renderStatistics(stats) {
    try {
      // Aggiorna stat cards
      const totalFountains = stats.total_fountains || 0;
      const totalNils = stats.statistics ? stats.statistics.length : 0;
      const avgDensity = stats.max_density && stats.min_density 
        ? ((stats.max_density + stats.min_density) / 2).toFixed(1) 
        : '---';

      document.getElementById('stat-total-fountains').textContent = totalFountains;
      document.getElementById('stat-total-nils').textContent = totalNils;
      document.getElementById('stat-avg-density').textContent = avgDensity;

      // Aggiorna tabella statistiche
      if (stats.statistics && this.statisticsTable) {
        this.statisticsTable.innerHTML = '';

        stats.statistics.forEach(nil => {
          const tr = document.createElement('tr');
          const density = nil.density_fountains_per_km2 || 0;
          const category = this.getDensityCategory(density);

          tr.innerHTML = `
            <td><strong>${this.escapeHtml(String(nil.nil_id))}</strong></td>
            <td>${this.escapeHtml(nil.nil_name || 'N/A')}</td>
            <td>${nil.fountain_count || 0}</td>
            <td>${parseFloat(density).toFixed(2)}</td>
            <td><span class="badge badge-${category}">${category}</span></td>
          `;
          this.statisticsTable.appendChild(tr);
        });
      }
    } catch (error) {
      console.error('Error rendering statistics:', error);
      if (this.statisticsTable) {
        this.statisticsTable.innerHTML = '<tr><td colspan="5">Errore nel caricamento statistiche</td></tr>';
      }
    }
  }

  /**
   * Ottieni categoria densità
   */
  getDensityCategory(density) {
    if (density < 1) return 'very-low';
    if (density < 3) return 'low';
    if (density < 5) return 'medium';
    if (density < 7) return 'high';
    return 'very-high';
  }

  /**
   * Mostra loading overlay
   */
  showLoading() {
    if (this.loadingOverlay) {
      this.loadingOverlay.classList.remove('hidden');
    }
  }

  /**
   * Nascondi loading overlay
   */
  hideLoading() {
    if (this.loadingOverlay) {
      this.loadingOverlay.classList.add('hidden');
    }
  }

  /**
   * Escape HTML per prevenire XSS
   */
  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Istanza globale
let homePage;

// Inizializza quando DOM è pronto
document.addEventListener('DOMContentLoaded', () => {
  homePage = new HomePage();
});
