import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = self.load_sound("2d_game/assets/background_music.mp3")
        self.collect_sound = self.load_sound("2d_game/assets/collect_sound.wav")
        self.music_volume = 0.5
        self.sound_volume = 1.0

    def load_sound(self, file_path):
        if os.path.exists(file_path):
            return pygame.mixer.Sound(file_path)
        else:
            print(f"Warning: Sound file '{file_path}' not found. Using silent placeholder.")
            return pygame.mixer.Sound(buffer=b'\x00' * 44100)  # 1 second of silence

    def play_background_music(self):
        if self.background_music:
            self.background_music.play(loops=-1)

    def stop_background_music(self):
        if self.background_music:
            self.background_music.stop()

    def play_collect_sound(self):
        if self.collect_sound:
            self.collect_sound.play()

    def set_music_volume(self, volume):
        self.music_volume = volume
        if self.background_music:
            self.background_music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        self.sound_volume = volume
        if self.collect_sound:
            self.collect_sound.set_volume(self.sound_volume)

    def toggle_music(self):
        if pygame.mixer.get_busy():
            self.stop_background_music()
        else:
            self.play_background_music()

    def toggle_sound(self):
        if self.sound_volume > 0:
            self.set_sound_volume(0)
        else:
            self.set_sound_volume(1)