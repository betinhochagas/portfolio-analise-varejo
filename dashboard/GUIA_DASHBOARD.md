# 📈 Guia — Construindo o Dashboard

Fonte de dados: **`dados/tratado/vendas_tratado.csv`** (já limpo pelo ETL).

O objetivo é um dashboard de 1 página que responda: *"Como vão as vendas?"*

---

## Opção A — Looker Studio (100% online, grátis, gera link para o portfólio) ⭐

**Recomendado para portfólio** porque você compartilha um **link público** que o
recrutador clica e vê o dashboard ao vivo.

1. Acesse https://lookerstudio.google.com (login com conta Google).
2. **Criar → Relatório → Fazer upload de arquivos (CSV)** → envie `vendas_tratado.csv`.
3. Monte os elementos abaixo.
4. **Compartilhar → Qualquer pessoa com o link pode ver** → copie o link para o README.

## Opção B — Power BI Desktop (o BI nº 1 da vaga)

1. Abra o Power BI Desktop → **Obter dados → Texto/CSV** → `vendas_tratado.csv`.
2. Confirme os tipos de coluna (data como Data, valores como Número decimal).
3. Monte os mesmos elementos abaixo.
4. Salve como `dashboard/dashboard_varejo.pbix` e exporte um PDF/print para o README.

---

## 🧱 Elementos do dashboard (valem para as duas ferramentas)

### Linha de KPIs (cartões no topo)
| Cartão | Métrica |
|--------|---------|
| Faturamento | `SUM(valor_total)` |
| Lucro | `SUM(lucro)` |
| Ticket médio | `AVG(valor_total)` |
| Nº de vendas | `COUNT(venda_id)` |
| Margem % | `SUM(lucro) / SUM(valor_total)` |

### Gráficos
1. **Linha** — Faturamento por `ano_mes` (evolução no tempo)
2. **Barras** — Faturamento por `categoria`
3. **Barras horizontais** — Top 10 `produto` por faturamento
4. **Pizza/Rosca** — Faturamento por `regiao`
5. **Barras** — Faturamento por `canal`
6. **Mapa** (opcional no Looker) — Faturamento por `cidade`

### Filtros (segmentações)
- `ano` · `categoria` · `regiao` · `canal`

---

## 🎨 Dicas de apresentação
- Formate valores como moeda (R$) e use separador de milhar.
- Título claro no topo: **"Painel de Vendas — Varejo"**.
- Paleta sóbria (azuis/verdes), poucos textos, foco nos números.
- Deixe 1 insight escrito no rodapé (ex.: *"Eletrônicos lideram, mas Alimentos têm maior margem"*).

Quando terminar, salve o link (Looker) ou o `.pbix` + print (Power BI) nesta pasta
e adicione o link/print no `README.md`.
