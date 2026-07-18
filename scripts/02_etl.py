"""
02_etl.py
---------
ETL (Extract, Transform, Load) da base de varejo.

  EXTRACT  -> le dados/bruto/vendas_bruto.csv
  TRANSFORM-> limpa, padroniza e enriquece os dados
  LOAD     -> grava:
                * dados/tratado/vendas_tratado.csv   (para o BI/Power BI)
                * dados/tratado/varejo.db  (SQLite - modelo estrela p/ SQL)

O objetivo e transformar dado bruto e "sujo" em dado confiavel e pronto
para analise. Cada etapa esta comentada e reporta o que foi corrigido.
"""

import os
import sqlite3
import numpy as np
import pandas as pd

PASTA_BRUTO = os.path.join("dados", "bruto")
PASTA_TRATADO = os.path.join("dados", "tratado")
os.makedirs(PASTA_TRATADO, exist_ok=True)


def log(msg):
    print(f"  - {msg}")


# ===========================================================================
# EXTRACT
# ===========================================================================
print("[1/3] EXTRACT - lendo base bruta...")
df = pd.read_csv(os.path.join(PASTA_BRUTO, "vendas_bruto.csv"), encoding="utf-8-sig")
linhas_inicio = len(df)
log(f"{linhas_inicio:,} linhas lidas")


# ===========================================================================
# TRANSFORM
# ===========================================================================
print("\n[2/3] TRANSFORM - limpando e padronizando...")

# 1) Remove linhas duplicadas
antes = len(df)
df = df.drop_duplicates(subset="venda_id", keep="first")
log(f"Duplicatas removidas: {antes - len(df):,}")

# 2) Padroniza texto das categorias (tira espacos, corrige maiuscula/minuscula)
df["categoria"] = (
    df["categoria"].astype(str).str.strip().str.title()
)
# Corrige acentuacao/nome padronizado
df["categoria"] = df["categoria"].replace({
    "Casa E Decoracao": "Casa e Decoracao",
})
log(f"Categorias padronizadas: {sorted(df['categoria'].unique())}")

# 3) Padroniza forma de pagamento (pix, PIX, Pix -> 'Pix')
df["forma_pagamento"] = (
    df["forma_pagamento"].astype(str).str.strip().str.title()
)
df["forma_pagamento"] = df["forma_pagamento"].replace({"Nan": np.nan})
log("Formas de pagamento padronizadas")

# 4) Trata valores nulos
#    - cidade nula -> "Nao Informado"
#    - forma_pagamento nula -> moda (valor mais frequente)
n_cidade = df["cidade"].isnull().sum()
df["cidade"] = df["cidade"].fillna("Nao Informado")
moda_pag = df["forma_pagamento"].mode()[0]
n_pag = df["forma_pagamento"].isnull().sum()
df["forma_pagamento"] = df["forma_pagamento"].fillna(moda_pag)
log(f"Nulos tratados -> cidade: {n_cidade} | forma_pagamento: {n_pag} (preenchido com '{moda_pag}')")

# 5) Normaliza datas (mistura de AAAA-MM-DD e DD/MM/AAAA -> datetime)
def parse_data(valor):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return pd.to_datetime(valor, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["data_venda"] = df["data_venda"].apply(parse_data)
n_data_ruim = df["data_venda"].isnull().sum()
df = df.dropna(subset=["data_venda"])
log(f"Datas normalizadas (linhas com data invalida removidas: {n_data_ruim})")

# 6) Corrige valores_total negativos (erro de sistema) -> valor absoluto
n_neg = (df["valor_total"] < 0).sum()
df["valor_total"] = df["valor_total"].abs()
log(f"Valores negativos corrigidos: {n_neg}")

# 7) Enriquecimento - colunas calculadas uteis para analise
df["custo_total"] = (df["custo_unitario"] * df["quantidade"]).round(2)
df["lucro"] = (df["valor_total"] - df["custo_total"]).round(2)
df["margem_pct"] = np.where(
    df["valor_total"] > 0,
    (df["lucro"] / df["valor_total"] * 100).round(1),
    0,
)
df["ano"] = df["data_venda"].dt.year
df["mes"] = df["data_venda"].dt.month
df["ano_mes"] = df["data_venda"].dt.strftime("%Y-%m")
df["dia_semana"] = df["data_venda"].dt.day_name()
df["trimestre"] = "T" + df["data_venda"].dt.quarter.astype(str)
log("Colunas calculadas: custo_total, lucro, margem_pct, ano, mes, ano_mes, dia_semana, trimestre")

# 8) Ordena colunas e por data
colunas = [
    "venda_id", "data_venda", "ano", "mes", "ano_mes", "trimestre", "dia_semana",
    "produto_id", "produto", "categoria",
    "quantidade", "preco_unitario", "desconto",
    "custo_unitario", "custo_total", "valor_total", "lucro", "margem_pct",
    "regiao", "cidade", "canal", "forma_pagamento", "cliente_id",
]
df = df[colunas].sort_values("data_venda").reset_index(drop=True)

log(f"Linhas finais: {len(df):,} (de {linhas_inicio:,} originais)")


# ===========================================================================
# LOAD
# ===========================================================================
print("\n[3/3] LOAD - gravando saidas...")

# 1) CSV tratado (fonte para Power BI / Looker Studio)
caminho_csv = os.path.join(PASTA_TRATADO, "vendas_tratado.csv")
df.to_csv(caminho_csv, index=False, encoding="utf-8-sig")
log(f"CSV tratado: {caminho_csv}")

# 2) Modelo estrela no SQLite (para praticar/mostrar SQL)
caminho_db = os.path.join(PASTA_TRATADO, "varejo.db")
if os.path.exists(caminho_db):
    os.remove(caminho_db)
con = sqlite3.connect(caminho_db)

# Dimensao Produto
dim_produto = (
    df[["produto_id", "produto", "categoria", "custo_unitario", "preco_unitario"]]
    .drop_duplicates(subset="produto_id")
    .sort_values("produto_id")
    .reset_index(drop=True)
)

# Dimensao Local
dim_local = (
    df[["regiao", "cidade"]]
    .drop_duplicates()
    .sort_values(["regiao", "cidade"])
    .reset_index(drop=True)
)
dim_local.insert(0, "local_id", range(1, len(dim_local) + 1))

# Dimensao Tempo
dim_tempo = (
    df[["data_venda", "ano", "mes", "ano_mes", "trimestre", "dia_semana"]]
    .drop_duplicates(subset="data_venda")
    .sort_values("data_venda")
    .reset_index(drop=True)
)

# Tabela Fato (com chave de local)
fato = df.merge(dim_local, on=["regiao", "cidade"], how="left")
fato_vendas = fato[[
    "venda_id", "data_venda", "produto_id", "local_id", "cliente_id",
    "quantidade", "preco_unitario", "desconto",
    "custo_total", "valor_total", "lucro", "canal", "forma_pagamento",
]]

dim_produto.to_sql("dim_produto", con, index=False, if_exists="replace")
dim_local.to_sql("dim_local", con, index=False, if_exists="replace")
dim_tempo.to_sql("dim_tempo", con, index=False, if_exists="replace")
fato_vendas.to_sql("fato_vendas", con, index=False, if_exists="replace")

con.commit()
con.close()
log(f"Banco SQLite (modelo estrela): {caminho_db}")
log("Tabelas: fato_vendas, dim_produto, dim_local, dim_tempo")

print("\n[OK] ETL concluido com sucesso!")
