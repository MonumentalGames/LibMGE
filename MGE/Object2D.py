import pygame
from .MGE import Program
from .Mouse import mouse_button
from .Mesh import *

class Object2D:
    def __init__(self, localization=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), mesh=Mesh(plane)):
        self.localization = localization
        self.rotation = rotation
        self.scale = scale
        self.Mesh = mesh
        self.size = size
        self.border_size = 0
        self.border_color = (100, 100, 255)
        self.border_radius = [0, 0, 0, 0]
        self.xy = None
        self.cursor = 11
        self.material = None
        self.variables = {}

        self.object_render = False
        self.always_render = False

        self.cache_object = pygame.Surface((0, 0))

    def draw_object(self, screen, camera=None):
        if screen.get_screen_type() == "Internal":
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

            #if self.scale:
            #    if self.xy == "x":
            #        res = cache_screen_size[0] / self.scale[0]
            #    elif self.xy == "y":
            #        res = cache_screen_size[1] / self.scale[1]
            #    else:
            #        res = 50
            #    cache_screen_size = (int(res * self.scale[0]), int(res * self.scale[1]))

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
                cache_localization = [cache_localization[0] + cache_screen_localization[0], cache_localization[1] + cache_screen_localization[1]]
            except TypeError:
                print("Error")
                cache_localization = screen.localization

            #cache_localization = cache_localization + screen.localization
        elif screen.get_screen_type() == "main":
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

        if self.material is not None:
            if self.material.texture or 254 >= self.material.alpha >= 0 or self.rotation > 0 or not self.Mesh.Mesh == plane:
                if not self.material.object_render or not self.object_render or self.always_render:
                    if self.material.texture:
                        self.material.render()
                        img_cache = self.material.Surface
                        cache_object = pygame.transform.scale(img_cache, [cache_size[0], cache_size[1]])
                    else:
                        cache_object = pygame.Surface((cache_size[0], cache_size[1]))
                        cache_object.fill(self.material.color)


                    self.cache_object = pygame.Surface(self.size, pygame.SRCALPHA)
                    if self.Mesh.Mesh == plane:
                        pygame.draw.rect(self.cache_object, (255, 255, 255, 255), (0, 0, *self.size), border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                    else:
                        pygame.draw.polygon(self.cache_object, (255, 255, 255, 255), self.Mesh.get_mesh(cache_localization, self.scale))
                    self.cache_object.blit(cache_object, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

                    if 254 >= self.material.alpha >= 0:
                        self.cache_object.set_alpha(self.material.alpha)
                    if not self.rotation == 0:
                        self.cache_object = pygame.transform.rotate(self.cache_object, self.rotation)

                    self.material.object_render = True
                    self.object_render = True

                if not self.border_size == 0:
                    screen.screen.blit(self.cache_object, (cache_localization[0], cache_localization[1]))
                    pygame.draw.rect(screen.screen, self.border_color, (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), self.border_size, border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                else:
                    #pygame.draw.rect(cache_object, self.material.get_color(), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_radius=self.border_radius)
                    screen.screen.blit(self.cache_object, (cache_localization[0], cache_localization[1]))
            else:
                try:
                    if not self.border_size == 0:
                        pygame.draw.rect(screen.screen, self.material.get_color(), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                        pygame.draw.rect(screen.screen, self.border_color, (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), self.border_size, border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                    else:
                        pygame.draw.rect(screen.screen, self.material.get_color(), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                except TypeError:
                    print("Error")
        else:
            if not self.border_size == 0:
                pygame.draw.rect(screen.screen, (120, 120, 255), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
                pygame.draw.rect(screen.screen, self.border_color, (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), self.border_size, border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])
            else:
                pygame.draw.rect(screen.screen, (120, 120, 255), (cache_localization[0], cache_localization[1], cache_size[0], cache_size[1]), border_top_right_radius=self.border_radius[0], border_top_left_radius=self.border_radius[1], border_bottom_right_radius=self.border_radius[2], border_bottom_left_radius=self.border_radius[3])

    def over(self, screen):
        if screen.get_screen_type() == "main":
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
        elif screen.get_screen_type() == "Internal":
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

            #if self.scale:
            #    if self.xy == "x":
            #        res = cache_screen_size[0] / self.scale[0]
            #    elif self.xy == "y":
            #        res = cache_screen_size[1] / self.scale[1]
            #    else:
            #        res = 50
            #    cache_screen_size = (int(res * self.scale[0]), int(res * self.scale[1]))

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

            ##-----------------------------------------------------##

            # print(f"internal{screen.localization}-{screen.size}")

            try:
                cache_localization = [cache_localization[0] + loc_camera[0], cache_localization[1] + loc_camera[1]]
                cache_localization = [cache_localization[0] + cache_screen_localization[0], cache_localization[1] + cache_screen_localization[1]]
            except TypeError:
                print("Error")
                cache_localization = screen.localization

            # cache_localization = cache_localization + screen.localization
        else:
            loc_camera = screen.camera.get_location()
            cache_size = self.size
            try:
                cache_localization = [self.localization[0] + loc_camera[0], self.localization[1] + loc_camera[1]]
            except TypeError:
                print("Error")
                cache_localization = [0, 0]

        #######

        mouse_lok = pygame.mouse.get_pos()
        # loc_camera = camera.get_location()
        if cache_localization[0] < mouse_lok[0] < cache_localization[0] + cache_size[0] and cache_localization[1] < mouse_lok[1] < cache_localization[1] + cache_size[1]:
            return True

    def button(self, button, screen):
        if self.over(screen):
            Program.cursor(self.cursor)
            if mouse_button(button):
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

    def set_border(self, border_size=None, border_color=None, border_radius=None):
        if border_size is None:
            pass
        else:
            self.border_size = border_size
        if border_size is None:
            pass
        else:
            self.border_color = border_color
        if border_size is None:
            pass
        else:
            self.border_radius = [border_radius, border_radius, border_radius, border_radius]

    def set_border_size(self, border_size):
        self.border_size = border_size

    def set_border_color(self, border_color=(100, 100, 255)):
        self.border_color = border_color

    def set_border_radius(self, radius=0, higher_right=0, higher_left=0, bottom_right=0, bottom_left=0):
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

    def set_material(self, material):
        self.material = material
        self.object_render = False
        self.material.object_render = False

    def set_background(self, p):
        pass

    def set_cursor(self, cursor):
        self.cursor = cursor

    def get_localization(self):
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

        if cache_localization[0] == "center_obj":
            cache_localization[0] = (size_screen[0] - cache_size[0]) / 2
        if cache_localization[1] == "center_obj":
            cache_localization[1] = (size_screen[1] - cache_size[1]) / 2

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
        #   cache_size = (int(res * self.scale[0]), int(res * self.scale[1]))

        return cache_size

    def motion(self, axis, axis_type, speed):
        # vec = pygame.math.Vector2

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
