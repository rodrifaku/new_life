from django.shortcuts import render, redirect
from .forms import FormularioEntrar, FormularioRegistro
from sweetify import success, warning
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def mostrar_entrar(request):
    if request.method == 'GET':
        contexto = {
            'titulo': 'Bienvenido',
            'formulario': FormularioEntrar()
        }
        return render(request, 'entrar.html', contexto)
    if request.method == 'POST':
        datos_usuario = FormularioEntrar(data=request.POST)
        es_valido = datos_usuario.is_valid()
        if es_valido:
            # Login
            usuario = datos_usuario.cleaned_data['usuario']
            password = datos_usuario.cleaned_data['contrasenia_usuario']
            usuario_valido = authenticate(username=usuario, password=password)
            if usuario_valido is not None:
                login(request, usuario_valido)
                success(request, f"Bienvenido {usuario_valido.username}")
                return redirect('mostrar_principal')
        contexto = {
            'titulo': 'Bienvenido',
            'formulario': datos_usuario
        }
        warning(request, 'Usuario y contrasña incorrecto')
        return render(request, 'entrar.html', contexto)


def mostrar_registro(request):
    if request.method == 'GET':
        contexto = {
            'formulario': FormularioRegistro()
        }
        return render(request, 'registro.html', contexto)

    if request.method == 'POST':
        datos_usuario = FormularioRegistro(data=request.POST)
        es_valido = datos_usuario.is_valid()  # True o False
        if es_valido:  # Valido == True
            datos_usuario.save()
            success(request, 'Registrado correctamente',
                    text="Gracias por ser parte", timer=3000, button="OK")
            return redirect('mostrar_entrar')
        contexto = {
            'formulario': datos_usuario
        }
        warning(request, 'Ups...',
                text="Valide sus datos", button="ok")
        return render(request, 'registro.html', contexto)


def cerrar_sesion(request):
    if request.user.is_authenticated:
        logout(request)
        success(request, 'Correcto',
                text="La sesión se cerró correctamente", button="Ok", timer=3000)
    return redirect('mostrar_principal')

# Create your views here.
