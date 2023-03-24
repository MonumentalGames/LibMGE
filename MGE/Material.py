import pygame
from PIL import ImageFilter

from .MGE import Program

class Material:
    def __init__(self, texture=False, color=(120, 120, 255), alpha=255):
        self.color = color
        self.alpha = alpha
        if texture:
            self.texture = texture
        else:
            self.texture = None
        self.Surface = pygame.Surface((16, 16))

        self.n_surf = 0
        self.surf_temp = 0

        self.object_render = False
        self.always_render = False

    def render(self):
        if self.texture.image is not None:
            if self.texture.image.type == "movie":
                pass
            elif self.texture.image.type == "simple image":
                cache_img = self.texture.image.image
                if self.texture.blurr >= 1:
                    cache_img = cache_img.filter(ImageFilter.BoxBlur(self.texture.blurr))
                self.Surface = pygame.image.fromstring(cache_img.tobytes(), cache_img.size, cache_img.mode)
            elif self.texture.image.type == "gif":
                if self.surf_temp >= Program.get_fps() / self.texture.image.data_gif["fps"]:
                    if self.n_surf <= len(self.texture.image.data_gif["data"]) - 1:
                        self.Surface = self.texture.image.data_gif["data"][self.n_surf]
                        self.n_surf += 1
                    else:
                        self.Surface = self.texture.image.data_gif["data"][0]
                        self.n_surf = 1
                    self.surf_temp = 0
                self.surf_temp += 1
                self.always_render = True
        elif self.texture.sprite is not None:
            cache_img = self.texture.sprite.get_img_sprite()
            self.Surface = pygame.image.fromstring(cache_img.tobytes(), cache_img.size, cache_img.mode)

    #def update_movie(self):
    #    updated = False
    #    frame = None
    #    val = None
    #    while self.texture.image.video.get_pts() > self.texture.image.frames * self.texture.image.frame_delay:
    #        frame, val = self.texture.image.video.get_frame()
    #        self.texture.image.frames += 1
    #        updated = True
    #    if updated:
    #        if val == "eof":
    #            pass
    #            self.texture.active = False
    #        elif not frame == None:
    #            self.Surface = pygame.image.frombuffer(frame[0].to_bytearray()[0], frame[0].get_size(), "RGB")
    #    return updated

    def add_texture(self, texture):
        self.texture = texture

    def set_color(self, color):
        self.color = color

    def set_alpha(self, alpha):
        print(alpha)
        self.alpha = alpha

    def get_color(self):
        return self.color

    def get_alpha(self):
        return self.alpha

    def get_textures(self):
        return self.texture
