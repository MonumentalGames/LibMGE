import pygame

class Line:
    def __init__(self, start, end, size):
        self.start = start
        self.end = end
        self.size = size

        self.material = None

    def draw_object(self, screen, camera=None):
        if camera is not None:
            loc_camera = camera.get_location()
        else:
            loc_camera = screen.camera.get_location()
        size_screen = screen.get_size()
        cache_screen_localization = [0, 0]
        cache_start = list(self.start).copy()
        cache_end = list(self.end).copy()
        cache_size = list(self.size).copy()

        if screen.__Window_Type__ == "Internal":
            cache_screen_localization = screen.get_localization()

        if "%" in str(cache_size):
            cache_size = size_screen[0] / 100 * int(str(cache_size).replace("%", ""))

        for number in range(2):
            if "%" in str(cache_start[number]):
                cache_start[number] = size_screen[number] / 100 * int(str(cache_start[number]).replace("%", ""))
            elif cache_start[number] == "center_obj":
                cache_start[number] = size_screen[number] / 2

        for number in range(2):
            if "%" in str(cache_end[number]):
                cache_end[number] = size_screen[number] / 100 * int(str(cache_end[number]).replace("%", ""))
            elif cache_end[number] == "center_obj":
                cache_end[number] = size_screen[number] / 2

        cache_start = [cache_start[0] + loc_camera[0] + cache_screen_localization[0], cache_start[1] + loc_camera[1] + cache_screen_localization[1]]
        cache_end = [cache_end[0] + loc_camera[0] + cache_screen_localization[0], cache_end[1] + loc_camera[1] + cache_screen_localization[1]]

        if self.material is not None:
            pygame.draw.line(screen.screen, self.material.color, cache_start, cache_end, cache_size)
        else:
            pygame.draw.line(screen.screen, (120, 120, 255), cache_start, cache_end, cache_size)

    def set_start_end(self, start, end):
        self.start = start
        self.end = end

    def set_size(self, size):
        self.size = size

    def set_material(self, material):
        self.material = material
