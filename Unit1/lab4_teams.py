class Producto:
    def __init__(self, nombre, precio, tipo):
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo

class Observador:
    def actualizar(self, pedido):
        raise NotImplementedError("ERROR: Las subclases no se pudieron implementar")

class ServicioEmail(Observador):
    def actualizar(self, pedido):
        print(f"Email: Pedido enviado al cliente {pedido.cliente}.")

class ServicioSMS(Observador):
    def actualizar(self, pedido):
        print(f"SMS: Su pedido #{pedido.numero} ha sido {pedido.estado.lower()}.")

class ServicioApp(Observador):
    def actualizar(self, pedido):
        print(f"App: Estado actualizado a {pedido.estado}.")

class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.productos = []
        self.estado = "CREADO"
        self.observadores = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def quitar_observador(self, observador):
        self.observadores.remove(observador)

    def notificar_observadores(self):
        for observador in self.observadores:
            observador.actualizar(self)

    def calcular_total(self):
        total = 0

        for producto in self.productos:

            if producto.tipo == "electronico":
                total += producto.precio * 1.16

            elif producto.tipo == "ropa":
                total += producto.precio * 1.08

            elif producto.tipo == "alimento":
                total += producto.precio * 1.00

        return total

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.notificar_observadores()

    def mostrar_pedido(self):
        print(f"\nPedido #{self.numero}")
        print(f"Cliente: {self.cliente}")
        print(f"Estado: {self.estado}")

        print("\nProductos:")

        for producto in self.productos:
            print(
                f"- {producto.nombre}: "
                f"${producto.precio:.2f}"
            )

        print(f"\nTotal: ${self.calcular_total():.2f}")


pedido = Pedido(1001, "Ana")

pedido.agregar_producto(
    Producto("Laptop", 15000, "electronico")
)

pedido.agregar_producto(
    Producto("Playera", 500, "ropa")
)

pedido.agregar_producto(
    Producto("Cereal", 100, "alimento")
)

pedido.agregar_observador(ServicioEmail())
pedido.agregar_observador(ServicioSMS())
pedido.agregar_observador(ServicioApp())

pedido.mostrar_pedido()

pedido.cambiar_estado("ENVIADO")

print("\nNuevo estado:", pedido.estado)

"Pregunta de reflexion: ¿Cómo podemos notificar a diferentes objetos que ocurrió un evento sin que el objeto principal tenga que conocer los detalles de cada uno? El sujeto, en este caso el pedido contiene una interfaz que cuenta con una lista de objetos. Cada variante del observador tiene una forma diferente de 'reaccionar', asi se puede agregar sin que se modifique el pedido en si."