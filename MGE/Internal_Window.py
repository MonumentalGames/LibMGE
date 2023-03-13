from .MGE import Program
from .Camera import Camera

pygame = Program.pygame

class Internal_Window:
    def __init__(self, localization: list, size: list):
        self.__Window_Type__ = "Internal"

        self.screen = Program.screen.screen

        self.localization = localization
        self.size = size

        self.cache_screen = pygame.Surface(size, pygame.SRCALPHA)

        self.camera = Camera()

        self.sdl2 = False
        self.opengl = False

        self.render = False
        self.always_render = False

    def set_loc_size(self, localization: list, size: list):
        self.localization = localization
        self.size = size

    def get_localization(self):
        size_screen = Program.screen.screen.get_size()
        cache_size = self.get_size()
        cache_localization = self.localization.copy()

        for number in range(2):
            if "%" in str(cache_localization[number]):
                cache_localization[number] = size_screen[number] / 100 * int(str(cache_localization[number]).replace("%", ""))
            elif cache_localization[number] == "center_obj":
                cache_localization[number] = (size_screen[number] - cache_size[number]) / 2

        return list(cache_localization)

    def get_size(self):
        size_screen = Program.screen.screen.get_size()
        cache_size = self.size.copy()

        for number in range(2):
            if "%" in str(cache_size[number]):
                cache_size[number] = size_screen[number] / 100 * int(str(cache_size[number]).replace("%", ""))

        return list(cache_size)
