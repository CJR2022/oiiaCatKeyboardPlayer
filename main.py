import customtkinter
import sys
from sound_manager import SoundManager
from keyboard_listener import KeyboardHandler

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("OIIA CAT Keyboard Sound Player")
        self.geometry("400x450")
        self.resizable(False, False)

        # Initialize logic
        self.sound_manager = SoundManager()
        self.keyboard_handler = KeyboardHandler(self.sound_manager)
        self.keyboard_handler.start()

        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Title Label
        self.title_label = customtkinter.CTkLabel(self, text="OIIA CAT Keyboard Sound Player", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Switch (On/Off)
        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(self, text="Sound Enabled", command=self.toggle_sound,
                                              variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.grid(row=1, column=0, padx=20, pady=10)

        # Volume Label
        self.volume_label = customtkinter.CTkLabel(self, text="Volume: 100%")
        self.volume_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        # Volume Slider
        self.slider = customtkinter.CTkSlider(self, from_=0, to=1, command=self.change_volume)
        self.slider.set(1.0)
        self.slider.grid(row=3, column=0, padx=20, pady=(0, 20))

        # Debounce Label
        self.debounce_label = customtkinter.CTkLabel(self, text="Debounce Time: 0.10s")
        self.debounce_label.grid(row=4, column=0, padx=20, pady=(10, 0))

        # Debounce Slider
        self.debounce_slider = customtkinter.CTkSlider(self, from_=0.01, to=1.0, command=self.change_debounce)
        self.debounce_slider.set(0.1)
        self.debounce_slider.grid(row=5, column=0, padx=20, pady=(0, 20))

        # Protocol for closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_sound(self):
        if self.switch_var.get() == "on":
            self.keyboard_handler.set_active(True)
        else:
            self.keyboard_handler.set_active(False)

    def change_volume(self, value):
        self.sound_manager.set_volume(value)
        self.volume_label.configure(text=f"Volume: {int(value * 100)}%")

    def change_debounce(self, value):
        self.sound_manager.set_debounce_time(value)
        self.debounce_label.configure(text=f"Debounce Time: {value:.2f}s")

    def on_closing(self):
        self.keyboard_handler.stop()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
