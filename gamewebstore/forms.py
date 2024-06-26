from django import forms
from .models import *
from .enumeraciones import *
from django.contrib.auth.forms import UserCreationForm

# Usuarios
class UserForm(UserCreationForm):
    pass

class PerfilForm(forms.ModelForm):

    class Meta:
        model=Perfil
        fields=['telefono', 'ciudad', 'direccion']

class UpdatePerfilForm(forms.ModelForm):

    class Meta:
        model=Perfil
        fields=['telefono', 'ciudad', 'direccion']

#Juegos
class JuegoForm(forms.ModelForm):

    class Meta:
        model = Juego
        fields = ['id', 'nomb_juego', 'genero', 'consola', 'precio', 'stock', 'descripcion', 'foto_juego']

class UpdateJuegoForm(forms.ModelForm):

    class Meta:
        model = Juego
        fields = ['nomb_juego', 'genero', 'consola', 'precio', 'stock', 'descripcion', 'foto_juego']