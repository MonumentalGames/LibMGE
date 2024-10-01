from ._sdl.sdl2 import SDL_Color
from .Log import LogError

__all__ = ["Color"]

class Color:
    def __init__(self, *color):
        self._r = self._g = self._b = self._a = 255
        self._SetColor(*color)

    def __repr__(self):
        return f"<%s.%s color=(%d, %d, %d, %d) at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._r, self._g, self._b, self._a,
            id(self)
        )

    def _SetColor(self, *color):
        color = color[0] if len(color) == 1 else color
        if isinstance(color, (tuple, list)):
            if all(isinstance(c, int) for c in color):
                self.RGBA = color
            elif all(isinstance(c, float) for c in color):
                self.RGBA01 = color
            else:
                LogError(f"The value '{color}' is not recognized as a color")
        elif isinstance(color, int):
            self.Uint32 = color
        elif isinstance(color, str):
            self.Hex = color
        elif isinstance(color, SDL_Color):
            self.SDLColor = color
        else:
            LogError(f"The value '{color}' is not recognized as a color")

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = 0 if r < 0 else 255 if r > 255 else r

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, r):
        self._g = 0 if r < 0 else 255 if r > 255 else r

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, r):
        self._b = 0 if r < 0 else 255 if r > 255 else r

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, a):
        self._a = 0 if a < 0 else 255 if a > 255 else a

    @property
    def RGB(self):
        return self._r, self._g, self._b

    @RGB.setter
    def RGB(self, color):
        if isinstance(color, (tuple, list)) and all(isinstance(c, int) for c in color):
            self.r, self.g, self.b = color[0], color[1], color[2]
        else:
            LogError(f"The value '{color}' is not recognized as a RGB color")

    @property
    def RGBA(self):
        return self._r, self._g, self._b, self._a

    @RGBA.setter
    def RGBA(self, color):
        if isinstance(color, (tuple, list)) and all(isinstance(c, int) for c in color):
            self.RGB = color[0], color[1], color[2]
            self.a = self._a if len(color) < 4 else color[3]
        else:
            LogError(f"The value '{color}' is not recognized as a RGBA color")

    @property
    def RGB01(self):
        return round(self._r / 255, 4), round(self._g / 255, 4), round(self._b / 255, 4)

    @RGB01.setter
    def RGB01(self, color):
        if isinstance(color, (tuple, list)) and all(isinstance(c, float) for c in color):
            self.RGB = round(color[0] * 255), round(color[1] * 255), round(color[2] * 255)
        else:
            LogError(f"The value '{color}' is not recognized as a RGB01 color")

    @property
    def RGBA01(self):
        return round(self._r / 255, 4), round(self._g / 255, 4), round(self._b / 255, 4), round(self._a / 255, 4)

    @RGBA01.setter
    def RGBA01(self, color):
        if isinstance(color, (tuple, list)) and all(isinstance(c, float) for c in color):
            self.RGBA = round(color[0] * 255), round(color[1] * 255), round(color[2] * 255), round(color[3] * 255)
        else:
            LogError(f"The value '{color}' is not recognized as a RGBA01 color")

    @property
    def Uint32(self):
        return (self._r << 0) | (self._g << 8) | (self._b << 16) | (self._a << 24)

    @Uint32.setter
    def Uint32(self, color):
        if isinstance(color, int):
            self.RGBA = (color >> 0) & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF, (color >> 24) & 0xFF
        else:
            LogError(f"The value '{color}' is not recognized as a color")

    @property
    def Hex(self):
        _color = f"{self._r:02X}{self._g:02X}{self._b:02X}{self._a:02X}"
        if all(_color[i] == _color[i + 1] for i in range(0, 8, 2)):
            _color = _color[::2]
        if len(_color) == 4 and _color[3] == 'F':
            _color = _color[:3]
        elif len(_color) == 8 and _color[6:] == 'FF':
            _color = _color[:6]
        return f"#{_color}"

    @Hex.setter
    def Hex(self, color):
        if isinstance(color, str):
            _color = color.lstrip("#")
            _color = "".join([char * 2 for char in _color]) if len(_color) == 3 or len(_color) == 4 else _color
            _color = _color + "FF" if len(_color) == 6 else _color
            try:
                self.RGBA = int(_color[0:2], 16), int(_color[2:4], 16), int(_color[4:6], 16), int(_color[6:8], 16)
            except ValueError:
                LogError(f"The value '{color}' is not recognized as a hexadecimal color")
        else:
            LogError(f"The value '{color}' is not recognized as a hexadecimal color")

    @property
    def Color(self):
        return self.RGBA

    @Color.setter
    def Color(self, *color):
        self._SetColor(*color)

    @property
    def SDLColor(self) -> SDL_Color:
        return SDL_Color(*self.RGBA)

    @SDLColor.setter
    def SDLColor(self, color: SDL_Color):
        if isinstance(color, SDL_Color):
            self.RGBA = color.r, color.g, color.b, color.a
        else:
            LogError(f"The value '{color}' is not recognized as a color SDL_Color")
