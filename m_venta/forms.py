from django.forms import ModelForm
from .models import Producto, Categoria


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
            'categoria'
            ]



