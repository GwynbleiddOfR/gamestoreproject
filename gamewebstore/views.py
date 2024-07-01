from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Juego, Perfil, Cart, CartItem, Venta
from .forms import JuegoForm, UpdateJuegoForm, UserForm, PerfilForm, UpdatePerfilForm, EstadoVentaForm
from django.contrib import messages
from os import remove, path
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.db.models import Q
from .viewmodel import MostrarDatosUsuarios
from .decorators import perfil_completo_requerido

# Create your views here.
def cerrar_sesion(request):
    logout(request)
    return redirect(to='index')

def index(request):
    query = request.GET.get('q')
    consola = request.GET.get('consola')
    
    if query:
        juegos = Juego.objects.filter(nomb_juego__icontains=query)
        if not juegos.exists():
            messages.error(request, 'Lo sentimos, el juego que buscas no se encuentra en nuestro catálogo.')
            juegos = Juego.objects.all()
    else:
        juegos = Juego.objects.all()
    
    if consola:
        juegos_filtrados = juegos.filter(consola=consola)
        if juegos_filtrados.exists():
            juegos = juegos_filtrados
    
    datos = {
        "juegos": juegos
    }

    return render(request,'gamewebstore/index.html', datos)

@permission_required('gamewebstore.add_juego')
def adminGames(request):
    query = request.GET.get('q')
    if query:
        juegos = Juego.objects.filter(
            Q(nomb_juego__icontains=query) | 
            Q(id__icontains=query) |
            Q(genero__icontains=query) |
            Q(consola__icontains=query) |
            Q(precio__icontains=query) |
            Q(stock__icontains=query) |
            Q(descripcion__icontains=query)
        )
        if not juegos.exists():
            messages.error(request, 'Ningún juego coincide con la búsqueda.')
            juegos = Juego.objects.all()
    else:
        juegos = Juego.objects.all()
    
    datos = {
        "juegos": juegos
    }

    return render(request,'gamewebstore/adminGames.html', datos)

@permission_required('gamewebstore.add_user')
def administrador(request):
    query = request.GET.get('q')
    #usuarios = User.objects.all()
    perfiles = Perfil.objects.all()
    
    print("***************************")
    #print(usuarios)
    if query:
        perfiles = perfiles.filter(
            Q(usuario__username__icontains=query) |
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(usuario__email__icontains=query) |
            Q(ciudad__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query)
        )
    if not perfiles.exists():
        messages.error(request, 'Ningún usuario coincide con la búsqueda.')
        perfiles = Perfil.objects.all()

    usuarios_view = []
    for per in perfiles:
        usrview = MostrarDatosUsuarios()
        nombreu=per.usuario.username
        useruser=User.objects.get(username=nombreu)
        idql=str(useruser.id)

        print(idql)
        usrview.id_usuario=idql
        usrview.username=per.usuario.username
        usrview.first_name = per.usuario.first_name
        usrview.last_name =per.usuario.last_name
        usrview.email=per.usuario.email
        usrview.date_joined=per.usuario.date_joined
        usrview.ciudad=per.ciudad
        usrview.direccion=per.direccion
        usrview.telefono=per.telefono
        #print(usrview)
        usuarios_view.append(usrview)
    
    datos={
        "usuarios":usuarios_view
        
    }
    return render(request,'gamewebstore/administrador.html', datos)

def carrito(request):
    return render(request,'gamewebstore/carrito.html')

@login_required
@perfil_completo_requerido
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
                estado='EN PREPARACIÓN',
                fecha=timezone.now()
            )
        
    for item in cart.items.all():
        juego = item.juego
        juego.stock -= item.cantidad
        juego.save()

    cart.items.clear()
    
    messages.success(request, 'Pago realizado con éxito. Gracias por tu compra.')
    return redirect('cart_detail')

@permission_required('gamewebstore.change_juego')
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

@permission_required('gamewebstore.delete_juego')
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

@permission_required('gamewebstore.delete_user')
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
            perfil.perfil_completo = True
            perfil.save()
            messages.warning(request,"Perfil modificado")
            return redirect(to="userProfile", username=request.user.username)
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
            usuarionuevo=get_object_or_404(User,username=form.cleaned_data["username"])
            perfil=Perfil()
            perfil.usuario=usuarionuevo
            perfil.save()
            return redirect(to="login")

    datos={
        "form":form
    }

    return render(request,'registration/register.html', datos)

@permission_required('gamewebstore.add_user')
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

@login_required
def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    perfil_usuario, created = Perfil.objects.get_or_create(usuario=user)
    
    datos = {
        'perfil': perfil_usuario,
        'user': user
    }

    return render(request,'gamewebstore/userProfile.html', datos)

@login_required
def vistaCompras(request):
    query = request.GET.get('q')
    ventas = Venta.objects.filter(usuario=request.user).order_by('-fecha')

    if query:
        ventas_filtradas = ventas.filter(
            Q(juego__nomb_juego__icontains=query) |
            Q(juego__consola__icontains=query) |
            Q(cantidad__icontains=query) |
            Q(estado__icontains=query)
        )
        if ventas_filtradas.exists():
            ventas = ventas_filtradas

    datos={
        "ventas":ventas
    }

    return render(request,'gamewebstore/vistaCompras.html', datos)

@permission_required('gamewebstore.add_juego')
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

@permission_required('gamewebstore.view_venta')
def vistaVentas(request):
    query = request.GET.get('q')
    ventas = Venta.objects.all().order_by('-fecha')

    if query:
        ventas_filtradas = ventas.filter(
            Q(id__icontains=query) |
            Q(juego__id__icontains=query) |
            Q(juego__nomb_juego__icontains=query) |
            Q(juego__consola__icontains=query) |
            Q(cantidad__icontains=query) |
            Q(usuario__username__icontains=query) |
            Q(usuario__email__icontains=query) |
            Q(estado__icontains=query) |
            Q(fecha__icontains=query)
        )
        if ventas_filtradas.exists():
            ventas = ventas_filtradas

    if request.method == 'POST':
        venta_id = request.POST.get('venta_id')
        venta = get_object_or_404(Venta, id=venta_id)
        form = EstadoVentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('vistaVentas')
    else:
        form = EstadoVentaForm()

    datos={
        'ventas': ventas,
        'form': form
    }

    return render(request, 'gamewebstore/vistaVentas.html', datos)
