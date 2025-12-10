# Próximos Passos - Guia de Implementação

Este documento detalha os próximos passos implementados e como utilizá-los.

## ✅ O Que Foi Adicionado

### 1. Setup Automatizado

#### setup.py
Script Python interativo que:
- ✓ Verifica versão do Python (3.8+)
- ✓ Cria diretórios necessários
- ✓ Instala dependências
- ✓ Valida configurações
- ✓ Inicializa banco de dados
- ✓ Cria dados de exemplo

**Uso:**
```bash
python setup.py
```

#### setup.sh
Script Bash para setup completo:
- ✓ Cria ambiente virtual
- ✓ Ativa ambiente
- ✓ Executa setup.py

**Uso:**
```bash
./setup.sh
```

### 2. Containerização Docker

#### Dockerfile
Container production-ready com:
- Python 3.10 slim
- Dependências instaladas
- Banco de dados inicializado
- Health checks configurados
- Porta 5000 exposta

**Uso:**
```bash
docker build -t normas-aps .
docker run -p 5000:5000 normas-aps
```

#### docker-compose.yml
Orquestração multi-serviço:
- **web**: Portal web (porta 5000)
- **collector**: Coleta de dados
- Volumes para persistência
- Restart automático

**Uso:**
```bash
docker-compose up -d        # Iniciar
docker-compose logs -f      # Ver logs
docker-compose down         # Parar
```

### 3. GitHub Actions - CI/CD

#### .github/workflows/ci.yml
Pipeline de integração contínua:
- ✓ Testes em Python 3.8, 3.9, 3.10, 3.11
- ✓ Validação de configurações
- ✓ Verificação de estrutura
- ✓ Quality checks
- ✓ Cache de dependências

**Execução:** Automática em push/PR

#### .github/workflows/deploy-pages.yml
Deploy automático do portal:
- ✓ Build do site estático
- ✓ Deploy no GitHub Pages
- ✓ Cópia de documentação

**Execução:** Automática no push para main

### 4. Scripts Utilitários

#### scripts/collect_data.py
Script completo de coleta:
- ✓ Executa 3 camadas de coleta
- ✓ Atualiza banco de dados
- ✓ Gera relatórios de qualidade
- ✓ Logging detalhado
- ✓ Tratamento de erros

**Uso:**
```bash
python scripts/collect_data.py
```

**Funcionalidades:**
- Coleta BVSMS (Layer 1)
- Parse de consolidações (Layer 2)
- Scraping de programas (Layer 3)
- Atualização incremental do DB
- Relatórios JSON automáticos

#### scripts/export_data.py
Exportação multi-formato:
- ✓ JSON (pretty ou minified)
- ✓ JSONL (uma norma por linha)
- ✓ CSV (planilha)
- ✓ HTML (relatório visual)
- ✓ Relationships (grafo)

**Uso:**
```bash
# Exportar para JSON
python scripts/export_data.py json

# Exportar para CSV
python scripts/export_data.py csv

# Gerar relatório HTML
python scripts/export_data.py html

# Exportar tudo
python scripts/export_data.py all

# Especificar arquivo de saída
python scripts/export_data.py json -o meu_export.json
```

## 🎯 Fluxos de Trabalho Recomendados

### Fluxo 1: Desenvolvimento Local

```bash
# 1. Clone e setup
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA
./setup.sh

# 2. Ativar ambiente (nas próximas vezes)
source venv/bin/activate

# 3. Coletar dados
python scripts/collect_data.py

# 4. Iniciar portal
python -m src.portal.app

# 5. Acessar
# http://localhost:5000
```

### Fluxo 2: Deploy com Docker

```bash
# 1. Clone
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA

# 2. Iniciar serviços
docker-compose up -d

# 3. Verificar logs
docker-compose logs -f web

# 4. Coletar dados (execução única)
docker-compose run collector

# 5. Acessar portal
# http://localhost:5000

# 6. Parar quando necessário
docker-compose down
```

### Fluxo 3: Deploy em Servidor

```bash
# 1. Setup no servidor
ssh usuario@servidor
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA

# 2. Usar Docker para produção
docker-compose -f docker-compose.yml up -d

# 3. Configurar cron para coleta automática
crontab -e
# Adicionar: 0 2 * * * cd /caminho/para/Normas-APS-IA && docker-compose run collector

# 4. Configurar nginx ou Apache como reverse proxy
# Exemplo nginx:
# location / {
#     proxy_pass http://localhost:5000;
# }
```

### Fluxo 4: CI/CD com GitHub

```bash
# 1. Fork/Clone do repositório
# 2. Fazer alterações
# 3. Commit e push

git add .
git commit -m "Minhas alterações"
git push

# 4. GitHub Actions executa automaticamente:
#    - Testes em múltiplas versões Python
#    - Validações de qualidade
#    - Deploy no GitHub Pages (se branch main)

# 5. Verificar resultado
# https://github.com/seu-usuario/Normas-APS-IA/actions
```

## 📊 Monitoramento e Manutenção

### Verificar Status do Sistema

```bash
# Status dos containers
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Uso de recursos
docker stats

# Verificar banco de dados
sqlite3 data/normas_aps.db "SELECT COUNT(*) FROM norms;"
```

### Backup de Dados

```bash
# Backup do banco de dados
cp data/normas_aps.db data/backups/normas_aps_$(date +%Y%m%d).db

# Backup de exports
tar -czf backups/exports_$(date +%Y%m%d).tar.gz data/exports/
```

### Atualização do Sistema

```bash
# Atualizar código
git pull origin main

# Reconstruir containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Ou sem Docker:
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 🔧 Troubleshooting

### Problema: Setup falha

**Solução:**
```bash
# Verificar Python
python --version  # Deve ser 3.8+

# Instalar dependências manualmente
pip install -r requirements.txt

# Verificar logs
cat logs/*.log
```

### Problema: Docker não inicia

**Solução:**
```bash
# Verificar Docker
docker --version
docker-compose --version

# Limpar containers antigos
docker-compose down -v
docker system prune -a

# Reconstruir
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Portal não carrega

**Solução:**
```bash
# Verificar se porta está em uso
lsof -i :5000

# Usar porta diferente
python -c "from src.portal.app import run_portal; run_portal(port=8080)"

# Verificar logs
tail -f logs/*.log
```

### Problema: Coleta falha

**Solução:**
```bash
# Verificar conectividade
ping bvsms.saude.gov.br

# Executar com mais logging
python scripts/collect_data.py --verbose

# Testar camadas individualmente
python -m src.scrapers.bvsms_scraper
```

## 📈 Próximos Passos Sugeridos

### Curto Prazo (Próximas Semanas)

1. **Povoar banco com dados reais**
   ```bash
   python scripts/collect_data.py
   ```

2. **Configurar coleta automática**
   - Adicionar cron job ou GitHub Actions schedule
   - Executar semanalmente

3. **Personalizar portal**
   - Ajustar cores em `src/portal/static/css/style.css`
   - Adicionar logo em templates

4. **Criar relatórios customizados**
   - Estender `scripts/export_data.py`
   - Adicionar novos formatos

### Médio Prazo (Próximos Meses)

1. **Ampliar fontes de dados**
   - Adicionar novos scrapers
   - Integrar APIs oficiais

2. **Melhorar visualização**
   - Adicionar gráficos (D3.js, Chart.js)
   - Timeline interativa

3. **Implementar autenticação**
   - Sistema de usuários
   - Controle de acesso

4. **API REST completa**
   - Endpoints CRUD
   - Documentação OpenAPI/Swagger

### Longo Prazo (6+ Meses)

1. **Machine Learning**
   - Classificação automática de temas
   - Extração de entidades
   - Sumarização automática

2. **Análise avançada**
   - Impacto de mudanças normativas
   - Predição de alterações
   - Análise de sentimento

3. **Integração com outros sistemas**
   - APIs externas
   - Webhooks
   - Notificações

4. **Escalabilidade**
   - PostgreSQL em vez de SQLite
   - Cache com Redis
   - Load balancing

## 🎓 Recursos de Aprendizado

### Para Desenvolvedores

- `docs/developer_guide.md` - Arquitetura detalhada
- `docs/quick_start.md` - Guia rápido
- `examples/usage_example.py` - Exemplos práticos
- `tests/` - Suite de testes como referência

### Para Usuários

- `README.md` - Visão geral
- `PROJECT_SUMMARY.md` - Resumo do projeto
- Portal web - Documentação interativa em `/about`

### Para Operações

- `.github/workflows/` - Pipelines CI/CD
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Orchestration

## 📞 Suporte

Para questões e problemas:
1. Consultar documentação
2. Verificar logs em `logs/`
3. Abrir issue no GitHub
4. Consultar exemplos em `examples/`

---

**Sistema pronto para produção! 🚀**
