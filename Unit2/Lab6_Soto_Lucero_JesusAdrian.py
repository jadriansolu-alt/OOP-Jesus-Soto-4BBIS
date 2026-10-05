import os
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class SmartDevice(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def turn_on(self) -> str:
        pass


class Light(SmartDevice):
    def __init__(self):
        super().__init__("Light")

    def turn_on(self) -> str:
        return f"{self.name} is now ON. Brightening the room!"

    def turn_off(self) -> str:
        return f"{self.name} is now OFF. Dimming the room."


class TV(SmartDevice):
    def __init__(self):
        super().__init__("TV")

    def turn_on(self) -> str:
        return f"{self.name} is now ON. Enjoy your favorite shows!"

    def turn_off(self) -> str:
        return f"{self.name} is now OFF. See you next time!"

    def change_channel(self, channel: int) -> str:
        return f"{self.name} channel changed to {channel}. Enjoy watching!"

    def volume_up(self) -> str:
        return f"{self.name} volume increased. Louder sound!"

    def volume_down(self) -> str:
        return f"{self.name} volume decreased. Quieter sound."


class AirConditioner(SmartDevice):
    def __init__(self):
        super().__init__("Air Conditioner")

    def turn_on(self) -> str:
        return f"{self.name} is now ON. Cooling the room!"

    def turn_off(self) -> str:
        return f"{self.name} is now OFF. Warming the room."

    def set_temperature(self, temperature: int) -> str:
        return f"{self.name} temperature set to {temperature}°C. Comfortable environment!"


class PolymorphicAppTemplate(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- 1. WINDOW SETTINGS ---
        self.title("Lab 6: Polymorphism with GUI")
        self.geometry("480x360")
        self.resizable(False, False)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "app_icon.png")

        if os.path.exists(icon_path):
            self.app_icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self.app_icon)
        else:
            print("Warning: Icon file 'app_icon.png' not found. Using default icon.")

        # --- 2. OBJECT REGISTRY ---
        # Instancias de cada dispositivo polimórfico
        self.items = {
            "Light": Light(),
            "TV": TV(),
            "Air Conditioner": AirConditioner(),
        }

        # Construir la interfaz
        self._build_interface()

    def _build_interface(self):
        # Header / Title Banner
        lbl_header = tk.Label(
            self,
            text="Smart Home Center",
            font=("Times New Roman", 15, "bold"),
            fg="#2c3e50"
        )
        lbl_header.pack(pady=12)

        # Selection Group (Radiobuttons)
        group_box = tk.LabelFrame(
            self,
            text=" Select an Option ",
            font=("Times New Roman", 11, "bold"),
            padx=15,
            pady=10
        )
        group_box.pack(fill="x", padx=20, pady=5)

        # Selección por defecto: primera llave del diccionario
        first_key = list(self.items.keys())[0]
        self.selected_key = tk.StringVar(value=first_key)

        # Genera un radiobutton por cada elemento en self.items
        for key in self.items.keys():
            rb = ttk.Radiobutton(
                group_box,
                text=key,
                value=key,
                variable=self.selected_key
            )
            rb.pack(anchor="w", pady=3)

        # Trigger Action Button
        btn_action = tk.Button(
            self,
            text="Turn On Device",
            command=self._handle_action,
            bg="#2980b9",
            fg="white",
            font=("Times New Roman", 10, "bold"),
            relief="raised",
            cursor="hand2",
            padx=12,
            pady=6
        )
        btn_action.pack(pady=15)

        # Output / Results Box
        self.lbl_output = tk.Label(
            self,
            text="Select an option above and click 'Turn On Device'.",
            font=("Times New Roman", 10, "italic"),
            bg="#ecf0f1",
            fg="#34495e",
            relief="groove",
            height=3,
            wraplength=420,
            justify="center"
        )
        self.lbl_output.pack(fill="x", padx=20, pady=5)

    def _handle_action(self):
        # 1. Obtener la opción seleccionada por el usuario
        chosen_key = self.selected_key.get()

        # 2. Obtener el objeto polimórfico activo
        active_object: SmartDevice = self.items[chosen_key]

        # 3. EJECUCIÓN POLIMÓRFICA:
        # Se llama al método común turn_on()
        result_message = active_object.turn_on()

        # 4. Mostrar el resultado en la interfaz
        self.lbl_output.config(text=result_message, font=("Times New Roman", 10, "normal"))


# LAUNCHER
if __name__ == "__main__":
    app = PolymorphicAppTemplate()
    app.mainloop()