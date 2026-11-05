from models.products_model import Producto
import exportadores

class ProductsController:
    def __init__(self):
        self.model = Producto()

    def obtener_productos(self):
        return self.model.obtener_todos()

    def guardar_producto(self, nombre, precio, stock):
        nuevo = Producto(nombre=nombre, precio=precio, stock=stock)
        return nuevo.guardar(), "Producto guardado correctamente."

    def exportar_productos(self, formato, ruta_archivo):
        datos = self.model.obtener_todos()
        if not datos:
            return False, "No hay datos para exportar."

        mapa_formatos = {
            "CSV": exportadores.ExportadorCSV,
            "TXT": exportadores.ExportadorTXT,
            "JSON": exportadores.ExportadorJSON,
            "PDF": exportadores.ExportadorPDF
        }

        if formato in mapa_formatos:
            clase_exportadora = mapa_formatos[formato]
            # Polimorfismo en acción
            exportador = clase_exportadora()
            exportador.exportar(datos, ruta_archivo)
            return True, "Exportación exitosa."
        
        return False, f"Formato {formato} no soportado."
