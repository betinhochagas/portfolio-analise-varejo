# Painel de Vendas — Power BI (guia de construção)

Réplica do dashboard do Looker Studio, agora em **Power BI** (a ferramenta pedida
na maioria das vagas de Analista no Brasil). Mesmo CSV, mesmos KPIs e gráficos.

**Fonte de dados:** `../../dados/tratado/vendas_looker.csv`
**Medidas DAX:** ver [`medidas_dax.md`](medidas_dax.md)

---

## 0. Instalar o Power BI Desktop
- Jeito mais fácil: **Microsoft Store** → busque *"Power BI Desktop"* → Instalar
  (atualiza sozinho). Alternativa: download direto em
  https://www.microsoft.com/pt-br/download/details.aspx?id=58494
- É **gratuito** e roda só no **Windows**.

---

## 1. Importar o CSV com o LOCALE correto ⚠️ (passo que evita erro de números)
O CSV usa **ponto** como decimal (ex.: `290.04`), mas o Windows pt-BR usa vírgula.
Se importar sem cuidado, `290.04` vira `29.004`. Faça assim:

1. **Página Inicial → Obter dados → Texto/CSV** → selecione
   `dados/tratado/vendas_looker.csv`.
2. Na prévia, clique em **Transformar Dados** (NÃO clique em "Carregar" ainda) —
   abre o **Power Query**.
3. Para **cada coluna decimal** abaixo, clique no **ícone de tipo** (no cabeçalho)
   → **Usando Localidade...** → Tipo: **Número Decimal** → Localidade:
   **Inglês (Estados Unidos)** → OK:
   - `preco_unitario`, `desconto`, `custo_unitario`, `custo_total`,
     `valor_total`, `lucro`, `margem_pct`
4. Confira que `data_venda` está como **Data** (formato ISO AAAA-MM-DD é lido ok;
   se vier errado, use "Usando Localidade → Data → Inglês (EUA)").
5. As colunas inteiras (`venda_id`, `ano`, `mes`, `quantidade`, `produto_id`,
   `cliente_id`) podem ficar como **Número Inteiro**.
6. **Página Inicial → Fechar e Aplicar**.

> ✅ Teste rápido: crie a medida `Faturamento` (passo 2) — tem que dar
> **R$ 12.229.507,07**. Se der um número gigante/estranho, o locale não foi aplicado.

---

## 2. Criar as medidas
Abra [`medidas_dax.md`](medidas_dax.md) e crie as 5 medidas
(**Modelagem → Nova medida**), ajustando o formato de cada uma.

---

## 3. Montar os visuais (replicando o Looker)

**Linha de KPIs (topo)** — 5 visuais do tipo **Cartão** (`Card`):
| Cartão | Campo |
|--------|-------|
| Faturamento | medida `Faturamento` |
| Lucro | medida `Lucro` |
| Ticket Médio | medida `Ticket Médio` |
| Nº de Vendas | medida `Nº de Vendas` |
| Margem % | medida `Margem %` |

**Gráficos:**
| Visual | Tipo | Eixo / Categoria | Valor |
|--------|------|------------------|-------|
| Evolução mensal | **Gráfico de linhas** | `ano_mes` | `Faturamento` |
| Faturamento por categoria | **Barras/Colunas** | `categoria` | `Faturamento` |
| Faturamento por região | **Barras/Colunas** | `regiao` | `Faturamento` |
| Vendas por canal | **Rosca (Donut)** | `canal` | `Faturamento` |

Dica de layout: KPIs numa faixa no topo; linha ocupando a largura no meio;
as 3 barras/rosca embaixo. Ordene as barras por valor decrescente
(seta no canto do visual → "Classificar eixo").

---

## 4. Formatar e salvar
- Título do relatório: **"Painel de Vendas — Varejo"**.
- Tema: **Exibir → Temas** (escolha um escuro pra combinar com o Looker, se quiser).
- Salve como: `dashboard/powerbi/painel_vendas.pbix`.
- Exporte um print da tela como `imagens/06_powerbi_dashboard.png` para o README
  principal.

---

## O que isto demonstra
- **Power BI** (requisito "indispensável" de muitas vagas): importação, tratamento
  no **Power Query**, **medidas DAX**, e construção de dashboard.
- **Atenção a locale/tipos** — problema real de dados que você sabe resolver.
- Mesma análise, **duas ferramentas de BI** (Looker + Power BI) no portfólio.
