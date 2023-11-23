from django.shortcuts import render, redirect
from .forms import FormularioEntrar, FormularioRegistro, CustomUserChangeForm, CustomPasswordChangeForm
from sweetify import success, warning
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from .models import CustomUser
from m_venta.models import DireccionDespacho
from m_venta.forms import DireccionDespachoForm


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


@login_required
def profile(request):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtén el usuario actualmente autenticado
        user = request.user
        # Obtén la dirección de despacho del usuario (si existe)
        direccion_despacho = DireccionDespacho.objects.get(user=user)
        if request.method == 'POST':
            # Utiliza la instancia del usuario en el formulario
            form = CustomUserChangeForm(request.POST, instance=user)
            direccion_form = DireccionDespachoForm(
                request.POST, instance=direccion_despacho)
            # Verifica si ambos formularios son válidos
            if direccion_form.is_valid() and form.is_valid():
                form.save()
            # Actualiza la dirección de despacho
            #form.mail
            
            direccion_despacho.direccion = direccion_form.cleaned_data.get(
                'direccion')
            direccion_despacho.comuna = direccion_form.cleaned_data.get(
                'comuna')
            direccion_despacho.ciudad = direccion_form.cleaned_data.get(
                'ciudad')
            direccion_despacho.save()

            return redirect('profile')

        else:
            # Utiliza la instancia del usuario en el formulario
            form = CustomUserChangeForm(instance=user, initial={
                                        'direccion': direccion_despacho.direccion,
                                        'comuna': direccion_despacho.comuna,
                                        'ciudad': direccion_despacho.ciudad})
            direccion_form = DireccionDespachoForm(instance=direccion_despacho)

        return render(request, 'profile.html', {'form': form, 'direccion_form': direccion_form})
    else:
        # El usuario no está autenticado, redirige a la página de inicio de sesión
        return redirect('entrar')


class CustomPasswordChangeView(PasswordChangeView):
    # Reemplaza con tu formulario personalizado
    form_class = CustomPasswordChangeForm
    template_name = 'change_password.html'  # Reemplaza con la plantilla que desees
    success_url = reverse_lazy('password_change_done')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'password.html', {'form': form})
