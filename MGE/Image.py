import os
from ctypes import c_uint8, c_uint32
from numpy import frombuffer, uint8, mean, ndarray
from urllib.request import urlopen
from threading import Thread

from ._sdl import sdl2, sdlimage
from .Log import LogError
from .Constants import ImageFormat
from .Color import Color

__all__ = ["Image", "Icon", "CreateAnimatedImage",
           "LoadImage", "LoadImageUrl", "LoadIcon",
           "SaveImagePNG", "SaveImageJPG",
           "NewImage",
           "DefaultIcon",
           "image_to_icon", "icon_to_image", "image_to_numpyArray", "compare_image"]

class Image:
    def __init__(self):
        self.images = []
        self.delays = []
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
        sdl2.SDL_FillRect(self.images[0], None, sdl2.SDL_MapRGBA(self.images[0].format, *color.RGBA))

    @property
    def count(self):
        return len(self.images)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: list):
        _images = []
        for _image in self.images:
            new_surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, size[0], size[1], self._format[0], self._format[1])
            sdl2.SDL_BlitScaled(_image, None, new_surface, None)
            sdl2.SDL_FreeSurface(_image)
            _images.append(new_surface.contents)
        del self.images, self._size
        self.images = _images
        self._size = list(size)

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, _format):
        _images = []
        for _image in self.images:
            new_surface = sdl2.SDL_ConvertSurfaceFormat(_image, _format[1], 0)
            sdl2.SDL_FreeSurface(_image)
            _images.append(new_surface.contents)
        del self.images
        self.images = _images
        self._format = _format

    @property
    def color(self):
        pixel_buffer = (c_uint8 * (self._size[0] * self._size[1] * self._format[0] // 8)).from_address(self.images[0].pixels)
        surface_array = frombuffer(pixel_buffer, dtype=uint8)

        pixels = surface_array.reshape((self._size[1], self._size[0], self._format[0] // 8))

        # Calculando a média de cada canal de cor (R, G, B, A)
        media_cor = mean(pixels, axis=(0, 1))

        _color = Color(list(media_cor.astype(int)))
        _color.a = 255

        return _color

    @property
    def animated(self):
        return len(self.images) > 1

    def crop(self, location, size):
        _images = []
        for _image in self.images:
            new_surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, size[0], size[1], self._format[0], self._format[1])
            sdl2.SDL_BlitSurface(_image, sdl2.SDL_Rect(*location, *size), new_surface, None)
            sdl2.SDL_FreeSurface(_image)
            _images.append(new_surface.contents)
        del self.images
        self.images = _images
        self._size = list(size)

    def copy(self):
        _new_image = Image()
        for _image in self.images:
            _new_image.images.append(sdl2.SDL_DuplicateSurface(_image).contents)
        _new_image.delays = self.delays
        _new_image._size = self.size
        _new_image._format = self.format
        return _new_image

    def close(self):
        for _image in self.images:
            sdl2.SDL_FreeSurface(_image)
        del self

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
        if path[-4:] == ".gif":
            _Gif = sdlimage.IMG_LoadAnimation(path.encode()).contents
            for frame in range(_Gif.count):
                _Image.images.append(_Gif.frames[frame].contents)
                _Image.delays.append(float(_Gif.delays[frame]))
        else:
            _Image.images.append(sdlimage.IMG_Load(path.encode()).contents)
            _Image.delays.append(0)

    if len(_Image.images) == 0 or not _Image.images[0]:
        LogError(f"Unable to load image '{path}'")
        _Image.images = [sdl2.SDL_CreateRGBSurfaceWithFormat(0, 16, 16, ImageFormat.ARGB[0], ImageFormat.ARGB[1]).contents]
        _Image.delays = [0]

    _Image._size = (_Image.images[0].w, _Image.images[0].h)
    _Image._format = ImageFormat.ARGB
    return _Image

def _loadImageUrl(url):
    _Image = Image()
    try:
        with urlopen(url) as res:
            _chunkSize = -1
            image_bytes = bytes()
            while True:
                chunk = res.read(_chunkSize if _chunkSize > 0 else -1)
                image_bytes += chunk
                if not chunk or _chunkSize <= 0:
                    del chunk
                    break
                del chunk
    except Exception as e:
        pass
    else:
        sdl_image = sdl2.SDL_RWFromConstMem(image_bytes, len(image_bytes))
        if sdlimage.IMG_isGIF(sdl_image):
            _Gif = sdlimage.IMG_LoadAnimation_RW(sdl_image).contents
            for frame in range(_Gif.count):
                _Image.images.append(_Gif.frames[frame].contents)
                _Image.delays.append(float(_Gif.delays[frame]))
        else:
            _Image.images.append(sdlimage.IMG_Load_RW(sdl_image).contents)
            _Image.delays.append(0)
        sdl2.SDL_FreeRW(sdl_image)
        del image_bytes, sdl_image

    if len(_Image.images) == 0 or not _Image.images[0]:
        LogError(f"Unable to load image '{url}'")
        _Image.images = [sdl2.SDL_CreateRGBSurfaceWithFormat(0, 16, 16, ImageFormat.ARGB[0], ImageFormat.ARGB[1]).contents]
        _Image.delays = [0]

    _Image._size = (_Image.images[0].w, _Image.images[0].h)
    _Image._format = ImageFormat.ARGB

    return _Image

def LoadImageUrl(url: str | list | tuple, mult: bool = False) -> Image | tuple | None:
    if isinstance(url, str):
        return _loadImageUrl(url)
    elif isinstance(url, (list, tuple)):
        _image = []
        _threads = []

        def _load(__num):
            _image.insert(__num, _loadImageUrl(url[__num]))

        for num in range(len(url)):
            if mult:
                _thread = Thread(target=_load, args=(num, ), daemon=True)
                _thread.start()
                _threads.append(_thread)
            else:
                _load(num)

        for t in _threads:
            t.join()

        return tuple(_image)
    return None

def LoadIcon(path: str) -> Icon:
    _Icon = Icon()
    if os.path.exists(path):
        if path[-4:] == ".ico":
            _Icon.icon = sdlimage.IMG_LoadICO_RW(sdl2.SDL_RWFromFile(path.encode(), b"r")).contents
    if not _Icon.icon:
        LogError(f"Unable to load icon '{path}'")
        _Icon.icon = sdl2.SDL_CreateRGBSurfaceWithFormat(0, 16, 16, ImageFormat.ARGB[0], ImageFormat.ARGB[1]).contents
    _Icon._size = (_Icon.icon.w, _Icon.icon.h)
    return _Icon

def NewImage(mode=ImageFormat.ARGB, size: list | tuple = (32, 32), color: Color = None) -> Image:
    _image = Image()
    _image.images.append(sdl2.SDL_CreateRGBSurfaceWithFormat(0, size[0], size[1], mode[0], mode[1]).contents)
    _image._size = list(size)
    _image._format = mode
    _image.delays.append(0)
    if color is not None:
        _image.fill(color)
    return _image

def CreateAnimatedImage(images: list[Image] | tuple[Image]):
    _Image = Image()
    _Image._size = max(images, key=lambda _img: _img.size[0] * _img.size[1], default=None).size
    _Image._format = ImageFormat.ARGB
    for img in images:
        for _image in img.images:
            if _Image.size[0] > img.size[0] or _Image.format != img.format:
                new_surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, _Image.size[0], _Image.size[1], _Image.format[0], _Image.format[1])
                sdl2.SDL_BlitScaled(_image, None, new_surface, None)
                _image = new_surface.contents
            _Image.images.append(_image)
        for _delay in img.delays:
            _Image.delays.append(_delay)

    return _Image

def SaveImagePNG(image: Image, path="image.png"):
    sdlimage.IMG_SavePNG(image.images[0], path.encode())

def SaveImageJPG(image: Image, path="image.jpg", quality=80):
    sdlimage.IMG_SaveJPG(image.images[0], path.encode(), quality)

#def SaveImageGIF(image: Image, path="image.GIF"):
#    pass

def image_to_icon(image: Image) -> Icon:
    icon = Icon()
    icon.icon = sdl2.SDL_ConvertSurfaceFormat(image.images[0], ImageFormat.ARGB[1], 0).contents
    icon._size = image.size
    return icon

def icon_to_image(icon: Icon) -> Image:
    _image = Image()
    _image.images.append(sdl2.SDL_DuplicateSurface(icon.icon).contents)
    _image.delays.append(0)
    _image._size = icon.size
    _image._format = ImageFormat.ARGB
    return _image

def _sdl2_surface_to_numpy_array(surface: sdl2.SDL_Surface) -> ndarray:
    width, height = surface.w, surface.h
    depth = surface.format.contents.BytesPerPixel * 8

    pixel_buffer = (c_uint8 * (width * height * depth // 8)).from_address(surface.pixels)
    surface_array = frombuffer(pixel_buffer, dtype=uint8)
    surface_array = surface_array.reshape((height, width, depth // 8))

    return surface_array.copy()

def image_to_numpyArray(image: Image) -> ndarray:
    return _sdl2_surface_to_numpy_array(image.images[0])

def compare_image(image1: Image, image2: Image) -> bool:
    if image1.size != image2.size:
        return False
    pixels1 = image_to_numpyArray(image1)
    pixels2 = image_to_numpyArray(image2)
    pixels = pixels1 == pixels2
    return bool(pixels.all())

def _test_RGBA_mod(surface1, surface2, mult, r, g, b, a):
    if surface1.w == surface2.w and surface1.h == surface2.h:
        pixels, pitch = surface1.pixels, surface1.pitch
        bytes_per_pixel = surface1.format.contents.BytesPerPixel

        pixels2 = surface2.pixels

        def _line_mod():
            for x in range(surface1.w):
                pixel_offset = y * pitch + x * bytes_per_pixel

                _a = c_uint8.from_address((pixels if a else pixels2) + pixel_offset + 3).value
                _r = c_uint8.from_address((pixels if r else pixels2) + pixel_offset + 0).value
                _g = c_uint8.from_address((pixels if g else pixels2) + pixel_offset + 1).value
                _b = c_uint8.from_address((pixels if b else pixels2) + pixel_offset + 2).value

                pixel_value = (_a << 0) | (_r << 8) | (_g << 16) | (_b << 24)

                c_uint32.from_address(surface2.pixels + y * surface2.pitch + x * 4).value = pixel_value

        _threads = []

        for y in range(surface1.h):
            if mult:
                _thread = Thread(target=_line_mod, daemon=True)
                _thread.start()
                _threads.append(_thread)
            else:
                _line_mod()

        for t in _threads:
            t.join()

_path = f"{os.path.abspath(os.path.dirname(__file__))}/logo.ico"
if os.path.exists(_path):
    DefaultIcon = LoadIcon(_path)
elif os.path.exists("./logo.ico"):
    DefaultIcon = LoadIcon("./logo.ico")
else:
    _icon = NewImage(ImageFormat.ARGB, (1, 1), Color((0, 0, 0)))
    DefaultIcon = image_to_icon(_icon)
    _icon.close()
