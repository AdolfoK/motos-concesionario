from django.contrib import admin

from .models import Moto


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ("marca", "modelo", "cilindrada", "precio", "stock")
    list_filter = ("marca",)
    search_fields = ("marca", "modelo")
