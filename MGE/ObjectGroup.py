from .Window import Window
from .Camera import Camera
from .Text import ObjectText
from .Object2D import Object2D
from .Line import Line

class ObjectGroup:
    def __init__(self, objects, location=(0, 0)):
        self._objects = objects

    def load(self, window: Window):
        for obj in self._objects:
            if isinstance(obj, Object2D):
                obj.render(window)
            elif isinstance(obj, ObjectText):
                obj._single_threading_render()

    def draw_object(self, window: Window, camera: Camera = None):
        for obj in self._objects:
            if isinstance(obj, (Object2D, Line)):
                obj.draw_object(window, camera)
            elif isinstance(obj, ObjectText):
                obj.draw_object(window, camera, True)
