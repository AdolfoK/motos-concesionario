from rest_framework.routers import DefaultRouter

from .views import MotoViewSet

router = DefaultRouter()
router.register(r"motos", MotoViewSet, basename="moto")

urlpatterns = router.urls
