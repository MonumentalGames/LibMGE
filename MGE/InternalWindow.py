from ctypes import c_uint8, byref

from .Common import _temp, AllEvents, _calculate_object2d
from .Log import LogCritical
from .Time import Time, fps_to_time, get_fps_from_time
from ._sdl import sdl2, sdlgfx
from .Color import Color
from .Image import Image
from .Texture import _get_sdl2_texture_size
from .Camera import Camera
from .Mesh import rotate_point
from .Mouse import GetMousePosition
from .Constants import Pivot2D, ImageFormat

__all__ = ["InternalWindow"]

class InternalWindow:
    def __init__(self, location=(0, 0), rotation: int = 0, size=(1280, 720), scale=(1, 1), resolution=(1280, 720), camera=Camera()):
        self.__WindowActive__ = True

        self._size = list(size)
        self._location = list(location)
        self._rotation = rotation
        self._scale = scale
        self._resolution = resolution
        self._pivot = Pivot2D.TopLeftSide
        self._border_size = 0
        self._border_color = Color((100, 100, 255))
        self._border_radius = [0, 0, 0, 0]
        self._cursor = 11

        self.camera = camera

        self.window = sdl2.SDL_CreateRGBSurface(0, self._resolution[0], self._resolution[1], 32, 0, 0, 0, 0).contents
        self.renderer = sdl2.SDL_CreateSoftwareRenderer(self.window)

        self._variables = {}
        self._clear_color = (0, 0, 0, 255)

        self._frameRateLimit = 60
        self._cache = {"clear_screen": True, "fill": True, "times": {"standard_time": Time(fps_to_time(self._frameRateLimit)), "title_time": Time(0.5), "optimized_time": {"time_start": Time(0.5), "time_loop": Time(fps_to_time(2))}}}
        self.frameRate = 0

        self.cache_object = None

        self.drawnObjects = []
        self.object_render = False
        self.render_all_objects = True

    def __repr__(self):
        return f"<%s.%s resolution=%dx%d at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._resolution[0],
            self._resolution[1],
            id(self)
        )

    @property
    def frameRateLimit(self):
        return self._frameRateLimit

    @frameRateLimit.setter
    def frameRateLimit(self, value):
        self._frameRateLimit = value
        self._cache["times"]["standard_time"].delta_time = fps_to_time(self._frameRateLimit) if not self._frameRateLimit == -1 else 0

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables):
        self._variables = variables

    def render(self, window=None):
        if self.cache_object is not None:
            sdl2.SDL_DestroyTexture(self.cache_object)
            self.cache_object = None
        self.cache_object = sdl2.SDL_CreateTextureFromSurface(window.renderer if window is not None else sdl2.SDL_GetRenderer(sdl2.SDL_GetWindowFromID(1)), self.window).contents
        self.object_render = True

    def drawObject(self, window, camera: Camera = None, still_frame_optimization: bool = False):
        if window.__WindowActive__ and self.__WindowActive__:
            if self not in window.drawnObjects:
                window.drawnObjects.append(self)
                render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if render:
                    if len(self.drawnObjects) == 0:
                        window.drawSquare(cache_location, cache_size, self._rotation, 0, Color(self._clear_color))
                        self.frameRate = self._frameRateLimit
                        return

                    if still_frame_optimization:
                        if AllEvents() or any(_temp.KeyboardState):
                            self._cache["times"]["optimized_time"]["time_start"].restart()
                        else:
                            if self._cache["times"]["optimized_time"]["time_start"].tick():
                                if not self._cache["times"]["optimized_time"]["time_loop"].tick(True):
                                    window.blit(self.cache_object, cache_location, cache_size, 0)
                                    return
                    if self._cache["times"]["standard_time"].tick(True):
                        self.frameRate = get_fps_from_time(self._cache["times"]["standard_time"])

                        self.drawnObjects.clear()
                        self._cache["clear_screen"] = True
                        self._cache["fill"] = True

                        if not self.object_render:
                            self.render()
                        else:
                            sdl2.SDL_UpdateTexture(self.cache_object, None, self.window.pixels, self.window.pitch)

                    window.blit(self.cache_object, cache_location, cache_size, self._rotation)

    def hover(self) -> bool:
        cache_location, cache_size = self._location, self._resolution
        mouse_lok = GetMousePosition()
        if cache_location[0] < mouse_lok[0] < cache_location[0] + cache_size[0] and cache_location[1] < mouse_lok[1] < cache_location[1] + cache_size[1]:
            #_temp.MouseCursor = self._cursor
            return True

    def recreate(self, location=(0, 0), rotation: int = 0, size=(1280, 720), scale=(1, 1), resolution=(1280, 720), camera=Camera()):
        self.close()
        self.__init__(location=location, rotation=rotation, size=size, scale=scale, resolution=resolution, camera=camera)

    def close(self):
        self.clear(True)
        if self.window is not None:
            sdl2.SDL_FreeSurface(self.window)
        if self.renderer is not None:
            sdl2.SDL_DestroyRenderer(self.renderer)
        if self.cache_object is not None:
            sdl2.SDL_DestroyTexture(self.cache_object)
        self.window = self.renderer = self.cache_object = None
        self.__WindowActive__ = False

    def clear(self, force=False, color=(0, 0, 0, 255)):
        if self.__WindowActive__:
            if force or self._cache["clear_screen"]:
                tmp = self.color
                self._clear_color = color
                self.color = color
                sdl2.SDL_RenderClear(self.renderer)
                self.color = tmp
                self._cache["clear_screen"] = False
                self._cache["fill"] = True

    def getImage(self):
        _Image = Image()
        _Image.images.append(self.window)
        _Image.delays.append(0)
        _Image._size = self._resolution
        _Image._format = ImageFormat.ARGB
        return _Image

    def blit(self, surface: Image | sdl2.SDL_Surface | sdl2.SDL_Texture, location=(0, 0), size=None, rotation: int = 0):
        if self.__WindowActive__:
            create_texture = False
            if isinstance(surface, Image):
                texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, surface.images[0])
                sdl2.SDL_SetTextureScaleMode(texture, 1)
                create_texture = True
                _size = surface.size if size is None else size
            elif isinstance(surface, sdl2.SDL_Surface):
                texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, surface)
                sdl2.SDL_SetTextureScaleMode(texture, 1)
                create_texture = True
                _size = (surface.w, surface.h) if size is None else size
            elif isinstance(surface, sdl2.SDL_Texture):
                texture = surface
                _size = _get_sdl2_texture_size(texture) if size is None else size
            else:
                return

            if rotation != 0:
                sdl2.SDL_RenderCopyExF(self.renderer, texture, None, sdl2.SDL_FRect(*location, *_size), rotation, sdl2.SDL_FPoint(_size[0] // 2, _size[1] // 2), sdl2.SDL_FLIP_NONE)
            else:
                sdl2.SDL_RenderCopy(self.renderer, texture, None, sdl2.SDL_Rect(*location, *_size))
            if create_texture:
                sdl2.SDL_DestroyTexture(texture)

    def drawPixel(self, location, color: Color):
        sdlgfx.pixelRGBA(self.renderer, *location, *color.RGBA)

    def drawSquare(self, location, size, rotation, radius, color: Color):
        if self.__WindowActive__:
            def _square(renderer_, location_, size_, radius_, color_):
                if radius_ > 0:
                    sdlgfx.roundedBoxRGBA(renderer_, location_[0], location_[1], location_[0] + size_[0] - 1, location_[1] + size_[1] - 1, radius_, *color_.RGBA)
                else:
                    sdlgfx.boxRGBA(renderer_, location_[0], location_[1], location_[0] + size_[0] - 1, location_[1] + size_[1] - 1, *color_.RGBA)

            if rotation != 0:
                mask = sdl2.SDL_CreateRGBSurface(0, size[0], size[1], 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000).contents
                _renderer = sdl2.SDL_CreateSoftwareRenderer(mask)
                _square(_renderer, [0, 0], size, radius, color)
                _texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, mask).contents
                sdl2.SDL_SetTextureScaleMode(_texture, 1)
                self.blit(_texture, [location[0], location[1]], size, rotation)
                sdl2.SDL_DestroyTexture(_texture)
                sdl2.SDL_DestroyRenderer(_renderer)
                sdl2.SDL_FreeSurface(mask)
            else:
                _square(self.renderer, location, size, radius, color)

    def drawEdgesSquare(self, location, size, rotation, line_size, radius, color: Color):
        if self.__WindowActive__:
            if line_size != 0:
                def _hollow_square(renderer_, location_, size_, line_size_, radius_, color_):
                    for num in range(line_size_ if line_size_ > 0 else -line_size_):
                        num = num if line_size_ > 0 else -num
                        if radius_ > 0:
                            sdlgfx.roundedRectangleRGBA(renderer_, location_[0] - num, location_[1] - num, location_[0] + size_[0] + num, location_[1] + size_[1] + num, radius_, *color_.RGBA)
                        else:
                            sdlgfx.rectangleRGBA(renderer_, location_[0] - num, location_[1] - num, location_[0] + size_[0] + num, location_[1] + size_[1] + num, *color_.RGBA)

                if rotation not in [0, 90, 180, 240, 360]:
                    _size = [size[0] + (line_size * 2 if line_size > 1 else 0), size[1] + (line_size * 2 if line_size > 1 else 0)]
                    _location = [line_size if line_size > 1 else 0, line_size if line_size > 1 else 0]
                    mask = sdl2.SDL_CreateRGBSurface(0, _size[0], _size[1], 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000).contents
                    _renderer = sdl2.SDL_CreateSoftwareRenderer(mask)
                    _hollow_square(_renderer, _location, size, line_size, radius, color)
                    self.blit(mask, [location[0] - _location[0], location[1] - _location[1]], None, rotation)
                    sdl2.SDL_DestroyRenderer(_renderer)
                    sdl2.SDL_FreeSurface(mask)
                else:
                    _hollow_square(self.renderer, location, size, line_size, radius, color)

    def drawLine(self, start, end, size, color: Color):
        if self.__WindowActive__:
            if size != 0:
                if size == 1:
                    sdlgfx.aalineRGBA(self.renderer, *start, *end, *color.RGBA)
                else:
                    sdlgfx.thickLineRGBA(self.renderer, *start, *end, size if size > 0 else -size, *color.RGBA)

    def drawPolygon(self, location, scale, rotation: int, mesh: list[list[int, int]], color: Color):
        if self.__WindowActive__:
            _mesh = [(round(point[0] * scale[0]), round(point[1] * scale[1])) for point in mesh]

            if rotation != 0:
                _max_vx = max(round(point[0] * scale[0]) for point in mesh)
                _max_vy = max(round(point[1] * scale[1]) for point in mesh)
                _mesh = [rotate_point(v[0], v[1], _max_vx / 2, _max_vy / 2, rotation) for v in _mesh]

            _vx = [point[0] + location[0] for point in _mesh]
            _vy = [point[1] + location[1] for point in _mesh]
            _n = len(_vx)

            sdlgfx.filledPolygonRGBA(self.renderer, (sdl2.Sint16 * _n)(*map(int, _vx)), (sdl2.Sint16 * _n)(*map(int, _vy)), _n, *color.RGBA)

    def drawEdgesPolygon(self, location, scale, rotation, mesh, color: Color):
        if self.__WindowActive__:
            _mesh = [(round(point[0] * scale[0]), round(point[1] * scale[1])) for point in mesh]

            if rotation != 0:
                _max_vx = max(round(point[0] * scale[0]) for point in mesh)
                _max_vy = max(round(point[1] * scale[1]) for point in mesh)
                _mesh = [rotate_point(v[0], v[1], _max_vx / 2, _max_vy / 2, rotation) for v in _mesh]

            _vx = [point[0] + location[0] for point in _mesh]
            _vy = [point[1] + location[1] for point in _mesh]
            _n = len(_vx)

            sdlgfx.polygonRGBA(self.renderer, (sdl2.Sint16 * _n)(*map(int, _vx)), (sdl2.Sint16 * _n)(*map(int, _vy)), _n, *color.RGBA)

    @property
    def color(self) -> tuple:
        r, g, b, a = c_uint8(0), c_uint8(0), c_uint8(0), c_uint8(0)
        ret = sdl2.SDL_GetRenderDrawColor(self.renderer, byref(r), byref(g), byref(b), byref(a))
        if ret is None:
            LogCritical("Window_error")
        return r.value, g.value, b.value, a.value

    @color.setter
    def color(self, color: Color | list[int, int, int, int]):
        ret = sdl2.SDL_SetRenderDrawColor(self.renderer, *color)
        if ret < 0:
            LogCritical("Window_error")

    @property
    def opacity(self):
        return

    @opacity.setter
    def opacity(self, opacity):
        pass

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location[0], location[1]

    @property
    def size(self) -> list[int, int]:
        # return calculate_size(self.size, Program.screen.get_size())
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: int | float):
        if self._rotation != rotation:
            self._rotation = round(rotation, 4)
            self._rotation %= 360

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def pivot(self):
        return self._pivot

    @pivot.setter
    def pivot(self, pivot):
        self._pivot = pivot

    @property
    def resolution(self) -> tuple:
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        if self._resolution != resolution:
            self._resolution = resolution
            if self.window is not None:
                sdl2.SDL_FreeSurface(self.window)
            if self.renderer is not None:
                sdl2.SDL_DestroyRenderer(self.renderer)
            if self.cache_object is not None:
                sdl2.SDL_DestroyTexture(self.cache_object)
            self.window = self.renderer = self.cache_object = None

            self.window = sdl2.SDL_CreateRGBSurface(0, self._resolution[0], self._resolution[1], 32, 0, 0, 0, 0)
            self.renderer = sdl2.SDL_CreateSoftwareRenderer(self.window)

            self.object_render = False

    @property
    def logicalResolution(self) -> tuple:
        return self._resolution

    @logicalResolution.setter
    def logicalResolution(self, resolution):
        self._resolution = resolution
