import os
import pymediainfo
import pygame
from PIL import Image as PIL_Image

from .Platform import Platform

if not Platform.system == "Android":
    import ffpyplayer.player

class Image:
    def __init__(self, directory_img=None, mode="RGB", size=(32, 32), color=(120, 120, 255)):
        if directory_img is not None:
            if os.path.exists(directory_img):
                self.path = directory_img
                if self.path[-4:] == ".png" or self.path[-4:] == ".jpg":
                    try:
                        self.image = PIL_Image.open(self.path)
                    except FileNotFoundError:
                        self.image = PIL_Image.new(mode, size, color=color)

                    self.type = "simple image"
                    self.size = self.image.size
                elif self.path[-4:] == ".gif":
                    self.type = "gif"
                elif self.path[-4:] == ".mp4":
                    if not Platform.system == "Android":
                        self.video = ffpyplayer.player.MediaPlayer(self.path)

                        info = self.get_file_data()

                        self.duration = info["duration"]
                        self.frames = 0
                        self.frame_delay = 1 / info["frame rate"]
                        self.size = info["original size"]
                        self.image = pygame.Surface((0, 0))

                        self.active = True
                        self.type = "movie"
                else:
                    try:
                        self.image = self.image = PIL_Image.open(self.path)
                    except:
                        self.image = PIL_Image.new("RGB", size, color=color)
                    self.format = "jpg"
            else:
                try:
                    self.image = PIL_Image.frombytes(mode, size, directory_img)
                except:
                    self.image = PIL_Image.new(mode, size, color=color)
                self.format = "jpg"
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

    def get_file_data(self):
        if self.type == "movie":
            info = pymediainfo.MediaInfo.parse(self.path).video_tracks[0]
            return {"path": self.path,
                    "name": os.path.splitext(os.path.basename(self.path))[0],
                    "frame rate": float(info.frame_rate),
                    "frame count": info.frame_count,
                    "duration": info.duration / 1000,
                    "original size": (info.width, info.height),
                    "original aspect ratio": info.other_display_aspect_ratio[0]}
