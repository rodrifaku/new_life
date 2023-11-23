from django.forms import ModelForm
from .models import Producto, Categoria, DireccionDespacho, Proveedor


class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = [
            'nombre'
        ]


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [
            'modelo',
            'marca',
            'descripcion',
            'foto',
            'precio',
            'categoria',
            'cantidad_fisico',
            'cantidad_web'
        ]


class DireccionDespachoForm(ModelForm):
    class Meta:
        model = DireccionDespacho
        fields = ['direccion', 'comuna', 'ciudad']

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'