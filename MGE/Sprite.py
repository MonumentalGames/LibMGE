from PIL import Image as PIL_Image
import os

class Sprite:
    def __init__(self, directory_img=None, localization=(0, 0), size=(0, 0), number_sprites=(2, 2)):
        self.localization = localization
        self.size = size
        self.number_sprites = number_sprites
        if directory_img is not None:
            if os.path.exists(directory_img):
                self.path = directory_img
                if self.path[-4:] == ".png" or self.path[-4:] == ".jpg":
                    try:
                        self.image = PIL_Image.open(self.path)
                    except:
                        self.image = PIL_Image.new("RGB", (128, 128), color=(120, 120, 255))

                    self.type = "sprite"

    def get_img_sprite(self, index=1):
        start = [self.localization[0] + self.size[0] * index, self.localization[1] + self.size[1] * index]
        end = [self.localization[0] + self.size[0] * (index + 1), self.localization[1] + self.size[1]]
        z = (start[0], start[1], end[0], end[1])
        print(z)
        test = (50, 50, 100, 100)

        return self.image.crop(z)

    def get_size_localization(self):
        return [self.size, self.localization]
