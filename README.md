# Grafo Normativo da APS

Sistema abrangente de mapeamento e análise da legislação estruturante da Atenção Primária à Saúde (APS) no Brasil.

## 🎯 Visão Geral

Em vez de uma simples lista de portarias, este sistema representa as normas da APS como um **grafo** com:
- **Nós**: documentos normativos (Constituição, leis, decretos, portarias, resoluções, notas técnicas)
- **Relações**: institui, altera, revoga, regulamenta, consolida, efeitos financeiros

## 📊 Cobertura

### Temporal
- **Período**: 2010-2025
- Garantia de completude através de varredura sistemática por ano

### Fontes Oficiais
- **Planalto**: Constituição, leis, decretos
- **BVSMS/SaudeLegis**: Portarias do MS e SAPS
- **Portarias de Consolidação**: GM/MS nº 6/2017 e SAPS nº 1/2021
- **SAPS**: Lista oficial de normas estruturantes da ESF

### Temática
- Organização da APS (PNAB, estrutura)
- Financiamento (Previne Brasil, Portaria 3.493/2024)
- Sistemas de Informação (e-SUS, SISAB)
- Força de Trabalho (ACS, ACE, credenciamento)
- Equidade e Saúde Bucal

## 🏗️ Arquitetura

```
├── config.yaml                 # Configuração central
├── requirements.txt            # Dependências Python
├── src/
│   ├── models/                 # Modelos de dados e banco
│   │   ├── database.py        # SQLAlchemy models
│   │   └── __init__.py
│   ├── scrapers/              # Coleta de dados (3 camadas)
│   │   ├── base_scraper.py   # Classe base
│   │   ├── bvsms_scraper.py  # Camada 1: varredura ampla
│   │   ├── consolidation_parser.py  # Camada 2: consolidações
│   │   ├── program_scraper.py       # Camada 3: programas
│   │   └── __init__.py
│   ├── utils/                 # Utilitários
│   │   ├── quality_checker.py # Validação de qualidade
│   │   ├── graph_analysis.py  # Análise de grafo
│   │   └── __init__.py
│   └── portal/                # Interface web
│       ├── app.py            # Flask application
│       ├── templates/        # HTML templates
│       └── static/           # CSS, JS
├── data/                      # Dados coletados
│   ├── processed/            # Dados processados
│   └── schemas/              # Schemas de dados
├── scripts/                   # Scripts de coleta e processamento
├── tests/                     # Testes
└── docs/                      # Documentação adicional
```

## 🚀 Início Rápido

### Instalação Automática (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA

# Execute o script de setup
./setup.sh
```

O script automaticamente:
- Cria ambiente virtual
- Instala dependências
- Valida configurações
- Inicializa o banco de dados
- Cria dados de exemplo

### Instalação Manual

```bash
# Clone o repositório
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o setup
python setup.py
```

### Instalação com Docker

```bash
# Clone o repositório
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA

# Construir e iniciar com Docker Compose
docker-compose up -d

# O portal estará disponível em http://localhost:5000
```

### Coleta de Dados

```bash
# Pipeline completo (recomendado)
python main.py

# Ou use o script de coleta
python scripts/collect_data.py

# Coleta por camadas individuais
python -m src.scrapers.bvsms_scraper      # Camada 1
python -m src.scrapers.consolidation_parser  # Camada 2
python -m src.scrapers.program_scraper     # Camada 3
```

### Executar Portal Web

```bash
python -m src.portal.app
# Acesse http://localhost:5000
```

## 📋 Metodologia de Coleta

### Estratégia em 3 Camadas

#### Camada 1: Varredura Ampla (2010-2025)
Busca no BVSMS por termos-chave em cada ano:
- "Atenção Básica", "Atenção Primária", "ESF"
- "eAP", "eSB", "ACS", "ACE"
- "SISAB", "e-SUS", "Informatiza APS"
- "PMAQ", "Previne Brasil"
- "financiamento", "capitação", "desempenho"

#### Camada 2: Consolidações
Parser de:
- Portaria de Consolidação GM/MS nº 6/2017 (financiamento)
- Portaria de Consolidação SAPS nº 1/2021 (APS)
- Extração de anexos, artigos citados, programas listados

#### Camada 3: Programas Específicos
Coleta especializada para:
- **Previne Brasil** (Portaria 2.979/2019)
- **Novo Cofinanciamento** (Portaria 3.493/2024)
- **PMAQ** (histórico)
- **Informatiza APS**

## 🔍 Schema de Dados

### Norm (Norma)
```python
{
    'id_norma': str,              # Identificador único
    'tipo': str,                  # Lei, Decreto, Portaria, etc.
    'orgao': str,                 # GM/MS, SAPS, etc.
    'numero': str,                # Número da norma
    'ano': int,                   # Ano de publicação
    'data_publicacao': date,      # Data de publicação
    'ementa': str,                # Ementa/descrição
    'tema_principal': str,        # Tema principal
    'status_vigencia': str,       # vigente, revogada, alterada_parcial
    'efeitos_financeiros_partir_de': date,  # Data de efeitos financeiros
    'url_html': str,              # Link para documento HTML
    'url_pdf': str,               # Link para documento PDF
    'fonte': str                  # planalto, bvsms, etc.
}
```

### Relationship (Relação)
```python
{
    'source_norm_id': int,        # Norma de origem
    'target_norm_id': int,        # Norma de destino
    'relationship_type': str,     # institui, altera, revoga, etc.
    'description': str,           # Descrição da relação
    'article_reference': str      # Artigo que estabelece a relação
}
```

## ✅ Critérios de Qualidade

O sistema valida completude através de:

1. **Cobertura temporal**: Todos os anos 2010-2025 com registros
2. **Cobertura por fonte**: Planalto, BVSMS, Consolidações
3. **Cobertura temática**: Organização, Financiamento, Informação, Força de Trabalho
4. **Consistência do grafo**: Relações bidirecionais verificadas
5. **Checkpoint manual**: Comparação com lista oficial SAPS/ESF

Exemplo de execução:
```bash
python -m src.utils.quality_checker
```

## 📈 Análise de Grafo

Funcionalidades disponíveis:
- Encontrar normas revogadas
- Identificar normas ativas
- Mapear cadeias de consolidação
- Linha do tempo de efeitos financeiros
- Agrupamento por tema
- Caminhos entre normas

Exemplo:
```python
from src.utils import build_graph_from_norms

# Construir grafo
graph = build_graph_from_norms(norms_list)

# Análises
revoked = graph.find_revoked_norms()
active = graph.find_active_norms()
timeline = graph.get_financial_timeline()
```

## 🌐 Portal Web

O portal oferece navegação por:

### Por Tema
- Organização da APS
- Financiamento
- Sistemas de Informação
- Força de Trabalho

### Por Ano
Seleção de qualquer ano entre 2010-2025

### Por Status de Vigência
- Vigentes
- Revogadas
- Alteradas parcialmente

### Normas Estruturantes
Acesso direto às normas-chave:
- LC 141/2012
- Decreto 7.508/2011
- Portaria de Consolidação SAPS 1/2021
- Portaria 2.979/2019 (Previne Brasil)
- Portaria 3.493/2024 (Novo Cofinanciamento)

## 🤖 Material para Treinamento de IA

O sistema processa documentos para:
1. Conversão HTML/PDF para texto limpo
2. Separação por artigos e anexos
3. Marcação com tags (tema, nível, vigência, efeitos)
4. Geração de datasets Q&A
5. Resumos técnicos para embeddings
6. Casos de uso por porte de município

## 🛠️ Scripts Utilitários

### Coleta de Dados
```bash
# Coleta completa com todas as camadas
python scripts/collect_data.py
```

### Exportação de Dados
```bash
# Exportar para JSON
python scripts/export_data.py json

# Exportar para CSV
python scripts/export_data.py csv

# Exportar relatório HTML
python scripts/export_data.py html

# Exportar tudo
python scripts/export_data.py all
```

### Automação com GitHub Actions
O repositório inclui workflows para:
- **CI/CD**: Testes automáticos em múltiplas versões do Python
- **Deploy**: Publicação automática do portal no GitHub Pages
- **Quality Checks**: Validação de código e estrutura

## 📚 Normas-Chave Incluídas

### Estruturantes
- **LC 141/2012**: Financiamento do SUS
- **Decreto 7.508/2011**: Organização interfederativa
- **Portaria de Consolidação GM/MS 6/2017**: Financiamento
- **Portaria de Consolidação SAPS 1/2021**: APS

### Programas
- **Portaria 2.979/2019**: Previne Brasil
- **Portaria 3.493/2024**: Novo cofinanciamento APS
- **PMAQ**: Histórico de qualidade
- **Informatiza APS**: e-SUS e SISAB

## 🔗 Links Úteis

- [Planalto - Legislação](http://www.planalto.gov.br)
- [BVSMS - SaudeLegis](https://bvsms.saude.gov.br/bvs/saudelegis)
- [Ministério da Saúde](https://www.gov.br/saude)
- [SAPS - Legislação ESF](https://www.gov.br/saude/pt-br)

## 🛠️ Tecnologias

- **Backend**: Python 3.8+
- **Database**: SQLite com SQLAlchemy
- **Web**: Flask
- **Scraping**: BeautifulSoup, Requests
- **Análise**: NLTK, spaCy
- **Frontend**: HTML5, CSS3, JavaScript

## 📄 Licença

Este projeto é de código aberto para fins educacionais e de pesquisa.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📧 Contato

Para questões e sugestões, abra uma issue no GitHub.

---

**Nota**: Este é um sistema de referência que demonstra a metodologia proposta. Para uso em produção, seria necessário implementar tratamento de erros mais robusto, autenticação, caching, e integração completa com as APIs oficiais.