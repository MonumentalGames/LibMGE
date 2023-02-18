import pygame
from pygame._sdl2 import Window, Renderer
from pygame._sdl2 import messagebox as mess

#from .Camera import Camera

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

        #if "%" in str(cache_localization[0]):
        #   cache_000 = str(cache_localization[0]).replace("%", "")
        #    cache_000 = int(cache_000)
        #   cache_localization = (size_screen[0] / 100 * cache_000, cache_localization[1])
        #if "%" in str(cache_localization[1]):
        #    cache_000 = str(cache_localization[1]).replace("%", "")
        #    cache_000 = int(cache_000)
        #    cache_localization = [cache_localization[0], size_screen[1] / 100 * cache_000]

        return cache_localization

    def get_size(self):
        return self.size

    def get_screen_type(self):
        return self.__Window_Type__

def test():
    print("oi")

def messagebox(title: str = "MGE", message: str = "Hello!", info: bool = True, buttons=(("Yes", "exit"), ("No", test), ("Chance", None)), ):
    buttons_name = []
    buttons_fun = []

    for but in buttons:
        buttons_name.append(but[0])
        buttons_fun.append(but[1])

    me = mess(
        title=title,
        message=message,
        info=info,
        buttons=buttons_name,
        )

    fun = buttons_fun[me]

    if fun is None:
        pass
    else:
        print(fun)
        try:
            fun()
        except:
            pass

    print(me)

#messagebox()
