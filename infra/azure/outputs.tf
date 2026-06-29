# Valores que consume la capa de AWS (via terraform_remote_state) y el .env.

output "pg_fqdn" {
  description = "Host (FQDN) del servidor PostgreSQL."
  value       = azurerm_postgresql_flexible_server.pg.fqdn
}

output "pg_database" {
  description = "Nombre de la base de datos."
  value       = azurerm_postgresql_flexible_server_database.db.name
}

output "pg_admin_user" {
  description = "Usuario administrador de PostgreSQL."
  value       = var.db_admin_user
}

output "storage_account_name" {
  description = "Nombre de la cuenta de almacenamiento (Blob)."
  value       = azurerm_storage_account.sa.name
}

output "storage_account_key" {
  description = "Clave de acceso de la cuenta de almacenamiento."
  value       = azurerm_storage_account.sa.primary_access_key
  sensitive   = true
}

output "storage_container" {
  description = "Contenedor de Blob para las imagenes."
  value       = azurerm_storage_container.media.name
}

output "blob_endpoint" {
  description = "Endpoint base del Blob Storage."
  value       = azurerm_storage_account.sa.primary_blob_endpoint
}
