
class Texture:
    def __init__(self, image=None, sprite=None):
        if image is not None:
            if image.type == "simple image":
                self.image = image
            elif image.type == "gif":
                self.image = image
            #elif image.type == "movie":
            #    self.image = image
            self.sprite = None
        elif sprite is not None:
            self.sprite = sprite
            self.image = None
        self.blurr = 0

    def set_image(self, image=None, sprite=None):
        if image is not None:
            if image.type == "simple image":
                self.image = image
            #elif image.type == "movie":
            #    self.image = image
            self.sprite = None
        elif sprite is not None:
            self.sprite = sprite
            self.image = None

    def set_blurr(self, blurr):
        self.blurr = blurr

    #def get_playback_data(self):
    #    if self.image.type == "movie":
    #        return {"active": self.image.active,
    #                "time": self.image.video.get_pts(),
    #                "volume": self.image.video.get_volume(),
    #                "paused": self.image.video.get_pause(),
    #                "size": self.image.size}
