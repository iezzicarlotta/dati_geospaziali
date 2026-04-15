/**
 * API Client - Fontanelle Milano
 * Gestisce le chiamate HTTP verso il backend
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiClient {
  /**
   * Ricerca fontanelle per NIL
   * @param {number} nilId - ID del NIL
   * @param {number} pageSize - Numero di risultati per pagina
   * @returns {Promise<Object>}
   */
  static async searchByNil(nilId, pageSize = 10) {
    try {
      const response = await fetch(`${API_BASE_URL}/fountains/search/by-nil`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nil_id: nilId,
          page: 1,
          page_size: pageSize,
        }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error in searchByNil:', error);
      throw error;
    }
  }

  /**
   * Ricerca fontanelle entro un raggio da un punto
   * @param {number} latitude - Latitudine
   * @param {number} longitude - Longitudine
   * @param {number} radius - Raggio in metri
   * @param {number} pageSize - Numero di risultati per pagina
   * @returns {Promise<Object>}
   */
  static async searchNearby(latitude, longitude, radius = 500, pageSize = 10) {
    try {
      const response = await fetch(`${API_BASE_URL}/fountains/search/nearby`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: latitude,
          longitude: longitude,
          radius_meters: radius,
          limit: pageSize,
        }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error in searchNearby:', error);
      throw error;
    }
  }

  /**
   * Ricerca fontanelle con filtri avanzati
   * @param {Object} filters - Filtri (municipio, cap)
   * @param {number} pageSize - Numero di risultati per pagina
   * @returns {Promise<Object>}
   */
  static async searchAdvanced(filters, pageSize = 10) {
    try {
      const response = await fetch(`${API_BASE_URL}/fountains/search/advanced`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nil_id: filters.nil_id || null,
          nil_name: filters.nil_name || null,
          municipio: filters.municipio || null,
          cap: filters.cap || null,
          page: 1,
          page_size: pageSize,
        }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error in searchAdvanced:', error);
      throw error;
    }
  }

  /**
   * Ottieni statistiche e dati choropleth
   * @returns {Promise<Object>}
   */
  static async getStatistics() {
    try {
      const response = await fetch(`${API_BASE_URL}/fountains/choropleth`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error in getStatistics:', error);
      throw error;
    }
  }

  /**
   * Ottieni health check
   * @returns {Promise<Object>}
   */
  static async getHealthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/fountains/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error in getHealthCheck:', error);
      throw error;
    }
  }

  /**
   * Health check
   * @returns {Promise<Object>}
   */
  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error in healthCheck:', error);
      throw error;
    }
  }
}
