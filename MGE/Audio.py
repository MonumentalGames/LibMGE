import pygame
#import pyaudio
import os

class audio:

    volume = 100

    class Sound:
        def __init__(self, path):
            if os.path.exists(path):
                self.sound = pygame.mixer.Sound(path)
            self.volume = 100
            self.sound.set_volume((self.volume / 100) / 200 * audio.volume)

        def set_volume(self, volume):
            self.volume = volume
            self.sound.set_volume((self.volume / 100) / 200 * audio.volume)

        def play(self, loops=-1):
            self.sound.set_volume((self.volume / 100) / 200 * audio.volume)
            self.sound.play(loops)

        def stop(self):
            self.sound.stop()

    class Music:
        def __init__(self, path):
            if os.path.exists(path):
                self.music = pygame.mixer.music
                self.music.load(path)
            self.volume = 100
            self.music.set_volume((self.volume / 100) / 200 * audio.volume)

        def set_volume(self, volume):
            self.volume = volume
            self.music.set_volume((self.volume / 100) / 200 * audio.volume)

        def play(self, loops=-1):
            self.music.set_volume((self.volume / 100) / 200 * audio.volume)
            #pygame.mixer.Channel(0).play(self.music)
            #pygame.mixer.Channel(0).p
            self.music.play(loops)
            self.music.set_pos(50)

        def stop(self):
            self.music.stop()
