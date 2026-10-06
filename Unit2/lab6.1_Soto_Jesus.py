import os
import tkinter as tk
from abc import ABC, abstractmethod
from datetime import datetime
from tkinter import ttk

class SmartDevice(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def turn_on(self) -> str:
        pass

    @abstractmethod
    def turn_off(self) -> str:
        pass


class SmartSpeaker(SmartDevice):
    def __init__(self, name: str = "Echo Dot 5"):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON. Enjoy your favorite music!"

    def turn_off(self) -> str:
        return f"{self.name} is OFF. Music playback stopped."


class SmartTv(SmartDevice):
    def __init__(self, name: str = "LG Smart Tv"):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON. Enjoy your favorite shows!"

    def turn_off(self) -> str:
        return f"{self.name} is OFF. Display powered down."


class SmartLight(SmartDevice):
    def __init__(self, name: str = "Smart Light"):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON. Brighten up your space!"

    def turn_off(self) -> str:
        return f"{self.name} is OFF. Lights out."


# NEW DEVICE CLASS (Demonstrates Scalability)
class SmartAirConditioner(SmartDevice):
    def __init__(self, name: str = "Nest SmartAirConditioner"):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON. Climate control set to 22°C."

    def turn_off(self) -> str:
        return f"{self.name} is OFF. Eco mode activated."


# ==========================================
# TKINTER GRAPHICAL USER INTERFACE
# ==========================================

class SmartHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- 1. WINDOW SETTINGS ---
        self.title("Lab 6: Polymorphism Jesus Adrian Soto Lucero")
        self.geometry("520x580")
        self.resizable(False, False)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "icon.png")
        if os.path.exists(icon_path):
            self.iconphoto(False, tk.PhotoImage(file=icon_path))

        # --- 2. OBJECT REGISTRY ---
        # Adding a new device only requires registering it here!
        self.items = {
            "TV": SmartTv(),
            "Speaker": SmartSpeaker(),
            "Light": SmartLight(),
            "Air Conditioner": SmartAirConditioner(),
        }

        self._build_interface()

    def _build_interface(self):
        # Header / Title Banner
        lbl_header = tk.Label(
            self,
            text="Smart Home Center",
            font=("Times New Roman", 22, "bold"),
            fg="#2c3e50"
        )
        lbl_header.pack(pady=10)

        # Selection Group (Radiobuttons)
        group_box = tk.LabelFrame(
            self,
            text=" Select a Device ",
            font=("Times New Roman", 14, "bold"),
            padx=15,
            pady=8
        )
        group_box.pack(fill="x", padx=20, pady=5)

        first_key = list(self.items.keys())[0]
        self.selected_key = tk.StringVar(value=first_key)

        for key in self.items.keys():
            rb = ttk.Radiobutton(
                group_box,
                text=key,
                value=key,
                variable=self.selected_key
            )
            rb.pack(anchor="w", pady=2)

        # Action Buttons Frame
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        # Turn On Button
        btn_turn_on = tk.Button(
            btn_frame,
            text="Turn On Device",
            command=lambda: self._handle_action("on"),
            bg="#45fb91",
            fg="white",
            font=("Times New Roman", 11, "bold"),
            relief="raised",
            cursor="hand2",
            padx=10,
            pady=4
        )
        btn_turn_on.grid(row=0, column=0, padx=8)

        # Turn Off Button
        btn_turn_off = tk.Button(
            btn_frame,
            text="Turn Off Device",
            command=lambda: self._handle_action("off"),
            bg="#c72a18",
            fg="white",
            font=("Times New Roman", 11, "bold"),
            relief="raised",
            cursor="hand2",
            padx=10,
            pady=4
        )
        btn_turn_off.grid(row=0, column=1, padx=8)

        # Status Banner
        self.lbl_output = tk.Label(
            self,
            text="Select a device and press an action button.",
            font=("Times New Roman", 10, "italic"),
            bg="#ecf0f1",
            fg="#2e045e",
            relief="groove",
            height=2,
            wraplength=460,
            justify="center"
        )
        self.lbl_output.pack(fill="x", padx=20, pady=5)

        # Activity Log Group
        log_frame = tk.LabelFrame(
            self,
            text=" Activity Log ",
            font=("Times New Roman", 12, "bold"),
            padx=10,
            pady=5
        )
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Listbox + Scrollbar
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log_listbox = tk.Listbox(
            log_frame,
            font=("Consolas", 9),
            yscrollcommand=scrollbar.set,
            selectmode="single"
        )
        self.log_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.log_listbox.yview)

    def _handle_action(self, action_type: str):
        chosen_key = self.selected_key.get()
        active_object: SmartDevice = self.items[chosen_key]

        # Polymorphic execution based on action type
        if action_type == "on":
            result_message = active_object.turn_on()
        else:
            result_message = active_object.turn_off()

        # 1. Update status display
        self.lbl_output.config(text=result_message, font=("Times New Roman", 10, "normal"))

        # 2. Append formatted timestamped log entry
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_entry = f"{timestamp} {result_message}"
        self.log_listbox.insert(tk.END, log_entry)
        self.log_listbox.see(tk.END)  # Auto-scroll to bottom


# LAUNCHER
if __name__ == "__main__":
    app = SmartHomeApp()
    app.mainloop()