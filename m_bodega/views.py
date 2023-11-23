from django.shortcuts import render
from m_venta.models import OrdenDespacho, Venta


def ordenes_pendientes(request):
    # Obtener órdenes de despacho pendientes
    ordenes_pendientes = OrdenDespacho.objects.filter(despachado=True)

    return render(request, 'negocio/ordenes_pendientes.html', {'ordenes_pendientes': ordenes_pendientes})


def detalles_venta(request, numero_orden):
    orden_despacho = get_object_or_404(
        OrdenDespacho, numero_orden=numero_orden)
    venta = orden_despacho.boleta
    detalles_venta = venta.detalleventa_set.all()
    direccion_despacho = venta.usuario.direcciondespacho

    return render(request, 'negocio/detalles_venta.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'direccion_despacho': direccion_despacho,
    })
