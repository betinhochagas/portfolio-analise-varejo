# CLAUDE.md

Contexto do projeto para assistentes de IA (Claude Code) e colaboradores.

## Visão geral
Projeto de portfólio de **Análise de Dados** de varejo: pipeline end-to-end que vai do dado bruto ("sujo") até o dashboard, cobrindo ETL, modelagem, SQL, análise em Python e Business Intelligence. Os dados são **fictícios** (gerados com Faker) para fins de demonstração.

## Estrutura
```
dados/bruto/        CSV bruto gerado (com nulos, duplicados, datas inconsistentes)
dados/tratado/      CSV limpo (vendas_tratado.csv), CSV p/ BI (vendas_looker.csv), SQLite (varejo.db)
scripts/            01_gerar_dados.py -> 02_etl.py -> 03_construir_notebook.py
sql/analises.sql    10 consultas de negócio (JOIN, window functions, CTE)
notebooks/          análise exploratória com gráficos
imagens/            gráficos exportados (usados no README)
dashboard/          guia de construção do dashboard
```

## Como rodar o pipeline
```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
python scripts/01_gerar_dados.py  # gera a base bruta
python scripts/02_etl.py          # limpa + gera CSV tratado e SQLite (modelo estrela)
python scripts/03_construir_notebook.py
```
O ETL usa **semente fixa** (reprodutível). Ordem importa: 01 → 02 → 03.

## Modelo de dados (SQLite `dados/tratado/varejo.db`)
Modelo estrela: `fato_vendas` + `dim_produto`, `dim_local`, `dim_tempo`.

## Dashboard (BI)
Construído no **Looker Studio** a partir de `dados/tratado/vendas_looker.csv`.
- KPIs: Faturamento, Lucro, Ticket médio, Nº de vendas, Margem %
- Gráficos: evolução mensal, faturamento por categoria, por região, por canal

## Convenções
- Código e comentários em **português** (público-alvo).
- Números reprodutíveis (seeds fixas). Não commitar `.venv/`.
- `valor_total` é o faturamento; margem = SUM(lucro)/SUM(valor_total).

## Stack
Python (pandas, numpy, matplotlib, seaborn, Faker, SQLAlchemy) · SQL/SQLite · Jupyter · Looker Studio · Git
