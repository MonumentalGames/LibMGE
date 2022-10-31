from .MGE import Program
from .Camera import Camera

pygame = Program.pygame

class Internal_Window:
    def __init__(self, localization, size):
        self.screen = Program.screen.screen
        #self.screen = pygame.Surface(size, pygame.SRCALPHA)
        #pygame.draw.rect(self.screen, (30, 30, 30, 255), (0, 0, *size))

        self.localization = localization
        self.size = size

        self.cache_screen = pygame.Surface(size, pygame.SRCALPHA)

        self.camera = Camera()

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
