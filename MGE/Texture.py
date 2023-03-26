
class Texture:
    def __init__(self, image=None, sprite=None):
        if image is not None:
            if image.type == "simple image":
                self.image = image
            elif image.type == "gif":
                self.image = image
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
