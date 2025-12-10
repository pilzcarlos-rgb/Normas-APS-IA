// Estado da aplicação
let currentFilter = 'all';
let currentTab = 'todas';
let currentTopic = null;
let searchQuery = '';

// Inicializar aplicação
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    renderNormas();
});

function initializeApp() {
    // Atualizar estatísticas
    const stats = getStats();
    document.getElementById('totalPortarias').textContent = stats.portarias;
    document.getElementById('totalResolucoes').textContent = stats.resolucoes;
    document.getElementById('totalLeis').textContent = stats.leis;
    document.getElementById('totalNotas').textContent = stats.notas;
    document.getElementById('totalManuais').textContent = stats.manuais;
}

function setupEventListeners() {
    // Filtros de tipo
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            renderNormas();
        });
    });

    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            currentTab = this.dataset.tab;
            currentTopic = null;
            renderNormas();
        });
    });

    // Busca
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', function() {
        searchQuery = this.value.toLowerCase();
        renderNormas();
    });
}

function filterNormas() {
    let filtered = Object.entries(normasData).map(([id, norma]) => ({ id, ...norma }));

    // Filtro por tipo
    if (currentFilter !== 'all') {
        filtered = filtered.filter(norma => {
            if (currentFilter === 'manual') {
                return ['manual', 'caderno', 'guia', 'cartilha', 'instrumento', 'documento', 'modelo'].includes(norma.type);
            }
            return norma.type === currentFilter;
        });
    }

    // Filtro por aba
    if (currentTab === 'essenciais') {
        filtered = filtered.filter(norma => norma.essential);
    } else if (currentTab === 'recentes') {
        filtered = filtered.filter(norma => norma.year >= 2024);
        filtered.sort((a, b) => b.year - a.year);
    } else if (currentTab === 'temas') {
        return renderTopics();
    }

    // Filtro por tema (quando selecionado)
    if (currentTopic) {
        filtered = filtered.filter(norma => 
            norma.topics && norma.topics.includes(currentTopic)
        );
    }

    // Filtro de busca
    if (searchQuery) {
        filtered = filtered.filter(norma => {
            const searchText = `${norma.title} ${norma.description} ${norma.tags.join(' ')} ${norma.number || ''}`.toLowerCase();
            return searchText.includes(searchQuery);
        });
    }

    return filtered;
}

function renderNormas() {
    const container = document.getElementById('normasContainer');
    
    if (currentTab === 'temas') {
        renderTopics();
        return;
    }

    const normas = filterNormas();

    if (normas.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div style="font-size: 4em; margin-bottom: 20px;">📋</div>
                <h3>Nenhuma norma encontrada</h3>
                <p>Tente ajustar os filtros ou termo de busca</p>
            </div>
        `;
        return;
    }

    container.innerHTML = normas.map(norma => createNormaCard(norma)).join('');
}

function createNormaCard(norma) {
    const typeLabels = {
        portaria: 'Portaria',
        resolucao: 'Resolução',
        lei: 'Lei',
        nota: 'Nota Técnica',
        manual: 'Manual',
        caderno: 'Caderno AB',
        guia: 'Guia',
        cartilha: 'Cartilha',
        instrumento: 'Instrumento',
        documento: 'Documento',
        modelo: 'Modelo',
        faq: 'FAQ',
        diretrizes: 'Diretrizes'
    };

    const linksHtml = norma.links.map(link => {
        const hasLocal = link.url.startsWith('documentos/');
        const icon = hasLocal ? '📄' : '🔗';
        return `<a href="${link.url}" class="btn btn-primary" ${hasLocal ? '' : 'target="_blank"'}>${icon} ${link.text}</a>`;
    }).join('');

    const tagsHtml = norma.tags.map(tag => `<span class="tag">${tag}</span>`).join('');

    const essentialBadge = norma.essential ? '<span class="tag" style="background: #ffd700; color: #000; font-weight: bold;">⭐ Essencial</span>' : '';

    return `
        <div class="norma-card" data-type="${norma.type}">
            <div class="type ${norma.type}">${typeLabels[norma.type] || norma.type}</div>
            <h3>${norma.title}</h3>
            <p class="description">${norma.description}</p>
            <div class="tags">
                ${essentialBadge}
                ${tagsHtml}
                <span class="tag" style="background: #e3f2fd; color: #1976d2;">${norma.year}</span>
            </div>
            <div class="actions">
                ${linksHtml}
            </div>
        </div>
    `;
}

function renderTopics() {
    const container = document.getElementById('normasContainer');
    const topics = getTopics();

    // Se um tema está selecionado, mostrar normas desse tema
    if (currentTopic) {
        const normas = getNormasByTopic(currentTopic);
        container.innerHTML = `
            <div style="grid-column: 1 / -1; margin-bottom: 20px;">
                <button class="btn btn-secondary" onclick="backToTopics()" style="margin-bottom: 10px;">← Voltar para Temas</button>
                <h2 class="section-title">📌 ${currentTopic}</h2>
                <p style="color: #666; margin-bottom: 20px;">${normas.length} norma(s) encontrada(s)</p>
            </div>
            ${normas.map(norma => createNormaCard(norma)).join('')}
        `;
        return;
    }

    // Mostrar lista de temas
    const topicsHtml = topics.map(topic => {
        const count = getNormasByTopic(topic).length;
        return `
            <div class="norma-card" onclick="selectTopic('${topic}')" style="cursor: pointer;">
                <div class="type portaria">Tema</div>
                <h3>${topic}</h3>
                <p class="description">${count} norma(s) relacionada(s)</p>
                <div class="actions">
                    <button class="btn btn-primary">Ver Normas →</button>
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = `
        <div style="grid-column: 1 / -1; margin-bottom: 20px;">
            <h2 class="section-title">🗂️ Navegação por Temas</h2>
            <p style="color: #666;">Selecione um tema para ver todas as normas relacionadas</p>
        </div>
        ${topicsHtml}
    `;
}

function selectTopic(topic) {
    currentTopic = topic;
    renderNormas();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function backToTopics() {
    currentTopic = null;
    renderNormas();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Função para download de todas as normas (futuro)
function downloadAllNormas() {
    // Criar notificação toast em vez de alert
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #2c3e50;
        color: white;
        padding: 20px 30px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 9999;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;
    toast.innerHTML = `
        <strong>⚙️ Em Desenvolvimento</strong><br>
        <span style="font-size: 14px; opacity: 0.9;">
            A funcionalidade de download em massa está em desenvolvimento. 
            Por enquanto, baixe individualmente cada norma.
        </span>
    `;
    
    // Adicionar animação
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(toast);
    
    // Remover após 5 segundos
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}
