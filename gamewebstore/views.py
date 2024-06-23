from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Juego, Perfil
from .forms import JuegoForm, UpdateJuegoForm, UserForm, PerfilForm, UpdatePerfilForm
from django.contrib import messages
from os import remove, path
from django.conf import settings
from django.contrib.auth.models import User

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
    perfiles = Perfil.objects.all()
    datos = {
        "perfiles": perfiles
    }
    return render(request,'gamewebstore/administrador.html', datos)

def carrito(request):
    return render(request,'gamewebstore/carrito.html')

def modificarjuego(request, id):
    juego = get_object_or_404(Juego, id=id)
    form = UpdateJuegoForm(instance=juego)
    
    if request.method=="POST":
        form=UpdateJuegoForm(data=request.POST,files=request.FILES,instance=juego)
        if form.is_valid():
            form.save()
            messages.warning(request,"Juego modificado")
            return redirect(to="adminGames")
    
    datos={
        "form":form,
        "juego":juego
    }

    return render(request, 'gamewebstore/modificarjuego.html', datos)

def deleteGame(request, id):
    juego=get_object_or_404(Juego, id=id)
    
    if request.method=="POST":
        remove(path.join(str(settings.MEDIA_ROOT).replace('/media',''))+juego.foto_juego.url)
        juego.delete()
        messages.warning(request,"Juego eliminado")
        return redirect(to="adminGames")
        
    datos={
        "juego":juego
    }

    return render(request,'gamewebstore/deleteGame.html', datos)

def deleteUser(request, id):
    usuario = get_object_or_404(User, id=id)
    
    if request.method == "POST":
        Perfil.objects.filter(usuario=usuario).delete()
        usuario.delete()
        messages.warning(request, "Usuario eliminado")
        return redirect(to="administrador")
        
    datos = {
        "usuario": usuario
    }

    return render(request,'gamewebstore/deleteUser.html', datos)

def descriptionGame(request, id):
    juego=get_object_or_404(Juego, id=id)
    
    datos={
        "juego":juego
    }

    return render(request,'gamewebstore/descriptionGame.html', datos)

def editarPerfil(request):
    usr = request.user
    perfil_existente = Perfil.objects.filter(usuario=usr).first()

    if request.method == "POST":
        form = PerfilForm(data=request.POST, instance=perfil_existente)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = usr
            perfil.save()
            messages.warning(request,"Perfil modificado")
            return redirect(to="userProfile")
    else:
        if perfil_existente:
            form = PerfilForm(instance=perfil_existente)
        else:
            form = PerfilForm()

    datos = {"form": form}
    return render(request, 'gamewebstore/editarPerfil.html', datos)

def forgetPassword(request):
    return render(request,'gamewebstore/forgetPassword.html')

def gatoRandom(request):
    return render(request,'gamewebstore/gatoRandom.html')

def msgVerificarEmail(request):
    return render(request,'gamewebstore/msgVerificarEmail.html')

def register(request):
    form=UserForm()

    if request.method=="POST":
        form=UserForm(data=request.POST)
        if form.is_valid():
            form.save()

            return redirect(to="login")

    datos={
        "form":form
    }

    return render(request,'registration/register.html', datos)

def editarusuario(request, id):
    usuario = get_object_or_404(User, id=id)
    perfil_usuario = get_object_or_404(Perfil, usuario=usuario)
    
    if request.method == "POST":
        form = UpdatePerfilForm(request.POST, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.warning(request, "Usuario modificado")
            return redirect('administrador')
    else:
        form = UpdatePerfilForm(instance=perfil_usuario)

    datos = {
        'form': form
    }

    return render(request,'gamewebstore/editarusuario.html', datos)

def userProfile(request):
    usr = request.user
    perfil_usuario, created = Perfil.objects.get_or_create(usuario=usr)
    
    datos = {
        'perfil': perfil_usuario
    }

    return render(request,'gamewebstore/userProfile.html', datos)

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
