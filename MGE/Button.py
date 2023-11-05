from ._sdl import sdl2, sdlttf
from .Window import Window
from .InternalWindow import InternalWindow
from .Image import Image, Icon, icon_to_image
from .Common import _temp, _calculate_object2d
from .Camera import Camera
from .Material import Material, DefaultMaterial
from .Color import Color
from .Time import Time, fps_to_time
from .Constants import Pivot2D
from .Mouse import MouseButton, GetMousePosition

__all__ = ["Button", "ButtonText", "ButtonImage", "ButtonIcon"]

#location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), material=DefaultMaterial, mesh=Meshes2D.Plane
#location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), material=DefaultMaterial, material_hover=DefaultMaterial
#location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), material=DefaultMaterial

def simpleHover(localization, size):
    _position = GetMousePosition()
    return True if localization[0] < _position[0] < localization[0] + size[0] and localization[1] < _position[1] < localization[1] + size[1] else False

class _button:
    def __init__(self, location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1)):
        self._size = list(size)
        self._location = list(location)
        self._rotation = rotation
        self._scale = list(scale)
        self._pivot = Pivot2D.TopLeftSide
        self._cursor = 11

    def hover(self, window: Window | InternalWindow, camera: Camera):
        render, cache_localization, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
        return True if render and simpleHover(cache_localization, cache_size) else False

    def button(self, button: int, window, camera: Camera, multiple_click: bool = False) -> bool:
        self.button_active = True
        if self.hover(window, camera):
            _temp.MouseCursor = self._cursor
            if MouseButton(button, multiple_click):
                return True
        return False

    @property
    def location(self) -> list[int, int]:
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def size(self) -> list[int, int]:
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

    def cursor(self, cursor: int):
        self._cursor = cursor

class Button(_button):
    def __init__(self, location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), material=DefaultMaterial, material_hover=DefaultMaterial):
        super().__init__(location, rotation, size, scale)
        self._border_size = 0
        self._border_color = Color((100, 100, 255))
        self._border_radius = [0, 0, 0, 0]

        self._material = material
        self._material_hover = material_hover

        self.motion_tick_time = {"x": Time(fps_to_time(60)), "y": Time(fps_to_time(60))}

        self.variables = {}

        self._showMoreDetailsOfCollisions = False

        self.object_render = self.thed_render = self.always_render = False

        self.cache_object = None
        self.cache_object_hover = None
        self.cache_object_tx = None
        self.cache_object_tx_hover = None

        self.button_active = False

    def render(self, window):
        if not self.object_render:
            if len(self._material.textures) > 0:
                if self.cache_object is None:
                    self.cache_object = self._material.render()
                    if self.cache_object_tx is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx)
                    self.cache_object_tx = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object).contents
                if self.cache_object_hover is None:
                    self.cache_object_hover = self._material_hover.render()
                    if self.cache_object_tx_hover is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
                    self.cache_object_tx_hover = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object_hover).contents
            else:
                if self.cache_object is not None or self.cache_object_hover is not None:
                    self.cleanCache()
                self._material.render()
            self.object_render = True

    def draw_button(self, window, camera: Camera = None):
        if window.__Window_Active__:
            if self not in window.draw_objects:
                render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if render:
                    window.draw_objects.append(self)
                    if not self.object_render or self.always_render or window.render_all_objects:
                        self.object_render = False
                        self.render(window)

                    _material, _cache_object, _cache_object_tx = (self._material_hover, self.cache_object_hover, self.cache_object_tx_hover) if simpleHover(cache_location, cache_size) else (self._material, self.cache_object, self.cache_object_tx)

                    if _cache_object is None:
                        window.drawSquare(cache_location, cache_size, self._rotation, self._border_radius[0], _material.color)
                    else:
                        ret = _material.updade()
                        if ret:
                            _cache_object = _material.surface
                            sdl2.SDL_UpdateTexture(_cache_object_tx, None, _cache_object.pixels, _cache_object.pitch)
                        window.blit(_cache_object_tx, cache_location, cache_size, self._rotation)
                    if self._border_size != 0:
                        window.drawEdgesSquare(cache_location, cache_size, self._rotation, self._border_size, self._border_radius[0], self._border_color)

    def cleanCache(self):
        self.cache_object = None
        self.cache_object_hover = None
        if self.cache_object_tx is not None:
            sdl2.SDL_DestroyTexture(self.cache_object_tx)
            self.cache_object_tx = None
        if self.cache_object_tx_hover is not None:
            sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
            self.cache_object_tx_hover = None

    def close(self):
        self.cleanCache()
        del self

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material: Material):
        if self._material != material:
            self._material = material
            self.object_render = self._material.object_render = False

    @property
    def materialHover(self):
        return self._material_hover

    @materialHover.setter
    def materialHover(self, material: Material):
        if self._material_hover != material:
            self._material_hover = material
            self.object_render = self._material_hover.object_render = False

class ButtonText(_button):
    def __init__(self, location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), material=DefaultMaterial, material_hover=DefaultMaterial):
        super().__init__(location, rotation, size, scale)

        self._border_size = 0
        self._border_color = Color((100, 100, 255))
        self._border_radius = [0, 0, 0, 0]

        self._material = material
        self._material_hover = material_hover
        self.materials = [self._material, self._material_hover]

        self.motion_tick_time = {"x": Time(fps_to_time(60)), "y": Time(fps_to_time(60))}

        self.variables = {}

        self._showMoreDetailsOfCollisions = False

        self.object_render = self.thed_render = self.always_render = False

        self.cache_object = None
        self.cache_object_hover = None
        self.cache_object_tx = None
        self.cache_object_tx_hover = None

        self.button_active = False

    def render(self, window):
        if not self.object_render:
            if len(self._material.textures) > 0:
                if self.cache_object is None:
                    self.cache_object = self._material.render()
                    if self.cache_object_tx is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx)
                    self.cache_object_tx = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object).contents
                if self.cache_object_hover is None:
                    self.cache_object_hover = self._material_hover.render()
                    if self.cache_object_tx_hover is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
                    self.cache_object_tx_hover = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object_hover).contents
            else:
                if self.cache_object is not None or self.cache_object_hover is not None:
                    self.cleanCache()
                self._material.render()
            self.object_render = True

    def draw_button(self, window, camera: Camera = None):
        if window.__Window_Active__:
            if self not in window.draw_objects:
                render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if render:
                    window.draw_objects.append(self)
                    if not self.object_render or self.always_render or window.render_all_objects:
                        self.object_render = False
                        self.render(window)

                    _material, _cache_object, _cache_object_tx = (self._material_hover, self.cache_object_hover, self.cache_object_tx_hover) if simpleHover(cache_location, cache_size) else (self._material, self.cache_object, self.cache_object_tx)

                    if _cache_object is None:
                        window.drawSquare(cache_location, cache_size, self._rotation, self._border_radius[0], _material.color)
                    else:
                        ret = _material.updade()
                        if ret:
                            _cache_object = _material.surface
                            sdl2.SDL_UpdateTexture(_cache_object_tx, None, _cache_object.pixels, _cache_object.pitch)
                        window.blit(_cache_object_tx, cache_location, cache_size, self._rotation)
                    if self._border_size != 0:
                        window.drawEdgesSquare(cache_location, cache_size, self._rotation, self._border_size, self._border_radius[0], self._border_color)

    def cleanCache(self):
        self.cache_object = None
        self.cache_object_hover = None
        if self.cache_object_tx is not None:
            sdl2.SDL_DestroyTexture(self.cache_object_tx)
            self.cache_object_tx = None
        if self.cache_object_tx_hover is not None:
            sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
            self.cache_object_tx_hover = None

    def close(self):
        self.cleanCache()
        del self

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material: Material):
        if self._material != material:
            self._material = material
            self.object_render = self._material.object_render = False

    @property
    def materialHover(self):
        return self._material_hover

    @materialHover.setter
    def materialHover(self, material: Material):
        if self._material_hover != material:
            self._material_hover = material
            self.object_render = self._material_hover.object_render = False

class ButtonImage(_button):
    def __init__(self, location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), image=None, image_hover=None):
        super().__init__(location, rotation, size, scale)
        self._border_size = 0
        self._border_color = Color((100, 100, 255))
        self._border_radius = [0, 0, 0, 0]

        self._image = image
        self._image_hover = image_hover

        self.motion_tick_time = {"x": Time(fps_to_time(60)), "y": Time(fps_to_time(60))}

        self.variables = {}

        self._showMoreDetailsOfCollisions = False

        self.object_render = self.thed_render = self.always_render = False

        self.cache_object = None
        self.cache_object_hover = None
        self.cache_object_tx = None
        self.cache_object_tx_hover = None

        self.button_active = False

    def render(self, window):
        if not self.object_render:
            if self.cache_object is None:
                self.cache_object = self._image.image
                if self.cache_object_tx is not None:
                    sdl2.SDL_DestroyTexture(self.cache_object_tx)
                self.cache_object_tx = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object).contents
                sdl2.SDL_SetTextureScaleMode(self.cache_object_tx, 1)
            if self.cache_object_hover is None:
                self.cache_object_hover = self._image_hover.image
                if self.cache_object_tx_hover is not None:
                    sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
                self.cache_object_tx_hover = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object_hover).contents
                sdl2.SDL_SetTextureScaleMode(self.cache_object_tx_hover, 1)

    def draw_button(self, window, camera: Camera = None):
        if window.__Window_Active__:
            if self not in window.draw_objects:
                render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if render:
                    window.draw_objects.append(self)
                    if not self.object_render or self.always_render or window.render_all_objects:
                        self.object_render = False
                        self.render(window)

                    _cache_object_tx = self.cache_object_tx_hover if simpleHover(cache_location, cache_size) else self.cache_object_tx

                    window.blit(_cache_object_tx, cache_location, cache_size, self._rotation)
                    if self._border_size != 0:
                        window.drawEdgesSquare(cache_location, cache_size, self._rotation, self._border_size, self._border_radius[0], self._border_color)

    def cleanCache(self):
        self.cache_object = None
        self.cache_object_hover = None
        if self.cache_object_tx is not None:
            sdl2.SDL_DestroyTexture(self.cache_object_tx)
            self.cache_object_tx = None
        if self.cache_object_tx_hover is not None:
            sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
            self.cache_object_tx_hover = None

    def close(self):
        self.cleanCache()
        del self

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image: Material):
        if self._image != image:
            self._image = image
            self.object_render = False

    @property
    def imageHover(self):
        return self._image_hover

    @imageHover.setter
    def imageHover(self, image: Material):
        if self._image_hover != image:
            self._image_hover = image
            self.object_render = False

class ButtonIcon(ButtonImage):
    def __init__(self, location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), icon=None, icon_hover=None):
        super().__init__(location, rotation, size, scale, icon_to_image(icon), icon_to_image(icon_hover))
