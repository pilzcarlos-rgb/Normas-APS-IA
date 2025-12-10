# Quick Start Guide

Este guia rápido ajudará você a começar a usar o Sistema de Grafo Normativo da APS.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA
```

### 2. Crie um ambiente virtual

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## Uso Básico

### Inicializar o Banco de Dados

```bash
python -c "from src.models import init_database; init_database()"
```

Isso criará o arquivo `data/normas_aps.db` com todas as tabelas necessárias.

### Executar a Coleta de Dados

#### Opção 1: Pipeline Completo

Execute o pipeline completo de coleta e análise:

```bash
python main.py
```

Isso executará:
- Camada 1: Varredura BVSMS (2010-2025)
- Camada 2: Parse de consolidações
- Camada 3: Coleta de programas específicos
- Validação de qualidade
- Análise de grafo

#### Opção 2: Camadas Individuais

Execute cada camada separadamente:

**Camada 1 - BVSMS:**
```bash
python -m src.scrapers.bvsms_scraper
```

**Camada 2 - Consolidações:**
```bash
python -m src.scrapers.consolidation_parser
```

**Camada 3 - Programas:**
```bash
python -m src.scrapers.program_scraper
```

### Executar o Portal Web

```bash
python -m src.portal.app
```

Acesse http://localhost:5000 no seu navegador.

## Exemplos de Uso

### Exemplo 1: Criar e Consultar Normas

```python
from src.models import init_database, Norm
from datetime import datetime

# Inicializar banco
engine, Session = init_database()
session = Session()

# Criar uma nova norma
norma = Norm(
    id_norma='PORTARIA_2979_2019',
    tipo='Portaria GM/MS',
    orgao='GM/MS',
    numero='2979',
    ano=2019,
    data_publicacao=datetime(2019, 11, 12),
    ementa='Institui o Programa Previne Brasil',
    tema_principal='financiamento',
    status_vigencia='vigente',
    fonte='bvsms',
    url_html='https://bvsms.saude.gov.br/...'
)

session.add(norma)
session.commit()

# Consultar normas
normas_2019 = session.query(Norm).filter_by(ano=2019).all()
print(f"Encontradas {len(normas_2019)} normas de 2019")
```

### Exemplo 2: Análise de Grafo

```python
from src.utils import build_graph_from_norms

# Carregar normas do banco
norms = [...]  # Lista de dicionários com dados das normas

# Construir grafo
graph = build_graph_from_norms(norms)

# Análises
normas_ativas = graph.find_active_norms()
normas_revogadas = graph.find_revoked_norms()
timeline_financeira = graph.get_financial_timeline()
clusters_tematicos = graph.get_theme_clusters()

print(f"Normas ativas: {len(normas_ativas)}")
print(f"Normas revogadas: {len(normas_revogadas)}")
print(f"Temas: {list(clusters_tematicos.keys())}")
```

### Exemplo 3: Validação de Qualidade

```python
from src.utils import QualityChecker

# Carregar normas
norms = [...]  # Lista de dicionários

# Executar verificações
checker = QualityChecker(norms)
report = checker.run_all_checks()

print(f"Score de qualidade: {report['quality_score']:.2f}%")
print(f"Avisos: {len(report['warnings'])}")
print(f"Erros: {len(report['errors'])}")

# Ver detalhes
for check_name, check_result in report['checks'].items():
    print(f"\n{check_name}:")
    print(f"  Passou: {check_result['pass']}")
```

## Estrutura de Dados

### Formato de uma Norma

```python
{
    'id_norma': 'PORTARIA_2979_2019',
    'tipo': 'Portaria GM/MS',
    'orgao': 'GM/MS',
    'numero': '2979',
    'ano': 2019,
    'data_publicacao': '2019-11-12',
    'ementa': 'Institui o Programa Previne Brasil',
    'tema_principal': 'financiamento',
    'temas_secundarios': ['organizacao_aps', 'sistemas_informacao'],
    'status_vigencia': 'vigente',
    'efeitos_financeiros_partir_de': '2020-01-01',
    'url_html': 'https://...',
    'url_pdf': 'https://...',
    'fonte': 'bvsms',
    'altera': ['PORTARIA_123_2018'],
    'revoga': [],
    'regulamenta': []
}
```

## Navegação no Portal Web

O portal oferece várias formas de explorar as normas:

### Por Tema
- **Organização da APS**: PNAB, estrutura
- **Financiamento**: Previne Brasil, cofinanciamento
- **Sistemas de Informação**: e-SUS, SISAB
- **Força de Trabalho**: ACS, ACE, credenciamento

### Por Ano
Selecione qualquer ano entre 2010-2025 para ver todas as normas daquele período.

### Por Status
- **Vigentes**: Normas atualmente em vigor
- **Revogadas**: Normas que foram canceladas
- **Alteradas**: Normas que sofreram modificações parciais

### Busca
Use a busca para encontrar normas específicas por:
- Número da norma
- Palavras-chave na ementa
- Tema
- Ano

## Exportação de Dados

### Exportar para JSON

```python
import json
from src.models import init_database, Norm

engine, Session = init_database()
session = Session()

# Buscar normas
normas = session.query(Norm).all()

# Converter para dicionários
normas_dict = [n.to_dict() for n in normas]

# Salvar JSON
with open('normas_export.json', 'w', encoding='utf-8') as f:
    json.dump(normas_dict, f, ensure_ascii=False, indent=2)
```

### Exportar Grafo para Visualização

```python
from src.utils import build_graph_from_norms
import json

graph = build_graph_from_norms(norms)
graph_data = graph.export_graph_data()

with open('graph_export.json', 'w', encoding='utf-8') as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=2)
```

## Troubleshooting

### Erro: ModuleNotFoundError

**Problema**: Módulos Python não encontrados

**Solução**: Certifique-se de que as dependências estão instaladas:
```bash
pip install -r requirements.txt
```

### Erro: Database is locked

**Problema**: SQLite não permite múltiplos escritores

**Solução**: 
- Feche outros processos que estão usando o banco
- Use PostgreSQL para ambientes de produção

### Portal não inicia

**Problema**: Porta 5000 já está em uso

**Solução**: Use uma porta diferente:
```bash
python -c "from src.portal.app import run_portal; run_portal(port=8080)"
```

## Próximos Passos

1. **Explore a documentação completa** em `docs/developer_guide.md`
2. **Veja exemplos avançados** nos testes em `tests/`
3. **Configure coleta automática** com cron ou scheduler
4. **Personalize o portal** modificando templates e estilos
5. **Contribua** com melhorias e novos recursos

## Recursos Adicionais

- [README Principal](../README.md)
- [Guia do Desenvolvedor](developer_guide.md)
- [Schema de Dados](../data/schemas/norm_schema.json)
- [Configuração](../config.yaml)

## Suporte

Para dúvidas e problemas:
1. Consulte a documentação
2. Veja os exemplos nos testes
3. Abra uma issue no GitHub

---

**Nota**: Este sistema é um framework de referência. Para uso em produção, implemente tratamento de erros adicional, autenticação, e otimizações de performance conforme necessário.
