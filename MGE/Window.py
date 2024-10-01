from ctypes import c_int, c_uint8, byref, sizeof, windll

from .Common import AllEvents, WindowEvents, _temp, _calculate_object2d
from .Keyboard import KeyboardState
from .Time import Time, fps_to_time, get_fps_from_time
from ._sdl import sdl2, sdlgfx
from .Color import Color
from .Texture import _get_sdl2_texture_size
from .Camera import Camera
from .Image import Image, Icon, DefaultIcon, image_to_icon
from .Platform import Platform
from .Monitors import Monitors
from .Constants import All, WindowFlag, ImageFormat, Pivot2D
from .Mesh import rotate_point
from .Log import LogError, LogCritical
from .Mouse import object2dSimpleHover

__all__ = ["Window", "CreateGlWindow", "InternalWindow"]

class _Window:
    def __init__(self):
        self.__WindowActive__ = True

        self._resolution = None

        self.window = None
        self.context = None
        self.renderer = None
        self.__WindowId__ = -1

        self._variables = {}

        self._frameRateLimit = Monitors[0].frameRate
        self._cache = {"clear_screen": True, "fill": True, "times": {"standard_time": Time(fps_to_time(self._frameRateLimit)), "title_time": Time(0.5), "optimized_time": {"time_start": Time(0.5), "time_loop": Time(fps_to_time(2))}}, "window_tx": None}
        self.frameRate = 0

        self.drawnObjects = []
        self.render_all_objects = True

    @property
    def flags(self):
        if not self.__WindowId__ < 0:
            return sdl2.SDL_GetWindowFlags(self.window)
        else:
            return 0

    @property
    def frameRateLimit(self):
        return self._frameRateLimit

    @frameRateLimit.setter
    def frameRateLimit(self, value):
        self._frameRateLimit = value
        self._cache["times"]["standard_time"].delta_time = fps_to_time(self._frameRateLimit) if self._frameRateLimit > 0 else 0

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables):
        self._variables = variables

    def close(self):
        self.clear(True)
        if self.window is not None:
            if self.__WindowId__ < 0:
                sdl2.SDL_FreeSurface(self.window)
            else:
                sdl2.SDL_DestroyWindow(self.window)
        if self.renderer is not None:
            sdl2.SDL_DestroyRenderer(self.renderer)
        if self.context is not None:
            sdl2.SDL_GL_DeleteContext(self.context)
        if self.__WindowId__ < 0 and self._cache["window_tx"] is not None:
            sdl2.SDL_DestroyTexture(self._cache["window_tx"])
            self._cache["window_tx"] = None
        self.window = self.renderer = None
        self.__WindowActive__ = False

    def clear(self, force=False, color=(0, 0, 0, 255)):
        if self.__WindowActive__ and not (self.flags >> 1) & 1:
            if force or self._cache["clear_screen"]:
                tmp = self.color
                self.color = color
                sdl2.SDL_RenderClear(self.renderer)
                self.color = tmp
                self._cache["clear_screen"] = False
                self._cache["fill"] = True

    def getImage(self):
        _Image = Image()
        if self.__WindowId__ < 0:
            _Image.images.append(self.window)
        else:
            _Image.images.append(sdl2.SDL_CreateRGBSurface(0, self._resolution[0], self._resolution[1], 32, 0, 0, 0, 0).contents)
            sdl2.SDL_RenderReadPixels(self.renderer, None, sdl2.SDL_PIXELFORMAT_ARGB8888, _Image.images[0].pixels, _Image.images[0].pitch)
        _Image.delays.append(0)
        _Image._size = self._resolution
        _Image._format = ImageFormat.ARGB
        return _Image

    def blit(self, surface: Image | sdl2.SDL_Surface | sdl2.SDL_Texture, location=(0, 0), size=None, rotation: int = 0):
        if self.__WindowActive__ and not (self.flags >> 1) & 1:
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
        if self.__WindowActive__ and not (self.flags >> 1) & 1:
            def _square(renderer_, location_, size_, radius_, color_):
                if isinstance(radius_, (tuple, list)) and len(radius_) == 4:
                    if all(x == radius_[0] for x in radius_):
                        sdlgfx.roundedBoxRGBA(renderer_, location_[0], location_[1], location_[0] + size_[0] - 1, location_[1] + size_[1] - 1, radius_[0], *color_.RGBA)
                    else:
                        sdlgfx.filledPieRGBA(renderer_, location_[0] + radius_[0], location_[1] + radius_[0], radius_[0], 180, 270, *color_.RGBA)
                        sdlgfx.filledPieRGBA(renderer_, location_[0] + radius_[1] - 1, location_[1] + size_[1] - radius_[1] - 1, radius_[1], 90, 180, *color_.RGBA)
                        sdlgfx.filledPieRGBA(renderer_, location_[0] + radius_[1] + size_[0] - radius_[1] - radius_[2] - 1, location_[1] + size_[1] - radius_[2] - 1, radius_[2], 0, 90, *color_.RGBA)
                        sdlgfx.filledPieRGBA(renderer_, location_[0] + radius_[0] + size_[0] - radius_[0] - radius_[3] - 1, location_[1] + radius_[3], radius_[3], 270, 360, *color_.RGBA)
                        sdlgfx.boxRGBA(renderer_, location_[0] + radius_[0], location_[1], location_[0] + size_[0] - 1 - radius_[3], location_[1] + size_[1] // 2 - 1, *color_.RGBA)
                        sdlgfx.boxRGBA(renderer_, location_[0] + radius_[1], location_[1] + size_[1] // 2, location_[0] + size_[0] - 1 - radius_[2], location_[1] + size_[1] - 1, *color_.RGBA)
                        sdlgfx.boxRGBA(renderer_, location_[0], location_[1] + radius_[0], location_[0] + size_[0] // 2 - 1, location_[1] + size_[1] - 1 - radius_[1], *color_.RGBA)
                        sdlgfx.boxRGBA(renderer_, location_[0] + size_[0] // 2, location_[1] + radius_[3], location_[0] + size_[0] - 1, location_[1] + size_[1] - 1 - radius_[2], *color_.RGBA)
                elif isinstance(radius_, int) and radius_ > 0:
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
        if self.__WindowActive__ and not (self.flags >> 1) & 1:
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
        if self.__WindowActive__ and not (self.flags >> 1) & 1:
            if size != 0:
                if size == 1:
                    sdlgfx.aalineRGBA(self.renderer, *start, *end, *color.RGBA)
                else:
                    sdlgfx.thickLineRGBA(self.renderer, *start, *end, size if size > 0 else -size, *color.RGBA)

    def drawPolygon(self, location, scale, rotation: int, mesh: list[list[int, int]], color: Color):
        if self.__WindowActive__ and not (self.flags >> 1) & 1:
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
        if self.__WindowActive__ and not (self.flags >> 1) & 1:
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
        if not (self.flags >> 1) & 1:
            r, g, b, a = c_uint8(0), c_uint8(0), c_uint8(0), c_uint8(0)
            ret = sdl2.SDL_GetRenderDrawColor(self.renderer, byref(r), byref(g), byref(b), byref(a))
            if ret is None:
                #sys.exit("Window_error")
                LogError("error getting render color")
            return r.value, g.value, b.value, a.value
        return 0, 0, 0, 0

    @color.setter
    def color(self, color: Color | list[int, int, int, int]):
        if not (self.flags >> 1) & 1:
            ret = sdl2.SDL_SetRenderDrawColor(self.renderer, *color)
            if ret < 0:
                LogError("error when changing rendering color")

class Window(_Window):
    def __init__(self, title="MGE", icon: Icon = DefaultIcon, resolution=(1280, 720), location=(300, 300), logical_resolution=(0, 0), shape=None, camera=Camera(), render_driver=All, flags=WindowFlag.Shown | WindowFlag.Resizable):
        super().__init__()

        self._title = title
        self._location = location
        self._resolution = resolution
        self._logical_resolution = logical_resolution

        self.camera = camera

        self._shape = shape
        if self._shape is None:
            self.window = sdl2.SDL_CreateWindow(self._title, self._location[0], self._location[1], self._resolution[0], self._resolution[1], flags)
        else:
            self.window = sdl2.SDL_CreateShapedWindow(self._title.encode(), self._location[0], self._location[1], self._resolution[0], self._resolution[1], flags)
            sdl2.SDL_SetWindowShape(self.window, self._shape, sdl2.SDL_WindowShapeMode())
        if (flags >> 1) & 1:
            self.context = sdl2.SDL_GL_CreateContext(self.window)
        else:
            self.renderer = sdl2.SDL_CreateRenderer(self.window, render_driver, 0x00000002 | 0x00000008 if Platform.drivers[render_driver].hardware or render_driver == -1 else 0x00000001 | 0x00000008)
        self.__WindowId__ = sdl2.SDL_GetWindowID(self.window)
        _wmInfo = sdl2.SDL_SysWMinfo()
        sdl2.SDL_GetWindowWMInfo(self.window, _wmInfo)
        self._hwnd = _wmInfo.info.win.window
        del _wmInfo
        self.logicalResolution = self._logical_resolution
        self.icon = self._icon = icon

    def __repr__(self):
        return f"<%s.%s resolution=%dx%d at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._resolution[0],
            self._resolution[1],
            id(self)
        )

    @property
    def hwnd(self):
        return self._hwnd

    def update(self, still_frame_optimization: bool = False):
        if self.__WindowActive__:
            if still_frame_optimization:
                if AllEvents() or any(KeyboardState()):
                    self._cache["times"]["optimized_time"]["time_start"].restart()
                else:
                    if self._cache["times"]["optimized_time"]["time_start"].tick():
                        if not self._cache["times"]["optimized_time"]["time_loop"].tick(True):
                            return False
            if self._cache["times"]["standard_time"].tick(True):
                self.frameRate = get_fps_from_time(self._cache["times"]["standard_time"])

                self._resolution = list(sdl2.SDL_GetWindowSize(self.window))

                if WindowEvents(self.__WindowId__, 14):
                    self.close()
                    return

                self.drawnObjects.clear()
                self._cache["clear_screen"] = True
                self._cache["fill"] = True

                if (self.flags >> 1) & 1:
                    sdl2.SDL_GL_SwapWindow(self.window)
                else:
                    sdl2.SDL_RenderPresent(self.renderer)
                return True
        return False

    def recreate(self, title="MGE", icon: Icon = DefaultIcon, resolution=(1280, 720), location=(300, 300), logical_resolution=(0, 0), shape=None, camera=Camera(), flags=WindowFlag.Shown | WindowFlag.Resizable):
        self.close()
        self.__init__(title=title, icon=icon, resolution=resolution, location=location, logical_resolution=logical_resolution, shape=shape, camera=camera, flags=flags)

    def restore(self):
        sdl2.SDL_RestoreWindow(self.window)

    def show(self):
        sdl2.SDL_ShowWindow(self.window)

    def hide(self):
        sdl2.SDL_HideWindow(self.window)

    def maximize(self):
        sdl2.SDL_MaximizeWindow(self.window)

    def minimize(self):
        sdl2.SDL_MinimizeWindow(self.window)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        if self._title != title:
            if self._cache["times"]["title_time"].tick(True):
                self._title = title
                sdl2.SDL_SetWindowTitle(self.window, title)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon: Image | Icon):
        if isinstance(icon, Icon):
            icon = icon
        elif isinstance(icon, Image):
            icon = image_to_icon(icon)
        else:
            LogError("incompatible icon")
            return
        sdl2.SDL_SetWindowIcon(self.window, icon.icon)
        self._icon = icon

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        if self._shape != shape:
            self._shape = shape
            if sdl2.SDL_IsShapedWindow(self.window):
                sdl2.SDL_SetWindowShape(self.window, self._shape, sdl2.SDL_WindowShapeMode())
            else:
                self.recreate(title=self._title, icon=self._icon, resolution=self._resolution, location=self._location, shape=self._shape, camera=self.camera, flags=self.flags)

    @property
    def opacity(self):
        return sdl2.SDL_GetWindowOpacity(self.window)

    @opacity.setter
    def opacity(self, opacity):
        sdl2.SDL_SetWindowOpacity(self.window, opacity)

    @property
    def location(self):
        if self.__WindowActive__:
            x, y = c_int(), c_int()
            sdl2.SDL_GetWindowPosition(self.window, x, y)
            return x.value, y.value
        return self._location

    @location.setter
    def location(self, location):
        if self.__WindowActive__:
            sdl2.SDL_SetWindowPosition(self.window, location[0], location[1])
        self._location = location[0], location[1]

    @property
    def resolution(self) -> tuple:
        if self.__WindowActive__:
            return sdl2.SDL_GetWindowSize(self.window)
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        if self.__WindowActive__:
            sdl2.SDL_SetWindowSize(self.window, resolution[0], resolution[1])
        self._resolution = resolution

    @property
    def minimumResolution(self):
        w, h = c_int(), c_int()
        sdl2.SDL_GetWindowMinimumSize(self.window, w, h)
        return w.value, h.value

    @minimumResolution.setter
    def minimumResolution(self, resolution):
        sdl2.SDL_SetWindowMinimumSize(self.window, resolution[0], resolution[1])

    @property
    def maximumResolution(self):
        w, h = c_int(), c_int()
        sdl2.SDL_GetWindowMaximumSize(self.window, w, h)
        return w.value, h.value

    @maximumResolution.setter
    def maximumResolution(self, resolution):
        sdl2.SDL_SetWindowMaximumSize(self.window, resolution[0], resolution[1])

    @property
    def logicalResolution(self) -> tuple:
        if not (self.flags >> 1) & 1:
            r1, r2 = c_int(), c_int()
            sdl2.SDL_RenderGetLogicalSize(self.renderer, r1, r2)
            self._logical_resolution = [r1.value, r2.value]
        return self._logical_resolution if self._logical_resolution[0] != 0 and self._logical_resolution[1] != 0 else self.resolution

    @logicalResolution.setter
    def logicalResolution(self, resolution):
        if not (self.flags >> 1) & 1:
            sdl2.SDL_RenderSetLogicalSize(self.renderer, resolution[0], resolution[1])
            self._logical_resolution = resolution

    @property
    def borderless(self):
        return bool((self.flags >> 4) & 1)

    @borderless.setter
    def borderless(self, v: bool):
        sdl2.SDL_SetWindowBordered(self.window, v)

    @property
    def resizable(self):
        return bool((self.flags >> 5) & 1)

    @resizable.setter
    def resizable(self, v: bool):
        sdl2.SDL_SetWindowResizable(self.window, v)

    @property
    def alwaysOnTop(self):
        return bool((self.flags >> 15) & 1)

    @alwaysOnTop.setter
    def alwaysOnTop(self, v: bool):
        sdl2.SDL_SetWindowAlwaysOnTop(self.window, v)

    def set_TitleBarColor(self, color: Color):
        if Platform.system.lower() == "windows" and Platform.system_version >= 22000:
            windll.dwmapi.DwmSetWindowAttribute(self._hwnd, 35, byref(c_int(color.Uint32 & ~0xFF000000)), sizeof(c_int))
        else:
            LogError("")

    def set_BorderColor(self, color: Color | None):
        if Platform.system.lower() == "windows" and Platform.system_version >= 22000:
            windll.dwmapi.DwmSetWindowAttribute(self._hwnd, 34, byref(c_int(0xFFFFFFFE if color is None or color.a == 0 else color.Uint32 & ~0xFF000000)), sizeof(c_int))
        else:
            LogError("")

    def set_TitleColor(self, color: Color):
        if Platform.system.lower() == "windows" and Platform.system_version >= 22000:
            windll.dwmapi.DwmSetWindowAttribute(self._hwnd, 36, byref(c_int(color.Uint32 & ~0xFF000000)), sizeof(c_int))
        else:
            LogError("")

def CreateGlWindow(title="MGE", icon: Icon = DefaultIcon, resolution=(1280, 720), location=(300, 300), shape=None, msaa=0, flags=WindowFlag.Shown | WindowFlag.Resizable) -> Window:
    if msaa:
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES, msaa)
    _window = Window(title=title, icon=icon, resolution=resolution, location=location, shape=shape, flags=flags | WindowFlag.Opengl)
    return _window

class InternalWindow(_Window):
    def __init__(self, location=(0, 0), rotation: int = 0, size=(1280, 720), scale=(1, 1), resolution=(1280, 720), camera=Camera()):
        super().__init__()

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

        self._clear_color = (0, 0, 0, 255)

        self._frameRateLimit = 60

        self.object_render = False

    def __repr__(self):
        return f"<%s.%s resolution=%dx%d at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._resolution[0],
            self._resolution[1],
            id(self)
        )

    def render(self, window=None):
        if self._cache["window_tx"] is not None:
            sdl2.SDL_DestroyTexture(self._cache["window_tx"])
            self._cache["window_tx"] = None
        self._cache["window_tx"] = sdl2.SDL_CreateTextureFromSurface(window.renderer if window is not None else sdl2.SDL_GetRenderer(sdl2.SDL_GetWindowFromID(1)), self.window).contents
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
                                    window.blit(self._cache["window_tx"], cache_location, cache_size, 0)
                                    return
                    if self._cache["times"]["standard_time"].tick(True):
                        self.frameRate = get_fps_from_time(self._cache["times"]["standard_time"])

                        self.drawnObjects.clear()
                        self._cache["clear_screen"] = True
                        self._cache["fill"] = True

                        if not self.object_render:
                            self.render()
                        else:
                            sdl2.SDL_UpdateTexture(self._cache["window_tx"], None, self.window.pixels, self.window.pitch)

                    window.blit(self._cache["window_tx"], cache_location, cache_size, self._rotation)

    def hover(self, window, camera: Camera = None) -> bool:
        if object2dSimpleHover(window, camera, self._location, self._size, self._scale, self._pivot):
            #_temp.MouseCursor = self._cursor
            return True
        return False

    def recreate(self, location=(0, 0), rotation: int = 0, size=(1280, 720), scale=(1, 1), resolution=(1280, 720), camera=Camera()):
        self.close()
        self.__init__(location=location, rotation=rotation, size=size, scale=scale, resolution=resolution, camera=camera)

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
            if self._cache["window_tx"] is not None:
                sdl2.SDL_DestroyTexture(self._cache["window_tx"])
            self.window = self.renderer = self._cache["window_tx"] = None

            self.window = sdl2.SDL_CreateRGBSurface(0, self._resolution[0], self._resolution[1], 32, 0, 0, 0, 0)
            self.renderer = sdl2.SDL_CreateSoftwareRenderer(self.window)

            self.object_render = False

    @property
    def logicalResolution(self) -> tuple:
        return self._resolution

    @logicalResolution.setter
    def logicalResolution(self, resolution):
        self._resolution = resolution
