"""
01_gerar_dados.py
------------------
Gera uma base de dados FICTICIA de varejo, simulando um sistema de vendas real.

De proposito, os dados vem com "sujeira" (valores nulos, duplicados, textos
inconsistentes, precos negativos). Isso e intencional: o script de ETL
(02_etl.py) sera responsavel por limpar tudo isso -- exatamente como acontece
no dia a dia de um Analista de Dados.

Saida: dados/bruto/vendas_bruto.csv
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker

# Semente fixa -> resultados reproduziveis (mesma base toda vez que roda)
random.seed(42)
np.random.seed(42)
fake = Faker("pt_BR")
Faker.seed(42)

# Caminho de saida
PASTA_BRUTO = os.path.join("dados", "bruto")
os.makedirs(PASTA_BRUTO, exist_ok=True)

# ---------------------------------------------------------------------------
# 1) Catalogo de produtos (categoria -> lista de produtos e faixa de preco)
# ---------------------------------------------------------------------------
CATALOGO = {
    "Eletronicos": [
        ("Smartphone", 800, 3500), ("Notebook", 2000, 6000),
        ("Fone de Ouvido", 50, 900), ("Smart TV", 1500, 5000),
        ("Tablet", 600, 2500), ("Mouse Gamer", 40, 350),
    ],
    "Vestuario": [
        ("Camiseta", 25, 120), ("Calca Jeans", 60, 250),
        ("Tenis", 90, 600), ("Jaqueta", 100, 450), ("Vestido", 70, 380),
    ],
    "Casa e Decoracao": [
        ("Luminaria", 40, 300), ("Jogo de Panelas", 120, 700),
        ("Almofada", 20, 90), ("Cortina", 60, 280),
    ],
    "Alimentos": [
        ("Cafe Especial", 20, 80), ("Chocolate Premium", 10, 60),
        ("Azeite Extra Virgem", 25, 90),
    ],
    "Esportes": [
        ("Bola de Futebol", 40, 200), ("Halteres", 80, 400),
        ("Bicicleta", 500, 3000),
    ],
    "Beleza": [
        ("Perfume", 90, 500), ("Kit Skincare", 60, 350),
        ("Secador de Cabelo", 70, 400),
    ],
}

REGIOES = {
    "Norte": ["Manaus", "Belem"],
    "Nordeste": ["Salvador", "Recife", "Fortaleza"],
    "Centro-Oeste": ["Brasilia", "Goiania"],
    "Sudeste": ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte"],
    "Sul": ["Curitiba", "Porto Alegre", "Florianopolis"],
}
# Pesos realistas: concentracao de vendas segue o mercado brasileiro
# (Sudeste dominante, Norte com menor participacao)
PESO_REGIAO = {
    "Sudeste": 44, "Sul": 20, "Nordeste": 19, "Centro-Oeste": 9, "Norte": 8,
}

FORMAS_PAGAMENTO = ["Cartao de Credito", "Cartao de Debito", "Pix", "Boleto", "Dinheiro"]
CANAIS = ["Loja Fisica", "E-commerce", "App"]

# ---------------------------------------------------------------------------
# 2) Monta a lista de produtos com IDs
# ---------------------------------------------------------------------------
produtos = []
pid = 1000
for categoria, itens in CATALOGO.items():
    for nome, custo_min, venda_max in itens:
        preco_custo = round(random.uniform(custo_min, custo_min * 1.4), 2)
        preco_venda = round(random.uniform(preco_custo * 1.3, venda_max), 2)
        produtos.append({
            "produto_id": pid,
            "produto": nome,
            "categoria": categoria,
            "preco_custo": preco_custo,
            "preco_venda": preco_venda,
        })
        pid += 1
df_produtos = pd.DataFrame(produtos)

# ---------------------------------------------------------------------------
# 3) Gera as vendas (tabela fato)
# ---------------------------------------------------------------------------
N_VENDAS = 12000
registros = []

for i in range(N_VENDAS):
    prod = df_produtos.sample(1).iloc[0]
    regiao = random.choices(
        list(PESO_REGIAO.keys()), weights=list(PESO_REGIAO.values())
    )[0]
    cidade = random.choice(REGIOES[regiao])

    # Data de venda entre 2024-01-01 e 2025-12-31
    data = fake.date_between(start_date="-30M", end_date="today")

    quantidade = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 12, 8, 5])[0]
    desconto = random.choices([0, 0.05, 0.10, 0.15, 0.20], weights=[55, 20, 12, 8, 5])[0]
    preco_unit = prod["preco_venda"]
    valor_total = round(preco_unit * quantidade * (1 - desconto), 2)

    registros.append({
        "venda_id": 100000 + i,
        "data_venda": data.strftime("%Y-%m-%d"),
        "produto_id": prod["produto_id"],
        "produto": prod["produto"],
        "categoria": prod["categoria"],
        "preco_unitario": preco_unit,
        "quantidade": quantidade,
        "desconto": desconto,
        "valor_total": valor_total,
        "regiao": regiao,
        "cidade": cidade,
        "canal": random.choice(CANAIS),
        "forma_pagamento": random.choice(FORMAS_PAGAMENTO),
        "cliente_id": random.randint(1, 800),
        "custo_unitario": prod["preco_custo"],
    })

df = pd.DataFrame(registros)

# ---------------------------------------------------------------------------
# 4) INTRODUZ SUJEIRA DE PROPOSITO (para o ETL limpar depois)
# ---------------------------------------------------------------------------
# 4.1) Categorias com grafia inconsistente (maiuscula/minuscula, espacos)
mask = df.sample(frac=0.08, random_state=1).index
df.loc[mask, "categoria"] = df.loc[mask, "categoria"].str.upper()
mask2 = df.sample(frac=0.05, random_state=2).index
df.loc[mask2, "categoria"] = "  " + df.loc[mask2, "categoria"] + "  "

# 4.2) Formas de pagamento escritas de formas diferentes
df.loc[df.sample(frac=0.04, random_state=3).index, "forma_pagamento"] = "pix"
df.loc[df.sample(frac=0.03, random_state=4).index, "forma_pagamento"] = "PIX"

# 4.3) Valores nulos em algumas colunas
df.loc[df.sample(frac=0.03, random_state=5).index, "cidade"] = np.nan
df.loc[df.sample(frac=0.02, random_state=6).index, "forma_pagamento"] = np.nan

# 4.4) Alguns valores_total negativos (erro de sistema)
idx_neg = df.sample(frac=0.01, random_state=7).index
df.loc[idx_neg, "valor_total"] = df.loc[idx_neg, "valor_total"] * -1

# 4.5) Linhas duplicadas
duplicatas = df.sample(frac=0.02, random_state=8)
df = pd.concat([df, duplicatas], ignore_index=True)

# 4.6) Datas em formato diferente em parte das linhas (DD/MM/AAAA)
mask_data = df.sample(frac=0.06, random_state=9).index
df.loc[mask_data, "data_venda"] = pd.to_datetime(
    df.loc[mask_data, "data_venda"]
).dt.strftime("%d/%m/%Y")

# Embaralha
df = df.sample(frac=1, random_state=10).reset_index(drop=True)

# ---------------------------------------------------------------------------
# 5) Salva
# ---------------------------------------------------------------------------
caminho = os.path.join(PASTA_BRUTO, "vendas_bruto.csv")
df.to_csv(caminho, index=False, encoding="utf-8-sig")

print(f"[OK] Base bruta gerada: {caminho}")
print(f"     Linhas: {len(df):,}  |  Colunas: {len(df.columns)}")
print(f"     Nulos por coluna:")
print(df.isnull().sum()[df.isnull().sum() > 0].to_string())
