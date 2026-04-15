/**
 * Tab Component - Gestione delle tab di ricerca
 */

class TabComponent {
  constructor() {
    this.tabBtns = document.querySelectorAll('.tab-btn');
    this.tabContents = document.querySelectorAll('.tab-content');
    this.init();
  }

  init() {
    this.tabBtns.forEach(btn => {
      btn.addEventListener('click', (e) => this.handleTabClick(e));
    });
  }

  /**
   * Gestisci click su un tab button
   */
  handleTabClick(event) {
    const btn = event.target;
    const tabId = btn.getAttribute('data-tab');

    if (!tabId) return;

    // Rimuovi active da tutti i button
    this.tabBtns.forEach(b => b.classList.remove('active'));

    // Rimuovi active da tutti i content
    this.tabContents.forEach(content => {
      content.classList.remove('active');
    });

    // Aggiungi active al button cliccato
    btn.classList.add('active');

    // Aggiungi active al content corrispondente
    const tabContent = document.getElementById(tabId);
    if (tabContent) {
      tabContent.classList.add('active');
    }
  }

  /**
   * Attiva un tab specifico
   * @param {string} tabId - ID del tab
   */
  activateTab(tabId) {
    const btn = document.querySelector(`[data-tab="${tabId}"]`);
    if (btn) {
      btn.click();
    }
  }
}

// Istanza globale
const tabs = new TabComponent();
