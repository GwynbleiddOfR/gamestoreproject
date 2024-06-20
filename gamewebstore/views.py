from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Juego
from .forms import JuegoForm, UpdateJuegoForm

# Create your views here.
def cerrar_sesion(request):
    logout(request)
    return redirect(to='index')

def index(request):
    juegos=Juego.objects.all()
    datos={
        "juegos":juegos
    }
    return render(request,'gamewebstore/index.html', datos)

def adminGames(request):
    juegos=Juego.objects.all()
    datos={
        "juegos":juegos
    }

    return render(request,'gamewebstore/adminGames.html', datos)

def administrador(request):
    return render(request,'gamewebstore/administrador.html')

def carrito(request):
    return render(request,'gamewebstore/carrito.html')

def modificarjuego(request, id):
    juego = get_object_or_404(Juego, id=id)
    form = UpdateJuegoForm(instance=juego)
    
    if request.method=="POST":
        form=UpdateJuegoForm(data=request.POST,files=request.FILES,instance=juego)
        if form.is_valid():
            form.save()
            return redirect(to="adminGames")
    
    
    datos={
        "form":form,
        "juego":juego
    }

    return render(request, 'gamewebstore/modificarjuego.html', datos)

def deleteGame(request):
    return render(request,'gamewebstore/deleteGame.html')

def deleteUser(request):
    return render(request,'gamewebstore/deleteUser.html')

def descriptionGame(request, id):
    juego=get_object_or_404(Juego, id=id)
    
    datos={
        "juego":juego
    }

    return render(request,'gamewebstore/descriptionGame.html', datos)

def editarPerfil(request):
    return render(request,'gamewebstore/editarPerfil.html')

def forgetPassword(request):
    return render(request,'gamewebstore/forgetPassword.html')

def gatoRandom(request):
    return render(request,'gamewebstore/gatoRandom.html')

def msgVerificarEmail(request):
    return render(request,'gamewebstore/msgVerificarEmail.html')

def register(request):
    return render(request,'gamewebstore/register.html')

def suspendUser(request):
    return render(request,'gamewebstore/suspendUser.html')

def userProfile(request):
    return render(request,'gamewebstore/userProfile.html')

def vistaCompras(request):
    return render(request,'gamewebstore/vistaCompras.html')

def vistaVender(request):
    form=JuegoForm()

    if request.method=="POST":
        form=JuegoForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(to="adminGames")
        
    datos={
        "form":form
    }

    return render(request,'gamewebstore/vistaVender.html', datos)

def vistaVentas(request):
    return render(request,'gamewebstore/vistaVentas.html')
