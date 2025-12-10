# Como Abrir o Sistema - Guia Rápido

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:
- Python 3.8 ou superior instalado
- Git instalado
- Terminal/Prompt de comando

## 🚀 Opção 1: Instalação Rápida (Recomendada)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA
```

### Passo 2: Executar o Setup Automático

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
python setup.py
```

### Passo 3: Abrir o Portal Web

Depois do setup, execute:

```bash
# Ativar o ambiente virtual (se não estiver ativo)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Iniciar o portal
python -m src.portal.app
```

### Passo 4: Acessar no Navegador

Abra seu navegador e acesse:
```
http://localhost:5000
```

## 🐳 Opção 2: Usar Docker (Mais Fácil)

Se você tem Docker instalado:

```bash
# Clonar o repositório
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA

# Iniciar com Docker
docker-compose up -d
```

Depois acesse: http://localhost:5000

## 🎯 Opção 3: Instalação Manual Passo a Passo

### Passo 1: Clonar

```bash
git clone https://github.com/pilzcarlos-rgb/Normas-APS-IA.git
cd Normas-APS-IA
```

### Passo 2: Criar Ambiente Virtual

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

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Inicializar o Banco de Dados

```bash
python -c "from src.models import init_database; init_database()"
```

### Passo 5: Abrir o Portal

```bash
python -m src.portal.app
```

### Passo 6: Acessar

Abra: http://localhost:5000

## 🔍 Comandos Úteis

### Verificar se está funcionando
```bash
# Ver se o servidor está rodando
curl http://localhost:5000
```

### Parar o servidor
```
Pressione CTRL+C no terminal
```

### Ver dados de exemplo
```bash
python examples/usage_example.py
```

### Coletar dados reais
```bash
python main.py
# ou
python scripts/collect_data.py
```

## ❓ Problemas Comuns

### Erro: "Porta 5000 já em uso"

**Solução:** Use outra porta:
```bash
python -c "from src.portal.app import run_portal; run_portal(port=8080)"
```
Depois acesse: http://localhost:8080

### Erro: "ModuleNotFoundError"

**Solução:** Ative o ambiente virtual e reinstale:
```bash
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Erro: "Python não encontrado"

**Solução:** Instale Python 3.8+:
- Windows: https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt install python3 python3-pip`

## 📱 Usando o Sistema

Depois de abrir no navegador:

1. **Navegar por Tema** - Clique em um dos temas (Financiamento, Organização, etc.)
2. **Buscar por Ano** - Use o seletor de ano (2010-2025)
3. **Filtrar por Status** - Clique em "Vigentes", "Revogadas" ou "Alteradas"
4. **Ver Normas Estruturantes** - Lista principal de normas-chave

## 🆘 Precisa de Ajuda?

1. Consulte `PROXIMOS_PASSOS.md` para guia completo
2. Consulte `README.md` para documentação técnica
3. Veja exemplos em `examples/usage_example.py`
4. Abra uma issue no GitHub

## ✅ Checklist Rápido

- [ ] Python 3.8+ instalado
- [ ] Repositório clonado
- [ ] Setup executado (./setup.sh ou python setup.py)
- [ ] Ambiente virtual ativado
- [ ] Portal iniciado (python -m src.portal.app)
- [ ] Navegador aberto em http://localhost:5000

---

**Dica:** Use Docker se quiser o método mais rápido! Apenas rode `docker-compose up -d` e está pronto! 🚀
