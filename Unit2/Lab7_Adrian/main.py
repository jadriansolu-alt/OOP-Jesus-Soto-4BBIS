import tkinter as tk
from view.login_view import LoginVentana

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginVentana(root)
    root.mainloop()