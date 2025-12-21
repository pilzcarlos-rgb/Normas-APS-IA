// Base de dados de normas APS
const normasData = {
    // Modelo de cofinanciamento da APS
    "portaria-3493-2024": {
        type: "portaria",
        title: "Portaria GM/MS nº 3.493/2024",
        description: "Estabelece o novo modelo de cofinanciamento da Atenção Primária à Saúde",
        year: 2024,
        number: "3.493/2024",
        tags: ["financiamento", "cofinanciamento", "componente fixo", "vínculo territorial", "qualidade", "essencial"],
        essential: true,
        links: [
            { text: "BVS - Texto oficial", url: "https://bvsms.saude.gov.br/bvs/saudelegis/gm/2024/prt3493_16_12_2024.html" },
            { text: "PDF Metodologia", url: "documentos/portarias/portaria-3493-2024-metodologia.pdf" }
        ],
        topics: ["Componente Fixo (eSF/eAP)", "Vínculo e Acompanhamento Territorial", "Qualidade", "Compensação de perdas", "Transição/implantação"]
    },
    
    "faq-financiamento-aps": {
        type: "faq",
        title: "Perguntas Frequentes do Novo Financiamento da APS",
        description: "Respostas para dúvidas comuns sobre o novo modelo de financiamento",
        year: 2024,
        tags: ["financiamento", "faq", "perguntas", "essencial"],
        essential: true,
        links: [
            { text: "FAQ - SAPS", url: "https://aps.saude.gov.br/financiamento/faq" }
        ],
        topics: ["Modelo de cofinanciamento", "Componente Fixo", "Vínculo Territorial", "Qualidade"]
    },

    "nota-tecnica-saps-conass-conasems-01-2024": {
        type: "nota",
        title: "Nota Técnica conjunta SAPS/CONASS/CONASEMS 01/2024",
        description: "Orientações conjuntas sobre implementação do novo financiamento",
        year: 2024,
        number: "01/2024",
        tags: ["nota técnica", "financiamento", "implementação", "essencial"],
        essential: true,
        links: [
            { text: "Nota Técnica PDF", url: "documentos/notas-tecnicas/nota-tecnica-conjunta-01-2024.pdf" }
        ],
        topics: ["Modelo de cofinanciamento", "Componente Fixo", "Vínculo Territorial", "Qualidade", "Transição"]
    },

    "portaria-161-2024": {
        type: "portaria",
        title: "Portaria SAPS/MS nº 161/2024",
        description: "Define metodologia do Componente II - Vínculo e Acompanhamento Territorial",
        year: 2024,
        number: "161/2024",
        tags: ["financiamento", "vínculo territorial", "metodologia", "cadastro"],
        essential: true,
        links: [
            { text: "Portaria SAPS 161/2024", url: "documentos/portarias/portaria-saps-161-2024.pdf" },
            { text: "PDF Completo", url: "documentos/portarias/portaria-saps-161-2024-completa.pdf" }
        ],
        topics: ["Vínculo e Acompanhamento Territorial", "Parâmetros de pessoas por equipe"]
    },

    "nota-metodologica-desco-2024": {
        type: "nota",
        title: "Nota Metodológica DESCO/SAPS 2024",
        description: "Nota metodológica sobre o componente de vínculo territorial",
        year: 2024,
        tags: ["metodologia", "vínculo territorial", "cadastro"],
        essential: false,
        links: [
            { text: "Nota Metodológica PDF", url: "documentos/notas-tecnicas/nota-metodologica-desco-2024.pdf" }
        ],
        topics: ["Vínculo e Acompanhamento Territorial", "Parâmetros de pessoas por equipe"]
    },

    "portaria-6907-2025": {
        type: "portaria",
        title: "Portaria GM/MS nº 6.907/2025",
        description: "Ajustes no componente qualidade do novo financiamento",
        year: 2025,
        number: "6.907/2025",
        tags: ["qualidade", "indicadores", "ajustes"],
        essential: true,
        links: [
            { text: "Portaria 6.907/2025", url: "documentos/portarias/portaria-6907-2025.pdf" }
        ],
        topics: ["Qualidade", "Transição/implantação"]
    },

    "portaria-7799-2025": {
        type: "portaria",
        title: "Portaria GM/MS nº 7.799/2025",
        description: "Atualizações do novo modelo de financiamento",
        year: 2025,
        number: "7.799/2025",
        tags: ["financiamento", "atualizações", "suspensão"],
        essential: true,
        links: [
            { text: "Portaria 7.799/2025", url: "documentos/portarias/portaria-7799-2025.pdf" }
        ],
        topics: ["Qualidade", "Transição/implantação", "Suspensão/regularização"]
    },

    "portaria-1654-2011": {
        type: "portaria",
        title: "Portaria GM/MS nº 1.654/2011",
        description: "Institui o Programa Nacional de Melhoria do Acesso e da Qualidade da Atenção Básica (PMAQ-AB)",
        year: 2011,
        number: "1.654/2011",
        tags: ["pmaq", "qualidade", "avaliação", "histórico"],
        essential: true,
        links: [
            { text: "Portaria 1.654/2011", url: "documentos/portarias/portaria-1654-2011.pdf" }
        ],
        topics: ["Qualidade", "Autoavaliação", "Processo de Trabalho"]
    },

    "manual-pmaq": {
        type: "manual",
        title: "Manual Instrutivo do PMAQ-AB",
        description: "Manual completo do Programa Nacional de Melhoria do Acesso e da Qualidade",
        year: 2015,
        tags: ["pmaq", "qualidade", "manual", "histórico", "essencial"],
        essential: true,
        links: [
            { text: "Manual PMAQ - BVS", url: "http://bvsms.saude.gov.br/bvs/publicacoes/manual_instrutivo_pmaq_atencao_basica.pdf" }
        ],
        topics: ["Qualidade", "Autoavaliação"]
    },

    "manual-pmaq-ciclo1": {
        type: "manual",
        title: "Manual Instrutivo PMAQ-AB — 1º Ciclo",
        description: "Manual do primeiro ciclo do PMAQ",
        year: 2012,
        tags: ["pmaq", "qualidade", "ciclo 1"],
        essential: false,
        links: [
            { text: "Manual 1º Ciclo", url: "documentos/manuais/pmaq-1-ciclo.pdf" }
        ],
        topics: ["Qualidade", "Autoavaliação"]
    },

    "manual-pmaq-ciclo2": {
        type: "manual",
        title: "Manual Instrutivo PMAQ-AB — 2º Ciclo",
        description: "Manual do segundo ciclo do PMAQ",
        year: 2013,
        tags: ["pmaq", "qualidade", "ciclo 2"],
        essential: false,
        links: [
            { text: "Manual 2º Ciclo", url: "documentos/manuais/pmaq-2-ciclo.pdf" }
        ],
        topics: ["Qualidade", "Autoavaliação"]
    },

    "manual-pmaq-ciclo3": {
        type: "manual",
        title: "Manual Instrutivo PMAQ-AB — 3º Ciclo",
        description: "Manual do terceiro ciclo do PMAQ",
        year: 2015,
        tags: ["pmaq", "qualidade", "ciclo 3"],
        essential: false,
        links: [
            { text: "Manual 3º Ciclo", url: "documentos/manuais/pmaq-3-ciclo.pdf" }
        ],
        topics: ["Qualidade", "Autoavaliação"]
    },

    "pmaq-documento-referencia": {
        type: "documento",
        title: "PMAQ-AB — Documento de Referência do Programa",
        description: "Documento de referência completo do PMAQ",
        year: 2011,
        tags: ["pmaq", "qualidade", "referência"],
        essential: false,
        links: [
            { text: "Documento de Referência", url: "documentos/manuais/pmaq-documento-referencia.pdf" }
        ],
        topics: ["Qualidade", "Autoavaliação"]
    },

    "amaq": {
        type: "instrumento",
        title: "AMAQ — 2ª Edição (2016)",
        description: "Autoavaliação para Melhoria do Acesso e da Qualidade da Atenção Básica",
        year: 2016,
        tags: ["amaq", "autoavaliação", "qualidade"],
        essential: true,
        links: [
            { text: "AMAQ 2ª Edição", url: "documentos/manuais/amaq-2-edicao.pdf" }
        ],
        topics: ["Qualidade", "Autoavaliação", "Processo de Trabalho"]
    },

    "amaq-nasf": {
        type: "instrumento",
        title: "AMAQ NASF",
        description: "Autoavaliação para equipes de Núcleo de Apoio à Saúde da Família",
        year: 2014,
        tags: ["amaq", "nasf", "autoavaliação"],
        essential: false,
        links: [
            { text: "AMAQ NASF", url: "documentos/manuais/amaq-nasf.pdf" }
        ],
        topics: ["Qualidade", "Autoavaliação", "Matriciamento"]
    },

    "cab-17-saude-bucal": {
        type: "caderno",
        title: "CAB nº 17 — Saúde Bucal",
        description: "Caderno de Atenção Básica sobre Saúde Bucal",
        year: 2008,
        tags: ["saúde bucal", "cab", "protocolo"],
        essential: true,
        links: [
            { text: "CAB 17 - PDF", url: "http://bvsms.saude.gov.br/bvs/publicacoes/saude_bucal.pdf" }
        ],
        topics: ["Saúde Bucal", "Processo de Trabalho"]
    },

    "diretrizes-brasil-sorridente": {
        type: "diretrizes",
        title: "Diretrizes da Política Nacional de Saúde Bucal (Brasil Sorridente)",
        description: "Diretrizes da política de saúde bucal no Brasil",
        year: 2004,
        tags: ["saúde bucal", "política nacional", "diretrizes"],
        essential: true,
        links: [
            { text: "Diretrizes Brasil Sorridente", url: "http://bvsms.saude.gov.br/bvs/publicacoes/politica_nacional_brasil_sorridente.pdf" }
        ],
        topics: ["Saúde Bucal"]
    },

    "portaria-5672-2024": {
        type: "portaria",
        title: "Portaria GM/MS nº 5.672/2024",
        description: "Define regras para INE/CNES na APS e credenciamento de estabelecimentos",
        year: 2024,
        number: "5.672/2024",
        tags: ["ine", "cnes", "credenciamento", "cadastro"],
        essential: true,
        links: [
            { text: "Portaria 5.672/2024", url: "documentos/portarias/portaria-5672-2024.pdf" }
        ],
        topics: ["SCNES/INE", "SIAPS"]
    },

    "portaria-5668-2024": {
        type: "portaria",
        title: "Portaria GM/MS nº 5.668/2024",
        description: "Define adequações e hipóteses de suspensão de incentivos da APS",
        year: 2024,
        number: "5.668/2024",
        tags: ["suspensão", "incentivos", "regularização"],
        essential: true,
        links: [
            { text: "Portaria 5.668/2024", url: "documentos/portarias/portaria-5668-2024.pdf" }
        ],
        topics: ["Suspensão/regularização", "SIAPS"]
    },

    "manual-esus-aps": {
        type: "manual",
        title: "Manual e-SUS APS",
        description: "Manual completo do sistema e-SUS Atenção Primária à Saúde",
        year: 2024,
        tags: ["e-sus", "siaps", "sistema", "manual", "essencial"],
        essential: true,
        links: [
            { text: "Manual e-SUS APS - SAPS", url: "https://aps.saude.gov.br/ape/esus" }
        ],
        topics: ["SIAPS"]
    },

    "guia-cadastros-esus": {
        type: "guia",
        title: "Guia de Preenchimento - Cadastros (e-SUS APS)",
        description: "Guia para preenchimento de cadastros no e-SUS APS",
        year: 2024,
        tags: ["e-sus", "cadastro", "guia"],
        essential: true,
        links: [
            { text: "Guia de Cadastros", url: "documentos/manuais/guia-cadastros-esus.pdf" }
        ],
        topics: ["SIAPS"]
    },

    "mici-esus": {
        type: "modelo",
        title: "Modelo de Informação - Cadastro Individual (MICI)",
        description: "Modelo de informação do cadastro individual do e-SUS APS",
        year: 2024,
        tags: ["e-sus", "cadastro", "modelo"],
        essential: false,
        links: [
            { text: "MICI", url: "documentos/manuais/mici-esus.pdf" }
        ],
        topics: ["SIAPS"]
    },

    "cartilha-emendas-2025": {
        type: "cartilha",
        title: "Cartilha de Emendas Parlamentares PLOA 2025",
        description: "Orientações sobre emendas parlamentares para a APS",
        year: 2025,
        tags: ["emendas", "orçamento", "parlamentar"],
        essential: false,
        links: [
            { text: "Cartilha FNS - Página", url: "https://www.gov.br/saude/pt-br/acesso-a-informacao/gestao-do-sus/articulacao-interfederativa/fns" },
            { text: "Cartilha PDF - BVS", url: "documentos/manuais/cartilha-emendas-2025.pdf" }
        ],
        topics: ["Emendas parlamentares"]
    },

    "portfolio-emendas-2025": {
        type: "cartilha",
        title: "Portfólio de Ações para Emendas Parlamentares 2025",
        description: "Portfólio de ações elegíveis para emendas parlamentares na APS",
        year: 2025,
        tags: ["emendas", "portfólio", "ações"],
        essential: false,
        links: [
            { text: "Portfólio MS", url: "documentos/manuais/portfolio-emendas-2025.pdf" }
        ],
        topics: ["Emendas parlamentares"]
    },

    "cab-28-v1-acolhimento": {
        type: "caderno",
        title: "CAB nº 28 v.1 — Acolhimento à Demanda Espontânea",
        description: "Caderno sobre acolhimento e classificação de risco na Atenção Básica",
        year: 2013,
        tags: ["acolhimento", "cab", "demanda espontânea"],
        essential: true,
        links: [
            { text: "CAB 28 v.1 - PDF", url: "http://bvsms.saude.gov.br/bvs/publicacoes/acolhimento_demanda_espontanea_cab28v1.pdf" }
        ],
        topics: ["Acolhimento e Classificação de Risco"]
    },

    "cab-28-v2-queixas": {
        type: "caderno",
        title: "CAB nº 28 v.2 — Queixas Mais Comuns na AB",
        description: "Caderno sobre manejo das queixas mais comuns na Atenção Básica",
        year: 2013,
        tags: ["acolhimento", "cab", "queixas comuns"],
        essential: true,
        links: [
            { text: "CAB 28 v.2 - PDF", url: "http://bvsms.saude.gov.br/bvs/publicacoes/acolhimento_demanda_espontanea_queixas_comuns_cab28v2.pdf" }
        ],
        topics: ["Acolhimento e Classificação de Risco"]
    }
};

// Função para obter estatísticas
function getStats() {
    const stats = {
        portarias: 0,
        resolucoes: 0,
        leis: 0,
        notas: 0,
        manuais: 0,
        total: 0
    };

    Object.values(normasData).forEach(norma => {
        stats.total++;
        if (norma.type === 'portaria') stats.portarias++;
        else if (norma.type === 'resolucao') stats.resolucoes++;
        else if (norma.type === 'lei') stats.leis++;
        else if (norma.type === 'nota') stats.notas++;
        else if (['manual', 'caderno', 'guia', 'cartilha', 'instrumento'].includes(norma.type)) stats.manuais++;
    });

    return stats;
}

// Função para obter temas únicos
function getTopics() {
    const topicsSet = new Set();
    Object.values(normasData).forEach(norma => {
        if (norma.topics) {
            norma.topics.forEach(topic => topicsSet.add(topic));
        }
    });
    return Array.from(topicsSet).sort();
}

// Função para obter normas por tema
function getNormasByTopic(topic) {
    return Object.entries(normasData)
        .filter(([_, norma]) => norma.topics && norma.topics.includes(topic))
        .map(([id, norma]) => ({ id, ...norma }));
}
