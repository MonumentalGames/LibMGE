import pygame

from .Window import Screen
from .Global_Cache import Cache
from .Version import version_print
from .Keyboard import keyboard
from .Platform import Platform

from OpenGL.GL import *
from OpenGL.GLU import *

class Object_Program:

    class Temp:
        Resolution = [0, 0]
        cursor = 0

    def __init__(self):
        self.screen = Screen()
        self.event = pygame.event.poll()
        self.time = {"mon": 0, "day": 0, "hours": 0, "min": 0, "sec": 0}
        self.clock = 0
        self.pygame = pygame

        self.default_font = pygame.font.get_default_font()

        #Cache.Temp.Screen.img = Image(pygame.Surface.convert(self.screen.screen))

    def init(self):
        self.pygame.init()
        self.pygame.font.init()
        self.set_caption("MGE")
        version_print()

    def update(self, still_frame_optimization: bool = False, save_last_rendered_frame: bool = True):
        if not self.clock == 0:
            self.screen.clock.tick(self.clock)

        #cache_time = time.localtime(time.time())
        #self.time = {"year": cache_time.tm_year, "mon": cache_time.tm_mon, "day": cache_time.tm_mday, "hour": cache_time.tm_hour, "min": cache_time.tm_min, "sec": cache_time.tm_sec}

        self.Temp.Resolution = list(self.screen.screen.get_size())
        self.event = pygame.event.poll()

        if Cache.Temp.Button["button_active"]:
            Cache.Temp.Button["button_active"] = False

        self.screen.render()

        if still_frame_optimization:
            if self.event or keyboard("all"):
                if not Platform.system == "Android":
                    if self.screen.opengl:
                        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                if not pygame.mouse.get_cursor().data[0] == self.Temp.cursor:
                    pygame.mouse.set_cursor(self.Temp.cursor)
                self.cursor(0)

                if save_last_rendered_frame:
                    Cache.Temp.Screen.img.set_img(pygame.Surface.convert(self.screen.screen))

                #pygame.display.update()
                pygame.display.flip()
        else:
            if not Platform.system == "Android":
                if self.screen.opengl:
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            if not pygame.mouse.get_cursor().data[0] == self.Temp.cursor:
                pygame.mouse.set_cursor(self.Temp.cursor)
            self.cursor(0)

            if save_last_rendered_frame:
                Cache.Temp.Screen.img.set_img(pygame.Surface.convert(self.screen.screen))

            pygame.display.flip()

        #self.event_render = False

    def cursor(self, cursor):
        self.Temp.cursor = cursor

    def set_clock(self, clock: int):
        self.clock = clock

    def set_caption(self, caption):
        self.pygame.display.set_caption(caption)

    def set_icon(self, image):
        cache_img = image.image
        self.pygame.display.set_icon(pygame.image.fromstring(cache_img.tobytes(), cache_img.size, cache_img.mode))

    def get_fps(self):
        return self.screen.clock.get_fps()

Program = Object_Program()
