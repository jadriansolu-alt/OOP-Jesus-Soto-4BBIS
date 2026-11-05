import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.products_model import Producto
from controller.products_controller import ProductsController
from PIL import Image, ImageTk
import os
from controller.config import db_config

class HomeVentana:
    def __init__(self, root, nombre_usuario):
        self.root = root
        self.root.title(f"Panel Principal - {nombre_usuario}")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.nombre_usuario = nombre_usuario
        self.controller = ProductsController()
        
        # Ruta de exportación
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        self.export_dir = os.path.abspath(os.path.join(root_dir, db_config['export_folder']))
        
        if not os.path.exists(self.export_dir):
            try:
                os.makedirs(self.export_dir, exist_ok=True)
            except Exception as e:
                print(f"Error creando carpeta de exportación: {e}")

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Encabezado
        lbl_bienvenida = tk.Label(self.root, text=f"Bienvenido/a, {self.nombre_usuario}", font=("Helvetica", 14, "bold"))
        lbl_bienvenida.pack(pady=15)

        # Contenedor principal con pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Pestaña Inicio
        self.frame_inicio = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.frame_inicio, text="Inicio")
        tk.Label(self.frame_inicio, text="Panel de control de inventario.", bg="white").pack(pady=50)

        # Pestaña Productos
        self.frame_productos = tk.Frame(self.notebook)
        self.notebook.add(self.frame_productos, text="Inventario de Productos")
        self._crear_seccion_productos()

    def _crear_seccion_productos(self):
        # Formulario
        frame_form = tk.LabelFrame(self.frame_productos, text=" Registro ", font=("Helvetica", 10, "bold"))
        frame_form.pack(side="left", fill="y", padx=15, pady=15, ipadx=10)

        tk.Label(frame_form, text="Nombre:").pack(anchor="w", pady=(5, 2))
        self.entry_nombre = tk.Entry(frame_form)
        self.entry_nombre.pack(fill="x", pady=2)

        tk.Label(frame_form, text="Precio:").pack(anchor="w", pady=(10, 2))
        self.entry_precio = tk.Entry(frame_form)
        self.entry_precio.pack(fill="x", pady=2)

        tk.Label(frame_form, text="Stock:").pack(anchor="w", pady=(10, 2))
        self.entry_stock = tk.Entry(frame_form)
        self.entry_stock.pack(fill="x", pady=2)

        tk.Button(frame_form, text="Guardar", bg="#4CAF50", command=self._guardar).pack(fill="x", pady=20)

        # Exportación
        tk.Label(frame_form, text=" Exportar ", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.combo_formato = ttk.Combobox(frame_form, values=["CSV", "TXT", "JSON", "PDF"], state="readonly")
        self.combo_formato.current(0)
        self.combo_formato.pack(fill="x", pady=2)

        tk.Button(frame_form, text="Exportar Reporte", bg="#2196F3", command=self._exportar).pack(fill="x", pady=20)

        # Tabla
        frame_tabla = tk.Frame(self.frame_productos)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
        self.tabla.pack(fill="both", expand=True)
        
        for col in ("ID", "Nombre", "Precio", "Stock"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor="center")

        self._cargar_datos()

    def _cargar_datos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        res = self.controller.obtener_productos()
        for p in res:
            self.tabla.insert("", "end", values=(p['id'], p['nombre'], f"{p['precio']:.2f}", p['stock']))

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        precio = self.entry_precio.get().strip()
        stock = self.entry_stock.get().strip()

        if not nombre or not precio or not stock:
            messagebox.showwarning("Falta datos", "Completa todos los campos.")
            return

        try:
            precio = float(precio)
            stock = int(stock)
            exito, msg = self.controller.guardar_producto(nombre, precio, stock)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self._cargar_datos()
                self.entry_nombre.delete(0, tk.END)
                self.entry_precio.delete(0, tk.END)
                self.entry_stock.delete(0, tk.END)
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Precio debe ser decimal y Stock entero.")

    def _exportar(self):
        formato = self.combo_formato.get()
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Exportar a {formato}?")
        if confirmar:
            nombre_archivo = f"Reporte_{formato.lower()}.{formato.lower()}"
            
            # CORRECCIÓN: Cambiar asksaveasdialog por asksaveasfilename
            ruta_final = filedialog.asksaveasfilename(
                title="SELECCIONE LA CARPETA Y EL NOMBRE DEL ARCHIVO",
                initialfile=nombre_archivo,
                defaultextension=f".{formato.lower()}",
                filetypes=[(f"{formato} files", f"*.{formato.lower()}"), ("Todos los archivos", "*.*")],
                initialdir=self.export_dir
            )

            if ruta_final:
                try:
                    carpeta = os.path.dirname(ruta_final)
                    if not os.path.exists(carpeta):
                        os.makedirs(carpeta, exist_ok=True)
                    
                    exito, msg = self.controller.exportar_productos(formato, ruta_final)
                    if exito:
                        messagebox.showinfo("Éxito", msg)
                    else:
                        messagebox.showerror("Error", msg)
                except Exception as e:
                    print(f"DEBUG: Error en exportar: {e}")
                    messagebox.showerror("Error de sistema", f"No se pudo completar la exportación:\n{e}")
            else:
                pass
        else:
            pass
