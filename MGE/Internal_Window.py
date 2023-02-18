from .MGE import Program
from .Window import Screen
from .Camera import Camera

pygame = Program.pygame

class Internal_Window:
    def __init__(self, localization: list, size: list):
        self.screen = Program.screen.screen

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
