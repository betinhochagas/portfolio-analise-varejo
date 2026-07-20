# 🔧 Ações para você (Roberto) — instalar ferramentas, migrar p/ .pbip, MCP da comunidade

> São 3 blocos. Faça na ordem. Onde é "clique na tela", só você consegue (GUI).
> O que dava pra automatizar, eu já fiz (venvs, downloads de código, config do pbixray).

---

## ✅ O que EU já deixei pronto (não precisa fazer nada)
- Instalei o **pbixray-mcp** (só-leitura de `.pbix`) num venv dedicado e **adicionei ao `.mcp.json`**.
  → Passa a valer **após você reiniciar o Claude Code**. Depois disso eu consigo *ler* o conteúdo
  de qualquer `.pbix` (medidas, tabelas, M, relações) — útil pra auditar o painel atual.
- Baixei o código do MCP da comunidade e instalei o subset offline (bloco 3 abaixo).
- Criei um **skill** (`.claude/skills/powerbi-varejo`) com nossas convenções — passo a usar sozinho.

---

## 1. Instalar as 2 ferramentas gratuitas (External Tools)

Ambas são **grátis** e, depois de instaladas, aparecem sozinhas numa faixa **"Ferramentas Externas"**
no Power BI Desktop (ligam no modelo aberto e conseguem escrever nele).

### Tabular Editor 2 (grátis, open-source)
- Site oficial: **https://github.com/TabularEditor/TabularEditor/releases** (baixe o instalador `.msi` mais recente)
  — ou pela loja de comando: `winget search TabularEditor` e instale o ID que aparecer.
- Para que serve: editar medidas em massa, aplicar `formatString`, e rodar o **Best Practice Analyzer
  (BPA)** localmente (aponta problemas de modelagem/DAX — ótimo pra portfólio).

### DAX Studio (grátis)
- Site oficial: **https://daxstudio.org/downloads/** (baixe o instalador do Windows).
- Para que serve: testar consultas DAX, medir performance, exportar dados.

> Depois de instalar as duas, **reabra o Power BI Desktop** com o `painel_vendas` e confira a faixa
> **"Ferramentas Externas"**. Se elas aparecerem lá, deu certo.

---

## 2. Migrar o projeto para .pbip (Developer Mode) — a peça central

Isso transforma o modelo em **arquivos de texto (TMDL)** que eu edito direto e versiono em git.
É o que mais destrava o meu trabalho (crio/edito medidas, colunas e relações sem depender da GUI).

**Passos no Power BI Desktop:**
1. **Arquivo → Opções e configurações → Opções**.
2. Em **Recursos de visualização (Preview features)**, marque:
   - ☑ **Salvar como Projeto do Power BI (.pbip)**
   - ☑ **Armazenar modelo semântico usando formato TMDL** (se aparecer separado)
3. **OK** e **reinicie o Power BI Desktop**.
4. Abra o `painel_vendas.pbix`, depois **Arquivo → Salvar como → tipo `.pbip`**, salvando em
   `dashboard/powerbi/` (pode manter o nome `painel_vendas`).
5. Resultado: surge uma pasta `painel_vendas.SemanticModel/definition/` com arquivos `.tmdl`
   (um por tabela/medida). **Me avise quando fizer** — aí eu passo a editar o modelo por ali.

> ⚠️ **Regra de ouro:** quando EU editar um arquivo `.tmdl`, o Power BI Desktop **não percebe sozinho**.
> Você precisa **fechar e reabrir** o Desktop para ver as mudanças. (É uma limitação oficial confirmada.)

---

## 3. (Opcional / experimental) MCP da comunidade — para IA montar VISUAIS

Este é o único caminho de eu montar cartões/gráficos (autoria PBIR) sobre um projeto `.pbip`, **offline**.
⚠️ É projeto de **autor único, em preview, não auditado** — por isso o Claude Code **me impediu** de
registrá-lo automaticamente. Você adiciona manualmente se topar o risco (baixo, pois só mexe em arquivos
locais do projeto e está em git — dá pra reverter).

**Eu já baixei o código e instalei as dependências offline.** Falta só você colar este bloco dentro de
`"mcpServers"` no arquivo **`C:\Engenharia de Dados\.mcp.json`** (depois da entrada `"pbixray"`, separando
com vírgula) e **reiniciar o Claude Code**:

```json
    "powerbi-community": {
      "type": "stdio",
      "command": "C:\\Engenharia de Dados\\mcp-tools\\powerbi-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Engenharia de Dados\\mcp-tools\\powerbi-mcp\\src\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Engenharia de Dados\\mcp-tools\\powerbi-mcp\\src"
      }
    }
```

> Sem as libs .NET (ADOMD), a **conexão ao vivo** com o Desktop fica indisponível — mas a **edição de
> `.pbip`/TMDL e a autoria de visuais (PBIR) funcionam** (é o que interessa). Se um dia quiser conexão ao
> vivo, aí sim precisaria instalar o SSMS/ADOMD.NET.

---

## Resumo do que muda depois disso
| Antes | Depois |
|-------|--------|
| Eu só leio o modelo; você monta tudo na GUI | Eu **crio/edito medidas, formatos, colunas e relações** como texto |
| Sem histórico do modelo | Modelo **versionado em git** (diff limpo) |
| Visuais 100% manuais | Visuais **automatizáveis** via MCP da comunidade (opcional) |
| Sem validação de boas práticas | **BPA** local no Tabular Editor 2 |
