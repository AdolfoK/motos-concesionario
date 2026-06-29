# =============================================================================
# Capa de DATOS en Azure: PostgreSQL gestionado + Blob Storage para imagenes.
# Equivale a lo descrito en el documento (Azure Database for PostgreSQL y
# Azure Blob Storage), provisionado con Terraform.
# =============================================================================

# Sufijo aleatorio para nombres que deben ser globalmente unicos.
resource "random_string" "sufijo" {
  length  = 6
  upper   = false
  special = false
}

# --- Grupo de recursos --------------------------------------------------------
resource "azurerm_resource_group" "rg" {
  name     = "${var.project_name}-rg"
  location = var.location
}

# --- PostgreSQL Flexible Server ----------------------------------------------
resource "azurerm_postgresql_flexible_server" "pg" {
  name                = "${var.project_name}-pg-${random_string.sufijo.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  version                = "16"
  administrator_login    = var.db_admin_user
  administrator_password = var.db_admin_password

  sku_name   = "B_Standard_B1ms" # Burstable, el mas economico
  storage_mb = 32768             # 32 GB

  # Acceso publico habilitado (controlado por reglas de firewall).
  # En produccion real se usaria integracion con VNet / endpoint privado,
  # tal como exige el documento.
  public_network_access_enabled = true

  zone = "1"

  # Evita que un cambio menor recree el servidor.
  lifecycle {
    ignore_changes = [zone, high_availability]
  }
}

# Base de datos de la aplicacion.
resource "azurerm_postgresql_flexible_server_database" "db" {
  name      = var.db_name
  server_id = azurerm_postgresql_flexible_server.pg.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Regla de firewall: permite el rango de IPs indicado (por defecto, todo: demo).
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow" {
  name             = "permitir-rango"
  server_id        = azurerm_postgresql_flexible_server.pg.id
  start_ip_address = var.allowed_ip_start
  end_ip_address   = var.allowed_ip_end
}

# --- Blob Storage para imagenes de motos -------------------------------------
resource "azurerm_storage_account" "sa" {
  name                     = "${var.project_name}sa${random_string.sufijo.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # Permite blobs con acceso de lectura publica (para servir las imagenes).
  allow_nested_items_to_be_public = true
}

resource "azurerm_storage_container" "media" {
  name                  = "media"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "blob" # lectura publica de los blobs
}
