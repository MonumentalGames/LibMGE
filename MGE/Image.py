import os
from PIL import Image as PIL_Image

class Image:
    def __init__(self, directory_img=None, mode="RGB", size=(32, 32), color=(120, 120, 255)):
        if directory_img is not None:
            if os.path.exists(directory_img):
                try:
                    self.image = PIL_Image.open(directory_img)
                except FileNotFoundError:
                    self.image = PIL_Image.new(mode, size, color=color)

                self.size = self.image.size
            else:
                try:
                    self.image = PIL_Image.frombytes(mode, size, directory_img)
                except:
                    self.image = PIL_Image.new(mode, size, color=color)
            #except TypeError:
            #    print("error")
            #    self.image = directory_img
            #    self.original_size = self.image.get_size()
            #    self.size = self.original_size
        else:
            self.image = PIL_Image.new(mode, size, color=color)
            self.size = self.image.size

    def set_img(self, directory_img=None, mode="RGB", size=(32, 32), color=(120, 120, 255)):
        if directory_img is not None:
            if os.path.exists(directory_img):
                try:
                    self.image = PIL_Image.open(directory_img)
                except FileNotFoundError:
                    self.image = PIL_Image.new(mode, size, color=color)
                self.size = self.image.size
        else:
            self.image = PIL_Image.new(mode, size, color=color)
            self.size = self.image.size
