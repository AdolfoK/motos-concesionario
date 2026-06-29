#!/bin/bash
set -euxo pipefail
exec > /var/log/user-data.log 2>&1

# --- Swap de 2GB: evita que el build de React agote la RAM en t3.micro ---
if [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

# --- Docker + Git ---
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y git
curl -fsSL https://get.docker.com | sh
usermod -aG docker ubuntu

# --- Clonar el repositorio ---
cd /opt
git clone -b ${repo_branch} ${repo_url} app
cd app

# --- Archivo .env con la configuracion de produccion (Azure + negocio) ---
cat > .env <<ENVEOF
DJANGO_SECRET_KEY=${django_secret_key}
DJANGO_ALLOWED_HOSTS=${allowed_hosts}
POSTGRES_DB=${pg_database}
POSTGRES_USER=${pg_user}
POSTGRES_PASSWORD=${pg_password}
POSTGRES_HOST=${pg_host}
POSTGRES_PORT=5432
AZURE_STORAGE_ACCOUNT=${storage_account}
AZURE_STORAGE_KEY=${storage_key}
AZURE_STORAGE_CONTAINER=${storage_container}
WHATSAPP_NUMERO=${whatsapp_numero}
DJANGO_ADMIN_USER=admin
DJANGO_ADMIN_PASSWORD=${admin_password}
ENVEOF

# --- Levantar la aplicacion ---
docker compose -f docker-compose.cloud.yml up -d --build
