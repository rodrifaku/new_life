from m_venta.models import DetalleVenta, Producto, Venta


class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}

        self.carrito = carrito

    def agregar(self, producto):
        if str(producto.id)not in self.carrito.keys():
            self.carrito[producto.id] = {
                "producto_id": producto.id,
                "modelo": producto.modelo,
                "marca": producto.marca,
                "cantidad": 1,
                "acumulado": producto.precio,
                "precio": str(producto.precio),
            }
        else:
            for key, value in self.carrito.items():
                if key == str(producto.id):
                    value["cantidad"] = value["cantidad"]+1
                    self.save()
                    break
        self.save()

    def save(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.save()

    def decrementar(self, producto):
        for key, value in self.carrito.items():
            if key == str(producto.id):
                value["cantidad"] = value["cantidad"] - 1

                if value["cantidad"] == 0:
                    self.eliminar(producto)
                    break
                self.save()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def guardar_venta(self):
        usuario = self.request.user
        venta = Venta(usuario=usuario)
        venta.save()
        venta_id = venta.id
        ids_productos = list(self.carrito.keys())
        productos = Producto.objects.filter(id__in=ids_productos)
        for producto in productos:
            item = self.carrito[str(producto.id)]
            cantidad = item["cantidad"]
            precio_unitario = item["precio"]

            detalle_venta = DetalleVenta.objects.create(
                venta_id=venta.id,
                producto_id=producto.id,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
            detalle_venta.save()

    def acomulado(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["acumulado"] += producto.precio
        self.save()

    def restar_acomulado(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["acumulado"] -= producto.precio
        self.save()
