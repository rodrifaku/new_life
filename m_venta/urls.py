from django.urls import path
from django.views.decorators.http import require_http_methods
from .views import (

    crear_producto,
    listar_productos,
    agregar_carrito,
    eliminar_carrito,
    mostrar_boleta,
    restar_carrito,
    limpiar_carrito,
    mostrar_carrito,
    confirmar_compra,
    mostrar_administracion,
    modificar_producto,
    eliminar_producto,
    historial_compras,
    historial_ventas,
    pago,
    inventario,
    mostrar_boleta_admin,
    direccion_despacho,
    bodega,
    mostrar_despacho,
    descontar_inventario,
    BoletaPDFView,
    agregar_categoria,
    crear_proveedor,
    lista_proveedores,
    crear_direccion

)

urlpatterns = [
    path('listar/', listar_productos, name='listar_productos'),
    path('crear/', crear_producto, name='crear_producto'),
    path('agregar/<int:id>/', agregar_carrito, name='agregar_carrito'),
    path('eliminar/<int:id>/', eliminar_carrito, name='eliminar_carrito'),
    path('restar/<int:id>/', restar_carrito, name='restar_carrito'),
    path('limpiar/', limpiar_carrito, name='limpiar_carrito'),
    path('mostrar_carrito/', mostrar_carrito, name='mostrar_carrito'),
    path('confirmar_compra/', confirmar_compra, name='confirmar_compra'),
    path('mostrar_administracion/', mostrar_administracion,
         name='mostrar_administracion'),
    path('modificar_producto/<id>', modificar_producto, name='modificar_producto'),
    path('eliminar_producto/<id>', eliminar_producto, name='eliminar_producto'),
    path('mostrar_boleta/<int:id_venta>/',
         mostrar_boleta, name='mostrar_boleta'),
    path('historial_compras/', historial_compras, name='historial_compras'),
    path('historial_ventas/', historial_ventas, name='historial_ventas'),
    path('pago/', pago, name='pago'),
    path('inventario/', inventario, name='inventario'),
    path('mostrar_boleta_admin<int:id_venta>/',
         mostrar_boleta_admin, name='mostrar_boleta_admin'),
    path('direccion_despacho/', direccion_despacho, name='direccion_despacho'),
    path('bodega/', bodega, name='bodega'),
    path('mostrar_despacho/<int:id_venta>/',
         mostrar_despacho, name='mostrar_despacho'),
    path('descontar_inventario/<int:id_venta>',
         descontar_inventario, name='descontar_inventario'),
    path('boleta-pdf/<int:id_venta>/', BoletaPDFView.as_view(), name='boleta_pdf'),
    path('agregar_categoria',agregar_categoria,name='agregar_categoria'),
    path('lista_proveedores/', lista_proveedores, name='lista_proveedores'),
    path('crear_proveedor/', crear_proveedor, name='crear_proveedor'),
    path('crear_direccion',crear_direccion, name='crear_direccion')







]
