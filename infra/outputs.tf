output "datasets_criados" {
  description = "Datasets do BigQuery gerenciados pelo Terraform."
  value       = { for k, ds in google_bigquery_dataset.camada : k => ds.dataset_id }
}
