from django.forms import (
    Form,
    TextInput,
    EmailInput,
    CharField,
    PasswordInput,
    BooleanField,
    CheckboxInput
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import AbstractUser


class FormularioRegistro(UserCreationForm):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['password1'].widget.attrs = {'class': 'form-control'}
        self.fields['password2'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = User
        fields = [
            'username',
            'last_name',
            'first_name',
            'email',
            'password1',
            'password2'

        ]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),

        }


class FormularioEntrar(Form):

    # entrar
    usuario = CharField(
        min_length=1,
        max_length=16,
        required=True,
        label='Ingrese usuario',
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }
        )
    )
    contrasenia_usuario = CharField(
        required=True,
        min_length=4,
        max_length=16,
        label='Ingrese contraseña',
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )
    recuerdame = BooleanField(
        required=False,
        label='Recordarme',
        widget=CheckboxInput(

        )
    )



class CustomUserChangeForm(UserChangeForm):
    bio = forms.CharField(max_length=500, required=False)
    direccion = forms.CharField(max_length=255, required=False)
    comuna = forms.CharField(max_length=100, required=False)
    ciudad = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',
                  'email', 'direccion', 'comuna', 'ciudad')


class CustomPasswordChangeForm(PasswordChangeForm):
    

    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'}),
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',
                  'email')
