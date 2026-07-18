# Imagem do Airflow estendida para o pipeline de varejo.
# Estrategia: dbt numa VIRTUALENV ISOLADA (/opt/dbt-venv) para nao conflitar
# com as dependencias fixas do Airflow. O script de carga (04) usa o Python do
# proprio Airflow, com google-cloud-bigquery instalado.
FROM apache/airflow:2.9.3

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
USER airflow

# venv isolada só para o dbt (evita conflito com o Airflow)
RUN python -m venv /opt/dbt-venv \
    && /opt/dbt-venv/bin/pip install --no-cache-dir dbt-bigquery==1.8.2

# lib para o script de carga 04 (compativel com o ambiente do Airflow)
RUN pip install --no-cache-dir google-cloud-bigquery==3.25.0
