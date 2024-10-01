from ._sdl import sdl2
from .Window import Window, InternalWindow
from .Image import icon_to_image
from .Common import _temp, _calculate_object2d
from .Camera import Camera
from .Material import Material, DefaultMaterial
from .Color import Color
from .Time import Time, fps_to_time
from .Constants import Pivot2D
from .Mouse import MouseButton, simpleHover, object2dSimpleHover
from .Text import _ObjectText, _DefaultFont

__all__ = ["Button", "ButtonText", "ButtonImage", "ButtonIcon"]

class _button:
    def __init__(self, location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1)):
        self._size = list(size)
        self._location = list(location)
        self._rotation = rotation
        self._scale = list(scale)
        self._pivot = Pivot2D.TopLeftSide
        self._cursor = 11

    def hover(self, window: Window | InternalWindow, camera: Camera):
        return object2dSimpleHover(window, camera, self._location, self._size, self._scale, self._pivot)

    def button(self, button: int, window, camera: Camera, multiple_click: bool = False) -> bool:
        #self.button_active = True
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

        self.object_render = True
        self.thed_render = self.always_render = False

        self.cache_object = None
        self.cache_object_hover = None
        self.cache_object_tx = None
        self.cache_object_tx_hover = None

        self.button_active = False

    def render(self, window):
        if self.object_render or self.always_render:
            if len(self._material.textures) > 0:
                if self.cache_object is None:
                    self._material.update()
                    self.cache_object = self._material.surface
                    if self.cache_object_tx is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx)
                    self.cache_object_tx = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object).contents
            else:
                if self.cache_object is not None:
                    self.cache_object = None
                    if self.cache_object_tx is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx)
                        self.cache_object_tx = None
                self._material.update()

            if len(self._material_hover.textures) > 0:
                if self.cache_object_hover is None:
                    self._material_hover.update()
                    self.cache_object_hover = self._material_hover.surface
                    if self.cache_object_tx_hover is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
                    self.cache_object_tx_hover = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object_hover).contents
            else:
                if self.cache_object_hover is not None:
                    self.cache_object_hover = None
                    if self.cache_object_tx_hover is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
                        self.cache_object_tx_hover = None
                self._material_hover.update()
            self.object_render = False

    def drawObject(self, window, camera: Camera = None):
        if window.__WindowActive__:
            if self not in window.drawnObjects:
                render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if render:
                    window.drawnObjects.append(self)

                    self.render(window)

                    _material, _cache_object, _cache_object_tx = (self._material_hover, self.cache_object_hover, self.cache_object_tx_hover) if simpleHover(window, cache_location, cache_size) else (self._material, self.cache_object, self.cache_object_tx)

                    if _cache_object is None:
                        window.drawSquare(cache_location, cache_size, self._rotation, self._border_radius[0], _material.color)
                    else:
                        _material.update()
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
            self.object_render = False

    @property
    def materialHover(self):
        return self._material_hover

    @materialHover.setter
    def materialHover(self, material: Material):
        if self._material_hover != material:
            self._material_hover = material
            self.object_render = False

class ButtonText(_button, _ObjectText):
    def __init__(self, location=(0, 0), rotation=0, size=(0, 0), scale=(1, 1), font_size: int = 20, text: str = "", font=_DefaultFont, material=DefaultMaterial, material_hover=DefaultMaterial):
        super().__init__(location, rotation, size, scale)
        super(_button, self).__init__(font_size, text, font)

        self._border_size = 0
        self._border_color = Color((100, 100, 255))
        self._border_radius = [0, 0, 0, 0]

        self._material = material
        self._material_hover = material_hover
        self.materials = [self._material, self._material_hover]

        self.motion_tick_time = {"x": Time(fps_to_time(60)), "y": Time(fps_to_time(60))}

        self.variables = {}

        self._showMoreDetailsOfCollisions = False

        self.object_render = True
        self.thed_render = self.always_render = False

        self.cache_object = None
        self.cache_object_hover = None
        self.cache_object_tx = None
        self.cache_object_tx_hover = None

        self.button_active = False

    def render(self, window):
        if self.object_render or self.always_render:
            self._render()
            if len(self._material.textures) > 0:
                if self.cache_object is None:
                    self._material.update()
                    self.cache_object = self._material.surface
                    if self.cache_object_tx is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx)
                    self.cache_object_tx = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object).contents
            else:
                if self.cache_object is not None:
                    self.cache_object = None
                    if self.cache_object_tx is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx)
                        self.cache_object_tx = None
                self._material.update()

            if len(self._material_hover.textures) > 0:
                if self.cache_object_hover is None:
                    self._material_hover.update()
                    self.cache_object_hover = self._material_hover.surface
                    if self.cache_object_tx_hover is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
                    self.cache_object_tx_hover = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object_hover).contents
            else:
                if self.cache_object_hover is not None:
                    self.cache_object_hover = None
                    if self.cache_object_tx_hover is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
                        self.cache_object_tx_hover = None
                self._material_hover.update()
            self.object_render = False

    def drawObject(self, window, camera: Camera = None, render=True):
        if window.__WindowActive__:
            if self not in window.drawnObjects:
                window.drawnObjects.append(self)
                _render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if _render:

                    self.render(window)

                    _material, _cache_object, _cache_object_tx = (self._material_hover, self.cache_object_hover, self.cache_object_tx_hover) if simpleHover(window, cache_location, cache_size) else (self._material, self.cache_object, self.cache_object_tx)

                    if _cache_object is None:
                        window.drawSquare(cache_location, cache_size, self._rotation, self._border_radius[0], _material.color)
                    else:
                        _material.update()
                        _cache_object = _material.surface
                        sdl2.SDL_UpdateTexture(_cache_object_tx, None, _cache_object.pixels, _cache_object.pitch)
                        window.blit(_cache_object_tx, cache_location, cache_size, self._rotation)
                    if render:
                        self._render()
                    window.blit(self._surface, [cache_location[0] + (cache_size[0] // 2) - (self.surfaceSize[0] // 2), cache_location[1] + (cache_size[1] // 2) - (self.surfaceSize[1] // 2)], None, self._rotation)
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
            self.object_render = True

    @property
    def materialHover(self):
        return self._material_hover

    @materialHover.setter
    def materialHover(self, material: Material):
        if self._material_hover != material:
            self._material_hover = material
            self.object_render = True

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
                self.cache_object = self._image.images[0]
                if self.cache_object_tx is not None:
                    sdl2.SDL_DestroyTexture(self.cache_object_tx)
                self.cache_object_tx = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object).contents
                sdl2.SDL_SetTextureScaleMode(self.cache_object_tx, 1)
            if self.cache_object_hover is None:
                self.cache_object_hover = self._image_hover.images[0]
                if self.cache_object_tx_hover is not None:
                    sdl2.SDL_DestroyTexture(self.cache_object_tx_hover)
                self.cache_object_tx_hover = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object_hover).contents
                sdl2.SDL_SetTextureScaleMode(self.cache_object_tx_hover, 1)
        self.object_render = True

    def drawObject(self, window, camera: Camera = None):
        if window.__WindowActive__:
            if self not in window.drawnObjects:
                render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if render:
                    window.drawnObjects.append(self)
                    if not self.object_render or self.always_render or window.render_all_objects:
                        self.object_render = False
                        self.render(window)

                    _cache_object_tx = self.cache_object_tx_hover if simpleHover(window, cache_location, cache_size) else self.cache_object_tx

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
