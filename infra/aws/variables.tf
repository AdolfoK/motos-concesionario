variable "project_name" {
  description = "Prefijo para nombrar los recursos."
  type        = string
  default     = "concesionaria"
}

variable "aws_region" {
  description = "Region de AWS (la del documento)."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Tipo de instancia EC2 (t3.micro es elegible para Free Tier)."
  type        = string
  default     = "t3.micro"
}

variable "ssh_public_key" {
  description = "Contenido de tu clave publica SSH (id_rsa.pub) para acceder a la instancia."
  type        = string
}

variable "my_ip_cidr" {
  description = "Tu IP publica en formato CIDR (ej: 190.1.2.3/32) para restringir el acceso SSH."
  type        = string
}

variable "repo_url" {
  description = "URL del repositorio Git (publico) a clonar en la instancia."
  type        = string
  default     = "https://github.com/AdolfoK/motos-concesionario.git"
}

variable "repo_branch" {
  description = "Rama a desplegar."
  type        = string
  default     = "main"
}

# --- Valores de la aplicacion (se inyectan en el .env del servidor) ----------
variable "db_admin_password" {
  description = "Contrasena de PostgreSQL (la MISMA que usaste en infra/azure)."
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Clave secreta de Django para produccion."
  type        = string
  sensitive   = true
}

variable "django_admin_password" {
  description = "Contrasena del usuario administrador de la app."
  type        = string
  sensitive   = true
  default     = "admin123"
}

variable "whatsapp_numero" {
  description = "Numero de WhatsApp de la concesionaria (formato internacional sin + ni espacios)."
  type        = string
  default     = "56912345678"
}
