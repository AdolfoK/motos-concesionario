from django.db import models


class Reserva(models.Model):
    """
    Solicitud de hora de servicio tecnico hecha por un cliente.

    El flujo se simplifica mediante WhatsApp: la reserva se registra en la
    base de datos (trazabilidad ACID) y, al confirmarla, el cliente es
    redirigido a WhatsApp con un mensaje pre-llenado dirigido a la
    concesionaria, que coordina y confirma la hora definitiva.
    """

    class TipoServicio(models.TextChoices):
        MANTENCION = "mantencion", "Mantencion"
        REVISION = "revision_tecnica", "Revision tecnica"
        REPARACION = "reparacion", "Reparacion"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"

    nombre_cliente = models.CharField(max_length=120)
    telefono = models.CharField(max_length=30)
    tipo_servicio = models.CharField(
        max_length=20, choices=TipoServicio.choices
    )
    fecha = models.DateField()
    bloque_horario = models.CharField(
        max_length=20, help_text="Ej: 09:00-10:00"
    )
    moto_marca = models.CharField(max_length=80)
    moto_modelo = models.CharField(max_length=80)
    patente = models.CharField(max_length=15, blank=True, default="")
    comentario = models.TextField(blank=True, default="")
    estado = models.CharField(
        max_length=12, choices=Estado.choices, default=Estado.PENDIENTE
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self) -> str:
        return f"{self.nombre_cliente} - {self.get_tipo_servicio_display()} ({self.fecha})"
