import pygame
from pygame._sdl2 import Window, Renderer
from PIL import Image as PIL_Image
from screeninfo import get_monitors

#from .Global_Cache import Cache
from .Camera import Camera
from .Platform import Platform

mode_flags = {"NOFRAME": 32, "RESIZABLE": 16, "FULLSCREEN": -2147483648}

class Screen_inputs:
    quit = 256

class Screen:
    def __init__(self, sdl2: bool = False):
        self.__Window_Type__ = "main"

        if sdl2:
            self.window_sdl2 = Window()
            self.screen_sdl2 = Renderer(self.window_sdl2)
        else:
            if Platform.system == "Android":
                self.screen = pygame.display.set_mode((0, 0))
            else:
                self.screen = pygame.display.set_mode((1, 1), 32)

        self.monitor_resolution = [get_monitors()[0].width, get_monitors()[0].height]

        self.object_draw_list = []

        self.sdl2 = sdl2
        self.opengl = False
        self.clock = pygame.time.Clock()
        self.camera = Camera()

    def get_screen_img(self):
        if self.sdl2:
            return
        else:
            image = self.screen
            image_size = self.get_size()
            raw_str = pygame.image.tostring(pygame.transform.scale(image, image_size), "RGB", False)
            return PIL_Image.frombytes("RGB", image_size, raw_str)

    def get_size(self):
        if self.sdl2:
            return list(self.window_sdl2.size)
        else:
            return self.screen.get_size()

    def set_localization(self, localization):
        if type(localization) is str:
            if localization.lower() == "center":
                cache_localization = [int((self.monitor_resolution[0] - self.get_size()[0]) / 2), int((self.monitor_resolution[1] - self.get_size()[1]) / 2)]
            else:
                return
        elif type(localization) is list:
            cache_localization = localization
        else:
            return
        if self.sdl2:
            self.window_sdl2.position = tuple(cache_localization)
        else:
            if not Platform.system == "Android" and not Platform.system == "Linux":
                pass
                #hwnd = pygame.display.get_wm_info()['window']
                #w, h = self.screen.get_size()
                #windll.user32.MoveWindow(hwnd, cache_localization[0], cache_localization[1], w, h, False)

    def set_size(self, x: int, y: int, mode: str = "", sdl2: bool = False):
        self.sdl2 = sdl2
        flag = mode_flags.get(mode.upper(), 0)
        if sdl2:
            self.window_sdl2.size = (x, y)
        else:
            self.window_sdl2 = None
            self.screen_sdl2 = None
            self.screen = pygame.display.set_mode((x, y), flag)
