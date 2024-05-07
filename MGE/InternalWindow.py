import sys
from ctypes import c_int, c_uint8, byref

from .Common import _temp, AllEvents, _calculate_object2d
from .Time import Time, fps_to_time, get_fps_from_time
from ._sdl import sdl2, sdlgfx
from .Color import Color
from .Texture import _get_sdl2_texture_size
from .Camera import Camera
from .Mesh import rotate_point
from .Mouse import GetMousePosition

__all__ = ["InternalWindow"]

class InternalWindow:
    def __init__(self, resolution=(1280, 720), location=(300, 300), logical_resolution=(0, 0), camera=Camera()):
        self.__Window_Active__ = True

        self._location = location
        self._resolution = resolution
        self._logical_resolution = logical_resolution

        self.window = sdl2.SDL_CreateRGBSurface(0, self._resolution[0], self._resolution[1], 32, 0, 0, 0, 0)
        self.renderer = sdl2.SDL_CreateSoftwareRenderer(self.window)

        self.logicalResolution = self._logical_resolution

        self._variables = {}
        self._clear_color = (0, 0, 0, 255)

        self.render_all_objects = True

        self._limit_time = 60
        self._cache = {"clear_screen": True, "fill": True, "times": {"standard_time": Time(fps_to_time(self._limit_time)), "title_time": Time(0.5), "optimized_time": {"time_start": Time(0.5), "time_loop": Time(fps_to_time(2))}}}
        self.fps = 0

        self.camera = camera

        self.cache_object = None

        self.draw_objects = []

    def __repr__(self):
        return f"<%s.%s resolution=%dx%d at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._resolution[0],
            self._resolution[1],
            id(self)
        )

    @property
    def limit_time(self):
        return self._limit_time

    @limit_time.setter
    def limit_time(self, value):
        self._limit_time = value
        self._cache["times"]["standard_time"].delta_time = fps_to_time(self._limit_time) if not self._limit_time == -1 else 0

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables):
        self._variables = variables

    def hover(self) -> bool:
        cache_location, cache_size = self._location, self._resolution
        mouse_lok = GetMousePosition()
        if cache_location[0] < mouse_lok[0] < cache_location[0] + cache_size[0] and cache_location[1] < mouse_lok[1] < cache_location[1] + cache_size[1]:
            #_temp.MouseCursor = self._cursor
            return True

    def render(self, window=None):
        if self.cache_object is not None:
            sdl2.SDL_DestroyTexture(self.cache_object)
            self.cache_object = None
        self.cache_object = sdl2.SDL_CreateTextureFromSurface(window.renderer if window is not None else sdl2.SDL_GetRenderer(sdl2.SDL_GetWindowFromID(1)), self.window.contents).contents

    def draw_window(self, window, still_frame_optimization: bool = False):
        if window.__Window_Active__ and self.__Window_Active__:
            if self not in window.draw_objects:
                window.draw_objects.append(self)
                render, cache_location, cache_size = _calculate_object2d(self._location, self._resolution, 0, [1, 1], window, None, 700)
                if render:
                    if len(self.draw_objects) == 0:
                        window.drawSquare(cache_location, cache_size, 0, 0, Color(self._clear_color))
                        self.fps = self._limit_time
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
                        self.fps = get_fps_from_time(self._cache["times"]["standard_time"])

                        self.draw_objects.clear()
                        self._cache["clear_screen"] = True
                        self._cache["fill"] = True

                        self.render()

                    window.blit(self.cache_object, cache_location, cache_size, 0)

    def set_window(self, resolution=(1280, 720), location=(300, 300)):
        self._location = tuple(location)
        self._resolution = tuple(resolution)

        self.window = sdl2.SDL_CreateRGBSurface(0, self._resolution[0], self._resolution[1], 32, 0, 0, 0, 0)
        self.renderer = sdl2.SDL_CreateSoftwareRenderer(self.window)

    def clear(self, force=False, color=(0, 0, 0, 255)):
        if self.__Window_Active__:
            if force or self._cache["clear_screen"]:
                tmp = self.color
                self._clear_color = color
                self.color = color
                sdl2.SDL_RenderClear(self.renderer)
                self.color = tmp
                self._cache["clear_screen"] = False
                self._cache["fill"] = True

    def blit(self, surface: sdl2.SDL_Surface | sdl2.SDL_Texture, location=(0, 0), size=None, rotation: int = 0):
        create_texture = False
        if isinstance(surface, sdl2.SDL_Surface):
            texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, surface)
            create_texture = True
        elif isinstance(surface, sdl2.SDL_Texture):
            texture = surface
        elif surface is None:
            return
        else:
            sys.exit("texture")

        size = _get_sdl2_texture_size(texture) if size is None else size

        if rotation != 0:
            sdl2.SDL_RenderCopyExF(self.renderer, texture, None, sdl2.SDL_FRect(*location, *size), rotation, sdl2.SDL_FPoint(size[0] // 2, size[1] // 2), sdl2.SDL_FLIP_NONE)
        else:
            sdl2.SDL_RenderCopy(self.renderer, texture, None, sdl2.SDL_Rect(*location, *size))
        if create_texture:
            sdl2.SDL_DestroyTexture(texture)

    def drawPixel(self, location, color: Color):
        sdlgfx.pixelRGBA(self.renderer, *location, *color.RGBA)

    def drawSquare(self, location, size, rotation, radius, color: Color):
        if self.__Window_Active__:
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
        if self.__Window_Active__:
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
        if self.__Window_Active__:
            if size != 0:
                if size == 1:
                    sdlgfx.aalineRGBA(self.renderer, *start, *end, *color.RGBA)
                else:
                    sdlgfx.thickLineRGBA(self.renderer, *start, *end, size if size > 0 else -size, *color.RGBA)

    def drawPolygon(self, location, scale, rotation: int, mesh: list[list[int, int]], color: Color):
        if self.__Window_Active__:
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
        if self.__Window_Active__:
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
            sys.exit("Window_error")
        return r.value, g.value, b.value, a.value

    @color.setter
    def color(self, color: Color | list[int, int, int, int]):
        ret = sdl2.SDL_SetRenderDrawColor(self.renderer, *color)
        if ret < 0:
            sys.exit("Window_error")

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
    def resolution(self) -> tuple:
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        self._resolution = resolution

    @property
    def logicalResolution(self) -> tuple:
        if self.__Window_Active__:
            r1, r2 = c_int(), c_int()
            sdl2.SDL_RenderGetLogicalSize(self.renderer, r1, r2)
            self._logical_resolution = [r1.value, r2.value]
        return self._logical_resolution if self._logical_resolution[0] != 0 and self._logical_resolution[1] != 0 else self.resolution

    @logicalResolution.setter
    def logicalResolution(self, resolution):
        if self.__Window_Active__:
            sdl2.SDL_RenderSetLogicalSize(self.renderer, resolution[0], resolution[1])
        self._logical_resolution = resolution
