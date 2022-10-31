import pygame
from pygame.locals import *
from PIL import Image as PIL_Image

from .Platform import Platform

if not Platform.system == "Android":
    from win32api import GetSystemMetrics
    from ctypes import windll

    #from OpenGL.GL import *
    from OpenGL.GLU import *

from .Camera import Camera

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1, 1), NOFRAME)

        if not Platform.system == "Android":
            self.monitor_resolution = [GetSystemMetrics(0), GetSystemMetrics(1)]

        self.opengl = False
        self.clock = pygame.time.Clock()
        self.camera = Camera()

    @staticmethod
    def get_screen_type():
        return "main"

    def get_screen_img(self):
        image = self.screen
        image_size = image.get_size()
        raw_str = pygame.image.tostring(pygame.transform.scale(image, image_size), "RGB", False)
        return PIL_Image.frombytes("RGB", image_size, raw_str)

    def get_size(self):
        return self.screen.get_size()

    def set_localization(self, localization):
        if not Platform.system == "Android":
            if type(localization) is str:
                if localization.lower() == "center":
                    cache_localization = [int((self.monitor_resolution[0] - self.screen.get_size()[0]) / 2), int((self.monitor_resolution[1] - self.screen.get_size()[1]) / 2)]
                else:
                    return
            elif type(localization) is list:
                cache_localization = localization
            else:
                return
            hwnd = pygame.display.get_wm_info()['window']
            w, h = self.screen.get_size()
            windll.user32.MoveWindow(hwnd, cache_localization[0], cache_localization[1], w, h, False)

    def set_size(self, x, y, mode=None, opengl=False):
        if Platform.system == "Android":
            opengl = False
        self.opengl = opengl
        if mode is None:
            if opengl:
                self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL)
                gluPerspective(45, (x / y), 0.1, 500.0)
            else:
                self.screen = pygame.display.set_mode((x, y))
        elif mode.upper() == "NOFRAME":
            if opengl:
                self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL | NOFRAME)
                gluPerspective(45, (x / y), 0.1, 500.0)
            else:
                self.screen = pygame.display.set_mode((x, y), NOFRAME)
        elif mode.upper() == "RESIZABLE":
            if opengl:
                self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL | RESIZABLE)
                gluPerspective(45, (x / y), 0.1, 500.0)
            else:
                self.screen = pygame.display.set_mode((x, y), RESIZABLE)
        elif mode.upper() == "FULLSCREEN":
            if opengl:
                self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL | FULLSCREEN)
                gluPerspective(45, (x / y), 0.1, 500.0)
            else:
                self.screen = pygame.display.set_mode((x, y), FULLSCREEN)
