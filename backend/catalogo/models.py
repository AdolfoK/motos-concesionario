from django.db import models


class Moto(models.Model):
    """Una motocicleta del catalogo de la concesionaria."""

    marca = models.CharField(max_length=80)
    modelo = models.CharField(max_length=80)
    cilindrada = models.PositiveIntegerField(help_text="Cilindrada en cc")
    precio = models.DecimalField(max_digits=12, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True, default="")
    # En produccion la imagen vive en Azure Blob Storage y aqui se persiste
    # la URL/referencia. En local se sube a MEDIA_ROOT.
    imagen = models.ImageField(upload_to="motos/", blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["marca", "modelo"]
        verbose_name = "Moto"
        verbose_name_plural = "Motos"

    def __str__(self) -> str:
        return f"{self.marca} {self.modelo} ({self.cilindrada}cc)"
