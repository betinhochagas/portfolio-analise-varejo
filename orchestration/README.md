# Orquestracao — Airflow em Docker (Fase 4)

Orquestra o pipeline `carregar_raw -> dbt_deps -> dbt_run -> dbt_test` com
**Apache Airflow** rodando em **Docker** (a forma indicada de usar Airflow no
Windows). Agendamento diario, com **retry** automatico em caso de falha.

```
inicio -> carregar_raw -> dbt_deps -> dbt_run -> dbt_test -> fim
             (04.py)       (dbt na venv isolada /opt/dbt-venv)
```

## Pre-requisitos
- **Docker Desktop** instalado e rodando.
- Fase 1 e Fase 2 prontas (script de carga + projeto dbt).
- Autenticado via `gcloud auth application-default login` (gera o arquivo ADC).

## Passo a passo (PowerShell, a partir de `orchestration/`)
```powershell
cd "C:\Engenharia de Dados\portfolio-varejo\orchestration"

# 1. Configurar o ambiente
copy .env.example .env
#    Edite .env: coloque seu GCP_PROJECT_ID e confira o GCP_ADC_PATH.

# 2. Subir o Airflow (build da imagem na 1a vez pode demorar alguns minutos)
docker compose up -d --build

# 3. Abrir a interface
#    http://localhost:8080   (login: admin / admin)

# 4. Ativar e disparar a DAG "pipeline_varejo" (toggle + botao Trigger).

# 5. Parar tudo quando terminar
docker compose down
```

## Como a autenticacao funciona (sem segredos no repo)
- O arquivo ADC do host (`GCP_ADC_PATH`) e montado **read-only** em
  `/opt/airflow/gcp/adc.json`.
- `GOOGLE_APPLICATION_CREDENTIALS` aponta para ele → o script de carga e o dbt
  autenticam automaticamente.
- O `.gitignore` bloqueia `.env`, logs e qualquer `*-key.json`.

## O que isto demonstra (competencias de DE)
- **Orquestracao** real com Airflow (DAG, dependencias, agendamento, retry).
- **Containerizacao** com Docker (ambiente reprodutivel, isolado do Windows).
- **Separacao de dependencias** (dbt em venv isolada da imagem do Airflow).
- Pipeline **de ponta a ponta**: ingestao → warehouse → transformacao → testes.

## Observacoes
- Imagem fixada em `apache/airflow:2.9.3` (comandos `webserver` / `db migrate`).
- LocalExecutor + Postgres (sem Celery/Redis) para manter leve.
- Quando a **Fase 3 (dlt)** existir, a task `carregar_raw` da lugar a ingestao real.
