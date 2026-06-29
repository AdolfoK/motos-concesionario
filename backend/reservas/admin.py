from django.contrib import admin

from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_cliente",
        "tipo_servicio",
        "fecha",
        "bloque_horario",
        "estado",
        "creado",
    )
    list_filter = ("estado", "tipo_servicio", "fecha")
    search_fields = ("nombre_cliente", "telefono", "patente")
    list_editable = ("estado",)
