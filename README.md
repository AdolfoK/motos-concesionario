# Concesionaria de Motos — Plataforma Web

Implementación de referencia de la **plataforma web para una concesionaria de
motos** descrita en el trabajo *"Arquitectura Híbrida y Planificación DevSecOps"*.

Incluye:

- **Catálogo administrable** (CRUD) con login de administrador.
- **Módulo de reserva de horas de servicio técnico vía WhatsApp** (flujo
  simplificado: la solicitud se registra y el cliente la confirma por WhatsApp).

## Arquitectura (mapeo con el documento)

| Componente | Tecnología | En la nube (producción) |
|-----------|------------|--------------------------|
| Frontend  | React + Vite, servido por nginx | AWS (cómputo, ALB, multi-AZ) |
| Backend   | Django REST Framework (Python 3.10) | AWS (cómputo) |
| Base de datos | PostgreSQL | Azure Database for PostgreSQL |
| Imágenes  | Almacenamiento local (media) | Azure Blob Storage |

Las imágenes Docker usan versiones fijadas (`python:3.10-slim-bullseye`,
`node:20-alpine`, `nginx:1.25-alpine`) tal como exige el documento.

## Requisitos

- Docker Desktop con Docker Compose.

## Cómo ejecutarlo (local)

```bash
# (opcional) personalizar variables
cp .env.example .env

# levantar todo
docker compose up --build
```

Servicios:

- **Frontend (web):** http://localhost:8080
- **API backend:** http://localhost:8000/api/
- **Admin de Django:** http://localhost:8000/admin/

Usuario administrador por defecto: **admin / admin123**
(se crea automáticamente junto con motos de ejemplo).

## Módulo de reservas por WhatsApp

1. El cliente entra a **Reservar hora**, completa el formulario y envía.
2. El backend guarda la reserva (trazabilidad) y devuelve un enlace `wa.me`
   con el mensaje pre-llenado.
3. Se abre WhatsApp con la concesionaria para confirmar la hora.

El número de destino se configura con la variable `WHATSAPP_NUMERO`
(formato internacional, sin `+` ni espacios; por defecto `56912345678`).

## Endpoints principales

| Método | Ruta | Acceso |
|--------|------|--------|
| POST | `/api/auth/login/` | Público (devuelve JWT) |
| GET  | `/api/motos/` | Público |
| POST/PATCH/DELETE | `/api/motos/` | Solo admin |
| POST | `/api/reservas/` | Público (devuelve `whatsapp_url`) |
| GET  | `/api/reservas/` | Solo admin |

## Detener

```bash
docker compose down          # conserva los datos
docker compose down -v       # elimina también la base de datos
```
