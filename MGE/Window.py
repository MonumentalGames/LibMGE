import pygame
#from pygame._sdl2 import Window, Renderer, messagebox
from PIL import Image as PIL_Image
from screeninfo import get_monitors

from .Camera import Camera

from ctypes import windll

#from OpenGL.GL import *
from OpenGL.GLU import *

mode_flags = {"NOFRAME": 32, "RESIZABLE": 16, "FULLSCREEN": -2147483648}

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1, 1), 32)
        #self.screen = Window()

        self.monitor_resolution = [get_monitors()[0].width, get_monitors()[0].height]

        self.object_draw_list = []

        self.opengl = False
        self.clock = pygame.time.Clock()
        self.camera = Camera()

    def render(self):
        pass
        #if self.object_draw_list:
        #    for obj in self.object_draw_list:
        #        print(obj["object"])
        #        obj["object"].render_object(obj["screen"], obj["camera"])
        #self.object_draw_list = []

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
        if type(localization) is str:
            if localization.lower() == "center":
                #cache_localization = [0, 0]
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

    def set_size(self, x: int, y: int, mode: str = "", opengl: bool = False):
        self.opengl = opengl
        flag = mode_flags.get(mode.upper(), 0)
        if opengl:
            self.screen = pygame.display.set_mode((x, y), flag | 1073741824 | 2)
            gluPerspective(45, (x / y), 0.1, 500.0)
        else:
            self.screen = pygame.display.set_mode((x, y), flag)
