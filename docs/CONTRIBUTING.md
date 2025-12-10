# Guia de Contribuição

Obrigado por contribuir com o Repositório de Normas APS! Este guia ajudará você a adicionar novas normas ou atualizar as existentes.

## 📝 Como Contribuir

### 1. Adicionar uma Nova Norma

#### Passo 1: Identifique a norma
- Verifique se a norma já não está no repositório
- Obtenha o documento oficial (PDF ou link)
- Identifique: tipo, número, data, órgão emissor

#### Passo 2: Adicione ao arquivo `data.js`
Edite o arquivo `data.js` na raiz do projeto e adicione um novo objeto seguindo o padrão:

```javascript
"identificador-unico": {
    type: "portaria",  // ou "resolucao", "lei", "nota", "manual", etc.
    title: "Título completo da norma",
    description: "Descrição breve e objetiva",
    year: 2024,
    number: "3.493/2024",  // opcional
    tags: ["tag1", "tag2", "tag3"],
    essential: true,  // ou false
    links: [
        { text: "Texto oficial", url: "https://..." },
        { text: "PDF", url: "documentos/tipo/arquivo.pdf" }
    ],
    topics: ["Tema 1", "Tema 2"]
}
```

#### Passo 3: Adicione o documento (se aplicável)
Se você tiver o PDF:
1. Baixe o documento oficial
2. Renomeie seguindo o padrão: `tipo-numero-ano.pdf`
3. Coloque na pasta correspondente em `/documentos/`
4. Atualize o link no `data.js`

#### Passo 4: Crie documentação detalhada (opcional)
Use os templates em `/templates/` para criar uma página detalhada da norma:
- Copie o template apropriado
- Preencha todas as seções
- Salve em `/normas/[tipo]/nome-do-arquivo.md`

### 2. Atualizar uma Norma Existente

1. Localize a norma no arquivo `data.js`
2. Atualize as informações necessárias
3. Se a norma foi revogada, adicione essa informação na descrição
4. Atualize os links se mudaram

### 3. Adicionar um Novo Tema

1. Adicione o tema no campo `topics` das normas relacionadas
2. O tema aparecerá automaticamente na navegação "Por Tema"

## 📋 Checklist de Qualidade

Antes de submeter sua contribuição, verifique:

- [ ] A norma tem um identificador único no `data.js`
- [ ] O tipo está correto (portaria, resolucao, lei, nota, manual, etc.)
- [ ] A descrição é clara e objetiva
- [ ] As tags são relevantes e ajudam na busca
- [ ] Os links funcionam e apontam para fontes oficiais
- [ ] Se houver PDF local, o arquivo está na pasta correta
- [ ] A data/ano está correto
- [ ] Os temas estão bem definidos

## 🎨 Padrões de Nomenclatura

### Identificadores no data.js
- Use letras minúsculas
- Separe palavras com hífen
- Inclua tipo e número: `portaria-3493-2024`

### Arquivos PDF
- Padrão: `tipo-numero-ano.pdf`
- Exemplos: 
  - `portaria-3493-2024.pdf`
  - `lei-8080-1990.pdf`
  - `nota-tecnica-01-2024.pdf`

### Arquivos Markdown
- Use nomes descritivos
- Separe palavras com hífen
- Exemplo: `portaria-2436-2017.md`

## 🏷️ Tags Recomendadas

Use tags consistentes para facilitar a busca:
- **Financiamento**: `financiamento`, `cofinanciamento`, `repasse`
- **Qualidade**: `qualidade`, `pmaq`, `avaliação`, `indicadores`
- **Sistemas**: `e-sus`, `siaps`, `cnes`, `ine`, `cadastro`
- **Saúde Bucal**: `saúde bucal`, `ceo`, `esb`
- **Equipes**: `esf`, `eap`, `nasf`, `equipes`
- **Processo**: `acolhimento`, `território`, `agenda`

## 🚀 Processo de Revisão

1. Submeta um Pull Request com suas mudanças
2. Aguarde a revisão de um mantenedor
3. Faça ajustes se solicitado
4. Sua contribuição será mesclada!

## 💡 Dicas

- **Fontes Oficiais**: Sempre use links de fontes oficiais (bvsms.saude.gov.br, planalto.gov.br, etc.)
- **Atualidade**: Priorize normas vigentes e recentes
- **Clareza**: Escreva descrições que um gestor possa entender rapidamente
- **Essenciais**: Marque como `essential: true` apenas normas realmente fundamentais

## ❓ Dúvidas

Se tiver dúvidas sobre como contribuir:
1. Abra uma [Issue](../../issues) no GitHub
2. Consulte exemplos no arquivo `data.js`
3. Revise as normas já documentadas

## 📞 Contato

Para questões sobre o repositório, abra uma Issue ou entre em contato com os mantenedores.

---

**Obrigado por contribuir para melhorar o acesso à informação na APS!** 🎉
