import pygame
from .MGE import Program
from .Vector import motion
from .Mouse import mouse_button
from .Material import Material
from .Mesh import *

class Pivot2D:
    CENTER = 800
    TOP_LEFT_SIDE = 700
    TOP_RIGHT_SIDE = 750
    LOWER_LEFT_SIDE = 600
    LOWER_RIGHT_SIDE = 650

class Object2D:
    def __init__(self, localization=(0, 0), rotation: int = 0, size=(0, 0), scale=(1, 1), mesh=Mesh(plane)):
        self.localization = localization
        self.rotation = rotation
        self.scale = scale
        self.Mesh = mesh
        self.size = list(size)
        self.border_size = 0
        self.border_color = (100, 100, 255)
        self.border_radius = [0, 0, 0, 0]
        self.xy = None
        self.cursor = 11
        self.material = Material()
        self.variables = {}

        self.object_render = False
        self.always_render = False

        self.cache_object = pygame.Surface((0, 0))

    def draw_object(self, screen, camera=None, pivot=Pivot2D.TOP_LEFT_SIDE):
        if camera is not None:
            loc_camera = camera.get_location()
        else:
            loc_camera = screen.camera.get_location()
        size_screen = screen.get_size()
        cache_screen_localization = [0, 0]
        cache_size = list(self.size).copy()
        cache_localization = list(self.localization).copy()

        if screen.__Window_Type__ == "Internal":
            cache_screen_localization = screen.get_localization()

        for number in range(2):
            if "%" in str(cache_size[number]):
                cache_size[number] = size_screen[number] / 100 * int(str(cache_size[number]).replace("%", ""))

        for number in range(2):
            if "%" in str(cache_localization[number]):
                cache_localization[number] = size_screen[number] / 100 * int(str(cache_localization[number]).replace("%", ""))
            elif cache_localization[number] == "center_obj":
                cache_localization[number] = (size_screen[number] - cache_size[number]) / 2

        cache_localization = [cache_localization[0] + loc_camera[0] + cache_screen_localization[0], cache_localization[1] + loc_camera[1] + cache_screen_localization[1]]

        if screen.sdl2:
            pass
        else:
            if self.material.texture or 254 >= self.material.alpha >= 0 or self.rotation > 0 or not self.Mesh.Mesh == plane:
                if not self.material.object_render or self.material.always_render or not self.object_render or self.always_render:
                    if self.material.texture:
                        self.material.render()
                        img_cache = self.material.Surface
                        cache_object = pygame.transform.scale(img_cache, [cache_size[0], cache_size[1]])
                    else:
                        cache_object = pygame.Surface((cache_size[0], cache_size[1]))
                        cache_object.fill(self.material.color)

                    self.cache_object = pygame.Surface(cache_size, pygame.SRCALPHA)
                    if self.Mesh.Mesh == plane:
                        pygame.draw.rect(self.cache_object, (255, 255, 255, 255), (0, 0, *cache_size), border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                    else:
                        pygame.draw.polygon(self.cache_object, (255, 255, 255, 255), self.Mesh.get_mesh(cache_localization, self.scale))
                    self.cache_object.blit(cache_object, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

                    if 254 >= self.material.alpha >= 0:
                        self.cache_object.set_alpha(self.material.alpha)
                    if not self.rotation == 0:
                        self.cache_object = pygame.transform.rotate(self.cache_object, self.rotation)

                    self.material.object_render = True
                    self.object_render = True

                if pivot == 800:
                    cache_localization = [cache_localization[0] - int(self.cache_object.get_width() / 2), cache_localization[1] - int(self.cache_object.get_height() / 2)]
                elif pivot == 750:
                    cache_localization[1] -= self.cache_object.get_height()
                elif pivot == 600:
                    cache_localization[0] -= self.cache_object.get_width()
                elif pivot == 650:
                    cache_localization = [cache_localization[0] - self.cache_object.get_width(), cache_localization[1] - self.cache_object.get_height()]

                if not self.border_size == 0:
                    screen.screen.blit(self.cache_object, (cache_localization[0], cache_localization[1]))
                    pygame.draw.rect(screen.screen, self.border_color, (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), self.border_size, border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                else:
                    # pygame.draw.rect(cache_object, self.material.get_color(), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_radius=self.border_radius)
                    screen.screen.blit(self.cache_object, (cache_localization[0], cache_localization[1]))
            else:

                if pivot == 800:
                    cache_localization = [cache_localization[0] - int(cache_size[0] / 2), cache_localization[1] - int(cache_size[1] / 2)]
                elif pivot == 750:
                    cache_localization[1] -= cache_size[1]
                elif pivot == 600:
                    cache_localization[0] -= cache_size[0]
                elif pivot == 650:
                    cache_localization = [cache_localization[0] - cache_size[0], cache_localization[1] - cache_size[1]]

                if not self.border_size == 0:
                    pygame.draw.rect(screen.screen, self.material.get_color(), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                    pygame.draw.rect(screen.screen, self.border_color, (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), self.border_size, border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                else:
                    pygame.draw.rect(screen.screen, self.material.get_color(), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])

    def over(self, screen, camera=None):
        if camera is not None:
            loc_camera = camera.get_location()
        else:
            loc_camera = screen.camera.get_location()
        size_screen = screen.screen.get_size()
        cache_screen_localization = [0, 0]
        cache_size = list(self.size).copy()
        cache_localization = list(self.localization).copy()

        if screen.__Window_Type__ == "Internal":
            cache_screen_localization = screen.get_localization()

        for number in range(2):
            if "%" in str(cache_size[number]):
                cache_size[number] = size_screen[number] / 100 * int(str(cache_size[number]).replace("%", ""))

        for number in range(2):
            if "%" in str(cache_localization[number]):
                cache_localization[number] = size_screen[number] / 100 * int(str(cache_localization[number]).replace("%", ""))
            elif cache_localization[number] == "center_obj":
                cache_localization[number] = (size_screen[number] - cache_size[number]) / 2

        cache_localization = [cache_localization[0] + loc_camera[0] + cache_screen_localization[0], cache_localization[1] + loc_camera[1] + cache_screen_localization[1]]

        mouse_lok = pygame.mouse.get_pos()
        if cache_localization[0] < mouse_lok[0] < cache_localization[0] + cache_size[0] and cache_localization[1] < mouse_lok[1] < cache_localization[1] + cache_size[1]:
            return True

    def button(self, button, screen, camera=None, multiple_click: bool = False):
        if self.over(screen, camera):
            Program.cursor(self.cursor)
            if mouse_button(button, multiple_click):
                return True

    def set_localization(self, localization):
        self.localization = localization

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.object_render = False
        if self.material is not None:
            self.material.object_render = False

    def set_size(self, size):
        self.size = size
        self.object_render = False
        if self.material is not None:
            self.material.object_render = False

    def set_loc_siz(self, localization, size):
        self.size = size
        self.localization = localization
        self.object_render = False
        if self.material is not None:
            self.material.object_render = False

    def set_border(self, border_size: int = None, border_color=None, border_radius: int = None):
        cache = [border_size, border_color, border_radius]
        n = 0
        for t in cache:
            if t is not None:
                if n == 0:
                    self.border_size = border_size
                if n == 1:
                    self.border_color = border_color
                if n == 2:
                    self.border_radius = [border_radius, border_radius, border_radius, border_radius]
            n += 1

    def set_border_size(self, border_size):
        self.border_size = border_size

    def set_border_color(self, border_color=(100, 100, 255)):
        self.border_color = border_color

    def set_border_radius(self, radius: int = 0, higher_right: int = 0, higher_left: int = 0, bottom_right: int = 0, bottom_left: int = 0):
        if radius:
            self.border_radius = [radius, radius, radius, radius]
        else:
            self.border_radius = [higher_right, higher_left, bottom_right, bottom_left]

    def set_scale(self, scale, xy):
        self.scale = scale
        self.xy = xy
        self.object_render = False
        if self.material is not None:
            self.material.object_render = False

    def set_material(self, material: Material):
        self.material = material
        self.object_render = False
        self.material.object_render = False

    def set_background(self, p):
        pass

    def set_cursor(self, cursor):
        self.cursor = cursor

    def get_localization(self):
        size_screen = Program.screen.screen.get_size()
        cache_size = list(self.size).copy()
        cache_localization = list(self.localization).copy()

        for number in range(2):
            if "%" in str(cache_size[number]):
                cache_size[number] = size_screen[number] / 100 * int(str(cache_size[number]).replace("%", ""))

        for number in range(2):
            if "%" in str(cache_localization[number]):
                cache_localization[number] = size_screen[number] / 100 * int(str(cache_localization[number]).replace("%", ""))
            elif cache_localization[number] == "center_obj":
                cache_localization[number] = (size_screen[number] - cache_size[number]) / 2

        return cache_localization.copy()

    def get_size(self):
        size_screen = Program.screen.screen.get_size()
        cache_size = list(self.size).copy()

        for number in range(2):
            if "%" in str(cache_size[number]):
                cache_size[number] = size_screen[number] / 100 * int(str(cache_size[number]).replace("%", ""))

        return cache_size.copy()

    def motion(self, axis, axis_type, speed):
        Program.Temp.ForceRender = True
        if axis_type == 10:  # global
            if axis == 1:  # x
                self.localization[0] += speed
            if axis == 2:  # y
                self.localization[1] += speed
        if axis_type == 30:  # local
            self.localization = motion(self, axis, speed)
