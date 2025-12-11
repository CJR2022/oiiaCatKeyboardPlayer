from pynput import keyboard

class KeyboardHandler:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.is_active = True
        self.listener = None

    def on_press(self, key):
        if self.is_active:
            try:
                self.sound_manager.play_next()
            except Exception as e:
                print(f"Error playing sound: {e}")

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
            
    def set_active(self, active):
        self.is_active = active
