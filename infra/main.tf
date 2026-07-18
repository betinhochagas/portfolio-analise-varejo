# Infraestrutura como codigo (IaC) — cria os datasets do BigQuery por codigo,
# em vez de clicar no console. Autenticacao via ADC
# (gcloud auth application-default login), a mesma das outras fases.

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
}

# As tres camadas do pipeline (medallion): raw -> staging -> marts.
locals {
  camadas = {
    raw     = var.dataset_raw
    staging = var.dataset_staging
    marts   = var.dataset_marts
  }
}

resource "google_bigquery_dataset" "camada" {
  for_each                   = local.camadas
  dataset_id                 = each.value
  location                   = var.location
  description                = "Camada '${each.key}' do pipeline de varejo (gerenciado via Terraform)."
  delete_contents_on_destroy = true

  labels = {
    projeto = "portfolio-varejo"
    camada  = each.key
  }
}
