from ctypes import c_int, byref

from ._sdl import sdl2
from .Monitors import Monitors
from .Common import _temp, AllEvents, _calculate_object2d

__all__ = ["GetMousePosition", "GetMouseGlobalPosition", "SetMousePosition", "SetMouseGlobalPosition",
           "SetMouseVisibility", "SetMouseCursor", "simpleHover", "object2dSimpleHover",
           "MouseMotion", "MouseGlobalMotion", "MouseButton", "MouseScroll", "MouseState", "MouseMovement"]

def MouseState(button):
    if button == -1:
        return _temp.MouseState
    if 0 < button < 6:
        return bool(_temp.MouseState[button - 1])
    return False

def GetMousePosition():
    x, y = c_int(0), c_int(0)
    sdl2.SDL_GetMouseState(byref(x), byref(y))
    return [x.value, y.value]

def GetMouseGlobalPosition():
    x, y = c_int(0), c_int(0)
    sdl2.SDL_GetGlobalMouseState(byref(x), byref(y))
    return [x.value, y.value]

def SetMousePosition(pos):
    sdl2.SDL_WarpMouseInWindow(None, int(pos[0]), int(pos[1]))

def SetMouseGlobalPosition(pos):
    sdl2.SDL_WarpMouseGlobal(int(pos[0]), int(pos[1]))

def SetMouseVisibility(visibility=True):
    sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE if visibility else sdl2.SDL_DISABLE)

def SetMouseCursor(cursor):
    _temp.MouseCursor = cursor if 0 <= cursor <= 12 else 0

def MouseMovement():
    loc = GetMousePosition()
    if _temp.Mouse["location"] != list(loc):
        if _temp.Mouse["location"] is None:
            _temp.Mouse["location"] = list(loc)
        ret = _temp.Mouse["location"][0] - loc[0], _temp.Mouse["location"][1] - loc[1]
        _temp.Mouse["location"] = loc
        return ret
    else:
        return 0, 0

def MouseMotion(axis, speed):
    _window_resolution = sdl2.SDL_GetWindowSize(sdl2.SDL_GetMouseFocus())
    _window_resolution = [10**6, 10**6] if not _window_resolution else _window_resolution
    _location = GetMousePosition()
    if axis == 1:  # x
        if _temp.mouse_motion_tick_time["x"].tick():
            _location[0] += speed
    elif axis == 2:  # y
        if _temp.mouse_motion_tick_time["y"].tick():
            _location[1] += speed
    for num in range(2):
        if _location[num] < 0:
            _location[num] = 0
        if _location[num] > _window_resolution[num] - 1:
            _location[num] = _window_resolution[num] - 1
    SetMousePosition(_location)

def MouseGlobalMotion(axis, speed):
    _window_resolution = Monitors[0].resolution
    _location = GetMouseGlobalPosition()
    if axis == 1:  # x
        if _temp.mouse_motion_tick_time["x"].tick():
            _location[0] += speed
    elif axis == 2:  # y
        if _temp.mouse_motion_tick_time["y"].tick():
            _location[1] += speed
    for num in range(2):
        if _location[num] < 0:
            _location[num] = 0
        if _location[num] > _window_resolution[num] - 1:
            _location[num] = _window_resolution[num] - 1
    SetMouseGlobalPosition(_location)

def MouseButton(button=1, multiple_click=False):
    for num in range(5):
        if button - 1 == num:
            if MouseState(-1)[num]:
                if not _temp.Mouse["button_cache"][num] or multiple_click:
                    _temp.Mouse["button_cache"][num] = _temp.Mouse["button_cache"][num] if multiple_click else True
                    return True
        if not MouseState(-1)[num]:
            _temp.Mouse["button_cache"][num] = False
    return False

def MouseScroll():
    for event in AllEvents():
        if event.type == sdl2.SDL_MOUSEWHEEL:
            return round(event.wheel.preciseY)
    return 0

def simpleHover(window, location, size):
    location = (location[0] + window.location[0], location[1] + window.location[1]) if window.__WindowId__ < 0 else location
    _position = GetMousePosition()
    return location[0] < _position[0] < location[0] + size[0] and location[1] < _position[1] < location[1] + size[1]

def object2dSimpleHover(window, camera, location, size, scale, pivot):
    _render, cache_location, cache_size = _calculate_object2d(location, size, 0, scale, window, camera, pivot)
    return _render and simpleHover(window, cache_location, cache_size)
