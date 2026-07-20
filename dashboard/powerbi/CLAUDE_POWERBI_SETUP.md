# 🤝 Claude ↔ Power BI — o melhor setup (pesquisa verificada · jan/2026)

> Fruto de uma pesquisa profunda com verificação adversarial de fontes (Microsoft
> Learn, GitHub oficial, blogs técnicos). Cada item marca a **confiança** e as
> **ressalvas**. Contexto do Roberto: **Power BI Desktop gratuito** (sem Premium/
> Fabric) no **Windows 11**, com o **MCP oficial da Microsoft já instalado**.

---

## 🎯 A conclusão em uma frase
O caminho mais robusto e **de graça** para o Claude fazer o máximo no Power BI é
tratar o modelo como **código-texto (.pbip + TMDL)** — o Claude edita medidas,
colunas e relações como arquivos, versionados em git — **complementado** pelo MCP
oficial (edição via conversa) e por ferramentas externas gratuitas (Tabular Editor 2,
DAX Studio). A **construção de visuais** continua sendo o ponto que mais depende da
GUI (ou de um MCP da comunidade, que tem risco).

---

## 1. O que o Claude CONSEGUE automatizar hoje (grátis, local)
| Tarefa | Como | Confiança |
|--------|------|-----------|
| Criar/editar **medidas DAX** (incl. `formatString`) | MCP oficial **ou** editar TMDL | Alta |
| Criar/editar **colunas, tabelas, relações** | MCP oficial **ou** TMDL | Alta |
| **Versionar** o modelo em git (diff limpo por objeto) | formato **.pbip + TMDL** | Alta |
| **Ler/inspecionar** um `.pbix` existente | MCP `pbixray` (só leitura) | Alta |
| **Validar** boas práticas (BPA) localmente | Tabular Editor 2 (grátis) | Média* |

\* BPA local via Tabular Editor 2 é viável, mas não foi verificado passo-a-passo na pesquisa.

## 2. O que ainda depende da GUI (ou tem ressalva)
- **Montar visuais** (cartões, gráficos, layout): o MCP **oficial NÃO** faz isso — ele
  mexe só no **modelo** (dados/medidas), não no **relatório**. Autoria de visual por IA
  só existe em MCP da comunidade (item 5), em *preview* e não auditado.
- **Ver as mudanças de TMDL**: o Power BI Desktop **não detecta** edição externa de
  arquivo — é preciso **fechar e reabrir o Desktop** para ele recarregar. *(Verificado,
  fonte oficial.)* Já a escrita via MCP/XMLA numa instância local **aparece na hora**.

---

## 3. MCP oficial da Microsoft (o que você já tem) — ajustar as flags
Repo: `github.com/microsoft/powerbi-modeling-mcp` · versão 0.4.0 · **Public Preview**.

Flags corretas (⚠️ corrige o que estava no handoff):
- `--readwrite` → **liga a escrita**; pede confirmação **uma vez por database** (via
  protocolo *MCP Elicitation*), não a cada edição.
- `--skipconfirmation` → aprova as escritas **sem** perguntar (é isto que destrava o
  Claude Code **não-interativo**, que hoje auto-recusa a confirmação).
- `--readonly` → modo seguro (bloqueia qualquer escrita). É o efeito prático de hoje.

**Conecta a:** arquivos do Desktop aberto · workspaces do Fabric · **pastas .pbip/TMDL**.

> Trade-off honesto do `--skipconfirmation`: ganha automação total, perde a “trava de
> segurança” que confirma antes de mudar o modelo. Como o modelo aqui é de portfólio
> (fictício) e está em git, o risco é baixo — dá pra reverter qualquer mudança.

---

## 4. Formato .pbip + TMDL (Developer Mode) — a peça central
- **.pbip** salva relatório + modelo como **texto plano** em pastas (git-friendly).
- **TMDL** = o modelo em texto, **um arquivo por objeto** (cada tabela, papel, cultura)
  → `git diff` limpo e merge sem dor. Feito para ser **legível/editável** por humano —
  e por isso pelo Claude, direto como arquivo.
- Cuidados: usa **tabs** (não espaços); salvar **UTF-8 sem BOM**; caminhos < 260 chars.
- Ainda em **preview** (deve virar padrão do .pbip no lançamento final).

---

## 5. Ferramentas “model as code” que combinam com o Claude
| Ferramenta | Custo | Para quê | Vale p/ você? |
|-----------|-------|----------|---------------|
| **Tabular Editor 2** | **Grátis** | Editar modelo, rodar **BPA** local, escrever `formatString` em massa | ✅ Sim |
| **DAX Studio** | **Grátis** | Testar/medir performance de DAX, rodar queries | ✅ Sim |
| **ALM Toolkit** | Grátis | Comparar/deployar diffs de modelo | Opcional |
| **Tabular Editor 3** | Pago | IDE completo (debugger DAX, VertiPaq Analyzer) | ❌ Não agora |
| **semantic-link-labs** (Python `sempy_labs`) | Grátis (lib) | TOM via XMLA + **BPA em massa** | ⚠️ Escrita XMLA no Service exige **Premium/Fabric** — você não tem. Só serve local/limitado |

External Tools (Tabular Editor 2, DAX Studio, ALM Toolkit) aparecem numa faixa do
Power BI Desktop e escrevem no modelo **em memória** (mudanças sincronizam no canvas).

---

## 6. MCP servers da comunidade (opcionais — mais poder, mais risco)
> ⚠️ Todos são **projetos de autor único**, contagens de ferramentas **auto-reportadas**
> (não auditadas), alguns pré-1.0. Avaliar segurança antes de usar em algo sério.

| Projeto | Destaque | Ressalva |
|---------|----------|----------|
| **sulaiman013/powerbi-mcp** | ~78 ferramentas; **autoria de relatório (PBIR): adiciona página/visual** + refactor seguro que renomeia no modelo E atualiza os visuais | É o **único** jeito de IA montar visual — mas em *preview*, não auditado; recursos cloud pedem Premium |
| **gurvinder-dhillon/powerbi-mcp** | Roda **DAX via REST** contra dataset **publicado** no Service | Exige publicar no Service + Service Principal (client secret) |
| **jonaolden/pbixray-mcp** | **Só leitura** de `.pbix` (13 ferramentas: medidas DAX, tabelas, M, relações) | Seguro (não altera nada). Ótimo p/ o Claude “ler” um pbix |
| **d0nk3yhm/pbix-mcp** | Diz ter 101 ferramentas | ❌ A alegação de ler/escrever .pbix em Python puro **foi REFUTADA** na pesquisa |

---

## 7. Skills / plugins do Claude para Power BI
- **Não há** skill/plugin **oficial da Anthropic** para Power BI/DAX (não encontrado na pesquisa).
- Existe iniciativa da comunidade **`pbi-cli`** (“dar ao Claude Code as skills de Power BI”) —
  não verificada a fundo; tratar como experimental.
- **Recomendação:** criar um **skill de projeto próprio** que ensine ao Claude as nossas
  convenções (import com locale en-US, nomes de medida ≠ coluna, `formatString` R$/%,
  a regra do *restart* após editar TMDL). Baixo custo, alto retorno de consistência.

---

## 8. Fluxo recomendado para o SEU caso (grátis, local)
1. **Adotar .pbip/TMDL**: salvar o projeto como `.pbip` (Developer Mode). O Claude passa
   a editar medidas/formatos/relações **como arquivos** → você **reabre o Desktop** p/ ver.
2. **MCP oficial** para sessões interativas (no Claude Desktop, onde você aprova) com
   `--readwrite`; opcional `--skipconfirmation` p/ automação total.
3. **Tabular Editor 2 + DAX Studio** como ferramentas externas gratuitas (validação/BPA).
4. **pbixray-mcp** (opcional) para o Claude ler `.pbix` já existentes.
5. **Visuais**: seguir manual na GUI **ou** testar o MCP da comunidade (sulaiman013) —
   ciente do risco. O resumo executivo e as medidas o Claude já entrega sozinho.

---

*Fontes primárias: Microsoft Learn (projects-overview, projects-dataset, desktop-external-tools,
mcp/mcp-servers-overview), github.com/microsoft/powerbi-modeling-mcp e semantic-link-labs,
tabulareditor.com, sqlbi.com. Pesquisa verificada em 19/07/2026.*
