from django.contrib import admin

from .models import Producto,Categoria


# Register your models here.
class ProductoAdminArea(admin.AdminSite):
    site_header = 'Productos admin'


productos_sitio = ProductoAdminArea(name='ProductosAdmin')

admin.site.register(Producto)
productos_sitio.register(Producto)

class CategoriaAdminArea(admin.AdminSite):
    site_header = 'Categoria admin'


productos_sitio = CategoriaAdminArea(name='CategoriaAdminArea')

admin.site.register(Categoria)
productos_sitio.register(Categoria)
