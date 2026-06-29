from rest_framework import serializers

from .models import Moto


class MotoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Moto
        fields = [
            "id",
            "marca",
            "modelo",
            "cilindrada",
            "precio",
            "stock",
            "descripcion",
            "imagen",
            "imagen_url",
            "creado",
            "actualizado",
        ]
        read_only_fields = ["id", "creado", "actualizado", "imagen_url"]
        extra_kwargs = {
            # 'imagen' se escribe pero no se devuelve cruda; se expone via imagen_url
            "imagen": {"write_only": True, "required": False},
        }

    def get_imagen_url(self, obj):
        if not obj.imagen:
            return None
        request = self.context.get("request")
        url = obj.imagen.url
        return request.build_absolute_uri(url) if request else url
