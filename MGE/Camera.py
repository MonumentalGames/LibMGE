from .Time import Time, fps_to_time

__all__ = ["Camera"]

class Camera:
    def __init__(self, location=(0, 0)):
        self._location = list(location)
        self.motion_tick_time = {"x": Time(fps_to_time(60)), "y": Time(fps_to_time(60))}

    def motionTimeStart(self, axis=-1):
        if axis == 1 or axis == -1:  # x
            self.motion_tick_time["x"].restart()
        if axis == 2 or axis == -1:  # y
            self.motion_tick_time["y"].restart()

    def motion(self, axis, speed):
        if axis == 1 or axis == -1:  # x
            self._location[0] += (speed if type(speed) == int or type(speed) == float else speed[0]) * self.motion_tick_time["x"].tickMotion()
        if axis == 2 or axis == -1:  # y
            self._location[1] += (speed if type(speed) == int or type(speed) == float else speed[1]) * self.motion_tick_time["y"].tickMotion()

    @property
    def location(self):
        return [int(self._location[0]), int(self._location[1])]

    @location.setter
    def location(self, location):
        self._location = location
