from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import Reserva
from .serializers import ReservaSerializer
from .whatsapp import construir_url


class ReservaViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Reservas de servicio tecnico.

    - create: publico. Registra la solicitud y devuelve el enlace de WhatsApp
      pre-llenado para que el cliente confirme con la concesionaria.
    - list / retrieve: solo administradores (para revisar las solicitudes).
    """

    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserva = serializer.save()
        data = self.get_serializer(reserva).data
        data["whatsapp_url"] = construir_url(reserva)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=201, headers=headers)
