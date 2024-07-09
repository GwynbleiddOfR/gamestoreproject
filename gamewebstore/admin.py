from django.contrib import admin
from .models import Juego, Venta

class AdmJuego(admin.ModelAdmin):
    list_display=['nomb_juego', 'genero', 'consola', 'precio', 'stock', 'descripcion', 'foto_juego']
    list_filter=['consola']

class AdmVenta(admin.ModelAdmin):
    list_display=['id', 'fecha', 'estado', 'usuario_id']

# Register your models here.
admin.site.register(Juego, AdmJuego)
admin.site.register(Venta, AdmVenta)