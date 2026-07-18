# Infra — Terraform (Fase 5)

Cria os datasets do BigQuery (`varejo_raw`, `varejo_staging`, `varejo_marts`)
como **codigo**, de forma versionada e reproduzivel — em vez de criar na mao
pelo console.

## Pre-requisitos
- [Terraform](https://developer.hashicorp.com/terraform/install) instalado.
- Autenticado via `gcloud auth application-default login`.

## Passo a passo (PowerShell, a partir de `infra/`)
```powershell
cd "C:\Engenharia de Dados\portfolio-varejo\infra"

copy terraform.tfvars.example terraform.tfvars
#   Edite terraform.tfvars: coloque seu project_id.

terraform init      # baixa o provider google
terraform plan      # mostra o que sera criado (revise!)
terraform apply     # cria os datasets (confirme com "yes")
```
Para remover tudo depois: `terraform destroy`.

## Observacoes
- O `google_bigquery_dataset.varejo_raw` pode coexistir com o
  `scripts/04_carregar_bigquery.py` (que usa `exists_ok=True`). Com o Terraform,
  o dataset passa a ser **gerenciado por IaC** — o ideal.
- O `.gitignore` bloqueia `*.tfstate` (pode conter metadados sensiveis) e
  `terraform.tfvars`. Em time, o state fica num backend remoto (GCS).

## O que isto demonstra (competencias de DE)
- **Infraestrutura como codigo** (IaC) com Terraform.
- Recursos parametrizados (`for_each`, `variables`) — DRY, sem repeticao.
- Ambiente **reproduzivel e versionado** (cria/destroi identico em segundos).
