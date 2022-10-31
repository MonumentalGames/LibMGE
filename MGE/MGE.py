import pygame
from PIL import Image as PIL_Image

from .Window import Screen
from .Keyboard import keyboard
from .Platform import Platform

if not Platform.system == "Android":
    from OpenGL.GL import *
    # from OpenGL.GLU import *

Object_List = []

MGE_ver = "1.0.9"

class Cache:
    class Temp:
        class Screen:

            class IMG:
                def __init__(self, img=None):
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

                def set_img(self, img=None):
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

    class Temp:
        Resolution = [0, 0]
        cursor = 0

    def __init__(self):
        pygame.init()
        pygame.font.init()

        #numpass, numfail = pygame.init()
        #print('Number of modules initialized successfully:', numpass)
        #print('Number of modules initialized fail:', numfail)

        self.screen = Screen()
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

Program = Object_Program()
