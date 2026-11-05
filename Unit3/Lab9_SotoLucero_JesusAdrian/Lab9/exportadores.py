from abc import ABC, abstractmethod
import csv
import json
from fpdf import FPDF

class Exportador(ABC):
    @abstractmethod
    def exportar(self, datos, ruta_archivo):
        pass

class ExportadorTXT(Exportador):
    def exportar(self, datos, ruta_archivo):
        with open(ruta_archivo, 'w', encoding='utf-8') as file:
            file.write("--- REPORTE DE PRODUCTOS ---\n")
            for p in datos:
                file.write(f"ID: {p['id']} | Nombre: {p['nombre']} | Precio: {p['precio']:.2f} | Stock: {p['stock']}\n")

class ExportadorCSV(Exportador):
    def exportar(self, datos, ruta_archivo):
        if not datos: return
        keys = datos[0].keys()
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(datos)

class ExportadorJSON(Exportador):
    def exportar(self, datos, ruta_archivo):
        with open(ruta_archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)

class ExportadorPDF(Exportador):
    def exportar(self, datos, ruta_archivo):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Reporte de Inventario de Productos", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        for p in datos:
            texto = f"Producto: {p['nombre']} - Precio: ${p['precio']:.2f} - Stock: {p['stock']}"
            pdf.cell(200, 10, txt=texto, ln=True)
        pdf.output(ruta_archivo)
