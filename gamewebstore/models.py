from django.db import models
from .enumeraciones import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings

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

class CartItem(models.Model):
    juego = models.ForeignKey('Juego', on_delete=models.CASCADE, verbose_name="Juego")
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_por_item = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def subtotal(self):
        return self.cantidad * self.precio_por_item

    def __str__(self):
        return f"{self.juego} - {self.cantidad} x {self.precio_por_item}"

class Cart(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario", related_name="carts")
    items = models.ManyToManyField(CartItem, verbose_name="Ítems", related_name="carts")

    def total(self):
        return sum([item.subtotal() for item in self.items.all()])

    def __str__(self):
        return f"Cart for {self.usuario}"