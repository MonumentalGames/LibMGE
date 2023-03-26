import pygame

from .Window import Screen
from .Global_Cache import Cache
from .Version import version_print
from .Keyboard import keyboard
from .Image import Image

class Object_Program:

    class Temp:
        Resolution = [0, 0]
        ForceRender = False
        cursor = 0

    def __init__(self):
        self.screen = None
        self.event = None
        self.clock = 0
        self.pygame = pygame
        self.default_font = None

    def init(self, title=None):
        #sdl2: bool = False
        self.pygame.init()
        self.pygame.font.init()

        self.screen = Screen()
        self.event = pygame.event.poll()

        self.default_font = pygame.font.get_default_font()

        self.set_caption(title if title else "MGE")
        self.set_icon(Image(color=(70, 70, 70)))
        version_print()

    def update(self, still_frame_optimization: bool = False, save_last_rendered_frame: bool = False):
        if not self.clock == 0:
            self.screen.clock.tick(self.clock)

        self.Temp.Resolution = list(self.screen.get_size())
        self.event = pygame.event.poll()

        if Cache.Temp.Button["button_active"]:
            Cache.Temp.Button["button_active"] = False

        if still_frame_optimization:
            if not (self.event or keyboard("all")) and not self.Temp.ForceRender:
                return

        self.Temp.ForceRender = False

        if not pygame.mouse.get_cursor().data[0] == self.Temp.cursor:
            pygame.mouse.set_cursor(self.Temp.cursor)
        self.cursor(0)

        if save_last_rendered_frame:
            Cache.Temp.Screen.img.set_img(pygame.Surface.convert(self.screen.screen))

        if self.screen.sdl2:
            self.screen.screen.clear()
            self.screen.screen.present()
        else:
            pygame.display.flip()

    def cursor(self, cursor):
        self.Temp.cursor = cursor

    def set_clock(self, clock: int):
        self.clock = clock

    def set_caption(self, caption):
        if self.screen.sdl2:
            pass
        else:
            self.pygame.display.set_caption(caption)

    def set_icon(self, image):
        if self.screen.sdl2:
            pass
        else:
            cache_img = image.image
            self.pygame.display.set_icon(pygame.image.fromstring(cache_img.tobytes(), cache_img.size, cache_img.mode))

    def get_fps(self):
        return self.screen.clock.get_fps()

Program = Object_Program()
