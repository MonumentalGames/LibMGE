from .Image import Image
from ._sdl import sdl2
from .Time import Time
from .Log import LogError

__all__ = ["Texture"]

def _get_sdl2_texture_size(texture):
    ret = sdl2.SDL_QueryTexture(texture)
    if ret is None:
        ret = [0, 0, 0, 0]
        LogError("getting texture attributes")
    return [ret[2], ret[3]]

class Texture:
    def __init__(self, image: Image = None):
        self._image = None
        if isinstance(image, Image):
            self._image = image
            self._time = Time(self._image.delays[0] / 1000)
            self._time_frame = 0
            self._frame = 0
        self._tx = {}
        self._alpha = 255
        self._blurr = 0
        self._RenderScaleQuality = 1
        self._render = False

    def render(self, renderer, force=False):
        if not self._render or force:
            if id(renderer) in self._tx:
                for tx in self._tx[id(renderer)]:
                    sdl2.SDL_DestroyTexture(tx)
            self._tx[id(renderer)] = []
            self._tx[id(renderer)].clear()
            if self._image.count == 1:
                self._tx[id(renderer)] = [sdl2.SDL_CreateTextureFromSurface(renderer, self._image.images[0]).contents]
            else:
                for num in range(self._image.count):
                    self._tx[id(renderer)].append(sdl2.SDL_CreateTextureFromSurface(renderer, self._image.images[num]).contents)
            self._UpdateScaleMode()
            self._render = True
        return self.tx

    def tx(self, renderer):
        if id(renderer) not in self._tx or not self._render:
            self.render(renderer, True)
        if len(self._tx[id(renderer)]) == 1:
            return self._tx[id(renderer)][0]
        self._time_frame += self._time.tickMotion()
        if self._time_frame > 1:
            _time_int = int(self._time_frame)
            self._time_frame -= _time_int

            self._frame += _time_int
            if self._frame >= self._image.count:
                self._frame = self._frame % self._image.count

            self._time.delta_time = self._image.delays[self._frame] / 1000
        return self._tx[id(renderer)][self._image.count - 1 if self._frame >= self._image.count else self._frame]

    def _UpdateScaleMode(self):
        for textures in self._tx.values():
            for texture in textures:
                sdl2.SDL_SetTextureScaleMode(texture, self._RenderScaleQuality)

    @property
    def count(self):
        return self._image.count

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image: Image = None):
        if isinstance(image, Image):
            self._image = image
            self._render = False

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha: int):
        self._alpha = alpha

    @property
    def blurr(self):
        return self._blurr

    @blurr.setter
    def blurr(self, blurr: int):
        self._blurr = blurr

    @property
    def RenderScaleQuality(self):
        return self._RenderScaleQuality

    @RenderScaleQuality.setter
    def RenderScaleQuality(self, quality):
        if self._RenderScaleQuality != quality:
            self._RenderScaleQuality = quality if 0 <= quality <= 1 else 1
            self._UpdateScaleMode()

