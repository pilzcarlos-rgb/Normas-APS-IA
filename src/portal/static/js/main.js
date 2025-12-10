// Main JavaScript for APS Normative Graph Portal

// Filter norms by status
function filterByStatus(status) {
    window.location.href = `/api/norms?status=${status}`;
}

// Search functionality
function searchNorms(query) {
    fetch(`/api/norms?search=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displayNorms(data.norms);
        })
        .catch(error => {
            console.error('Error searching norms:', error);
        });
}

// Display norms in a list
function displayNorms(norms) {
    const container = document.getElementById('norms-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (norms.length === 0) {
        container.innerHTML = '<p>Nenhuma norma encontrada.</p>';
        return;
    }
    
    norms.forEach(norm => {
        const normElement = createNormElement(norm);
        container.appendChild(normElement);
    });
}

// Create HTML element for a norm
function createNormElement(norm) {
    const div = document.createElement('div');
    div.className = 'norm-item';
    
    div.innerHTML = `
        <h3>
            <a href="/norm/${norm.id_norma}">
                ${norm.tipo} ${norm.numero}/${norm.ano}
            </a>
        </h3>
        <p class="norm-ementa">${norm.ementa}</p>
        <div class="norm-meta">
            <span class="norm-theme">${norm.tema_principal || 'N/A'}</span>
            <span class="norm-status status-${norm.status_vigencia}">
                ${norm.status_vigencia}
            </span>
        </div>
        ${norm.url_html ? `<a href="${norm.url_html}" target="_blank">Ver documento oficial</a>` : ''}
    `;
    
    return div;
}

// Load statistics
function loadStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateStatsDisplay(data);
        })
        .catch(error => {
            console.error('Error loading stats:', error);
        });
}

// Update statistics display
function updateStatsDisplay(stats) {
    const elements = {
        'total_norms': document.querySelector('.stat-card:nth-child(1) h3'),
        'active_norms': document.querySelector('.stat-card:nth-child(2) h3'),
        'revoked_norms': document.querySelector('.stat-card:nth-child(3) h3')
    };
    
    Object.keys(elements).forEach(key => {
        if (elements[key] && stats[key] !== undefined) {
            elements[key].textContent = stats[key];
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load initial statistics if on main page
    if (document.querySelector('.stats')) {
        loadStats();
    }
    
    // Setup search if search box exists
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchNorms(this.value);
            }, 300);
        });
    }
});

// Export functions for use in templates
window.filterByStatus = filterByStatus;
window.searchNorms = searchNorms;
