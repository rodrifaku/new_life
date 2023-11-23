from django.urls import path
from m_bodega.views import (
    ordenes_pendientes,
    detalles_venta
)


urlpatterns = [
    path('ordenes-pendientes/', ordenes_pendientes, name='ordenes_pendientes'),
    path('detalles-venta/<str:numero_orden>/',
         detalles_venta, name='detalles_venta')


]
