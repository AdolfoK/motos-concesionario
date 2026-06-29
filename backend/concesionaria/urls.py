"""Rutas raiz del proyecto."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def health(_request):
    """Endpoint de salud usado por el balanceador / docker healthcheck."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    # Autenticacion JWT (login de administradores)
    path("api/auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    # Modulos
    path("api/", include("catalogo.urls")),
    path("api/", include("reservas.urls")),
]

# En desarrollo Django sirve los archivos de media (imagenes de motos).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
