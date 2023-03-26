import os
import sys
import pygame
import cv2
import threading
from PIL import Image as PIL_Image

Supported_SimpleImage_Formats = [".jpg", ".png"]
Supported_Gif_Formats = [".gif"]

def load_gif(path, data_gif):
    gif = cv2.VideoCapture(path)

    success, video_image = gif.read()
    data_gif["fps"] = gif.get(cv2.CAP_PROP_FPS)

    gif_cache = data_gif["data"]
    gif_cache.clear()
    loop = success
    while loop:
        success, video_image = gif.read()
        if success:
            gif_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            gif_cache.append(gif_surf)
        else:
            loop = False

class Image:
    def __init__(self, directory_img=None, mode="RGB", size=(32, 32), color=(120, 120, 255)):
        self.path = directory_img

        self.data_gif = {"fps": 24, "data": []}
        self.image = PIL_Image.new("RGB", (16, 16), color)

        self.size = self.image.size
        self.type = None

        self.set_img(directory_img, mode, size, color)

    def set_img(self, directory_img=None, mode="RGB", size=(32, 32), color=(120, 120, 255)):
        if directory_img is not None:
            if os.path.exists(directory_img):
                self.path = directory_img
                # open Img
                if self.path[-4:] in Supported_SimpleImage_Formats:
                    try:
                        self.image = PIL_Image.open(self.path)
                    except FileNotFoundError:
                        self.image = PIL_Image.new(mode, size, color=color)
                    self.type = "simple image"
                    self.size = self.image.size
                # open gif
                elif self.path[-4:] in Supported_Gif_Formats:
                    self.data_gif = {"fps": 24, "data": []}
                    thread = threading.Thread(target=load_gif, args=(directory_img, self.data_gif))
                    thread.daemon = True
                    thread.start()
                    self.type = "gif"
                else:
                    sys.exit("unsupported file")
            else:
                try:
                    self.image = PIL_Image.frombytes(mode, size, directory_img)
                except:
                    sys.exit("unsupported file")
        else:
            self.image = PIL_Image.new(mode, size, color=color)
            self.size = self.image.size
            self.type = "simple image"
