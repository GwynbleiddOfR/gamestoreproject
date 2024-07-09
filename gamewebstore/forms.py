from django import forms
from .models import *
from .enumeraciones import *
from django.contrib.auth.forms import UserCreationForm

# Usuarios
class UserForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email','password1','password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class PerfilForm(forms.ModelForm):

    class Meta:
        model=Perfil
        fields=['telefono', 'ciudad', 'direccion']

class UpdatePerfilForm(forms.ModelForm):
    is_active = forms.BooleanField(label="Usuario activo", required=False)

    class Meta:
        model = Perfil
        fields = ['telefono', 'ciudad', 'direccion']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UpdatePerfilForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['is_active'].initial = user.is_active

    def save(self, commit=True):
        instance = super(UpdatePerfilForm, self).save(commit=False)
        user = instance.usuario
        user.is_active = self.cleaned_data['is_active']
        if commit:
            user.save()
            instance.save()
        return instance

#Juegos
class JuegoForm(forms.ModelForm):

    class Meta:
        model = Juego
        fields = ['id', 'nomb_juego', 'genero', 'consola', 'precio', 'stock', 'descripcion', 'foto_juego']

class UpdateJuegoForm(forms.ModelForm):

    class Meta:
        model = Juego
        fields = ['nomb_juego', 'genero', 'consola', 'precio', 'stock', 'descripcion', 'foto_juego']

# Venta
class EstadoVentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['estado']