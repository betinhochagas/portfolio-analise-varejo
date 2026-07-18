# dbt — Transformacao (Fase 2)

Projeto dbt que transforma a camada `raw` (bronze, criada na Fase 1) em um
**modelo estrela** consumivel pelo BI, com testes de qualidade e documentacao.

## Arquitetura das camadas
```
varejo_raw.raw_vendas   (bronze — carga da Fase 1)
        │
        ▼
staging/ stg_vendas      (view: limpeza 1:1)        -> dataset varejo_staging
        │
        ▼
marts/   dim_produto ─┐
         dim_local  ──┼─►  fct_vendas  (modelo estrela) -> dataset varejo_marts
         dim_tempo  ─┘
```

## Pre-requisitos
- Fase 1 concluida (tabela `varejo_raw.raw_vendas` existe no BigQuery).
- Autenticado via `gcloud auth application-default login` (mesma auth da Fase 1).
- `GCP_PROJECT_ID` definido no ambiente.

## Como rodar (PowerShell, a partir da pasta `dbt/`)
```powershell
# 1. Instalar o dbt-bigquery (de preferencia num venv)
pip install -r ../requirements-dbt.txt

# 2. Configurar o perfil de conexao
#    Copie profiles.yml.example para  ~/.dbt/profiles.yml
#    OU aponte o dbt para esta pasta:
$env:DBT_PROFILES_DIR = "."
$env:GCP_PROJECT_ID = "seu-projeto-id"

# 3. Instalar pacotes (dbt_utils) e validar a conexao
dbt deps
dbt debug

# 4. Construir tudo (models + testes de qualidade)
dbt build

# 5. Gerar e servir a documentacao + lineage (grafo)
dbt docs generate
dbt docs serve
```

## O que isto demonstra (competencias de DE)
- Transformacao **versionada em SQL** com camadas staging -> marts (medallion).
- **Modelo dimensional** (fato + dimensoes) com surrogate keys (`dbt_utils`).
- **Testes de qualidade**: `unique`, `not_null`, `relationships`, `accepted_values`.
- **Documentacao e lineage** automaticos (`dbt docs`).
- **Idempotencia**: `dbt build` recria os models de forma reprodutivel.
