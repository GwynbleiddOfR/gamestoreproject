from django.contrib import admin
from .models import Juego

class AdmJuego(admin.ModelAdmin):
    list_display=['nomb_juego', 'genero', 'consola', 'precio', 'stock', 'descripcion', 'foto_juego']
    list_filter=['consola']

# Register your models here.
admin.site.register(Juego, AdmJuego)