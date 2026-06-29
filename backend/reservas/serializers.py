from rest_framework import serializers

from .models import Reserva


class ReservaSerializer(serializers.ModelSerializer):
    tipo_servicio_display = serializers.CharField(
        source="get_tipo_servicio_display", read_only=True
    )

    class Meta:
        model = Reserva
        fields = [
            "id",
            "nombre_cliente",
            "telefono",
            "tipo_servicio",
            "tipo_servicio_display",
            "fecha",
            "bloque_horario",
            "moto_marca",
            "moto_modelo",
            "patente",
            "comentario",
            "estado",
            "creado",
        ]
        read_only_fields = ["id", "estado", "creado", "tipo_servicio_display"]
