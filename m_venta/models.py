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
    categoria = ForeignKey(Categoria, on_delete=CASCADE,null=True)

    def __str__(self):
        return self.modelo

    class Meta:
        verbose_name_plural = 'Productos'


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
