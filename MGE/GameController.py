import os
from .Color import Color
from .Constants import Colors
from ._sdl import sdl2

__all__ = ["Controller",
           "AllowBackgroundControllerEvents"]

class Controller:
    def __init__(self, index=0):
        self._controller = sdl2.SDL_GameController()
        self._name = ""
        self._led_color = Colors.Blue
        self._index = index
        self.buttons_cache = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        if sdl2.SDL_NumJoysticks() >= index + 1:
            self._controller = sdl2.SDL_GameControllerOpen(index)
            self._name = sdl2.SDL_GameControllerName(self._controller).decode()
            sdl2.SDL_GameControllerSetPlayerIndex(self._controller, 3)
            sdl2.SDL_GameControllerSetLED(self._controller, 0, 0, 255)

    def reload(self, index=-1):
        if sdl2.SDL_NumJoysticks() >= self._index + 1 if index == -1 else 1:
            self._controller = sdl2.SDL_GameControllerOpen(self._index if index == -1 or not type(index) == int else index)
            self._name = sdl2.SDL_GameControllerName(self._controller).decode()
            self._index = self._index if index == -1 or not type(index) == int else index

    def led(self, color: Color | bool):
        if isinstance(color, bool):
            if not color:
                sdl2.SDL_GameControllerSetLED(self._controller, 0, 0, 0)
                return
            color = self._led_color
        if isinstance(color, Color) and not color.RGB == (0, 0, 0):
            self._led_color = color
        sdl2.SDL_GameControllerSetLED(self._controller, *color.RGB)

    def button(self, button=0, multiple_click=False):
        buttons = []
        for num in range(21):
            if button == -1:
                buttons.append(bool(sdl2.SDL_GameControllerGetButton(self._controller, num)))
            else:
                if button == num:
                    if sdl2.SDL_GameControllerGetButton(self._controller, button):
                        if not self.buttons_cache[button] or multiple_click:
                            self.buttons_cache[button] = True
                            return True
                if not sdl2.SDL_GameControllerGetButton(self._controller, num):
                    self.buttons_cache[num] = False
        return buttons if buttons else False

    def analogStick(self, axis):
        xy = [0, 0]
        if axis == -1:
            xy = [0, 0, 0, 0]
            axis = (0, 1, 2, 3)
        elif axis == 0:
            axis = (0, 1)
        elif axis == 1:
            axis = (2, 3)
        for num in axis:
            value = sdl2.SDL_GameControllerGetAxis(self._controller, num)
            value = round(value / 32.767)
            xy[num] = value if not -50 < value < 50 else 0
        return xy

    def trigger(self, trigger):
        if trigger == 0:
            trigger = 4
        elif trigger == 1:
            trigger = 5
        value = sdl2.SDL_GameControllerGetAxis(self._controller, trigger)
        value = round(value / 32.767)
        value = value if not -5 < value < 5 else 0
        return value

def AllowBackgroundControllerEvents(value: bool):
    os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1" if value else "0"
