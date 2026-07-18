"""
DAG: pipeline_varejo — Fase 4 do roadmap de Engenharia de Dados.

Orquestra o fluxo do dado ate o modelo estrela no BigQuery:

    carregar_raw  ->  dbt_deps  ->  dbt_run  ->  dbt_test

- carregar_raw : roda scripts/04_carregar_bigquery.py (CSV -> camada raw)
- dbt_deps     : baixa pacotes do dbt (dbt_utils)
- dbt_run      : constroi staging + marts (modelo estrela)
- dbt_test     : roda os testes de qualidade (unique, not_null, relationships...)

O dbt roda numa virtualenv isolada (/opt/dbt-venv) para nao conflitar com o
Airflow. As credenciais vem via ADC (GOOGLE_APPLICATION_CREDENTIALS), montado
pelo docker-compose. Nenhum segredo no codigo.

Obs.: quando a Fase 3 (dlt) existir, a primeira task passa a ser a ingestao real.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

PROJECT_DIR = "/opt/airflow/project"
DBT_DIR = f"{PROJECT_DIR}/dbt"
DBT = "/opt/dbt-venv/bin/dbt"  # dbt na venv isolada

default_args = {
    "owner": "roberto",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="pipeline_varejo",
    description="Ingestao raw -> dbt (staging + marts estrela) no BigQuery",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["varejo", "bigquery", "dbt"],
) as dag:

    inicio = EmptyOperator(task_id="inicio")

    carregar_raw = BashOperator(
        task_id="carregar_raw",
        bash_command=f"python {PROJECT_DIR}/scripts/04_carregar_bigquery.py",
    )

    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"cd {DBT_DIR} && {DBT} deps",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && {DBT} run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && {DBT} test",
    )

    fim = EmptyOperator(task_id="fim")

    inicio >> carregar_raw >> dbt_deps >> dbt_run >> dbt_test >> fim
