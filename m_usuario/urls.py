from django.urls import path
from .views import (
    mostrar_entrar,
    mostrar_registro,
    cerrar_sesion,
    profile,
    CustomPasswordChangeView,
    PasswordChangeDoneView,
    change_password
)
urlpatterns = [
    path('entrar/', mostrar_entrar, name='mostrar_entrar'),
    path('registro/', mostrar_registro, name='mostrar_registro'),
    path('salir/', cerrar_sesion, name='cerrar_sesion'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
