"""
Crea datos iniciales para probar el sistema localmente:
- Un usuario administrador.
- Un conjunto de motos de ejemplo en el catalogo.

Idempotente: se puede ejecutar varias veces sin duplicar.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from catalogo.models import Moto

MOTOS_DEMO = [
    {
        "marca": "Honda",
        "modelo": "CB 500F",
        "cilindrada": 471,
        "precio": 5990000,
        "stock": 4,
        "descripcion": "Naked de media cilindrada, ideal ciudad y ruta.",
    },
    {
        "marca": "Yamaha",
        "modelo": "MT-03",
        "cilindrada": 321,
        "precio": 4790000,
        "stock": 6,
        "descripcion": "Naked liviana y agil, perfecta para iniciarse.",
    },
    {
        "marca": "Kawasaki",
        "modelo": "Ninja 400",
        "cilindrada": 399,
        "precio": 5490000,
        "stock": 3,
        "descripcion": "Deportiva accesible con gran rendimiento.",
    },
    {
        "marca": "Suzuki",
        "modelo": "V-Strom 650",
        "cilindrada": 645,
        "precio": 7990000,
        "stock": 2,
        "descripcion": "Trail versatil para viajes largos.",
    },
    {
        "marca": "Royal Enfield",
        "modelo": "Classic 350",
        "cilindrada": 349,
        "precio": 4290000,
        "stock": 5,
        "descripcion": "Estilo retro con motor monocilindrico suave.",
    },
    {
        "marca": "KTM",
        "modelo": "Duke 390",
        "cilindrada": 373,
        "precio": 5290000,
        "stock": 4,
        "descripcion": "Naked deportiva con electronica moderna.",
    },
]


class Command(BaseCommand):
    help = "Carga datos iniciales (admin + catalogo de motos demo)."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_ADMIN_USER", "admin")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD", "admin123")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "admin@concesionaria.cl")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f"Administrador '{username}' creado.")
            )
        else:
            self.stdout.write(f"Administrador '{username}' ya existe.")

        creadas = 0
        for data in MOTOS_DEMO:
            _, created = Moto.objects.get_or_create(
                marca=data["marca"], modelo=data["modelo"], defaults=data
            )
            creadas += int(created)
        self.stdout.write(
            self.style.SUCCESS(f"{creadas} moto(s) demo creada(s).")
        )
