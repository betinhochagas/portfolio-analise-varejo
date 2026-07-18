"""
04_carregar_bigquery.py — Fase 1 do roadmap de Engenharia de Dados.

Carrega o CSV tratado na camada `raw` (bronze) de um Data Warehouse no
Google BigQuery. Esta é a fronteira entre o pipeline local e a nuvem.

Caracteristicas de Engenharia de Dados demonstradas aqui:
  - Schema explicito (tipagem controlada, nao "autodetect")
  - Carga idempotente (WRITE_TRUNCATE: rodar de novo nao duplica dados)
  - Configuracao por variaveis de ambiente (nada de credencial no codigo)
  - Criacao do dataset sob demanda (create-if-not-exists)

Pre-requisitos:
  1. Projeto no Google Cloud (pode ser o BigQuery Sandbox, sem cartao).
  2. Autenticacao local via Application Default Credentials (ADC):
        gcloud auth application-default login
  3. pip install -r requirements-bigquery.txt

Uso (PowerShell):
    $env:GCP_PROJECT_ID = "seu-projeto-id"
    python scripts/04_carregar_bigquery.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from google.cloud import bigquery

# --------------------------------------------------------------------------- #
# Configuracao (via variaveis de ambiente, com defaults sensatos)
# --------------------------------------------------------------------------- #
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")          # obrigatorio
DATASET = os.environ.get("BQ_DATASET", "varejo_raw")   # camada bronze
TABLE = os.environ.get("BQ_TABLE", "raw_vendas")
LOCATION = os.environ.get("BQ_LOCATION", "US")         # ou "southamerica-east1"

# Caminho do CSV tratado (relativo a raiz do projeto)
CSV_PATH = Path(__file__).resolve().parent.parent / "dados" / "tratado" / "vendas_tratado.csv"

# Schema explicito da camada raw — espelha o CSV tratado (23 colunas).
SCHEMA = [
    bigquery.SchemaField("venda_id", "INT64"),
    bigquery.SchemaField("data_venda", "DATE"),
    bigquery.SchemaField("ano", "INT64"),
    bigquery.SchemaField("mes", "INT64"),
    bigquery.SchemaField("ano_mes", "STRING"),
    bigquery.SchemaField("trimestre", "STRING"),
    bigquery.SchemaField("dia_semana", "STRING"),
    bigquery.SchemaField("produto_id", "INT64"),
    bigquery.SchemaField("produto", "STRING"),
    bigquery.SchemaField("categoria", "STRING"),
    bigquery.SchemaField("quantidade", "INT64"),
    bigquery.SchemaField("preco_unitario", "FLOAT64"),
    bigquery.SchemaField("desconto", "FLOAT64"),
    bigquery.SchemaField("custo_unitario", "FLOAT64"),
    bigquery.SchemaField("custo_total", "FLOAT64"),
    bigquery.SchemaField("valor_total", "FLOAT64"),
    bigquery.SchemaField("lucro", "FLOAT64"),
    bigquery.SchemaField("margem_pct", "FLOAT64"),
    bigquery.SchemaField("regiao", "STRING"),
    bigquery.SchemaField("cidade", "STRING"),
    bigquery.SchemaField("canal", "STRING"),
    bigquery.SchemaField("forma_pagamento", "STRING"),
    bigquery.SchemaField("cliente_id", "INT64"),
]


def main() -> None:
    if not PROJECT_ID:
        sys.exit(
            "ERRO: defina a variavel de ambiente GCP_PROJECT_ID.\n"
            '  PowerShell:  $env:GCP_PROJECT_ID = "seu-projeto-id"'
        )
    if not CSV_PATH.exists():
        sys.exit(f"ERRO: CSV nao encontrado em {CSV_PATH}. Rode antes o scripts/02_etl.py.")

    client = bigquery.Client(project=PROJECT_ID, location=LOCATION)
    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET)
    table_ref = dataset_ref.table(TABLE)

    # 1) Cria o dataset (camada bronze) se ainda nao existir.
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = LOCATION
    client.create_dataset(dataset, exists_ok=True)
    print(f"[OK] Dataset pronto: {PROJECT_ID}.{DATASET} ({LOCATION})")

    # 2) Configura a carga: CSV, cabecalho, schema explicito, idempotente.
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,               # ignora o cabecalho
        schema=SCHEMA,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # idempotente
    )

    print(f"[..] Carregando {CSV_PATH.name} -> {DATASET}.{TABLE} ...")
    with CSV_PATH.open("rb") as fonte:
        load_job = client.load_table_from_file(fonte, table_ref, job_config=job_config)
    load_job.result()  # aguarda concluir

    # 3) Confere o resultado.
    tabela = client.get_table(table_ref)
    print(f"[OK] Carga concluida: {tabela.num_rows} linhas, {len(tabela.schema)} colunas.")
    print(f"     Tabela: {PROJECT_ID}.{DATASET}.{TABLE}")


if __name__ == "__main__":
    main()
