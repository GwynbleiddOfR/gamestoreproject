from django.db import models
from .enumeraciones import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    usuario=models.OneToOneField(User, related_name='usuario', on_delete=models.CASCADE)
    telefono=models.CharField(max_length=9, null=False)
    ciudad=models.CharField(max_length=15, choices=CIUDAD, null=False)
    direccion=models.CharField(max_length=200, null=False)

class Juego(models.Model):
    nomb_juego=models.CharField(max_length=100, null=False, verbose_name="Nombre")
    genero=models.CharField(max_length=50, null=False)
    consola=models.CharField(max_length=3, choices=TIPO_CONSOLA)
    precio=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(999999)])
    stock=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1),MaxValueValidator(99)])
    descripcion=models.TextField()
    foto_juego=models.ImageField(upload_to='juegos',null=False, verbose_name="Imagen")