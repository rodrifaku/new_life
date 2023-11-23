
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # Otros campos y opciones del modelo aquí
        pass

    # Agregar related_name a las relaciones con grupos y permisos
    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_set', blank=True)


class DireccionDespacho(models.Model):
    id_usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.direccion
