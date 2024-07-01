from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def perfil_completo_requerido(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.usuario.perfil_completo:
            messages.error(request, 'Por favor, completa tu perfil antes de comprar un juego')
            return redirect('editarPerfil')
        return view_func(request, *args, **kwargs)
    return _wrapped_view