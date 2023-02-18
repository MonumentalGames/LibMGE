
class Sprite:
    def __init__(self, texture="", localization=(0, 0), size=(0, 0)):
        self.texture = texture
        self.localization = localization
        self.size = size

    def get_size_localization(self):
        return [self.size, self.localization]
