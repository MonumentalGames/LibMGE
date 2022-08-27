
class Texture:
    def __init__(self, image):
        #self.original_image = image
        self.image = image
        self.blurr = 0

    def set_image(self, image):
        #self.original_image = image
        self.image = image

    def set_blurr(self, blurr):
        self.blurr = blurr
