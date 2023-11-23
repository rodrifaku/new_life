from django.db.models import (
    Model,
    CharField,
    TextField,
    ImageField,
    IntegerField,
    ForeignKey,
    DateTimeField,
    TimeField,
    CASCADE

)
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from m_bodega.models import OrdenDespacho
import uuid


class Categoria(Model):
    nombre = CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(Model):
    modelo = CharField(max_length=25, null=False)
    marca = CharField(max_length=25, null=False)
    descripcion = TextField(max_length=500, null=False)
    foto = ImageField(upload_to='img/', null=True)
    precio = IntegerField(null=False)
    categoria = ForeignKey(Categoria, on_delete=CASCADE, null=True)
    cantidad_web = IntegerField(default=0)
    cantidad_fisico = IntegerField(default=0)

    def __str__(self):
        return self.modelo

    class Meta:
        verbose_name_plural = 'Productos'


class CarritoManager(models.Manager):
    def create_carrito(self, user):
        carrito = self.create(user=user)
        return carrito


class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField('Producto', through='ItemCarrito')
    objects = CarritoManager()

    def __str__(self):
        return f"Carrito de {self.user.username}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    modelo = models.CharField(max_length=25)
    marca = models.CharField(max_length=25)
    cantidad = models.PositiveIntegerField(default=1)
    acumulado = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class DireccionDespacho(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Venta(Model):

    fecha_venta = DateTimeField(auto_now=True, null=False)
    hora_venta = TimeField(auto_now=True, null=False)
    total = IntegerField(null=True)
    usuario = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"Venta #{self.pk}"

    class Meta:
        verbose_name_plural = 'Ventas'


class DetalleVenta(Model):

    cantidad = IntegerField(null=False)
    precio_unitario = IntegerField(null=False)
    venta = ForeignKey(Venta, on_delete=CASCADE)
    producto = ForeignKey(Producto, on_delete=CASCADE)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def total(self):
        return sum(self.cantidad * self.precio_unitario)

    def __str__(self):
        return f"Detalle de venta #{self.pk}"

    class Meta:
        verbose_name_plural = 'Detalles de venta'



class Proveedor(models.Model):
    razon_social = models.CharField(max_length=255)
    rut = models.CharField(max_length=20, unique=True)
    giro = models.CharField(max_length=255)
    domicilio = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    persona_contacto = models.CharField(max_length=255)
    telefono_contacto = models.CharField(max_length=20)
    email = models.EmailField()
    sitio_web = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.razon_social

class Factura(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='DetalleFactura')
    fecha_emision = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura {self.id}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)




class OrdenCompra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='DetalleOrdenCompra')
    fecha_creacion = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Orden de Compra {self.id}'

class DetalleOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.orden_compra.total += self.cantidad * self.precio_unitario
        self.orden_compra.save()
        super().save(*args, **kwargs)







@receiver(post_save, sender=DetalleVenta)
def generar_orden_despacho(sender, instance, created, **kwargs):
    if created:
        # Cuando se crea un nuevo DetalleVenta, se verifica y/o crea la OrdenDespacho
        venta = instance.venta
        
        
        numero_orden = str(uuid.uuid4())[:8]
        orden_despacho, _ = OrdenDespacho.objects.get_or_create(boleta=venta, defaults={'numero_orden': numero_orden})
        
        # Puedes asignar un número de orden aquí si lo deseas
        orden_despacho.numero_orden = "3108" + str(venta.pk)
        orden_despacho.save()

        # Aquí puedes realizar cualquier otra lógica necesaria para la orden de despacho
