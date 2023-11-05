import ctypes

from ._sdl import sdl2
from .Monitors import Monitors
from .Common import _temp

__all__ = ["GetMousePosition", "GetMouseGlobalPosition", "SetMousePosition", "SetMouseGlobalPosition",
           "SetMouseVisibility", "SetMouseCursor",
           "MouseMotion", "MouseGlobalMotion", "MouseButton", "MouseState"]

def MouseState(button):
    if button == -1:
        return _temp.MouseState
    if 0 < button < 6:
        return bool(_temp.MouseState[button - 1])
    return False

def GetMousePosition():
    x, y = ctypes.c_int(0), ctypes.c_int(0)
    sdl2.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
    return [x.value, y.value]

def GetMouseGlobalPosition():
    x, y = ctypes.c_int(0), ctypes.c_int(0)
    sdl2.SDL_GetGlobalMouseState(ctypes.byref(x), ctypes.byref(y))
    return [x.value, y.value]

def SetMousePosition(pos):
    sdl2.SDL_WarpMouseInWindow(None, int(pos[0]), int(pos[1]))

def SetMouseGlobalPosition(pos):
    sdl2.SDL_WarpMouseGlobal(int(pos[0]), int(pos[1]))

def SetMouseVisibility(visibility=True):
    sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE if visibility else sdl2.SDL_DISABLE)

def SetMouseCursor(cursor):
    #sdl2.SDL_SetCursor(_temp.MouseCursors[cursor if 0 <= cursor <= 12 else 0])
    _temp.MouseCursor = cursor if 0 <= cursor <= 12 else 0

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
