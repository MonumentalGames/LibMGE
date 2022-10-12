import pygame
from PIL import ImageFilter

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

        self.object_render = False
        self.always_render = False

    def render(self):
        cache_img = self.texture.image.image
        if self.Sprite:
            cache_img = cache_img.crop(self.Sprite.get_size_localization())
        if self.texture.blurr >= 1:
            cache_img = cache_img.filter(ImageFilter.BoxBlur(self.texture.blurr))
        self.Surface = pygame.image.fromstring(cache_img.tobytes(), cache_img.size, cache_img.mode)

    def update_movie(self):
        updated = False
        frame = None
        val = None
        while self.texture.image.video.get_pts() > self.texture.image.frames * self.texture.image.frame_delay:
            frame, val = self.texture.image.video.get_frame()
            self.texture.image.frames += 1
            updated = True
        if updated:
            if val == "eof":
                pass
                self.texture.active = False
            elif not frame == None:
                self.Surface = pygame.image.frombuffer(frame[0].to_bytearray()[0], frame[0].get_size(), "RGB")
        return updated

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
