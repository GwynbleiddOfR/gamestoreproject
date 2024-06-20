from django import forms
from .models import *
from .enumeraciones import *

#Juegos
class JuegoForm(forms.ModelForm):

    class Meta:
        model = Juego
        fields = ['id', 'nomb_juego', 'genero', 'consola', 'precio', 'stock', 'descripcion', 'foto_juego']

class UpdateJuegoForm(forms.ModelForm):

    class Meta:
        model = Juego
        fields = ['nomb_juego', 'genero', 'consola', 'precio', 'stock', 'descripcion', 'foto_juego']