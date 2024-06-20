from django.urls import include, path
from .views import index, adminGames, administrador, carrito, deleteGame, deleteUser, descriptionGame, editarPerfil, forgetPassword, gatoRandom, msgVerificarEmail, register, suspendUser, userProfile, vistaCompras, vistaVender, vistaVentas, cerrar_sesion
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('adminGames/', adminGames, name='adminGames'),
    path('administrador/', administrador, name='administrador'),
    path('carrito/', carrito, name='carrito'),
    path('deleteGame/', deleteGame, name='deleteGame'),
    path('deleteUser/', deleteUser, name='deleteUser'),
    path('descriptionGame/', descriptionGame, name='descriptionGame'),
    path('editarPerfil/', editarPerfil, name='editarPerfil'),
    path('forgetPassword/', forgetPassword, name='forgetPassword'),
    path('gatoRandom/', gatoRandom, name='gatoRandom'),
    path('msgVerificarEmail/', msgVerificarEmail, name='msgVerificarEmail'),
    path('register/', register, name='register'),
    path('suspendUser/', suspendUser, name='suspendUser'),
    path('userProfile/', userProfile, name='userProfile'),
    path('vistaCompras/', vistaCompras, name='vistaCompras'),
    path('vistaVender/', vistaVender, name='vistaVender'),
    path('vistaVentas/', vistaVentas, name='vistaVentas'),
    path('cerrar_sesion', cerrar_sesion, name='cerrar_sesion'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)