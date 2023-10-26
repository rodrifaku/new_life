from m_venta import carrito
from m_venta.carrito import Carrito
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .forms import ProductoForm, CategoriaForm
from django.contrib.auth.decorators import login_required
from sweetify import success, warning
from .models import Venta, DetalleVenta, Producto
from django.contrib.auth.models import User

# Create your views here.


@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creado_por = request.user
            producto.save()
            success(request, f'Producto {producto.modelo} creado')
            return redirect('crear_producto')
        warning(request, 'Complete los campos correctamente')
    else:
        form = ProductoForm()

    return render(request, 'negocio/crear_producto.html', {'form': form})


def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'negocio/listar_productos.html', {'productos': productos})

def inventario(request):
    productos = Producto.objects.all()
    return render(request, 'negocio/inventario.html', {'productos': productos})

def mostrar_administracion(request):
    return render(request, 'negocio/administracion.html')


def mostrar_carrito(request):
    return render(request, 'negocio/productos_carrito.html')

def pago(request):
    return render(request, 'negocio/pago.html')
def agregar_carrito(request, id):

    carrito = Carrito(request)
    producto = Producto.objects.get(pk=id)
    carrito.agregar(producto)
    success(request, 'Agregado Correctamente al carro',
            text="Gracias", timer=3000, button="OK")
    return redirect('mostrar_carrito')


def eliminar_carrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(pk=id)
    carrito.eliminar(producto)
    success(request, 'Se elimino correctamente producto',
            text="Del carrrito de compras", timer=3000, button="OK")
    return redirect('mostrar_carrito')


def restar_carrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(pk=id)
    carrito.decrementar(producto)
    return redirect('mostrar_carrito')


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    success(request, 'Se elimino todo los productos',
            text="Del carrrito de compras", timer=3000, button="OK")
    return redirect('mostrar_carrito')


@login_required
def modificar_producto(request, id):
    producto = Producto.objects.get(id=id)
    contexto = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            success(request, 'Se editó correctamente el producto',
                    text="Dato modificado", timer=3000, button="OK")
            contexto['form'] = formulario
    return render(request, 'negocio/modificar_producto.html', contexto)


@login_required
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    warning(request, 'Producto eliminado correctamente')
    return redirect('listar_productos')


@login_required
def confirmar_compra(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        if not carrito:
            warning(request, 'Carro vacio',
                    text="Siga comprando", timer=3000, button="OK")
            return redirect('mostrar_carrito')
        else:
            usuario = request.user
            venta = Venta(usuario=usuario)
            venta.save()
            venta_id = venta.id

            carrito = request.session.get('carrito', {})
            total_venta = 0
            for id, datos_producto in carrito.items():
                producto_id = id
                cantidad = int(datos_producto['cantidad'])
                precio_unitario = int(datos_producto['precio'])

                detalleventa = DetalleVenta.objects.create(
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    producto_id=producto_id,
                    venta_id=venta_id
                )
                detalleventa.save()

                subtotal = cantidad * precio_unitario
                total_venta += subtotal

                venta.total = total_venta
                venta.save()

        carrito.clear()
        success(request, f'Boleta emitida')
        return redirect('mostrar_boleta', id_venta=venta.id)

    else:

        return redirect('mostrar_carrito')


@login_required
def mostrar_boleta(request, id_venta):
    venta = get_object_or_404(Venta, id=id_venta, usuario=request.user)
    detalles_venta = DetalleVenta.objects.filter(venta=venta)
    total = venta.total
    return render(request, 'negocio/mostrar_boleta.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'total': total
    })


@login_required
def historial_compras(request):
    usuario = request.user
    compras = Venta.objects.filter(usuario=usuario)

    return render(request, 'negocio/historial_compras.html', {'compras': compras})

@login_required
def historial_ventas(request):
    compras = Venta.objects.all()
    return render(request, 'negocio/historial_ventas.html', {'compras': compras})

def agregar_categoria(request):
    if request.method == 'POST':
        if form.is_valid():
            form = CategoriaForm(request.POST)
            form.save()
            return redirect('lista_categorias')  # Redirige a la página de lista de categorías
    else:
        form = CategoriaForm()
    return render(request, 'agregar_categoria.html', {'form': form})