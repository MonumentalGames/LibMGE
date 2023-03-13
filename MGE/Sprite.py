from PIL import Image as PIL_Image
import os

class Sprite:
    def __init__(self, directory_img=None, localization=(0, 0), size=(0, 0)):
        self.localization = localization
        self.size = size
        if directory_img is not None:
            if os.path.exists(directory_img):
                self.path = directory_img
                if self.path[-4:] == ".png" or self.path[-4:] == ".jpg":
                    try:
                        self.image = PIL_Image.open(self.path)
                    except:
                        self.image = PIL_Image.new("RGB", (128, 128), color=(120, 120, 255))

                    self.type = "sprite"

    def get_img_sprite(self, index):
        return self.image.crop((self.localization[0] * (index + 1), self.localization[1], self.localization[0] * (index + 1) + self.size, self.localization[1] + self.size))

    def get_size_localization(self):
        return [self.size, self.localization]
