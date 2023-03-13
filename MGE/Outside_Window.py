import pygame
from pygame._sdl2 import Window, Renderer

from .Camera import Camera

class Outside_Window:
    def __init__(self, localization: list, size: list):
        self.__Window_Type__ = "Outside"

        self.screen = Window()
        self.renderer = Renderer(self.screen)

        self.localization = localization
        self.size = size

        self.cache_screen = pygame.Surface(size, pygame.SRCALPHA)

        self.camera = Camera()

        self.opengl = False

        self.render = False
        self.always_render = False

    def set_loc_size(self, localization: list, size: list):
        self.localization = localization
        self.size = size

    def get_localization(self):
        cache_localization = self.localization

        return cache_localization

    def get_size(self):
        return self.size

    def get_screen_type(self):
        return self.__Window_Type__
