import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image as PIL_Image, ImageFilter as ImageFilter
import threading
import time
import os

Object_List = []

ver = "0.0.1"

class Cache:
    class Temp:
        class Screen:
            class IMG:
                def __init__(self, img=False, mode="RGB"):
                    if img:
                        self.image = img
                        image_size = self.image.get_size()

                        res = 480 / image_size[1]
                        image_size = (int(res * image_size[0]), int(res * image_size[1]))

                        raw_str = pygame.image.tostring(pygame.transform.scale(self.image, image_size), mode, False)
                        self.image = PIL_Image.frombytes(mode, image_size, raw_str)
                        self.size = self.image.size
                    else:
                        self.image = PIL_Image.new(mode, (32, 32), color=(0, 0, 0))
                        self.size = self.image.size

                def set_img(self, img=False, mode="RGB"):
                    if img:
                        self.image = img
                        image_size = self.image.get_size()

                        res = 480 / image_size[1]
                        image_size = (int(res * image_size[0]), int(res * image_size[1]))

                        raw_str = pygame.image.tostring(pygame.transform.scale(self.image, image_size), mode, False)
                        self.image = PIL_Image.frombytes(mode, image_size, raw_str)
                        self.size = self.image.size
                    else:
                        self.image = PIL_Image.new(mode, (32, 32), color=(0, 0, 0))
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
            self.clock = pygame.time.Clock()
            self.camera = self.Camera()

        @staticmethod
        def get_screen_type():
            return "main"

        def set_size(self, x, y, mode=False, opengl=False):
            if not mode:
                if opengl:
                    self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL)
                else:
                    self.screen = pygame.display.set_mode((x, y))
            elif mode == "RESIZABLE":
                if opengl:
                    self.screen = pygame.display.set_mode((x, y), DOUBLEBUF | OPENGL)
                else:
                    self.screen = pygame.display.set_mode((x, y), pygame.RESIZABLE)

    class Temp:
        Resolution = [0, 0]
        cursor = 0

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = self.Screen()
        self.event = pygame.event.poll()
        self.time = {"mon": 0, "day": 0, "hours": 0, "min": 0, "sec": 0}
        self.clock = 0
        self.pygame = pygame

        self.mouse_pos = pygame.mouse.get_pos()

        self.default_font = pygame.font.get_default_font()

        #Cache.Temp.Screen.img = Image(pygame.Surface.convert(self.screen.screen))

    def update(self, still_frame_optimization=False, save_last_rendered_frame=True):
        if not self.clock == 0:
            self.screen.clock.tick(self.clock)

        #cache_time = time.localtime(time.time())
        #self.time = {"year": cache_time.tm_year, "mon": cache_time.tm_mon, "day": cache_time.tm_mday, "hour": cache_time.tm_hour, "min": cache_time.tm_min, "sec": cache_time.tm_sec}

        self.Temp.Resolution = self.screen.screen.get_size()
        self.event = pygame.event.poll()

        self.mouse_pos = pygame.mouse.get_pos()

        if still_frame_optimization:
            if self.event or keyboard("all"):
                if not pygame.mouse.get_cursor().data[0] == self.Temp.cursor:
                    pygame.mouse.set_cursor(self.Temp.cursor)
                self.cursor(0)

                if save_last_rendered_frame:
                    Cache.Temp.Screen.img.set_img(pygame.Surface.convert(self.screen.screen))

                #pygame.display.update()
                pygame.display.flip()
        else:
            if not pygame.mouse.get_cursor().data[0] == self.Temp.cursor:
                pygame.mouse.set_cursor(self.Temp.cursor)
            self.cursor(0)

            if save_last_rendered_frame:
                Cache.Temp.Screen.img.set_img(pygame.Surface.convert(self.screen.screen))

            pygame.display.update()

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

    def get_mouse_pos(self):
        return self.mouse_pos

class Internal_Screen:
    def __init__(self, screen, localization, size):
        self.screen = screen.screen
        self.localization = localization
        self.size = size

        self.camera = Program.screen.Camera()

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

    @staticmethod
    def get_screen_type():
        return "Internal"

class ObjectText:
    def __init__(self, localization, size, text="", font=pygame.font.get_default_font()):
        self.localization = localization
        self.size = size

        self.font = font
        self.color = [255, 255, 255]
        self.text = text
        self.text_render_cache = False

        self.cursor = 11

        self.text_render = None
        self.text_render_font = None
        self.text_render_size = None

    def set_font(self, font):
        if self.font == font:
            pass
        else:
            self.font = font

    def set_color(self, color):
        if self.color == color:
            pass
        else:
            self.color = color
            self.text_render_cache = False

    def set_text(self, text):
        if self.text == text:
            pass
        else:
            self.text = text
            self.text_render_cache = False

    def set_localization(self, localization):
        if self.localization == localization:
            pass
        else:
            self.localization = localization
            self.text_render_cache = False

    def set_size(self, size):
        if self.size == size:
            pass
        else:
            self.size = size
            self.text_render_cache = False

    def set_loc_siz(self, localization, size):
        if self.size == size:
            pass
        else:
            self.size = size
            self.text_render_cache = False
        if self.localization == localization:
            pass
        else:
            self.localization = localization
            self.text_render_cache = False

    def get_text(self):
        return self.text

    def get_text_size(self):
        if self.text_render_cache:
            pass
        else:
            self.render()
        return self.text_render_size

    def render(self):
        self.text_render_font = pygame.font.SysFont(self.font, self.size)
        self.text_render_size = self.text_render_font.size(self.text)
        self.text_render = self.text_render_font.render(self.text, 1, self.color)
        self.text_render_cache = True

    def draw_object(self, screen, render):
        loc_camera = screen.camera.get_location()
        if screen.get_screen_type() == "main":
            size_screen = screen.screen.get_size()
            cache_localization = self.localization

            if "%" in str(cache_localization[0]):
                cache_000 = str(cache_localization[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_localization = (size_screen[0] / 100 * cache_000, cache_localization[1])
            if "%" in str(cache_localization[1]):
                cache_000 = str(cache_localization[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_localization = [cache_localization[0], size_screen[1] / 100 * cache_000]

            if cache_localization[0] == "center_obj":
                cache_localization[0] = (size_screen[0] - cache_size[0]) / 2
            if cache_localization[1] == "center_obj":
                cache_localization[1] = (size_screen[1] - cache_size[1]) / 2

            try:
                cache_localization = [cache_localization[0] + loc_camera[0], cache_localization[1] + loc_camera[1]]
            except TypeError:
                print("Error")
                cache_localization = [0, 0]
        elif screen.get_screen_type() == "Internal":
            size_screen = screen.screen.get_size()

            cache_screen_size = screen.size
            cache_screen_localization = screen.localization

            cache_size = self.size
            cache_localization = self.localization

            if "%" in str(cache_screen_localization[0]):
                cache_000 = str(cache_screen_localization[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_localization = (size_screen[0] / 100 * cache_000, cache_screen_localization[1])
            if "%" in str(cache_screen_localization[1]):
                cache_000 = str(cache_screen_localization[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_localization = [cache_screen_localization[0], size_screen[1] / 100 * cache_000]

            if "%" in str(cache_screen_size[0]):
                cache_000 = str(cache_screen_size[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_size = (size_screen[0] / 100 * cache_000, cache_screen_size[1])
            if "%" in str(cache_screen_size[1]):
                cache_000 = str(cache_screen_size[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_size = (cache_screen_size[0], size_screen[1] / 100 * cache_000)

            if cache_screen_localization[0] == "center_obj":
                cache_screen_localization[0] = (size_screen[0] - cache_screen_size[0]) / 2
            if cache_screen_localization[1] == "center_obj":
                cache_screen_localization[1] = (size_screen[1] - cache_screen_size[1]) / 2

            ##-----------------------------------------------------##

            if "%" in str(cache_localization[0]):
                cache_000 = str(cache_localization[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_localization = (size_screen[0] / 100 * cache_000, cache_localization[1])
            if "%" in str(cache_localization[1]):
                cache_000 = str(cache_localization[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_localization = [cache_localization[0], size_screen[1] / 100 * cache_000]

            if cache_localization[0] == "center_obj":
                cache_localization[0] = (size_screen[0] - cache_size[0]) / 2
            if cache_localization[1] == "center_obj":
                cache_localization[1] = (size_screen[1] - cache_size[1]) / 2

            try:
                cache_localization = [cache_localization[0] + loc_camera[0], cache_localization[1] + loc_camera[1]]
                cache_localization = [cache_localization[0] + cache_screen_localization[0], cache_localization[1] + cache_screen_localization[1]]
            except TypeError:
                print("Error")
                cache_localization = screen.localization
        else:
            cache_size = self.size
            try:
                cache_localization = [self.localization[0] + loc_camera[0], self.localization[1] + loc_camera[1]]
            except TypeError:
                print("Error")
                cache_localization = [0, 0]

        if render:
            if self.text:
                if self.text_render_cache:
                    screen.screen.blit(self.text_render, (cache_localization[0], cache_localization[1]))
                else:
                    self.render()
                    if self.text_render_cache:
                        screen.screen.blit(self.text_render, (cache_localization[0], cache_localization[1]))
            else:
                pass
        else:
            if not self.text_render_cache:
                pass
            if self.text:
                screen.screen.blit(self.text_render, (cache_localization[0], cache_localization[1]))

class Object2D:
    def __init__(self, localization, size):
        self.localization = localization
        self.size = size
        self.model = None
        self.scale = None
        self.border_radius = 0
        self.xy = None
        self.cursor = 11
        self.material = Material_Error
        self.variables = {}

    def draw_object(self, screen, camera=None, index=1):
        if screen.get_screen_type() == "main":
            if camera:
                loc_camera = camera.get_location()
            else:
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

            if self.scale:
                if self.xy == "x":
                    res = cache_size[0] / self.scale[0]
                elif self.xy == "y":
                    res = cache_size[1] / self.scale[1]
                else:
                    res = 50
                cache_size = (int(res * self.scale[0]), int(res * self.scale[1]))

            if cache_localization[0] == "center_obj":
                cache_localization[0] = (size_screen[0] - cache_size[0]) / 2
            if cache_localization[1] == "center_obj":
                cache_localization[1] = (size_screen[1] - cache_size[1]) / 2

            try:
                cache_localization = [cache_localization[0] + loc_camera[0], cache_localization[1] + loc_camera[1]]
            except TypeError:
                print("Error")
                cache_localization = [0, 0]
        elif screen.get_screen_type() == "Internal":
            if camera:
                loc_camera = camera.get_location()
            else:
                loc_camera = screen.camera.get_location()
            size_screen = screen.screen.get_size()

            cache_screen_size = screen.size
            cache_screen_localization = screen.localization

            cache_size = self.size
            cache_localization = self.localization

            ##-----------------------------------------------------##

            if "%" in str(cache_screen_localization[0]):
                cache_000 = str(cache_screen_localization[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_localization = (size_screen[0] / 100 * cache_000, cache_screen_localization[1])
            if "%" in str(cache_screen_localization[1]):
                cache_000 = str(cache_screen_localization[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_localization = [cache_screen_localization[0], size_screen[1] / 100 * cache_000]

            if "%" in str(cache_screen_size[0]):
                cache_000 = str(cache_screen_size[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_size = (size_screen[0] / 100 * cache_000, cache_screen_size[1])
            if "%" in str(cache_screen_size[1]):
                cache_000 = str(cache_screen_size[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_size = (cache_screen_size[0], size_screen[1] / 100 * cache_000)

            if self.scale:
                if self.xy == "x":
                    res = cache_screen_size[0] / self.scale[0]
                elif self.xy == "y":
                    res = cache_screen_size[1] / self.scale[1]
                else:
                    res = 50
                cache_screen_size = (int(res * self.scale[0]), int(res * self.scale[1]))

            if cache_screen_localization[0] == "center_obj":
                cache_screen_localization[0] = (size_screen[0] - cache_screen_size[0]) / 2
            if cache_screen_localization[1] == "center_obj":
                cache_screen_localization[1] = (size_screen[1] - cache_screen_size[1]) / 2

            ##-----------------------------------------------------##

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

            if self.scale:
                if self.xy == "x":
                    res = cache_size[0] / self.scale[0]
                elif self.xy == "y":
                    res = cache_size[1] / self.scale[1]
                else:
                    res = 50
                cache_size = (int(res * self.scale[0]), int(res * self.scale[1]))

            if cache_localization[0] == "center_obj":
                cache_localization[0] = (size_screen[0] - cache_size[0]) / 2
            if cache_localization[1] == "center_obj":
                cache_localization[1] = (size_screen[1] - cache_size[1]) / 2

            ##-----------------------------------------------------##

            #print(f"internal{screen.localization}-{screen.size}")

            try:
                cache_localization = [cache_localization[0] + loc_camera[0], cache_localization[1] + loc_camera[1]]
                cache_localization = [cache_localization[0] + cache_screen_localization[0], cache_localization[1] + cache_screen_localization[1]]
            except TypeError:
                print("Error")
                cache_localization = screen.localization

            #cache_localization = cache_localization + screen.localization
        else:
            if camera:
                loc_camera = camera.get_location()
            else:
                loc_camera = screen.camera.get_location()
            cache_size = self.size
            try:
                cache_localization = [self.localization[0] + loc_camera[0], self.localization[1] + loc_camera[1]]
            except TypeError:
                print("Error")
                cache_localization = [0, 0]

        if self.material:
            if self.material.texture or 254 >= self.material.alpha >= 0:
                if self.material.texture:
                    self.material.render()
                    img_cache = self.material.Surface
                    cache_object = pygame.transform.scale(img_cache, [cache_size[0], cache_size[1]])
                else:
                    cache_object = pygame.Surface((cache_size[0], cache_size[1]))
                    cache_object.fill(self.material.color)
                if 254 >= self.material.alpha >= 0:
                    print(self.material.alpha)
                    cache_object.set_alpha(self.material.alpha)
                screen.screen.blit(cache_object, (cache_localization[0], cache_localization[1]))
            else:
                try:
                    pygame.draw.rect(screen.screen, self.material.get_color(), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_radius=self.border_radius)
                except TypeError:
                    print("Error")
        else:
            pygame.draw.rect(screen.screen, (200, 200, 200), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_radius=self.border_radius)

    def over(self, camera):
        loc_camera = camera.get_location()
        size_screen = Program.screen.screen.get_size()
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

        if self.scale:
            if self.xy == "x":
                res = cache_size[0] / self.scale[0]
            elif self.xy == "y":
                res = cache_size[1] / self.scale[1]
            else:
                res = 50
            cache_size = (int(res * self.scale[0]), int(res * self.scale[1]))

        if cache_localization[0] == "center_obj":
            cache_localization[0] = (size_screen[0] - cache_size[0]) / 2
        if cache_localization[1] == "center_obj":
            cache_localization[1] = (size_screen[1] - cache_size[1]) / 2

        #######

        mouse_lok = pygame.mouse.get_pos()
        #loc_camera = camera.get_location()
        if cache_localization[0] + loc_camera[0] < mouse_lok[0] < cache_localization[0] + loc_camera[0] + cache_size[0] and cache_localization[1] + loc_camera[1] < mouse_lok[1] < cache_localization[1] + loc_camera[1] + cache_size[1]:
            return True

    def button(self, button, camera):
        if self.over(camera):
            Program.cursor(self.cursor)
            if mouse_button(button):
                return True

    def set_localization(self, localization):
        self.localization = localization

    def set_size(self, size):
        self.size = size

    def set_loc_siz(self, localization, size):
        self.size = size
        self.localization = localization

    def set_border_radius(self, radius):
        self.border_radius = radius

    def set_scale(self, scale, xy):
        self.scale = scale
        self.xy = xy

    def set_material(self, material):
        self.material = material

    def set_cursor(self, cursor):
        self.cursor = cursor

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

        if self.scale:
            if self.xy == "x":
                res = cache_size[0] / self.scale[0]
            elif self.xy == "y":
                res = cache_size[1] / self.scale[1]
            else:
                res = 50
            cache_size = (int(res * self.scale[0]), int(res * self.scale[1]))

        return cache_size

    def motion(self, axis, axis_type, speed):
        #vec = pygame.math.Vector2

        if str(axis_type).lower() == "global":
            if str(axis).lower() == "x":
                self.localization[0] += speed
            if str(axis).lower() == "y":
                self.localization[1] += speed
        if str(axis_type).lower() == "local":
            if str(axis).lower() == "x":
                self.localization = [self.localization[0] + speed, self.localization[1]]
            if str(axis).lower() == "y":
                self.localization[1] = [self.localization[0], self.localization[1] + speed]

class Object3D:
    def __init__(self, model):
        self.model = model
        self.material = Material_Error


class Line2D:
    def __init__(self, start, end, size):
        self.start = start
        self.end = end
        self.size = size

        self.material = Material_Error

        self.color = [0, 0, 0]

    def draw_object(self, screen):
        loc_camera = screen.camera.get_location()
        #size_screen = screen.screen.get_size()

        cache_start = [self.start[0] + loc_camera[0], self.start[1] + loc_camera[1]]
        cache_end = self.end

        cache_size = self.size

        pygame.draw.line(Program.screen.screen, self.material.color, cache_start, cache_end, cache_size)

    def set_start_end(self, start, end):
        self.start = start
        self.end = end

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

    def set_material(self, material):
        self.material = material

class Line3D:
    def __init__(self):
        pass

class Material:
    def __init__(self, texture=False, color=(120, 120, 255), alpha=255):
        self.color = color
        self.alpha = alpha
        if texture:
            self.texture = texture
        else:
            self.texture = None
        self.Surface = None
        self.Sprite = None
        self.Sprite_Data = ["", [0, 0], [0, 0]]

    def render(self):
        cache_img = self.texture.image.image
        if self.Sprite:
            cache_img = cache_img.crop(self.Sprite.get_size_localization())
        if self.texture.blurr >= 1:
            cache_img = cache_img.filter(ImageFilter.BoxBlur(self.texture.blurr))
        self.Surface = pygame.image.fromstring(cache_img.tobytes(), cache_img.size, cache_img.mode)

    def add_texture(self, texture):
        self.texture = texture

    def set_color(self, color):
        self.color = color

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_color(self):
        return self.color

    def get_alpha(self):
        return self.alpha

    def get_textures(self):
        return self.texture

class Texture:
    def __init__(self, image):
        #self.original_image = image
        self.image = image
        self.blurr = 0

    def set_image(self, image):
        #self.original_image = image
        self.image = image

    def set_blurr(self, blurr):
        self.blurr = blurr

class Image:
    def __init__(self, directory_img=False, mode="RGB", size=(32, 32), color=(120, 120, 255)):
        if directory_img:
            if os.path.exists(directory_img):
                try:
                    self.image = PIL_Image.open(directory_img)
                except FileNotFoundError:
                    self.image = PIL_Image.new(mode, size, color=color)

                self.size = self.image.size
            else:
                try:
                    self.image = PIL_Image.frombytes(mode, size, directory_img)
                except:
                    self.image = PIL_Image.new(mode, size, color=color)
            #except TypeError:
            #    print("error")
            #    self.image = directory_img
            #    self.original_size = self.image.get_size()
            #    self.size = self.original_size
        else:
            self.image = PIL_Image.new(mode, size, color=color)
            self.size = self.image.size

    def set_img(self, directory_img=False, mode="RGB", size=(32, 32), color=(120, 120, 255)):
        if directory_img:
            if os.path.exists(directory_img):
                try:
                    self.image = PIL_Image.open(directory_img)
                except FileNotFoundError:
                    self.image = PIL_Image.new(mode, size, color=color)
                self.size = self.image.size
        else:
            self.image = PIL_Image.new(mode, size, color=color)
            self.size = self.image.size

class Sprite:
    def __init__(self, texture="", localization=(0, 0), size=(0, 0)):
        self.texture = texture
        self.localization = localization
        self.size = size

    def get_size_localization(self):
        return [self.size, self.localization]


def keyboard(key):
    key = str(key).lower()
    event_key = pygame.key.get_pressed()

    if key == "all":
        if event_key[pygame.K_1]:
            return True

        if event_key[pygame.K_2]:
            return True

        if event_key[pygame.K_3]:
            return True

        if event_key[pygame.K_4]:
            return True

        if event_key[pygame.K_5]:
            return True

        if event_key[pygame.K_6]:
            return True

        if event_key[pygame.K_7]:
            return True

        if event_key[pygame.K_8]:
            return True

        if event_key[pygame.K_9]:
            return True

        if event_key[pygame.K_0]:
            return True

        if event_key[pygame.K_a]:
            return True

        if event_key[pygame.K_b]:
            return True

        if event_key[pygame.K_c]:
            return True

        if event_key[pygame.K_d]:
            return True

        if event_key[pygame.K_e]:
            return True

        if event_key[pygame.K_f]:
            return True

        if event_key[pygame.K_g]:
            return True

        if event_key[pygame.K_h]:
            return True

        if event_key[pygame.K_i]:
            return True

        if event_key[pygame.K_j]:
            return True

        if event_key[pygame.K_k]:
            return True

        if event_key[pygame.K_l]:
            return True

        if event_key[pygame.K_m]:
            return True

        if event_key[pygame.K_n]:
            return True

        if event_key[pygame.K_o]:
            return True

        if event_key[pygame.K_p]:
            return True

        if event_key[pygame.K_q]:
            return True

        if event_key[pygame.K_r]:
            return True

        if event_key[pygame.K_s]:
            return True

        if event_key[pygame.K_t]:
            return True

        if event_key[pygame.K_u]:
            return True

        if event_key[pygame.K_v]:
            return True

        if event_key[pygame.K_w]:
            return True

        if event_key[pygame.K_x]:
            return True

        if event_key[pygame.K_y]:
            return True

        if event_key[pygame.K_z]:
            return True

        if event_key[pygame.K_ESCAPE]:
            return True

        if event_key[pygame.K_BACKSPACE]:
            return True

        if event_key[pygame.K_UP]:
            return True

        if event_key[pygame.K_DOWN]:
            return True

        if event_key[pygame.K_LEFT]:
            return True

        if event_key[pygame.K_RIGHT]:
            return True

        if event_key[pygame.K_SPACE]:
            return True

        if event_key[pygame.K_RETURN]:
            return True

        if event_key[pygame.K_LSHIFT] or event_key[pygame.K_RSHIFT]:
            return True

    if key == '1':
        if event_key[pygame.K_1]:
            return True
    if key == '2':
        if event_key[pygame.K_2]:
            return True
    if key == '3':
        if event_key[pygame.K_3]:
            return True
    if key == '4':
        if event_key[pygame.K_4]:
            return True
    if key == '5':
        if event_key[pygame.K_5]:
            return True
    if key == '6':
        if event_key[pygame.K_6]:
            return True
    if key == '7':
        if event_key[pygame.K_7]:
            return True
    if key == '8':
        if event_key[pygame.K_8]:
            return True
    if key == '9':
        if event_key[pygame.K_9]:
            return True
    if key == '0':
        if event_key[pygame.K_0]:
            return True

    if key == 'a':
        if event_key[pygame.K_a]:
            return True
    if key == 'b':
        if event_key[pygame.K_b]:
            return True
    if key == 'c':
        if event_key[pygame.K_c]:
            return True
    if key == 'd':
        if event_key[pygame.K_d]:
            return True
    if key == 'e':
        if event_key[pygame.K_e]:
            return True
    if key == 'f':
        if event_key[pygame.K_f]:
            return True
    if key == 'g':
        if event_key[pygame.K_g]:
            return True
    if key == 'h':
        if event_key[pygame.K_h]:
            return True
    if key == 'i':
        if event_key[pygame.K_i]:
            return True
    if key == 'j':
        if event_key[pygame.K_j]:
            return True
    if key == 'k':
        if event_key[pygame.K_k]:
            return True
    if key == 'l':
        if event_key[pygame.K_l]:
            return True
    if key == 'm':
        if event_key[pygame.K_m]:
            return True
    if key == 'n':
        if event_key[pygame.K_n]:
            return True
    if key == 'o':
        if event_key[pygame.K_o]:
            return True
    if key == 'p':
        if event_key[pygame.K_p]:
            return True
    if key == 'q':
        if event_key[pygame.K_q]:
            return True
    if key == 'r':
        if event_key[pygame.K_r]:
            return True
    if key == 's':
        if event_key[pygame.K_s]:
            return True
    if key == 't':
        if event_key[pygame.K_t]:
            return True
    if key == 'u':
        if event_key[pygame.K_u]:
            return True
    if key == 'v':
        if event_key[pygame.K_v]:
            return True
    if key == 'w':
        if event_key[pygame.K_w]:
            return True
    if key == 'x':
        if event_key[pygame.K_x]:
            return True
    if key == 'y':
        if event_key[pygame.K_y]:
            return True
    if key == 'z':
        if event_key[pygame.K_z]:
            return True

    if key == "esc":
        if event_key[pygame.K_ESCAPE]:
            return True

    if key == 'back':
        if event_key[pygame.K_BACKSPACE]:
            return True

    if key == 'up':
        if event_key[pygame.K_UP]:
            return True
    if key == 'down':
        if event_key[pygame.K_DOWN]:
            return True
    if key == 'left':
        if event_key[pygame.K_LEFT]:
            return True
    if key == 'right':
        if event_key[pygame.K_RIGHT]:
            return True

    if key == 'space':
        if event_key[pygame.K_SPACE]:
            return True

    if key == 'return':
        if event_key[pygame.K_RETURN]:
            return True

    if key == "shift":
        if event_key[pygame.K_LSHIFT] or event_key[pygame.K_RSHIFT]:
            return True

    if key == 'f1':
        if event_key[pygame.K_F1]:
            return True
    if key == 'f2':
        if event_key[pygame.K_F2]:
            return True
    if key == 'f3':
        if event_key[pygame.K_F3]:
            return True
    if key == 'f4':
        if event_key[pygame.K_F4]:
            return True
    if key == 'f5':
        if event_key[pygame.K_F5]:
            return True
    if key == 'f6':
        if event_key[pygame.K_F6]:
            return True
    if key == 'f7':
        if event_key[pygame.K_F7]:
            return True
    if key == 'f8':
        if event_key[pygame.K_F8]:
            return True
    if key == 'f9':
        if event_key[pygame.K_F9]:
            return True
    if key == 'f10':
        if event_key[pygame.K_F10]:
            return True
    if key == 'f11':
        if event_key[pygame.K_F11]:
            return True
    if key == 'f12':
        if event_key[pygame.K_F12]:
            return True

def mouse_button(button, multiple_click=False):
    if multiple_click:
        if button == 1:
            if pygame.mouse.get_pressed(3)[0]:
                return True
        if button == 2:
            if pygame.mouse.get_pressed(3)[1]:
                return True
        if button == 3:
            if pygame.mouse.get_pressed(3)[2]:
                return True
    else:
        if button == 1:
            if pygame.mouse.get_pressed(3)[0]:
                if not Cache.Mouse_Button.button_cache[0]:
                    Cache.Mouse_Button.button_cache[0] = True
                    return True
        if button == 2:
            if pygame.mouse.get_pressed(3)[1]:
                if not Cache.Mouse_Button.button_cache[1]:
                    Cache.Mouse_Button.button_cache[1] = True
                    return True
        if button == 3:
            if pygame.mouse.get_pressed(3)[2]:
                if not Cache.Mouse_Button.button_cache[2]:
                    Cache.Mouse_Button.button_cache[2] = True
                    return True

        if not pygame.mouse.get_pressed(3)[0]:
            Cache.Mouse_Button.button_cache[0] = False
        if not pygame.mouse.get_pressed(3)[1]:
            Cache.Mouse_Button.button_cache[1] = False
        if not pygame.mouse.get_pressed(3)[2]:
            Cache.Mouse_Button.button_cache[2] = False

def text_box(text, type="all"):
    if type == "all":
        set_text = [True, True, True]
    elif type == "number":
        set_text = [False, True, False]
    else:
        set_text = [False, False, False]

    if set_text[0]:
        if keyboard("shift"):

            if keyboard("a"):
                if Cache.Temp.Keyboard.key_a_cache:
                    text += "A"
                    Cache.Temp.Keyboard.key_a_cache = False
            else:
                Cache.Temp.Keyboard.key_a_cache = True

            if keyboard("b"):
                if Cache.Temp.Keyboard.key_b_cache:
                    text += "B"
                    Cache.Temp.Keyboard.key_b_cache = False
            else:
                Cache.Temp.Keyboard.key_b_cache = True

            if keyboard("c"):
                if Cache.Temp.Keyboard.key_c_cache:
                    text += "C"
                    Cache.Temp.Keyboard.key_c_cache = False
            else:
                Cache.Temp.Keyboard.key_c_cache = True

            if keyboard("d"):
                if Cache.Temp.Keyboard.key_d_cache:
                    text += "D"
                    Cache.Temp.Keyboard.key_d_cache = False
            else:
                Cache.Temp.Keyboard.key_d_cache = True

            if keyboard("e"):
                if Cache.Temp.Keyboard.key_e_cache:
                    text += "E"
                    Cache.Temp.Keyboard.key_e_cache = False
            else:
                Cache.Temp.Keyboard.key_e_cache = True

            if keyboard("f"):
                if Cache.Temp.Keyboard.key_f_cache:
                    text += "F"
                    Cache.Temp.Keyboard.key_f_cache = False
            else:
                Cache.Temp.Keyboard.key_f_cache = True

            if keyboard("g"):
                if Cache.Temp.Keyboard.key_g_cache:
                    text += "G"
                    Cache.Temp.Keyboard.key_g_cache = False
            else:
                Cache.Temp.Keyboard.key_g_cache = True

            if keyboard("h"):
                if Cache.Temp.Keyboard.key_h_cache:
                    text += "H"
                    Cache.Temp.Keyboard.key_h_cache = False
            else:
                Cache.Temp.Keyboard.key_h_cache = True

            if keyboard("i"):
                if Cache.Temp.Keyboard.key_i_cache:
                    text += "I"
                    Cache.Temp.Keyboard.key_i_cache = False
            else:
                Cache.Temp.Keyboard.key_i_cache = True

            if keyboard("j"):
                if Cache.Temp.Keyboard.key_j_cache:
                    text += "J"
                    Cache.Temp.Keyboard.key_j_cache = False
            else:
                Cache.Temp.Keyboard.key_j_cache = True

            if keyboard("k"):
                if Cache.Temp.Keyboard.key_k_cache:
                    text += "K"
                    Cache.Temp.Keyboard.key_k_cache = False
            else:
                Cache.Temp.Keyboard.key_k_cache = True

            if keyboard("l"):
                if Cache.Temp.Keyboard.key_l_cache:
                    text += "L"
                    Cache.Temp.Keyboard.key_l_cache = False
            else:
                Cache.Temp.Keyboard.key_l_cache = True

            if keyboard("m"):
                if Cache.Temp.Keyboard.key_m_cache:
                    text += "M"
                    Cache.Temp.Keyboard.key_m_cache = False
            else:
                Cache.Temp.Keyboard.key_m_cache = True

            if keyboard("n"):
                if Cache.Temp.Keyboard.key_n_cache:
                    text += "N"
                    Cache.Temp.Keyboard.key_n_cache = False
            else:
                Cache.Temp.Keyboard.key_n_cache = True

            if keyboard("o"):
                if Cache.Temp.Keyboard.key_o_cache:
                    text += "O"
                    Cache.Temp.Keyboard.key_o_cache = False
            else:
                Cache.Temp.Keyboard.key_o_cache = True

            if keyboard("p"):
                if Cache.Temp.Keyboard.key_p_cache:
                    text += "P"
                    Cache.Temp.Keyboard.key_p_cache = False
            else:
                Cache.Temp.Keyboard.key_p_cache = True

            if keyboard("q"):
                if Cache.Temp.Keyboard.key_q_cache:
                    text += "Q"
                    Cache.Temp.Keyboard.key_q_cache = False
            else:
                Cache.Temp.Keyboard.key_q_cache = True

            if keyboard("r"):
                if Cache.Temp.Keyboard.key_r_cache:
                    text += "R"
                    Cache.Temp.Keyboard.key_r_cache = False
            else:
                Cache.Temp.Keyboard.key_r_cache = True

            if keyboard("s"):
                if Cache.Temp.Keyboard.key_s_cache:
                    text += "S"
                    Cache.Temp.Keyboard.key_s_cache = False
            else:
                Cache.Temp.Keyboard.key_s_cache = True

            if keyboard("t"):
                if Cache.Temp.Keyboard.key_t_cache:
                    text += "T"
                    Cache.Temp.Keyboard.key_t_cache = False
            else:
                Cache.Temp.Keyboard.key_t_cache = True

            if keyboard("u"):
                if Cache.Temp.Keyboard.key_u_cache:
                    text += "U"
                    Cache.Temp.Keyboard.key_u_cache = False
            else:
                Cache.Temp.Keyboard.key_u_cache = True

            if keyboard("v"):
                if Cache.Temp.Keyboard.key_v_cache:
                    text += "V"
                    Cache.Temp.Keyboard.key_v_cache = False
            else:
                Cache.Temp.Keyboard.key_v_cache = True

            if keyboard("w"):
                if Cache.Temp.Keyboard.key_w_cache:
                    text += "W"
                    Cache.Temp.Keyboard.key_w_cache = False
            else:
                Cache.Temp.Keyboard.key_w_cache = True

            if keyboard("x"):
                if Cache.Temp.Keyboard.key_x_cache:
                    text += "X"
                    Cache.Temp.Keyboard.key_x_cache = False
            else:
                Cache.Temp.Keyboard.key_x_cache = True

            if keyboard("y"):
                if Cache.Temp.Keyboard.key_y_cache:
                    text += "Y"
                    Cache.Temp.Keyboard.key_y_cache = False
            else:
                Cache.Temp.Keyboard.key_y_cache = True

            if keyboard("z"):
                if Cache.Temp.Keyboard.key_z_cache:
                    text += "Z"
                    Cache.Temp.Keyboard.key_z_cache = False
            else:
                Cache.Temp.Keyboard.key_z_cache = True

        if keyboard("a"):
            if Cache.Temp.Keyboard.key_a_cache:
                text += "a"
                Cache.Temp.Keyboard.key_a_cache = False
        else:
            Cache.Temp.Keyboard.key_a_cache = True

        if keyboard("b"):
            if Cache.Temp.Keyboard.key_b_cache:
                text += "b"
                Cache.Temp.Keyboard.key_b_cache = False
        else:
            Cache.Temp.Keyboard.key_b_cache = True

        if keyboard("c"):
            if Cache.Temp.Keyboard.key_c_cache:
                text += "c"
                Cache.Temp.Keyboard.key_c_cache = False
        else:
            Cache.Temp.Keyboard.key_c_cache = True

        if keyboard("d"):
            if Cache.Temp.Keyboard.key_d_cache:
                text += "d"
                Cache.Temp.Keyboard.key_d_cache = False
        else:
            Cache.Temp.Keyboard.key_d_cache = True

        if keyboard("e"):
            if Cache.Temp.Keyboard.key_e_cache:
                text += "e"
                Cache.Temp.Keyboard.key_e_cache = False
        else:
            Cache.Temp.Keyboard.key_e_cache = True

        if keyboard("f"):
            if Cache.Temp.Keyboard.key_f_cache:
                text += "f"
                Cache.Temp.Keyboard.key_f_cache = False
        else:
            Cache.Temp.Keyboard.key_f_cache = True

        if keyboard("g"):
            if Cache.Temp.Keyboard.key_g_cache:
                text += "g"
                Cache.Temp.Keyboard.key_g_cache = False
        else:
            Cache.Temp.Keyboard.key_g_cache = True

        if keyboard("h"):
            if Cache.Temp.Keyboard.key_h_cache:
                text += "h"
                Cache.Temp.Keyboard.key_h_cache = False
        else:
            Cache.Temp.Keyboard.key_h_cache = True

        if keyboard("i"):
            if Cache.Temp.Keyboard.key_i_cache:
                text += "i"
                Cache.Temp.Keyboard.key_i_cache = False
        else:
            Cache.Temp.Keyboard.key_i_cache = True

        if keyboard("j"):
            if Cache.Temp.Keyboard.key_j_cache:
                text += "j"
                Cache.Temp.Keyboard.key_j_cache = False
        else:
            Cache.Temp.Keyboard.key_j_cache = True

        if keyboard("k"):
            if Cache.Temp.Keyboard.key_k_cache:
                text += "k"
                Cache.Temp.Keyboard.key_k_cache = False
        else:
            Cache.Temp.Keyboard.key_k_cache = True

        if keyboard("l"):
            if Cache.Temp.Keyboard.key_l_cache:
                text += "l"
                Cache.Temp.Keyboard.key_l_cache = False
        else:
            Cache.Temp.Keyboard.key_l_cache = True

        if keyboard("m"):
            if Cache.Temp.Keyboard.key_m_cache:
                text += "m"
                Cache.Temp.Keyboard.key_m_cache = False
        else:
            Cache.Temp.Keyboard.key_m_cache = True

        if keyboard("n"):
            if Cache.Temp.Keyboard.key_n_cache:
                text += "n"
                Cache.Temp.Keyboard.key_n_cache = False
        else:
            Cache.Temp.Keyboard.key_n_cache = True

        if keyboard("o"):
            if Cache.Temp.Keyboard.key_o_cache:
                text += "o"
                Cache.Temp.Keyboard.key_o_cache = False
        else:
            Cache.Temp.Keyboard.key_o_cache = True

        if keyboard("p"):
            if Cache.Temp.Keyboard.key_p_cache:
                text += "p"
                Cache.Temp.Keyboard.key_p_cache = False
        else:
            Cache.Temp.Keyboard.key_p_cache = True

        if keyboard("q"):
            if Cache.Temp.Keyboard.key_q_cache:
                text += "q"
                Cache.Temp.Keyboard.key_q_cache = False
        else:
            Cache.Temp.Keyboard.key_q_cache = True

        if keyboard("r"):
            if Cache.Temp.Keyboard.key_r_cache:
                text += "r"
                Cache.Temp.Keyboard.key_r_cache = False
        else:
            Cache.Temp.Keyboard.key_r_cache = True

        if keyboard("s"):
            if Cache.Temp.Keyboard.key_s_cache:
                text += "s"
                Cache.Temp.Keyboard.key_s_cache = False
        else:
            Cache.Temp.Keyboard.key_s_cache = True

        if keyboard("t"):
            if Cache.Temp.Keyboard.key_t_cache:
                text += "t"
                Cache.Temp.Keyboard.key_t_cache = False
        else:
            Cache.Temp.Keyboard.key_t_cache = True

        if keyboard("u"):
            if Cache.Temp.Keyboard.key_u_cache:
                text += "u"
                Cache.Temp.Keyboard.key_u_cache = False
        else:
            Cache.Temp.Keyboard.key_u_cache = True

        if keyboard("v"):
            if Cache.Temp.Keyboard.key_v_cache:
                text += "v"
                Cache.Temp.Keyboard.key_v_cache = False
        else:
            Cache.Temp.Keyboard.key_v_cache = True

        if keyboard("w"):
            if Cache.Temp.Keyboard.key_w_cache:
                text += "w"
                Cache.Temp.Keyboard.key_w_cache = False
        else:
            Cache.Temp.Keyboard.key_w_cache = True

        if keyboard("x"):
            if Cache.Temp.Keyboard.key_x_cache:
                text += "x"
                Cache.Temp.Keyboard.key_x_cache = False
        else:
            Cache.Temp.Keyboard.key_x_cache = True

        if keyboard("y"):
            if Cache.Temp.Keyboard.key_y_cache:
                text += "y"
                Cache.Temp.Keyboard.key_y_cache = False
        else:
            Cache.Temp.Keyboard.key_y_cache = True

        if keyboard("z"):
            if Cache.Temp.Keyboard.key_z_cache:
                text += "z"
                Cache.Temp.Keyboard.key_z_cache = False
        else:
            Cache.Temp.Keyboard.key_z_cache = True



        if keyboard("space"):
            if Cache.Temp.Keyboard.key_specebar_cache:
                text += " "
                Cache.Temp.Keyboard.key_specebar_cache = False
        else:
            Cache.Temp.Keyboard.key_specebar_cache = True

    if set_text[1]:
        if keyboard("1"):
            if Cache.Temp.Keyboard.key_1_cache:
                text += "1"
                Cache.Temp.Keyboard.key_1_cache = False
        else:
            Cache.Temp.Keyboard.key_1_cache = True

        if keyboard("2"):
            if Cache.Temp.Keyboard.key_2_cache:
                text += "2"
                Cache.Temp.Keyboard.key_2_cache = False
        else:
            Cache.Temp.Keyboard.key_2_cache = True

        if keyboard("3"):
            if Cache.Temp.Keyboard.key_3_cache:
                text += "3"
                Cache.Temp.Keyboard.key_3_cache = False
        else:
            Cache.Temp.Keyboard.key_3_cache = True

        if keyboard("4"):
            if Cache.Temp.Keyboard.key_4_cache:
                text += "4"
                Cache.Temp.Keyboard.key_4_cache = False
        else:
            Cache.Temp.Keyboard.key_4_cache = True

        if keyboard("5"):
            if Cache.Temp.Keyboard.key_5_cache:
                text += "5"
                Cache.Temp.Keyboard.key_5_cache = False
        else:
            Cache.Temp.Keyboard.key_5_cache = True

        if keyboard("6"):
            if Cache.Temp.Keyboard.key_6_cache:
                text += "6"
                Cache.Temp.Keyboard.key_6_cache = False
        else:
            Cache.Temp.Keyboard.key_6_cache = True

        if keyboard("7"):
            if Cache.Temp.Keyboard.key_7_cache:
                text += "7"
                Cache.Temp.Keyboard.key_7_cache = False
        else:
            Cache.Temp.Keyboard.key_7_cache = True

        if keyboard("8"):
            if Cache.Temp.Keyboard.key_8_cache:
                text += "8"
                Cache.Temp.Keyboard.key_8_cache = False
        else:
            Cache.Temp.Keyboard.key_8_cache = True

        if keyboard("9"):
            if Cache.Temp.Keyboard.key_9_cache:
                text += "9"
                Cache.Temp.Keyboard.key_9_cache = False
        else:
            Cache.Temp.Keyboard.key_9_cache = True

        if keyboard("0"):
            if Cache.Temp.Keyboard.key_0_cache:
                text += "0"
                Cache.Temp.Keyboard.key_0_cache = False
        else:
            Cache.Temp.Keyboard.key_0_cache = True

        if keyboard("period"):
            if Cache.Temp.Keyboard.key_period_cache:
                text += "."
                Cache.Temp.Keyboard.key_period_cache = False
        else:
            Cache.Temp.Keyboard.key_period_cache = True

    if keyboard("back"):
        if Cache.Temp.Keyboard.key_backspace_cache:
            text = text[:-1]
            Cache.Temp.Keyboard.key_backspace_cache = False
    else:
        Cache.Temp.Keyboard.key_backspace_cache = True

    return str(text)

Program = Object_Program()

Material_Error = Material()
