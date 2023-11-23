from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from m_usuario.urls import urlpatterns as urlUsuario
from m_venta.urls import urlpatterns as urlVenta
from m_venta.admin import productos_sitio
from m_bodega.urls import urlpatterns as urlBodega
from m_venta.views import mostrar_administracion


from .views import (
    mostrar_principal,
    mostrar_productos,
    mostrar_nosotros,
    filtro_por_categoria

)

urlpatterns = [
    path('', mostrar_principal, name='mostrar_principal'),
    path('productos/', mostrar_productos, name='mostrar_productos'),
    path('mostrar_nosotros/', mostrar_nosotros,
         name='mostrar_nosotros'),
    path('', include('m_usuario.urls')),  # 1 opción
    path('', include('m_venta.urls')),
    path('', include('m_pago.urls')),
    path('', include('m_bodega.urls')),
    path('admin/', admin.site.urls),
    path('productosadmin/', productos_sitio.urls),
    path('filtrar-por-categoria/', filtro_por_categoria,
         name='filtro_por_categoria'),

]


admin.site.index_title = "Tienda Instrumentos"
admin.site.site_header = "Administracion de Tienda "
admin.site.site_title = "Sitio tienda"


if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
