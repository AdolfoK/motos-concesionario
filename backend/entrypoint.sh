#!/bin/sh
set -e

echo "Esperando a PostgreSQL en ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
python <<'PY'
import os
import time
import psycopg2

host = os.environ.get("POSTGRES_HOST", "db")
port = os.environ.get("POSTGRES_PORT", "5432")
db = os.environ.get("POSTGRES_DB", "concesionaria")
user = os.environ.get("POSTGRES_USER", "concesionaria")
pwd = os.environ.get("POSTGRES_PASSWORD", "concesionaria")

for intento in range(1, 31):
    try:
        psycopg2.connect(host=host, port=port, dbname=db, user=user, password=pwd).close()
        print("PostgreSQL disponible.")
        break
    except Exception as exc:  # noqa: BLE001
        print(f"  intento {intento}/30: {exc}")
        time.sleep(2)
else:
    raise SystemExit("No se pudo conectar a PostgreSQL.")
PY

echo "Generando migraciones de las apps..."
python manage.py makemigrations catalogo reservas --noinput

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Cargando datos iniciales (seed)..."
python manage.py seed

echo "Recolectando archivos estaticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor Gunicorn..."
exec gunicorn concesionaria.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -
