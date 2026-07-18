"""
03_construir_notebook.py
------------------------
Monta o notebook de analise exploratoria (notebooks/analise_vendas.ipynb)
usando nbformat. Depois basta executar com nbconvert para embutir os graficos.
"""
import nbformat as nbf
import os

nb = nbf.v4.new_notebook()
cells = []

def md(txt):
    cells.append(nbf.v4.new_markdown_cell(txt))

def code(src):
    cells.append(nbf.v4.new_code_cell(src))

md("""# Analise de Vendas de Varejo

**Portfolio de Analise de Dados**

Este notebook explora uma base de vendas de varejo (12.000 transacoes) para
responder perguntas de negocio e gerar insights estrategicos.

**Ferramentas:** Python (pandas, matplotlib, seaborn) + SQL (SQLite)

**Etapas:** os dados ja passaram por um processo de ETL
(`scripts/02_etl.py`) que limpou, padronizou e enriqueceu a base bruta.
""")

md("## 1. Importacao e carga dos dados")
code("""import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.titlesize"] = 13

df = pd.read_csv("../dados/tratado/vendas_tratado.csv", encoding="utf-8-sig",
                 parse_dates=["data_venda"])
print(f"Linhas: {len(df):,} | Colunas: {df.shape[1]}")
df.head()""")

md("## 2. Visao geral (KPIs)")
code("""faturamento = df["valor_total"].sum()
lucro = df["lucro"].sum()
ticket_medio = df["valor_total"].mean()
margem = lucro / faturamento * 100

print(f"Faturamento total..: R$ {faturamento:,.2f}")
print(f"Lucro total........: R$ {lucro:,.2f}")
print(f"Ticket medio.......: R$ {ticket_medio:,.2f}")
print(f"Margem media.......: {margem:.1f}%")
print(f"Itens vendidos.....: {df['quantidade'].sum():,}")
print(f"Periodo............: {df['data_venda'].min():%d/%m/%Y} a {df['data_venda'].max():%d/%m/%Y}")""")

md("## 3. Faturamento por categoria")
code("""cat = (df.groupby("categoria")["valor_total"].sum()
         .sort_values(ascending=False))

ax = cat.plot(kind="bar", color="#2563eb")
ax.set_title("Faturamento por Categoria")
ax.set_xlabel("")
ax.set_ylabel("Faturamento (R$)")
for i, v in enumerate(cat):
    ax.text(i, v, f"R${v/1e6:.1f}M", ha="center", va="bottom", fontsize=9)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("../imagens/01_faturamento_categoria.png", dpi=120, bbox_inches="tight")
plt.show()""")

md("""**Insight:** Eletronicos concentra a maior fatia do faturamento, mas
categorias como Alimentos e Vestuario tem margem percentual muito maior.
Vale analisar o equilibrio entre volume (Eletronicos) e rentabilidade.""")

md("## 4. Evolucao mensal do faturamento")
code("""mensal = df.groupby("ano_mes")["valor_total"].sum()

ax = mensal.plot(kind="line", marker="o", color="#16a34a")
ax.set_title("Evolucao Mensal do Faturamento")
ax.set_xlabel("")
ax.set_ylabel("Faturamento (R$)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../imagens/02_evolucao_mensal.png", dpi=120, bbox_inches="tight")
plt.show()""")

md("## 5. Participacao por regiao")
code("""regiao = (df.groupby("regiao")["valor_total"].sum()
            .sort_values(ascending=False))

ax = regiao.plot(kind="pie", autopct="%1.1f%%", startangle=90,
                 colors=sns.color_palette("Blues_r", len(regiao)))
ax.set_title("Participacao no Faturamento por Regiao")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("../imagens/03_regiao.png", dpi=120, bbox_inches="tight")
plt.show()""")

md("## 6. Margem de lucro por categoria")
code("""margem_cat = (df.groupby("categoria")
                .apply(lambda g: g["lucro"].sum() / g["valor_total"].sum() * 100)
                .sort_values(ascending=False))

ax = margem_cat.plot(kind="barh", color="#f59e0b")
ax.set_title("Margem de Lucro (%) por Categoria")
ax.set_xlabel("Margem (%)")
ax.set_ylabel("")
for i, v in enumerate(margem_cat):
    ax.text(v, i, f" {v:.1f}%", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("../imagens/04_margem_categoria.png", dpi=120, bbox_inches="tight")
plt.show()""")

md("## 7. Desempenho por canal de venda")
code("""canal = (df.groupby("canal")
           .agg(faturamento=("valor_total", "sum"),
                ticket_medio=("valor_total", "mean"),
                vendas=("venda_id", "count"))
           .sort_values("faturamento", ascending=False))
canal""")

md("""## 8. Conclusoes e recomendacoes

- **Eletronicos** lidera o faturamento (volume), enquanto **Alimentos e
  Vestuario** entregam as maiores margens -> oportunidade de impulsionar
  categorias rentaveis via cross-sell.
- O **faturamento cresce ao longo do periodo**, com sazonalidade clara em
  alguns meses -> planejar estoque e campanhas para os picos.
- A regiao **Sudeste** concentra a maior parte das vendas -> avaliar
  potencial de expansao nas regioes menos exploradas.
- Canais **digitais (E-commerce/App)** merecem atencao pelo ticket medio.

> Proximos passos: construir o dashboard no Power BI / Looker Studio para
> acompanhamento continuo desses indicadores.
""")

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12"},
}

os.makedirs("notebooks", exist_ok=True)
caminho = os.path.join("notebooks", "analise_vendas.ipynb")
with open(caminho, "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print(f"[OK] Notebook criado: {caminho}")
