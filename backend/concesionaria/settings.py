"""
Configuracion de Django para el proyecto Concesionaria de Motos.

Los valores sensibles y dependientes del entorno se leen de variables de
entorno (inyectadas via docker-compose / GitHub Secrets en produccion),
nunca se hardcodean credenciales en el codigo.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carga un archivo .env si existe (util en desarrollo local sin Docker)
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


# --- Seguridad ---------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "dev-insecure-key-cambiar-en-produccion"
)
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0,backend"
).split(",")

# --- Aplicaciones ------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",
    "corsheaders",
    "django_filters",
    # Apps del proyecto
    "catalogo",
    "reservas",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "concesionaria.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "concesionaria.wsgi.application"

# --- Base de datos -----------------------------------------------------------
# En produccion: Azure Database for PostgreSQL (subred privada).
# En local: contenedor PostgreSQL de docker-compose.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "concesionaria"),
        "USER": os.environ.get("POSTGRES_USER", "concesionaria"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "concesionaria"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# Azure Database for PostgreSQL exige conexiones SSL. Se activa con
# POSTGRES_SSLMODE=require (en local, sin definir, queda deshabilitado).
_pg_sslmode = os.environ.get("POSTGRES_SSLMODE", "")
if _pg_sslmode:
    DATABASES["default"]["OPTIONS"] = {"sslmode": _pg_sslmode}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internacionalizacion ----------------------------------------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# --- Archivos estaticos y media ----------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# En produccion las imagenes de motos se almacenan en Azure Blob Storage.
# En local se sirven desde el sistema de archivos (MEDIA_ROOT).
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Almacenamiento de archivos (media) -------------------------------------
# Si se definen las credenciales de Azure Blob Storage, las imagenes de motos
# se suben alli (como exige el documento). Si no, se usa el disco local.
AZURE_STORAGE_ACCOUNT = os.environ.get("AZURE_STORAGE_ACCOUNT", "")
AZURE_STORAGE_KEY = os.environ.get("AZURE_STORAGE_KEY", "")
AZURE_STORAGE_CONTAINER = os.environ.get("AZURE_STORAGE_CONTAINER", "media")

if AZURE_STORAGE_ACCOUNT and AZURE_STORAGE_KEY:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.azure_storage.AzureStorage",
            "OPTIONS": {
                "account_name": AZURE_STORAGE_ACCOUNT,
                "account_key": AZURE_STORAGE_KEY,
                "azure_container": AZURE_STORAGE_CONTAINER,
                # URL publica directa al blob (contenedor con acceso de lectura).
                "expiration_secs": None,
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Django REST Framework ----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

from datetime import timedelta  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# --- CORS --------------------------------------------------------------------
# El frontend (React/nginx) consume la API. En produccion se restringe al
# dominio publico; en local se permite el origen de desarrollo de Vite.
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost,http://localhost:80,http://localhost:5173,http://127.0.0.1:5173",
).split(",")
CORS_ALLOW_ALL_ORIGINS = env_bool("CORS_ALLOW_ALL_ORIGINS", DEBUG)

# --- Parametros de negocio ---------------------------------------------------
# Numero de WhatsApp de la concesionaria al que llegan las reservas.
# Formato internacional sin '+' ni espacios (ej: 56912345678).
WHATSAPP_NUMERO = os.environ.get("WHATSAPP_NUMERO", "56912345678")
