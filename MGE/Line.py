from .Window import Window
from .Camera import Camera
from .Material import Material
from .Common import _calculate_line

__all__ = ["Line"]

class Line:
    def __init__(self, start, end, size: int):
        self._start = start
        self._end = end
        self._size = size

        self.variables = {"_type": "Line"}

        self._material = Material()

    def drawObject(self, window: Window, camera: Camera = None):
        if not window.__WindowActive__ or not window.drawnObjects.addObject(id(self), self):
            return

        _render, cache_start, cache_end, cache_size = _calculate_line(self._start, self._end, self._size, window, camera)
        if not _render:
            return

        window.drawLine(cache_start, cache_end, cache_size, self._material.color)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = end

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = int(size)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material: Material):
        if self._material != material:
            self._material = material
