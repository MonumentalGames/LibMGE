from .Camera import Camera
from .Vector import motion
from .Mouse import GetMousePosition
from .Material import Material, DefaultMaterial
from .Constants import Pivot2D, Meshes2D
from .Mesh import *
from .Common import _temp, _calculate_object2d
from .Time import Time, fps_to_time
from .Window import Window
from .Color import Color
from ._sdl import sdl2

__all__ = ["Object2D"]

class Object2D:
    def __init__(self, location=(0, 0), rotation: int = 0, size=(0, 0), scale=(1, 1), material: Material = DefaultMaterial, mesh: Mesh2D = Meshes2D.Plane):
        self._size = list(size)
        self._location = list(location)
        self._rotation = rotation
        self._scale = list(scale)
        self._Mesh = mesh
        self._pivot = Pivot2D.TopLeftSide
        self._border_size = 0
        self._border_color = Color((100, 100, 255))
        self._border_radius = [0, 0, 0, 0]
        self._cursor = 11
        self._material = material

        self._motion_tick_time = {"x": Time(fps_to_time(60)), "y": Time(fps_to_time(60))}

        self.variables = {}

        self._showMoreDetailsOfCollisions = False

        self.object_render = self.thed_render = self.always_render = False

        self.cache_object = None
        self.cache_object_tx = None

    def render(self, window):
        if not self.object_render:
            if len(self._material.textures) > 0:
                if self.cache_object is None:
                    self._material.render()
                    self.cache_object = self._material.surface
                    if self.cache_object_tx is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx)
                        self.cache_object_tx = None
                    self.cache_object_tx = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object).contents
            else:
                if self.cache_object is not None:
                    self.cleanCache()
                self._material.render()
            self.object_render = True

    def draw_object(self, window: Window, camera: Camera = None):
        if window.__Window_Active__:
            if self not in window.draw_objects:
                render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if render:
                    window.draw_objects.append(self)
                    if not self.object_render or self.always_render or window.render_all_objects:
                        self.object_render = False
                        self.render(window)
                    if not self._Mesh.vertices:
                        if self.cache_object is None:
                            window.drawSquare(cache_location, cache_size, self._rotation, self._border_radius[0], self._material.color)
                        else:
                            ret = self._material.updade()
                            if ret:
                                self.cache_object = self._material.surface
                                sdl2.SDL_UpdateTexture(self.cache_object_tx, None, self.cache_object.pixels, self.cache_object.pitch)
                            window.blit(self.cache_object_tx, cache_location, cache_size, self._rotation)
                        if self._border_size != 0:
                            window.drawEdgesSquare(cache_location, cache_size, self._rotation, self._border_size, self._border_radius[0], self._border_color)
                    else:
                        if len(self._material.textures) > 0:
                            _color = self._material.surfaceColor
                        else:
                            _color = self._material.color
                        window.drawPolygon(cache_location, self._scale, self._rotation, self._Mesh.vertices, _color)

    def hover(self, window, camera: Camera = None) -> bool:
        render, cache_localization, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
        mouse_lok = GetMousePosition()
        if render and (cache_localization[0] < mouse_lok[0] < cache_localization[0] + cache_size[0] and cache_localization[1] < mouse_lok[1] < cache_localization[1] + cache_size[1]):
            _temp.MouseCursor = self._cursor
            return True

    def cleanCache(self):
        self.cache_object = None
        if self.cache_object_tx is not None:
            sdl2.SDL_DestroyTexture(self.cache_object_tx)
            self.cache_object_tx = None
        #if self.cache_object is not None:
        #    self.cache_object.close()
        #    del self.cache_object
        #    self.cache_object = None

    def close(self):
        self.cleanCache()
        del self

    @property
    def location(self) -> list[int, int]:
        #return calculate_location(self.localization, Program.screen.get_size())
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def size(self) -> list[int, int]:
        #return calculate_size(self.size, Program.screen.get_size())
        return self._size

    @size.setter
    def size(self, size):
        #if self._size != size:
        self._size = size
        #    self.object_render = False

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
        if self._scale != scale:
            self._scale = scale
            self.object_render = self._material.object_render = False

    @property
    def pivot(self):
        return self._pivot

    @pivot.setter
    def pivot(self, pivot):
        self._pivot = pivot

    @property
    def borderSize(self):
        return self._border_size

    @borderSize.setter
    def borderSize(self, border_size: int):
        self._border_size = border_size

    @property
    def borderColor(self):
        return self._border_color

    @borderColor.setter
    def borderColor(self, border_color: Color):
        self._border_color = border_color

    @property
    def borderRadius(self):
        return

    @borderRadius.setter
    def borderRadius(self, radius: int | tuple[int, int, int, int]):
        if type(radius) == int:
            self._border_radius = [radius, radius, radius, radius]
        elif type(radius) == tuple:
            self._border_radius = [radius[0], radius[1], radius[2], radius[3]]
        #self.border_radius = [higher_right, higher_left, bottom_right, bottom_left]

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material: Material):
        if self._material != material:
            self._material = material
            self.object_render = self._material.object_render = False

    def cursor(self, cursor: int):
        self._cursor = cursor

    def motion(self, axis, axis_type, speed: int | float | tuple):
        #Program.Temp.ForceRender = True
        if axis_type == 10:  # global
            if axis == 1 or axis == -1:  # x
                self._location[0] += (speed if type(speed) == int or type(speed) == float else speed[0]) * self._motion_tick_time["x"].tickMotion()
            if axis == 2 or axis == -1:  # y
                self._location[1] += (speed if type(speed) == int or type(speed) == float else speed[1]) * self._motion_tick_time["y"].tickMotion()
        if axis_type == 30:  # local
            if self._motion_tick_time["y"].tick():
                self.location = motion(self, axis, speed)

    def collision(self, objects: object | list, variables: str | list = "") -> bool | list:
        if not isinstance(objects, list):
            objects = [objects]

        def coll(s_objects, s_variables):
            _variables = {}
            if s_variables:
                if isinstance(s_variables, str):
                    if s_variables in s_objects.variables.keys():
                        if s_objects.variables[s_variables]:
                            _variables[s_variables] = s_objects.variables[s_variables]
                        else:
                            return False
                    else:
                        return False
                elif isinstance(s_variables, list):
                    for var in s_variables:
                        if var in s_objects.variables.keys():
                            if s_objects.variables[var]:
                                _variables[var] = s_objects.variables[var]
                    if not _variables:
                        return False
            if self._location[0] < s_objects._location[0] + s_objects._size[0] + 1 and self._location[0] + self._size[0] + 1 > s_objects._location[0] \
                    and self._location[1] < s_objects._location[1] + s_objects._size[1] + 1 and self._location[1] + self._size[1] + 1 > s_objects._location[1]:
                return [self, s_objects, _variables] if self._showMoreDetailsOfCollisions else True
            return False

        rets = []

        for ob in objects:
            if isinstance(ob, Object2D) and not ob == self:
                ret = coll(ob, variables)
                if ret:
                    rets.append(ret)
        if rets:
            return rets if self._showMoreDetailsOfCollisions else True
        return False
