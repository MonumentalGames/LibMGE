import os
#import pymediainfo
import pygame
import cv2
import threading
from PIL import Image as PIL_Image

#from .Platform import Platform

#if not Platform.system == "Android":
#    import ffpyplayer.player

def load_gif(path, data_gif):
    video = cv2.VideoCapture(path)

    success, video_image = video.read()
    data_gif["fps"] = video.get(cv2.CAP_PROP_FPS)

    movie_cache = data_gif["data"]
    movie_cache.clear()
    loop = success
    while loop:
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            movie_cache.append(video_surf)
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
                if self.path[-4:] == ".png" or self.path[-4:] == ".jpg":
                    try:
                        self.image = PIL_Image.open(self.path)
                    except FileNotFoundError:
                        self.image = PIL_Image.new(mode, size, color=color)
                    self.type = "simple image"
                    self.size = self.image.size
                elif self.path[-4:] == ".gif":
                    self.data_gif = {"fps": 24, "data": []}
                    thread = threading.Thread(target=load_gif, args=(directory_img, self.data_gif))
                    thread.daemon = True
                    thread.start()
                    self.type = "gif"
                # elif self.path[-4:] == ".mp4":
                #    if not Platform.system == "Android":
                #        self.video = ffpyplayer.player.MediaPlayer(self.path)

                #        self.type = "movie"
                #        info = self.get_file_data()

                #        self.duration = info["duration"]
                #        self.frames = 0
                #        self.frame_delay = 1 / info["frame rate"]
                #        self.size = info["original size"]
                #        self.image = pygame.Surface((16, 16))

                #        self.active = True
                else:
                    print("unsupported file")
            else:
                try:
                    self.image = PIL_Image.frombytes(mode, size, directory_img)
                except:
                    self.image = PIL_Image.new(mode, size, color=color)
                self.type = "simple image"
        else:
            self.image = PIL_Image.new(mode, size, color=color)
            self.size = self.image.size
            self.type = "simple image"

    #def get_file_data(self):
    #    if self.type == "movie":
    #        info = pymediainfo.MediaInfo.parse(self.path).video_tracks[0]
    #        return {"path": self.path,
    #                "name": os.path.splitext(os.path.basename(self.path))[0],
    #                "frame rate": float(info.frame_rate),
    #                "frame count": info.frame_count,
    #                "duration": info.duration / 1000,
    #                "original size": (info.width, info.height),
    #                "original aspect ratio": info.other_display_aspect_ratio[0]}
