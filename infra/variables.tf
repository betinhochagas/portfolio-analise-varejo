variable "project_id" {
  type        = string
  description = "ID do projeto no Google Cloud (o mesmo da Fase 1)."
}

variable "location" {
  type        = string
  description = "Regiao/multi-regiao dos datasets. Deve bater com a Fase 1."
  default     = "US"
}

variable "dataset_raw" {
  type        = string
  description = "Dataset da camada bronze (carga da Fase 1)."
  default     = "varejo_raw"
}

variable "dataset_staging" {
  type        = string
  description = "Dataset da camada staging (views do dbt)."
  default     = "varejo_staging"
}

variable "dataset_marts" {
  type        = string
  description = "Dataset da camada marts (modelo estrela do dbt)."
  default     = "varejo_marts"
}
