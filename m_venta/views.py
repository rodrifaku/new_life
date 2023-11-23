from django.shortcuts import render
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import os
from m_venta.carrito import Carrito
from django.views import View
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm, CategoriaForm, DireccionDespachoForm, ProveedorForm
from sweetify import success, warning
from .models import ItemCarrito, Venta, DetalleVenta, Producto, DireccionDespacho, Proveedor
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from datetime import datetime
from m_venta.carrito import Carrito
from django.contrib.auth.models import User
from m_bodega.models import OrdenDespacho
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config
from django.core.mail import EmailMessage, send_mail


def es_administrador(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(es_administrador)
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


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    # Obtener o crear el carrito del usuario actual
    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(user=request.user)
    else:
        # Manejo para usuarios no autenticados si es necesario
        # Puedes ajustar esto según tus necesidades
        messages.warning(
            request, 'Debes iniciar sesión para agregar productos al carrito.')
        # Redirigir a la página de inicio de sesión o donde sea necesario
        return redirect('iniciar_sesion')

    # Verificar si el producto ya está en el carrito
    item_carrito, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito, producto=producto)
    if not creado:
        # Incrementar la cantidad si el producto ya está en el carrito
        item_carrito.cantidad += 1
        item_carrito.save()

    success(
        request, f'Se ha agregado "{producto.modelo}" al carrito.')

    # Redirigir a la página de productos o donde sea necesario
    return redirect('negocio/productos_carrito.html')


def agregar_carrito(request, id):

    carrito = Carrito(request)
    producto = Producto.objects.get(pk=id)
    carrito.agregar(producto)
    success(request, 'Agregado Correctamente al carro',
            text="Gracias", timer=3000, button="OK")
    return redirect('mostrar_carrito')


def productos_carrito(request):
    carrito = Carrito(request)
    productos_en_carrito = carrito.obtener_productos_en_carrito()

    return render(request, 'negocio/productos_carrito.html', {'productos_en_carrito': productos_en_carrito})


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
    success(request, 'Se quito correctamente producto',
            text="Del carrrito de compras", timer=3000, button="OK")
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

                producto = Producto.objects.get(pk=producto_id)

                # Verificar si hay suficiente cantidad_web para la compra
                if producto.cantidad_web < cantidad:
                    warning(request, f'No hay suficiente stock web para {producto.modelo}')
                    return redirect('mostrar_carrito')

                detalleventa = DetalleVenta.objects.create(
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    producto_id=producto_id,
                    venta_id=venta_id
                )
                detalleventa.save()

                subtotal = cantidad * precio_unitario
                total_venta += subtotal

                producto = Producto.objects.get(pk=producto_id)
                producto.cantidad_web -= cantidad
                producto.save()

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

    # Renderiza la plantilla de boleta en HTML
    boleta_html = render_to_string('negocio/mostrar_boleta.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'total': total
        # Usa RequestContext para asegurar que el objeto request esté presente
    },  request=request)

    # Convierte el HTML a texto plano
    boleta_text = strip_tags(boleta_html)

    # Configura el asunto, el cuerpo y el remitente del correo
    subject = 'Boleta de compra'
    # Reemplaza USER_MAIL con la variable correcta de configuración
    from_email = config('USER_MAIL')
    to_email = [request.user.email]

    # Crea un objeto EmailMessage
    email = EmailMessage(subject, boleta_text, from_email, to_email)

    # Genera el PDF con xhtml2pdf y adjunta al correo
    pdf_content = generar_pdf(boleta_html)
    email.attach('boleta.pdf', pdf_content, 'application/pdf')

    # Envía el correo electrónico
    sent = email.send()

    if sent == 1:
        # El correo se envió correctamente
        print("Correo electrónico enviado exitosamente.")
        # Puedes agregar lógica adicional aquí según tus necesidades
    else:
        # Hubo un problema al enviar el correo
        print("Error al enviar el correo electrónico.")

    return render(request, 'negocio/mostrar_boleta.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'total': total
    })


def generar_pdf(html):
    result = BytesIO()

    # Creamos el objeto HttpResponse con el resultado (PDF)
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # Si se creó correctamente, devolvemos el contenido
    if not pdf.err:
        return result.getvalue()

    return b''


@login_required
def historial_compras(request):
    usuario = request.user
    compras = Venta.objects.filter(usuario=usuario)

    return render(request, 'negocio/historial_compras.html', {'compras': compras})


@user_passes_test(es_administrador)
def mostrar_boleta_admin(request, id_venta):
    venta = get_object_or_404(Venta, id=id_venta)
    detalles_venta = DetalleVenta.objects.filter(venta=venta)
    total = venta.total
    return render(request, 'negocio/mostrar_boleta.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'total': total
    })


@user_passes_test(es_administrador)
def mostrar_despacho(request, id_venta):
    venta = get_object_or_404(Venta, id=id_venta)
    detalles_venta = DetalleVenta.objects.filter(venta=venta)
    total = venta.total
    direccion_despacho = DireccionDespacho.objects.get(user=venta.usuario)
    return render(request, 'negocio/mostrar_despacho.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'total': total,
        'direccion_despacho': direccion_despacho
    })


@user_passes_test(es_administrador)
def descontar_inventario(request, id_venta):
    venta = get_object_or_404(Venta, id=id_venta)
    detalles_venta = DetalleVenta.objects.filter(venta=venta)
    orden_despacho = OrdenDespacho.objects.get(boleta=venta)

    try:
        # Descontar la cantidad física del inventario
        for detalle in detalles_venta:
            producto = detalle.producto
            cantidad_descontar = detalle.cantidad

            if cantidad_descontar <= producto.cantidad_fisico:
                producto.cantidad_fisico -= cantidad_descontar
                producto.save()
            else:
                warning(request, 'Stock insuficiente. No se puede despachar.')
                return redirect('bodega')
    except Exception as e:
        error(request, f'Ocurrió un error al descontar el inventario: {e}')
        return redirect('bodega')

    # Restablecer la orden de despacho como despachada
    orden_despacho.despachado = True
    orden_despacho.save()

    # Redirigir a la página de detalles de venta después de realizar el descuento
    success(request, 'Inventario descontado y orden despachada con éxito.')
    return redirect('bodega')


@user_passes_test(es_administrador)
def historial_ventas(request):
    fecha = request.GET.get('fecha', None)
    if fecha:
        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        compras = Venta.objects.filter(
            fecha_venta__date=fecha).order_by('-fecha_venta')
    else:
        compras = Venta.objects.all().order_by('-fecha_venta')

    return render(request, 'negocio/historial_ventas.html', {'compras': compras})


@user_passes_test(es_administrador)
def agregar_categoria(request):
    if request.method == 'POST':
        if form.is_valid():
            form = CategoriaForm(request.POST)
            form.save()
            # Redirige a la página de lista de categorías
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'agregar_categoria.html', {'form': form})


@login_required
def direccion_despacho(request):
    user = request.user
    carrito = request.session.get('carrito', {})

    if not carrito:
        warning(request, 'Carro vacío',
                         text="Siga comprando", timer=3000, button="OK")
        return redirect('mostrar_carrito')
    else:

        total = calcular_total(carrito)
        direccion_existente = DireccionDespacho.objects.filter(
            user=user).first()
        print("Direccion existente:", direccion_existente)

        if direccion_existente:
            messages.success(request, 'Ya tienes una dirección guardada.')
            direccion_info = {
                'direccion': direccion_existente.direccion,
                'comuna': direccion_existente.comuna,
                'ciudad': direccion_existente.ciudad,
            }
            # El usuario ya tiene una dirección, redirigir a la página de pagar
            return render(request, 'negocio/pago.html', {'user': user, 'total': total, 'direccion_info': direccion_info})
        else:
            if request.method == 'POST':
                form = DireccionDespachoForm(request.POST)
                if form.is_valid():
                    direccion_despacho = form.save(commit=False)
                    direccion_despacho.user = user
                    direccion_despacho.save()

                    messages.success(
                        request, 'Dirección guardada exitosamente.')
                    return render(request, 'negocio/pago.html', {'user': user, 'total': total, 'direccion_info': direccion_info})
            else:
                form = DireccionDespachoForm()

            return render(request, 'negocio/realizar_venta.html', {'form': form, 'total': total, 'user': user, 'direccion_despacho': direccion_despacho})

    return render(request, 'negocio/pago.html', {'direccion_info': direccion_info})


def calcular_total(carrito):
    # Lógica para calcular el total
    total = 0
    for producto_id, producto_info in carrito.items():
        precio = int(producto_info['precio'])
        cantidad = int(producto_info['cantidad'])
        total += precio * cantidad
    return total


@user_passes_test(es_administrador)
def bodega(request):

    ordenes_pendientes = OrdenDespacho.objects.filter(despachado=False)
    if not ordenes_pendientes:
        success(request, 'Estas el día',
                text="No existe despachos Pendientes", timer=3000, button="OK")
    return render(request, 'negocio/ordenes_pendientes.html', {'ordenes_pendientes': ordenes_pendientes})


class BoletaPDFView(View):
    def get(self, request, id_venta, *args, **kwargs):
        venta = Venta.objects.get(id=id_venta)
        detalles_venta = DetalleVenta.objects.filter(venta=venta)
        total = venta.total

        template_path = 'negocio/mostrar_boleta.html'
        context = {'venta': venta,
                   'detalles_venta': detalles_venta, 'total': total}

        # Utilizar render para obtener un diccionario de contexto
        html = render(request, template_path, context).content

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="boleta.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        return response


@user_passes_test(es_administrador)
def agregar_categoria(request):
    formulario_categoria = CategoriaForm()

    return render(request, 'agregar_categoria.html', {'formulario_categoria': formulario_categoria})


@user_passes_test(es_administrador)
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            # Cambia 'lista_proveedores' al nombre de la vista de tu lista de proveedores
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()

    return render(request, 'crear_proveedor.html', {'form': form})


def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'lista_proveedores.html', {'proveedores': proveedores})


message = Mail(from_email='newlife.tienda.online@gmail.com',
               to_emails='rfaundez.rodrigo@gmail.com',
               subject='test',
               plain_text_content='prueba de envio de correo',
               html_content='<strong> test test test </strong>')
try:
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

except Exception as e:
    print(str(e))


send_mail(

    'correo de prueba',
    'contenido.',
    ('USER_MAIL'),
    ['rfaundez.rodrigo@gmail.com'],
    fail_silently=False,
)
