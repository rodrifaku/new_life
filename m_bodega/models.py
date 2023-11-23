from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class OrdenDespacho(models.Model):
    boleta = models.OneToOneField('m_venta.Venta', on_delete=models.CASCADE)  # Ajusta el nombre de la aplicación si es necesario
    numero_orden = models.CharField(max_length=20, unique=True)  # Puedes ajustar la longitud según tus necesidades
    despachado = models.BooleanField(default=False)

    def __str__(self):
        return f"Orden de Despacho #{self.numero_orden}"