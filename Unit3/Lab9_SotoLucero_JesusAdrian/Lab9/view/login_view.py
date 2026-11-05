import tkinter as tk
from tkinter import messagebox
from models.login_model import Usuario
from view.home_view import HomeVentana
import os

class LoginVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Acceso al Sistema")
        self.root.geometry("350x380")
        self.root.resizable(False, False)
        self._crear_interfaz()

    def _crear_interfaz(self):
        tk.Label(self.root, text="Iniciar Sesión", font=("Helvetica", 16, "bold")).pack(pady=25)
        
        tk.Label(self.root, text="Usuario:").pack(anchor="w", padx=30)
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack(fill="x", padx=30)

        tk.Label(self.root, text="Contraseña:").pack(anchor="w", padx=30, pady=(10, 0))
        self.entry_pass = tk.Entry(self.root, show="*")
        self.entry_pass.pack(fill="x", padx=30)

        tk.Button(self.root, text="Entrar", bg="#2196F3", fg="white", 
                   font=("Helvetica", 11, "bold"), command=self._validar_login).pack(fill="x", padx=30, pady=30)

    def _validar_login(self):
        user = self.entry_usuario.get().strip()
        pw = self.entry_pass.get().strip()
        
        if not user or not pw:
            messagebox.showwarning("Error", "Campos vacíos")
            return

        usuario_obj = Usuario(user, pw)
        datos = usuario_obj.autenticar()
        
        if datos:
            messagebox.showinfo("Éxito", f"Bienvenido {datos['nombre']}")
            self.root.destroy()
            root_dash = tk.Tk()
            HomeVentana(root_dash, datos['nombre'])
            root_dash.mainloop()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
