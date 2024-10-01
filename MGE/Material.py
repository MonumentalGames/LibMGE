from numpy import frombuffer, uint8, mean
from ctypes import c_uint8
from .Texture import Texture
from .Color import Color
from .Constants import Colors
from ._sdl import sdl2

__all__ = ["Material", "DefaultMaterial", "ButtonDefaultMaterials"]

class Material:
    def __init__(self, texture: Texture | tuple = (), color: Color = Colors.StandardColor, alpha: int = 255):
        self._color = color

        self._alpha = alpha
        self._blurr = 0

        self._textures: list = []
        self._Cache_textures = []
        self.addTexture(texture)

        self._surface = sdl2.SDL_CreateRGBSurface(0, 16, 16, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000).contents
        sdl2.SDL_FillRect(self._surface, None, (self._color.b << 0) | (self._color.g << 8) | (self._color.r << 16) | (self.alpha << 24))
        self._surface_color = Color(self._color.RGBA)
        self._renderer = None

        self._render = True

    def __repr__(self):
        return f"<%s.%s color={self._color.RGBA} at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            id(self),
        )

    def render(self, size: tuple | list = None):
        if self._render:
            if self._renderer is not None:
                sdl2.SDL_DestroyRenderer(self._renderer)
                self._renderer = None
            sdl2.SDL_FreeSurface(self._surface)
            if len(self._textures) > 0:
                _size = max(self._textures, key=lambda _img: _img.image.size[0] * _img.image.size[1], default=None).image.size
                _size = _size if size is None else (_size if _size[0] * _size[1] > size[0] * size[1] else size)
                self._surface = sdl2.SDL_CreateRGBSurface(0, *_size, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000).contents
                self._renderer = sdl2.SDL_CreateSoftwareRenderer(self._surface)
                for tx in self._textures:
                    tx.render(self._renderer)
                self._render = False
                self.update()

                ## ----------------------------------------------- ##

                width, height = self._surface.w, self._surface.h
                depth = self._surface.format.contents.BytesPerPixel * 8

                pixel_buffer = (c_uint8 * (width * height * depth // 8)).from_address(self._surface.pixels)
                surface_array = frombuffer(pixel_buffer, dtype=uint8)

                pixels = surface_array.reshape((height, width, depth // 8))

                media_cor = mean(pixels, axis=(0, 1))

                self._surface_color.RGBA = [int(i) for i in list(media_cor.astype(int))]
                self._surface_color.a = 255

                del media_cor, pixels, surface_array, pixel_buffer, height, width, depth

                ## ----------------------------------------------- ##

            else:
                self._surface = sdl2.SDL_CreateRGBSurface(0, 16, 16, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000).contents
                sdl2.SDL_FillRect(self._surface, None, (self._color.b << 0) | (self._color.g << 8) | (self._color.r << 16) | (self.alpha << 24))
                self._render = False

                self._surface_color.RGBA = self._color.RGBA
                self._surface_color.a = self.alpha

            return self.surface

    def update(self):
        self.render()
        _textures = []
        for tx in self._textures:
            _textures.append(tx.tx(self._renderer))
        if self._Cache_textures != _textures:
            self._Cache_textures = _textures
            sdl2.SDL_RenderClear(self._renderer)
            for tx in _textures:
                sdl2.SDL_RenderCopy(self._renderer, tx, None, None)
            return True
        return False

    @property
    def surface(self):
        return self._surface

    @property
    def surfaceColor(self) -> Color:
        return self._surface_color

    @property
    def color(self) -> Color:
        return self._color

    @property
    def colorRGB(self):
        return self._color.RGB

    @property
    def colorRGBA(self):
        return self._color.RGBA

    @color.setter
    def color(self, color: Color):
        self._color = color

    @colorRGB.setter
    def colorRGB(self, color):
        self._color.RGB = color

    @colorRGBA.setter
    def colorRGBA(self, color):
        self._color.RGBA = color

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, alpha: int):
        self._alpha = alpha

    @property
    def blurr(self) -> int:
        return self._blurr

    @blurr.setter
    def blurr(self, blurr: int):
        self._blurr = blurr

    def addTexture(self, texture: Texture | tuple):
        if isinstance(texture, Texture):
            if texture not in self._textures:
                self._textures.append(texture)
        elif isinstance(texture, tuple):
            for tx in texture:
                if isinstance(tx, Texture):
                    if tx not in self._textures:
                        self._textures.append(tx)

    def removeTexture(self, texture: Texture | tuple | int):
        if isinstance(texture, Texture):
            if texture in self._textures:
                self._textures.remove(texture)
        elif isinstance(texture, int):
            self._textures.pop(texture)
        elif isinstance(texture, tuple):
            for tx in texture:
                if isinstance(tx, Texture):
                    if tx in self._textures:
                        self._textures.remove(tx)

    @property
    def textures(self) -> list[Texture]:
        return self._textures

    @textures.setter
    def textures(self, textures):
        self._textures = textures

DefaultMaterial = Material()

ButtonDefaultMaterials = [Material(color=Color(40, 40, 40)), Material(color=Color(35, 35, 35))]
