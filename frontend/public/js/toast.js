/**
 * Toast Notifications System
 * Gestisce le notifiche temporanee
 */

class ToastManager {
  constructor() {
    this.container = document.getElementById('toast-container');
    this.toasts = [];
  }

  /**
   * Mostra un toast
   * @param {string} message - Messaggio da mostrare
   * @param {string} type - Tipo (info, success, warning, error)
   * @param {number} duration - Durata in ms (0 = permanente)
   */
  show(message, type = 'info', duration = 3000) {
    const toastId = `toast-${Date.now()}`;
    const toastEl = document.createElement('div');
    toastEl.className = `toast toast-${type}`;
    toastEl.id = toastId;
    toastEl.setAttribute('role', 'alert');

    // Icon mapping
    const icons = {
      info: 'ℹ️',
      success: '✓',
      warning: '⚠️',
      error: '✕',
    };

    toastEl.innerHTML = `
      <div class="toast-content">
        <span class="toast-icon">${icons[type]}</span>
        <span class="toast-message">${this.escapeHtml(message)}</span>
        <button class="toast-close" aria-label="Chiudi notifica">×</button>
      </div>
    `;

    this.container.appendChild(toastEl);
    this.toasts.push(toastId);

    // Close button handler
    toastEl.querySelector('.toast-close').addEventListener('click', () => {
      this.remove(toastId);
    });

    // Auto-dismiss
    if (duration > 0) {
      setTimeout(() => {
        this.remove(toastId);
      }, duration);
    }

    return toastId;
  }

  /**
   * Rimuovi un toast
   * @param {string} toastId - ID del toast
   */
  remove(toastId) {
    const toastEl = document.getElementById(toastId);
    if (toastEl) {
      toastEl.classList.add('removing');
      setTimeout(() => {
        toastEl.remove();
        this.toasts = this.toasts.filter(id => id !== toastId);
      }, 300);
    }
  }

  /**
   * Mostra un toast di successo
   */
  success(message, duration = 3000) {
    return this.show(message, 'success', duration);
  }

  /**
   * Mostra un toast di errore
   */
  error(message, duration = 5000) {
    return this.show(message, 'error', duration);
  }

  /**
   * Mostra un toast di warning
   */
  warning(message, duration = 4000) {
    return this.show(message, 'warning', duration);
  }

  /**
   * Mostra un toast info
   */
  info(message, duration = 3000) {
    return this.show(message, 'info', duration);
  }

  /**
   * Rimuovi tutti i toasts
   */
  clearAll() {
    this.toasts.forEach(toastId => this.remove(toastId));
  }

  /**
   * Escape HTML per prevenire XSS
   */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Istanza globale
const toast = new ToastManager();
