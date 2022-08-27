import pygame

class Line:
    def __init__(self, start, end, size):
        self.start = start
        self.end = end
        self.size = size

        self.material = None

    def draw_object(self, screen):
        loc_camera = screen.camera.get_location()
        #size_screen = screen.screen.get_size()

        cache_start = [self.start[0] + loc_camera[0], self.start[1] + loc_camera[1]]
        cache_end = self.end

        cache_size = self.size

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
