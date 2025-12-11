import pygame
import os
import time

import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SoundManager:
    def __init__(self, sounds_dir="sounds"):
        pygame.mixer.init()
        self.sounds = {}
        self.current_index = 0
        self.last_input_time = 0
        self.volume = 1.0
        self.sounds_dir = resource_path(sounds_dir)
        self.load_sounds()

    def load_sounds(self):
        # Load sounds 0.wav through 11.wav
        for i in range(0, 12):
            file_path = os.path.join(self.sounds_dir, f"{i}.wav")
            if os.path.exists(file_path):
                try:
                    sound = pygame.mixer.Sound(file_path)
                    self.sounds[i] = sound
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
            else:
                print(f"Warning: {file_path} not found")

    def play_next(self):
        current_time = time.time()
        
        # Debounce: Ignore inputs if less than 0.1s has passed since last sound
        if current_time - self.last_input_time < 0.06:
            return

        # Check for timeout (2 seconds)
        if current_time - self.last_input_time > 2.0:
            self.current_index = 0
        
        # Play current sound
        if self.current_index in self.sounds:
            self.sounds[self.current_index].set_volume(self.volume)
            self.sounds[self.current_index].play()
        
        # Update index for next press
        self.current_index += 1
        if self.current_index > 11:
            self.current_index = 0
            
        self.last_input_time = current_time

    def set_volume(self, volume):
        # Volume is 0.0 to 1.0
        self.volume = max(0.0, min(1.0, volume))
