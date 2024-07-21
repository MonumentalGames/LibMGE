import sys
import os
import types
from ctypes import cast, POINTER as _P
from ._sdl import sdl2, sdlimage, sdlttf, sdlmixer
from .Time import Time as _Time, fps_to_time, get_fps_from_time
from .Monitors import _update_monitors_datas
from .Constants import All, Pivot2D
from .Mesh import edges, calculate_square_vertices, line_intersection

__all__ = ["_temp", "init", "update", "SetLogicClock", "GetLogicClock", "OpenUrl",
           "AllEvents", "QuitEvent", "WindowEvents", "AutoCalcs2D",
           "_calculate_size", "_calculate_location", "_calculate_object2d", "_calculate_line"]

class _temp:
    LogicClock = 1024

    mouse_motion_tick_time = {"x": _Time(fps_to_time(60)), "y": _Time(fps_to_time(60))}

    Time = {"LogicTime": _Time(fps_to_time(LogicClock))}

    Events = []

    KeyboardState = sdl2.SDL_GetKeyboardState(None)
    KeyboardCache = []
    for num in range(530):
        KeyboardCache.append(True)

    MouseState = [False, False, False, False, False]
    Mouse = {"location": None, "button_cache": [False, False, False, False, False]}

    MouseCursor = 0

    MouseCursors = []

    Button = {"button_active": False}

def init(video=True, audio=False, events=True, controller=False, sensor=False):
    if sdl2.SDL_Init(0) != 0:
        sys.exit("initializing SDL2")

    def sdl2_init(system):
        if sdl2.SDL_InitSubSystem(system) != 0:
            sys.exit(f"initializing the {system} subsystem")

    sdl2_init(sdl2.SDL_INIT_TIMER)
    if events:
        sdl2_init(sdl2.SDL_INIT_EVENTS)
    if video:
        sdl2_init(sdl2.SDL_INIT_VIDEO)
        for num in range(12):
            _temp.MouseCursors.append(sdl2.SDL_CreateSystemCursor(num).contents)
        _update_monitors_datas()
        sdlttf.TTF_Init()
        sdlimage.IMG_Init()
        os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"
    if audio:
        sdlmixer.Mix_OpenAudio(360000, sdl2.AUDIO_S16SYS, 2, 1024)
        sdlmixer.Mix_Init()
    if controller:
        sdl2_init(sdl2.SDL_INIT_JOYSTICK)
        sdl2_init(sdl2.SDL_INIT_GAMECONTROLLER)
    # if haptic:
    #    sdl2_init(sdl2.SDL_INIT_HAPTIC)
    if sensor:
        sdl2_init(sdl2.SDL_INIT_SENSOR)

def update():
    _temp.Time["LogicTime"].tickSleep()

    sdl2.SDL_PumpEvents()
    _events = (sdl2.SDL_Event * 10)()
    _num = sdl2.SDL_PeepEvents(cast(_events, _P(sdl2.SDL_Event)), 10, sdl2.SDL_GETEVENT, sdl2.SDL_FIRSTEVENT, sdl2.SDL_LASTEVENT)
    _temp.Events = list(_events)[:_num]

    _keyboard = sdl2.SDL_GetKeyboardState(None)
    _temp.KeyboardState = [bool(_keyboard[_num]) for _num in range(530)]

    _mouse = sdl2.SDL_GetMouseState(None, None)
    _temp.MouseState = [bool(_mouse & (1 << _num)) for _num in range(5)]

    if _temp.Button["button_active"]:
        _temp.Button["button_active"] = False
    sdl2.SDL_SetCursor(_temp.MouseCursors[_temp.MouseCursor])
    _temp.MouseCursor = 0

def SetLogicClock(logic_clock: int):
    _temp.Time["LogicTime"].delta_time = fps_to_time(logic_clock)

def GetLogicClock() -> int:
    return _temp.LogicClock

def OpenUrl(url: str):
    sdl2.SDL_OpenURL(url)

def AllEvents():
    return _temp.Events

def QuitEvent():
    for event in AllEvents():
        if event.type == 256:
            return True
    return False

def WindowEvents(window: int = All, event: int = All):
    for _event in AllEvents():
        if _event.type == 512:
            if window == _event.window.windowID or window == All:
                if event == _event.window.event or event == All:
                    return _event.window.event
    return 0

class AutoCalcs2D:
    @staticmethod
    def Percent(percent: int):
        return lambda location, size, size_window, scale: size_window / 100 * percent

    @staticmethod
    def Center():
        return lambda location, size, size_window, scale: size_window / 2

def _calculate_size(location, size, size_window, scale) -> list:
    return [round(size[num](location[num], size[num], size_window[num], scale[num]) * scale[num]) if callable(size[num]) else round(size[num] * scale[num]) for num in range(2)]

def _calculate_location(location, size, size_window, scale) -> list:
    return [round(location[num](location[num], size[num], size_window[num], scale[num])) if callable(location[num]) else round(location[num]) for num in range(2)]

def _calculate_object2d(location, size, rotation, scale, window, camera, pivot) -> list[bool, list[int, int], list[int, int]]:
    _location_camera = camera.location if camera is not None else window.camera.location
    _size_window = window.logicalResolution

    _size = _calculate_size((0, 0), size, _size_window, scale)
    _location = _calculate_location(location, _size, _size_window, scale)

    _location = [_location[0] + _location_camera[0], _location[1] + _location_camera[1]]

    if pivot == Pivot2D.Center:
        _location = [_location[0] - int(_size[0] // 2), _location[1] - int(_size[1] // 2)]
    elif pivot == Pivot2D.TopRightSide:
        _location[1] -= _size[1]
    elif pivot == Pivot2D.LowerLeftSide:
        _location[0] -= _size[0]
    elif pivot == Pivot2D.LowerRightSide:
        _location = [_location[0] - _size[0], _location[1] - _size[1]]

    render = False
    if _size[0] * -1 < _location[0] < _size_window[0] and _size[1] * -1 < _location[1] < _size_window[1]:
        render = True
    else:
        tt = edges(calculate_square_vertices(_location, _size, rotation))
        win_tt = edges([(0, 0), (0, window.resolution[1]), window.resolution, (window.resolution[0], 0)])

        for num in range(4):
            for num2 in range(4):
                if line_intersection(tt[num][0], tt[num][1], win_tt[num2][0], win_tt[num2][1]):
                    render = True

    return [render, _location, _size]

def _calculate_line(start, end, size, window, camera) -> list[bool, list[int, int], list[int, int], int]:
    _location_camera = camera.location if camera is not None else window.camera.location
    _size_window = window.resolution

    _size = _calculate_size((0, 0), (size, 0), _size_window, (1, 1))
    _start = _calculate_location(start, _size, _size_window, (1, 1))
    _end = _calculate_location(end, _size, _size_window, (1, 1))

    _start = [_start[0] + _location_camera[0], _start[1] + _location_camera[1]]
    _end = [_end[0] + _location_camera[0], _end[1] + _location_camera[1]]

    render = False
    if (_size[0] * -1 < _start[0] < _size_window[0] and (_size[0] * -1) < _start[1] < _size_window[1]) or ((_size[0] * -1) < _end[0] < _size_window[0] and (_size[0] * -1) < _end[1] < _size_window[1]):
        render = True
    else:
        win_tt = edges([(0, 0), (0, window.resolution[1]), window.resolution, (window.resolution[0], 0)])

        for num in range(4):
            if line_intersection(_start, _end, win_tt[num][0], win_tt[num][1]):
                render = True

    return [render, _start, _end, _size[0]]
