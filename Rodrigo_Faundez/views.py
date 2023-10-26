from django.shortcuts import render

from m_venta.models import Producto, Categoria
from .productos import productos


def mostrar_principal(request):
    return render(request, 'principal.html')


def mostrar_productos(request):
    contexto = {
        'productos': Producto.objects.all()
    }
    return render(request, 'productos.html', contexto)


def mostrar_nosotros(request):
    return render(request, 'nosotros.html')

def filtro_por_categoria(request):
    categoria_id = request.GET.get('categoria', None)
    
    # Obtén todos los productos si no se selecciona una categoría o filtra por categoría si se selecciona una
    if categoria_id:
        productos = Producto.objects.filter(categoria=categoria_id)
    else:
        productos = Producto.objects.all()

    # Obtén la lista de categorías para mostrar en el formulario
    categorias = Categoria.objects.all()  # Asegúrate de importar tu modelo Categoria

    return render(request, 'productos.html', {'productos': productos, 'categorias': categorias})