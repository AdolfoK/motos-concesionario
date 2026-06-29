variable "project_name" {
  description = "Prefijo para nombrar los recursos."
  type        = string
  default     = "concesionaria"
}

variable "location" {
  description = "Region de Azure (colindante con us-east-1 de AWS)."
  type        = string
  default     = "eastus"
}

variable "db_admin_user" {
  description = "Usuario administrador de PostgreSQL."
  type        = string
  default     = "pgadmin"
}

variable "db_admin_password" {
  description = "Contrasena del administrador de PostgreSQL (minimo 8, con mayus/minus/numero)."
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Nombre de la base de datos de la aplicacion."
  type        = string
  default     = "concesionaria"
}

variable "allowed_ip_start" {
  description = "Inicio del rango de IPs permitidas en el firewall de PostgreSQL. Por defecto abre a todo (solo demo)."
  type        = string
  default     = "0.0.0.0"
}

variable "allowed_ip_end" {
  description = "Fin del rango de IPs permitidas en el firewall de PostgreSQL."
  type        = string
  default     = "255.255.255.255"
}
