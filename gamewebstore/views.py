from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Juego, Perfil, Cart, CartItem, Venta
from .forms import JuegoForm, UpdateJuegoForm, UserForm, PerfilForm, UpdatePerfilForm
from django.contrib import messages
from os import remove, path
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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

@login_required
def add_to_cart(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    cart, created = Cart.objects.get_or_create(usuario=request.user)

    cart_item, created = CartItem.objects.get_or_create(juego=juego, precio_por_item=juego.precio)
    if not created:
        cart_item.cantidad += 1
        cart_item.save()

    cart.items.add(cart_item)
    messages.success(request, f'{juego.nomb_juego} fue añadido a tu carrito.')

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(usuario=request.user)
    return render(request, 'gamewebstore/cart_detail.html', {'cart': cart})

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        cart_item.cantidad = cantidad
        cart_item.save()
        messages.success(request, 'La cantidad fue actualizada.')
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'El ítem fue eliminado del carrito.')
    return redirect('cart_detail')

@login_required
def process_payment(request):
    cart, created = Cart.objects.get_or_create(usuario=request.user)
    if not cart.items.exists():
        messages.error(request, 'No tienes artículos en tu carrito.')
        return redirect('cart_detail')

    for item in cart.items.all():
        juego = item.juego
        if item.cantidad > juego.stock:
            messages.error(request, f'No hay suficiente stock para {juego.nomb_juego}.')
            return redirect('cart_detail')
        
        Venta.objects.create(
                usuario=request.user,
                juego=juego,
                cantidad=item.cantidad,
                total_venta=item.subtotal(),
                estado='pendiente',  # Estado inicial de la venta
                fecha=timezone.now()
            )
        
    for item in cart.items.all():
        juego = item.juego
        juego.stock -= item.cantidad
        juego.save()

    cart.items.clear()
    
    messages.success(request, 'Pago realizado con éxito. Gracias por tu compra.')
    return redirect('cart_detail')

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

@login_required
def vistaCompras(request):
    ventas = Venta.objects.filter(usuario=request.user).order_by('-fecha')

    datos={
        "ventas":ventas
    }

    return render(request,'gamewebstore/vistaCompras.html', datos)

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
    ventas = Venta.objects.all().order_by('-fecha')

    datos={
        "ventas":ventas
    }

    return render(request, 'gamewebstore/vistaVentas.html', datos)
