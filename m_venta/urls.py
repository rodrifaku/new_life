from django.urls import path
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
    inventario

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
    path('pago/', pago ,name='pago'),
    path('inventario/',inventario,name='inventario')


]
