from .Camera import Camera
from .Vector import object2dSimpleMotion
from .Mouse import object2dSimpleHover
from .Material import Material, DefaultMaterial
from .Constants import Pivot2D, Meshes2D
from .Mesh import edges, Mesh2D, calculate_square_vertices, line_intersection
from .Common import _temp, _calculate_object2d, _calculate_size
from .Time import Time, fps_to_time
from .Window import Window, InternalWindow
from .Color import Color
from ._sdl import sdl2

__all__ = ["Object2D"]

class Object2D:
    def __init__(self, location=(0, 0), rotation: int = 0, size=(0, 0), scale=(1, 1), material: Material = DefaultMaterial, mesh: Mesh2D = Meshes2D.Plane):
        self._size = list(size)
        self._location = list(location)
        self._rotation = rotation
        self._scale = list(scale)
        self._mesh = mesh
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
            s = _calculate_size((0, 0), self._size, window.logicalResolution, self._scale)
            if len(self._material.textures) > 0:
                if self.cache_object is None:
                    self._material.render(s)
                    self.cache_object = self._material.surface
                    if self.cache_object_tx is not None:
                        sdl2.SDL_DestroyTexture(self.cache_object_tx)
                        self.cache_object_tx = None
                    self.cache_object_tx = sdl2.SDL_CreateTextureFromSurface(window.renderer, self.cache_object).contents
                    sdl2.SDL_SetTextureScaleMode(self.cache_object_tx, 1)
            else:
                if self.cache_object is not None:
                    self.cleanCache()
                self._material.render(s)
            self.object_render = True

    def drawObject(self, window: Window | InternalWindow, camera: Camera = None):
        if window.__WindowActive__:
            if self not in window.drawnObjects:
                render, cache_location, cache_size = _calculate_object2d(self._location, self._size, self._rotation, self._scale, window, camera, self._pivot)
                if render:
                    window.drawnObjects.append(self)
                    if not self.object_render or self.always_render or window.render_all_objects:
                        self.render(window)
                    if not self._mesh.vertices:
                        if self.cache_object is None:
                            window.drawSquare(cache_location, cache_size, self._rotation, self._border_radius[0], self._material.color)
                        else:
                            self._material.update()
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
                        window.drawPolygon(cache_location, self._scale, self._rotation, self._mesh.vertices, _color)

    def hover(self, window, camera: Camera = None) -> bool:
        if object2dSimpleHover(window, camera, self._location, self._size, self._scale, self._pivot):
            _temp.MouseCursor = self._cursor
            return True
        return False

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
        if self._size != size:
            self._size = size
            self.object_render = False

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

    #@property
    #def borderRadius(self):
    #    return

    #@borderRadius.setter
    #def borderRadius(self, radius: int | tuple[int, int, int, int]):
    #    if type(radius) == int:
    #        self._border_radius = [radius, radius, radius, radius]
    #    elif type(radius) == tuple:
    #        self._border_radius = [radius[0], radius[1], radius[2], radius[3]]
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

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    def motion(self, axis, axis_type, speed: int | float | tuple):
        #Program.Temp.ForceRender = True
        if axis_type == 10:  # global
            if axis == 1 or axis == -1:  # x
                self._location[0] += (speed if type(speed) == int or type(speed) == float else speed[0]) * self._motion_tick_time["x"].tickMotion()
            if axis == 2 or axis == -1:  # y
                self._location[1] += (speed if type(speed) == int or type(speed) == float else speed[1]) * self._motion_tick_time["y"].tickMotion()
        if axis_type == 30:  # local
            if self._motion_tick_time["y"].tick():
                self.location = object2dSimpleMotion(self, axis, speed)

    def collision(self, window, objects: object | list = None, variables: str | list = None) -> bool | list:
        if objects is None:
            objects = window.drawnObjects
        elif isinstance(objects, Object2D):
            objects = [objects]

        def coll(_obj, _var):
            _vars = {}
            if _var and _var is not None and isinstance(_var, (str, list)):
                if isinstance(_var, str):
                    value = _obj.variables.get(_var)
                    if value and value is not None:
                        _vars[_var] = _obj.variables[_var]
                elif isinstance(_var, list):
                    for var in _var:
                        value = _obj.variables.get(var)
                        if value and value is not None:
                            _vars[var] = _obj.variables[var]
                if not _vars:
                    return False

            _edges_self = edges(calculate_square_vertices(self.location, self.size, self.rotation)) if not self.mesh.vertices else self.mesh.edges
            _edges_obj = edges(calculate_square_vertices(_obj.location, _obj.size, _obj.rotation)) if not _obj.mesh.vertices else _obj.mesh.edges

            for _num_edge_self in range(len(_edges_self)):
                for _num_edge_obj in range(len(_edges_obj)):
                    if line_intersection(_edges_self[_num_edge_self][0], _edges_self[_num_edge_self][1], _edges_obj[_num_edge_obj][0], _edges_obj[_num_edge_obj][1]):
                        return [self, _obj, _vars] if self._showMoreDetailsOfCollisions else True
            return False

        rets = []

        for obj in objects:
            if isinstance(obj, Object2D) and not obj == self:
                ret = coll(obj, variables)
                if ret:
                    rets.append(ret)
        if rets:
            return rets if self._showMoreDetailsOfCollisions else True
        return False
