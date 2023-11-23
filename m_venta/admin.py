from django.contrib import admin

from .models import Producto,Categoria, DireccionDespacho
from .forms import DireccionDespachoForm


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

class DireccionDespachoAdmin(admin.ModelAdmin):
    form = DireccionDespachoForm

    list_display = ('usuario','direccion', 'comuna', 'ciudad')
    def usuario(self, obj):
        return obj.user.username
    usuario.short_description = 'Usuario'

# Registra el modelo y el formulario en el administrador
admin.site.register(DireccionDespacho, DireccionDespachoAdmin)