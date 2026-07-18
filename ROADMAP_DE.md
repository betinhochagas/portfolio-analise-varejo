# 🛣️ Roadmap — Evolução para Engenharia de Dados

> Plano para evoluir este projeto (hoje um portfólio de **Analista de Dados**:
> Faker → pandas → SQLite → Looker) para um portfólio de **Engenharia de Dados**
> com stack de dados moderna. Pensado para **Windows**, ecossistema **Google**
> (BigQuery + Looker já em uso) e **free-tier**.

---

## 🎯 Arquitetura-alvo

```
Fonte real ──► Ingestão ──► Data Warehouse ──► Transformação ──► BI / consumo
 (API/CSV)     (dlt/Python)   (BigQuery)         (dbt)            (Looker)
                    │                                │
                    └──── Orquestração (Airflow/Dagster) ────┘
                              │
      Qualidade (dbt tests) · CI/CD (GitHub Actions) · IaC (Terraform) · Docker
```

O recrutador de DE precisa ver **5 pilares**: **nuvem**, **transformação como
código (dbt)**, **orquestração**, **testes de qualidade** e **automação
(CI/CD)**. O resto é diferencial.

---

## 📦 Fases

### Fase 0 — Reposicionamento (½ dia)
- Novo repo `pipeline-varejo-dataeng` (ou renomear) — deixar claro que é projeto
  de **Engenharia**, não de Analista.
- README com **diagrama de arquitetura** e a frase-chave: *"pipeline batch
  idempotente, do dado bruto ao mart analítico, orquestrado e testado."*
- Estrutura do modern data stack (`ingestion/`, `dbt/`, `orchestration/`,
  `infra/`, `.github/`).

### Fase 1 — Nuvem: BigQuery como Data Warehouse (1–2 dias) ⭐
**O pulo do gato.** Sai o SQLite, entra o BigQuery (free-tier: 10 GB
armazenamento + 1 TB query/mês).
- Integração natural com Google/Looker → o Looker passa a ler do **BigQuery**.
- Camada **`raw`** (bronze): dado cru, como chegou.
- **Deliverable:** dataset `varejo_raw` no BigQuery, carregado.

### Fase 2 — dbt: transformação como código (2–3 dias) ⭐
Coração de um portfólio DE moderno.
- `dbt-bigquery` com camadas **staging → intermediate → marts** (padrão
  medallion: bronze / silver / gold).
- Recriar o modelo estrela (`fato_vendas` + dimensões) **como models
  versionados em SQL**.
- **Testes** (`not_null`, `unique`, `relationships`, `accepted_values`).
- `dbt docs` gera **catálogo + lineage** automático (ótimo screenshot pro README).

### Fase 3 — Ingestão de fonte real (1–2 dias) ⭐
Trocar o Faker por dado não fictício — maior sinal de maturidade.
- Opções free: **API pública** (câmbio, IBGE, e-commerce público) ou o dataset
  **Online Retail** (UCI/Kaggle, transações reais de varejo).
- Ferramenta: **[dlt](https://dlthub.com)** (data load tool, Python nativo,
  incremental) — ou Python + `requests`.
- Provar **carga incremental** e **idempotência** (rodar 2x não duplica).

### Fase 4 — Orquestração (2–3 dias) ⭐
Nada de rodar `01/02/03` na mão.
- **Airflow** (via Docker) — padrão de mercado, melhor pro currículo. Ou
  **Dagster/Prefect** (mais leves no Windows, Python-nativo).
- Um DAG: `ingestão → dbt run → dbt test`, com **retry, agendamento e alerta**.
- No Windows, rodar tudo em **Docker Compose**.

### Fase 5 — Automação & Qualidade (1–2 dias)
- **CI/CD com GitHub Actions:** em cada PR, rodar `dbt build` + `sqlfluff`
  (lint de SQL). Basta adicionar `.github/workflows/`.
- **Terraform (IaC):** criar os datasets do BigQuery via código, não pela UI.
- **Docker:** empacotar o ambiente (reprodutível em qualquer máquina).

### Fase 6 — Diferenciais (opcional)
Streaming (Pub/Sub + BigQuery), PySpark num dataset maior, data contracts,
observabilidade (Elementary / re_data), ou GCP via free-tier ($300 de crédito).

---

## 🛣️ Caminho recomendado (o 80/20)

Se o tempo é curto, **não fazer tudo**. Este MVP já é um portfólio DE respeitável:

> **Fase 1 (BigQuery) + Fase 2 (dbt) + Fase 3 (fonte real) + Fase 4
> (orquestração) + CI/CD da Fase 5.**

Demonstra os 5 pilares. Terraform / Docker / streaming são "cerejas" para depois.

---

## ⚠️ Pontos de atenção
- **Curva de aprendizado real:** dbt e Airflow levam tempo — não é copiar/colar.
  Aprender fazendo isso é exatamente o que qualifica para a vaga.
- **Custo:** tudo cabe no free-tier. Cuidado para não deixar recurso ligado no GCP.
- **Windows:** Airflow nativo no Windows é sofrível → usar **Docker** (ou WSL2).
- Manter o **projeto de Analista** que já está pronto — continua válido. Este é
  um segundo projeto, mais sênior.

---

## ✅ Checklist de progresso

- [ ] Fase 0 — Reposicionamento (estrutura + README de arquitetura)
- [x] Fase 1 — BigQuery como DWH (dataset `raw` carregado) — ✅ **18/07/2026**: `portfolio-varejo.varejo_raw.raw_vendas`, 12.000 linhas, validado (total R$ 12.229.507,07)
- [x] Fase 2 — dbt (staging → marts + testes + docs/lineage) — ✅ **18/07/2026**: `dbt build` PASS=25 (4 models + 20 testes), star schema em `varejo_marts`, docs/lineage gerados
- [ ] Fase 3 — Ingestão de fonte real (dlt, carga incremental idempotente)
- [~] Fase 4 — Orquestração (Airflow/Dagster via Docker) — **scaffolding pronto** em `orchestration/`, falta rodar após as Fases 1–2
- [~] Fase 5 — CI/CD (GitHub Actions) + Terraform + Docker — **scaffolding pronto** (`.github/workflows/`, `infra/`); Docker já na Fase 4
- [ ] Fase 6 — Diferenciais (streaming, Spark, observabilidade)

---
*Documento vivo. Última atualização: 18/07/2026.*
