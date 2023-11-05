import sys
from ctypes import c_int, c_uint8, byref

from .Common import _temp, AllEvents, _calculate_object2d
from .Time import Time, fps_to_time, get_fps_from_time
from ._sdl import sdl2, sdlgfx
from .Color import Color
from .Texture import _get_sdl2_texture_size
from .Camera import Camera

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

    def render(self, window=None):
        if self.cache_object is not None:
            sdl2.SDL_DestroyTexture(self.cache_object)
            self.cache_object = None
        self.cache_object = sdl2.SDL_CreateTextureFromSurface(window.renderer if window is not None else sdl2.SDL_GetRenderer(sdl2.SDL_GetWindowFromID(1)), self.window.contents).contents

    def draw_window(self, window, camera: Camera, still_frame_optimization: bool = False):
        if window.__Window_Active__ and self.__Window_Active__:
            if self not in window.draw_objects:
                window.draw_objects.append(self)
                render, cache_location, cache_size = _calculate_object2d(self._location, self._resolution, [1, 1], window, camera, 700)
                if render:
                    if len(self.draw_objects) == 0:
                        window.draw_square(cache_location, cache_size, 0, 0, Color(self._clear_color))
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

    def draw_square(self, location, size, rotation, radius, color: Color):
        if radius > 0:
            sdlgfx.roundedBoxRGBA(self.renderer, location[0], location[1], location[0] + size[0] - 1, location[1] + size[1] - 1, radius, *color.RGBA)
        else:
            sdlgfx.boxRGBA(self.renderer, location[0], location[1], location[0] + size[0] - 1, location[1] + size[1] - 1, *color.RGBA)

    def draw_hollow_square(self, location, size, rotation, line_size, radius, color: Color):
        if line_size != 0:
            for num in range(line_size if line_size > 0 else -line_size):
                num = num if line_size > 0 else -num
                if radius > 0:
                    sdlgfx.roundedRectangleRGBA(self.renderer, location[0] - num, location[1] - num, location[0] + size[0] + num, location[1] + size[1] + num, radius, *color.RGBA)
                else:
                    sdlgfx.rectangleRGBA(self.renderer, location[0] - num, location[1] - num, location[0] + size[0] + num, location[1] + size[1] + num, *color.RGBA)

    def draw_line(self, start, end, size, color: Color):
        if size != 0:
            if size == 1:
                sdlgfx.aalineRGBA(self.renderer, *start, *end, *color.RGBA)
            else:
                sdlgfx.thickLineRGBA(self.renderer, *start, *end, size if size > 0 else -size, *color.RGBA)

    def Polygon(self, vx, vy, n, texture, texture_dx, texture_dy):
        sdlgfx.texturedPolygon(self.renderer, vx, vy, n, texture, texture_dx, texture_dy)

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
        if self.__Window_Active__:
            x, y = c_int(), c_int()
            sdl2.SDL_GetWindowPosition(self.window, x, y)
            return x.value, y.value
        return self._location

    @location.setter
    def location(self, location):
        if self.__Window_Active__:
            sdl2.SDL_SetWindowPosition(self.window, location[0], location[1])
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
