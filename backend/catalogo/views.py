from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .models import Moto
from .serializers import MotoSerializer


class MotoViewSet(viewsets.ModelViewSet):
    """
    CRUD del catalogo de motos.

    - Lectura (list / retrieve): publica, para que los clientes vean el catalogo.
    - Escritura (create / update / delete): solo administradores autenticados
      (permiso heredado de IsAuthenticatedOrReadOnly en settings).
    """

    queryset = Moto.objects.all()
    serializer_class = MotoSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filterset_fields = ["marca", "cilindrada"]
    search_fields = ["marca", "modelo", "descripcion"]
    ordering_fields = ["precio", "cilindrada", "marca", "creado"]
