import os
import sys
import ctypes
import numpy

from ._sdl import sdl2, sdlimage
from .Constants import ImageFormat
from .Color import Color

__all__ = ["Image", "ImageGif", "Icon",
           "LoadImage", "LoadGif", "LoadIcon",
           "SaveImagePNG", "SaveImageJPG",
           "NewImage",
           "DefaultIcon",
           "image_to_icon", "icon_to_image", "image_to_numpyArray", "compare_image"]

class Image:
    def __init__(self):
        self.image = None
        self._size = (0, 0)
        self._format = None

    def __repr__(self):
        return f"<%s.%s size=%dx%d at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._size[0],
            self._size[1],
            id(self),
        )

    def fill(self, color: Color):
        sdl2.SDL_FillRect(self.image, None, sdl2.SDL_MapRGBA(self.image.format, *color.RGBA))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: list):
        new_surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, size[0], size[1], self._format[0], self._format[1])
        sdl2.SDL_BlitScaled(self.image, None, new_surface, None)
        sdl2.SDL_FreeSurface(self.image)
        self.image = new_surface.contents
        self._size = (self.image.w, self.image.h)

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, _format):
        new_surface = sdl2.SDL_ConvertSurfaceFormat(self.image, _format[1], 0)
        sdl2.SDL_FreeSurface(self.image)
        self.image = new_surface.contents

    @property
    def color(self):
        pixel_buffer = (ctypes.c_uint8 * (self._size[0] * self._size[1] * self._format[0] // 8)).from_address(self.image.pixels)
        surface_array = numpy.frombuffer(pixel_buffer, dtype=numpy.uint8)

        pixels = surface_array.reshape((self._size[1], self._size[0], self._format[0] // 8))

        # Calculando a média de cada canal de cor (R, G, B, A)
        media_cor = numpy.mean(pixels, axis=(0, 1))

        _color = Color(list(media_cor.astype(int)))
        _color.a = 255

        return _color

    def crop(self, location, size):
        new_surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, size[0], size[1], self._format[0], self._format[1])
        sdl2.SDL_BlitSurface(self.image, sdl2.SDL_Rect(*location, *size), new_surface, None)
        sdl2.SDL_FreeSurface(self.image)
        self.image = new_surface.contents
        self._size = (self.image.w, self.image.h)

    def copy(self):
        _image = Image()
        _image.image = sdl2.SDL_DuplicateSurface(self.image).contents
        _image._size = self.size
        _image._format = self.format
        return _image

    def close(self):
        if self.image is not None:
            sdl2.SDL_FreeSurface(self.image)

class ImageGif:
    def __init__(self):
        self.frames = []
        self.delays = []
        self.count = 0
        self._size = (0, 0)

    def __repr__(self):
        return f"<%s.%s at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            id(self),
        )

    @property
    def size(self):
        return self._size

    def close(self):
        for surface in self.frames:
            sdl2.SDL_FreeSurface(surface)
        del self

#class Movie:
#    pass

class Icon:
    def __init__(self):
        self.icon = None
        self._size = (0, 0)

    def __repr__(self):
        return f"<%s.%s at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            id(self),
        )

    @property
    def size(self):
        return self._size

    def close(self):
        if self.icon is not None:
            sdl2.SDL_FreeSurface(self.icon)

def LoadImage(path: str) -> Image:
    _Image = Image()
    if os.path.exists(path):
        _Image.image = sdlimage.IMG_Load(path.encode()).contents
        if not _Image.image:
            sys.exit("unsupported file")
        _Image._size = (_Image.image.w, _Image.image.h)
        _Image._format = ImageFormat.ARGB
    else:
        sys.exit(f"""unsupported file ("{path}")""")
    return _Image

def LoadGif(path: str) -> ImageGif:
    _ImageGif = ImageGif()
    if os.path.exists(path):
        if path[-4:] == ".gif":
            _Gif = sdlimage.IMG_LoadAnimation(path.encode()).contents
        else:
            sys.exit("unsupported file")
        _ImageGif.count = _Gif.count
        _ImageGif._size = (_Gif.w, _Gif.h)
        for frame in range(_Gif.count):
            _ImageGif.frames.append(_Gif.frames[frame].contents)
            _ImageGif.delays.append(float(_Gif.delays[frame]))
    else:
        sys.exit(f"""unsupported file ("{path}")""")
    return _ImageGif

#def LoadMovie(path: str) -> Movie:
#    pass

def LoadIcon(path: str) -> Icon:
    icon = Icon()
    if os.path.exists(path):
        if path[-4:] == ".ico":
            icon.icon = sdlimage.IMG_LoadICO_RW(sdl2.SDL_RWFromFile(path.encode(), b"r+")).contents
            icon._size = (icon.icon.w, icon.icon.h)
        else:
            sys.exit(f"""unsupported file ("{path}")""")
    else:
        sys.exit(f"""unsupported file ("{path}")""")
    return icon

def NewImage(mode=ImageFormat.ARGB, size: list | tuple = (32, 32), color: Color = None) -> Image:
    _image = Image()
    _image.image = sdl2.SDL_CreateRGBSurfaceWithFormat(0, size[0], size[1], mode[0], mode[1]).contents
    _image._size = (_image.image.w, _image.image.h)
    _image._format = mode
    if color is not None:
        _image.fill(color)
    return _image

def SaveImagePNG(image: Image, path="image.png"):
    sdlimage.IMG_SavePNG(image.image, path.encode())

def SaveImageJPG(image: Image, path="image.jpg", quality=80):
    sdlimage.IMG_SaveJPG(image.image, path.encode(), quality)

def image_to_icon(image: Image) -> Icon:
    icon = Icon()
    icon.icon = sdl2.SDL_ConvertSurfaceFormat(image.image, ImageFormat.ARGB[1], 0).contents
    icon._size = image.size
    return icon

def icon_to_image(icon: Icon) -> Image:
    _image = Image()
    _image.image = sdl2.SDL_DuplicateSurface(icon.icon).contents
    _image._size = icon.size
    _image._format = ImageFormat.ARGB
    return _image

def _sdl2_surface_to_numpy_array(surface: sdl2.SDL_Surface) -> numpy.ndarray:
    width, height = surface.w, surface.h
    depth = surface.format.contents.BytesPerPixel * 8

    pixel_buffer = (ctypes.c_uint8 * (width * height * depth // 8)).from_address(surface.pixels)
    surface_array = numpy.frombuffer(pixel_buffer, dtype=numpy.uint8)
    surface_array = surface_array.reshape((height, width, depth // 8))

    return surface_array.copy()

def image_to_numpyArray(image: Image) -> numpy.ndarray:
    return _sdl2_surface_to_numpy_array(image.image)

def compare_image(image1: Image, image2: Image) -> bool:
    if image1.size != image2.size:
        return False
    pixels1 = image_to_numpyArray(image1)
    pixels2 = image_to_numpyArray(image2)
    pixels = pixels1 == pixels2
    return bool(pixels.all())

_path = f"{os.path.abspath(os.path.dirname(__file__))}/logo.ico"
if os.path.exists(_path):
    DefaultIcon = LoadIcon(_path)
elif os.path.exists("./logo.ico"):
    DefaultIcon = LoadIcon("./logo.ico")
else:
    _icon = NewImage(ImageFormat.ARGB, (1, 1), Color((0, 0, 0)))
    DefaultIcon = image_to_icon(_icon)
    del _icon
