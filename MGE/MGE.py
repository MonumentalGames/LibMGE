import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image as PIL_Image
#import threading
#import time
#import os

from .Keyboard import keyboard

Object_List = []

MGE_ver = "0.0.1"

class Cache:
    class Temp:
        class Screen:

            class IMG:
                def __init__(self, img=None, mode="RGB"):
                    if img is not None:
                        self.image = img
                        image_size = self.image.get_size()

                        #res = 480 / image_size[1]
                        #image_size = (int(res * image_size[0]), int(res * image_size[1]))

                        raw_str = pygame.image.tostring(pygame.transform.scale(self.image, image_size), "RGB", False)
                        self.image = PIL_Image.frombytes("RGB", image_size, raw_str)
                        self.size = self.image.size
                    else:
                        self.image = PIL_Image.new("RGB", (32, 32), color=(0, 0, 0))
                        self.size = self.image.size

                def set_img(self, img=None, mode="RGB"):
                    if img is not None:
                        self.image = img
                        image_size = self.image.get_size()

                        #res = 480 / image_size[1]
                        #image_size = (int(res * image_size[0]), int(res * image_size[1]))

                        raw_str = pygame.image.tostring(pygame.transform.scale(self.image, image_size), "RGB", False)
                        self.image = PIL_Image.frombytes("RGB", image_size, raw_str)
                        self.size = self.image.size
                    else:
                        self.image = PIL_Image.new("RGB", (32, 32), color=(0, 0, 0))
                        self.size = self.image.size
            img = IMG()

        class Keyboard:
            key_all_cache = True

            key_specebar_cache = True
            key_backspace_cache = True
            key_period_cache = True

            key_1_cache = True
            key_2_cache = True
            key_3_cache = True
            key_4_cache = True
            key_5_cache = True
            key_6_cache = True
            key_7_cache = True
            key_8_cache = True
            key_9_cache = True
            key_0_cache = True

            key_a_cache = True
            key_b_cache = True
            key_c_cache = True
            key_d_cache = True
            key_e_cache = True
            key_f_cache = True
            key_g_cache = True
            key_h_cache = True
            key_i_cache = True
            key_j_cache = True
            key_k_cache = True
            key_l_cache = True
            key_m_cache = True
            key_n_cache = True
            key_o_cache = True
            key_p_cache = True
            key_q_cache = True
            key_r_cache = True
            key_s_cache = True
            key_t_cache = True
            key_u_cache = True
            key_v_cache = True
            key_w_cache = True
            key_x_cache = True
            key_y_cache = True
            key_z_cache = True

            key_up_cache = True
            key_left_cache = True
            key_right_cache = True

    class Mouse_Button:
        button_cache = [False, False, False, False, False]

class Object_Program:
    class Screen:

        class Camera:
            def __init__(self, x=0, y=0):
                self.loc_x = x
                self.loc_y = y
                # self.loc_z = loc[2]

            def set_location(self, loc):
                self.loc_x = loc[0]
                self.loc_y = loc[1]
                # self.loc_z = loc[2]

            def get_location(self):
                return self.loc_x, self.loc_y

        def __init__(self):
            self.screen = pygame.display.set_mode((1, 1))
            self.opengl = False
            self.clock = pygame.time.Clock()
            self.camera = self.Camera()

        @staticmethod
        def get_screen_type():
            return "main"

        def get_screen_img(self):
            image = self.screen
            image_size = image.get_size()
            raw_str = pygame.image.tostring(pygame.transform.scale(image, image_size), "RGB", False)
            return PIL_Image.frombytes("RGB", image_size, raw_str)

        def set_size(self, x, y, mode=False, opengl=False):
            Program.Temp.Resolution = [x, y]
            self.opengl = opengl
            if not mode:
                if opengl:
                    self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL)
                    gluPerspective(45, (x / y), 0.1, 500.0)
                else:
                    self.screen = pygame.display.set_mode((x, y))
            elif mode == "RESIZABLE":
                if opengl:
                    self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL | RESIZABLE)
                    gluPerspective(45, (x / y), 0.1, 500.0)
                else:
                    self.screen = pygame.display.set_mode((x, y), RESIZABLE)
            elif mode == "FULLSCREEN":
                if opengl:
                    self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL | FULLSCREEN)
                    gluPerspective(45, (x / y), 0.1, 500.0)
                else:
                    self.screen = pygame.display.set_mode((x, y), FULLSCREEN)

    class Temp:
        Resolution = [0, 0]
        cursor = 0

    def __init__(self):
        pygame.init()
        pygame.font.init()

        #numpass, numfail = pygame.init()
        #print('Number of modules initialized successfully:', numpass)
        #print('Number of modules initialized fail:', numfail)

        self.screen = self.Screen()
        self.event = pygame.event.poll()
        self.time = {"mon": 0, "day": 0, "hours": 0, "min": 0, "sec": 0}
        self.clock = 0
        self.pygame = pygame

        self.default_font = pygame.font.get_default_font()

        #Cache.Temp.Screen.img = Image(pygame.Surface.convert(self.screen.screen))

    def update(self, still_frame_optimization=False, save_last_rendered_frame=True):
        if not self.clock == 0:
            self.screen.clock.tick(self.clock)


        #cache_time = time.localtime(time.time())
        #self.time = {"year": cache_time.tm_year, "mon": cache_time.tm_mon, "day": cache_time.tm_mday, "hour": cache_time.tm_hour, "min": cache_time.tm_min, "sec": cache_time.tm_sec}

        self.Temp.Resolution = self.screen.screen.get_size()
        self.event = pygame.event.poll()

        if still_frame_optimization:
            if self.event or keyboard("all"):
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
            if self.screen.opengl:
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            if not pygame.mouse.get_cursor().data[0] == self.Temp.cursor:
                pygame.mouse.set_cursor(self.Temp.cursor)
            self.cursor(0)

            if save_last_rendered_frame:
                Cache.Temp.Screen.img.set_img(pygame.Surface.convert(self.screen.screen))

            #pygame.display.update()
            pygame.display.flip()

        #self.event_render = False

    def cursor(self, cursor):
        self.Temp.cursor = cursor

    def set_clock(self, clock):
        self.clock = clock

    def set_caption(self, caption):
        self.pygame.display.set_caption(caption)

    def set_icon(self, image):
        cache_img = image.image
        self.pygame.display.set_icon(pygame.image.fromstring(cache_img.tobytes(), cache_img.size, cache_img.mode))

    def get_fps(self):
        return self.screen.clock.get_fps()

class Internal_Screen:
    def __init__(self, localization, size):
        self.screen = Program.screen.screen
        #self.screen = pygame.Surface(size, pygame.SRCALPHA)
        #pygame.draw.rect(self.screen, (30, 30, 30, 255), (0, 0, *size))

        self.localization = localization
        self.size = size

        self.cache_screen = pygame.Surface(size, pygame.SRCALPHA)

        self.camera = Program.screen.Camera()

        self.render = False
        self.always_render = False

    def draw_screen(self, screen):
        loc_camera = screen.camera.get_location()
        size_screen = screen.screen.get_size()
        cache_size = self.size
        cache_localization = self.localization

        if "%" in str(cache_localization[0]):
            cache_000 = str(cache_localization[0]).replace("%", "")
            cache_000 = int(cache_000)
            cache_localization = (size_screen[0] / 100 * cache_000, cache_localization[1])
        if "%" in str(cache_localization[1]):
            cache_000 = str(cache_localization[1]).replace("%", "")
            cache_000 = int(cache_000)
            cache_localization = [cache_localization[0], size_screen[1] / 100 * cache_000]

        if "%" in str(cache_size[0]):
            cache_000 = str(cache_size[0]).replace("%", "")
            cache_000 = int(cache_000)
            cache_size = (size_screen[0] / 100 * cache_000, cache_size[1])
        if "%" in str(cache_size[1]):
            cache_000 = str(cache_size[1]).replace("%", "")
            cache_000 = int(cache_000)
            cache_size = (cache_size[0], size_screen[1] / 100 * cache_000)

        #if self.scale:
        #    if self.xy == "x":
        #        res = cache_size[0] / self.scale[0]
        #    elif self.xy == "y":
        #        res = cache_size[1] / self.scale[1]
        #    else:
        #        res = 50
        #    cache_size = (int(res * self.scale[0]), int(res * self.scale[1]))

        if cache_localization[0] == "center_obj":
            cache_localization[0] = (size_screen[0] - cache_size[0]) / 2
        if cache_localization[1] == "center_obj":
            cache_localization[1] = (size_screen[1] - cache_size[1]) / 2

        try:
            cache_localization = [cache_localization[0] + loc_camera[0], cache_localization[1] + loc_camera[1]]
        except TypeError:
            print("Error")
            cache_localization = [0, 0]

        if not self.render or self.always_render:
            self.cache_screen = pygame.Surface(cache_size, pygame.SRCALPHA)
            pygame.draw.rect(self.cache_screen, (255, 255, 255, 255), (0, 0, *cache_size), border_radius=0)
            self.cache_screen.blit(self.screen, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            self.screen = pygame.Surface(cache_size, pygame.SRCALPHA)
            pygame.draw.rect(self.screen, (255, 255, 255, 255), (0, 0, *cache_size), border_radius=0)

            #if 254 >= self.material.alpha >= 0:
            #    self.cache_object.set_alpha(self.material.alpha)
            #if self.rotation > 0:
            #    self.cache_object = pygame.transform.rotate(self.cache_object, self.rotation)

            self.render = True

        #if not self.border_size == 0:
        #    screen.screen.blit(self.cache_object, (cache_localization[0], cache_localization[1]))
        #    pygame.draw.rect(screen.screen, self.border_color, (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), self.border_size, border_radius=self.border_radius)
        #else:
        #    # pygame.draw.rect(cache_object, self.material.get_color(), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_radius=self.border_radius)
        screen.screen.blit(self.cache_screen, (cache_localization[0], cache_localization[1]))

    def set_loc_size(self, localization, size):
        self.localization = localization
        self.size = size

    def get_localization(self):
        size_screen = Program.screen.screen.get_size()
        cache_localization = self.localization

        if "%" in str(cache_localization[0]):
            cache_000 = str(cache_localization[0]).replace("%", "")
            cache_000 = int(cache_000)
            cache_localization = (size_screen[0] / 100 * cache_000, cache_localization[1])
        if "%" in str(cache_localization[1]):
            cache_000 = str(cache_localization[1]).replace("%", "")
            cache_000 = int(cache_000)
            cache_localization = [cache_localization[0], size_screen[1] / 100 * cache_000]

        return cache_localization

    def get_size(self):
        size_screen = Program.screen.screen.get_size()
        cache_size = self.size

        if "%" in str(cache_size[0]):
            cache_000 = str(cache_size[0]).replace("%", "")
            cache_000 = int(cache_000)
            cache_size = (size_screen[0] / 100 * cache_000, cache_size[1])
        if "%" in str(cache_size[1]):
            cache_000 = str(cache_size[1]).replace("%", "")
            cache_000 = int(cache_000)
            cache_size = (cache_size[0], size_screen[1] / 100 * cache_000)

        #if self.scale:
        #    if self.xy == "x":
        #        res = cache_size[0] / self.scale[0]
        #    elif self.xy == "y":
        #        res = cache_size[1] / self.scale[1]
        #    else:
        #        res = 50
        #    cache_size = (int(res * self.scale[0]), int(res * self.scale[1]))

        return cache_size

    @staticmethod
    def get_screen_type():
        return "Internal"

Program = Object_Program()
