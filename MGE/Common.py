import sys
from ctypes import cast, POINTER as _P
from ._sdl import sdl2, sdlimage, sdlttf, sdlmixer
from .Time import Time as _Time, fps_to_time
from .Monitors import _update_monitors_datas
from .Constants import All, Pivot2D
from .Mesh import edges, calculate_square_vertices, line_intersection

__all__ = ["_temp", "init", "update", "SetLogicClock", "GetLogicClock", "OpenURL",
           "AllEvents", "QuitEvent", "WindowEvents"]

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
    Mouse = {"button_cache": [False, False, False, False, False]}

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

def OpenURL(url: str):
    sdl2.SDL_OpenURL(url.encode())

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

def _calculate_size(size, size_window, scale) -> list:
    cache_size = [s if isinstance(s, str) else int(s) for s in size]

    for num in range(2):
        if isinstance(size[num], str):
            if size[num].endswith('%'):
                cache_size[num] = int(size_window[num] * int(cache_size[num].replace('%', '')) / 100)
        cache_size[num] = int(cache_size[num] * scale[num])

    return cache_size

def _calculate_location(location, size_window) -> list:
    cache_location = [loc if isinstance(loc, str) else int(loc) for loc in location]

    for num in range(2):
        if isinstance(location[num], str):
            if location[num].endswith('%'):
                cache_location[num] = int(size_window[num] * int(location[num].replace('%', '')) / 100)
            elif location[num].lower() == 'center':
                cache_location[num] = int(size_window[num] / 2)

    return cache_location

def _calculate_object2d(location, size, rotation, scale, window, camera, pivot) -> list[bool, list[int, int], list[int, int]]:
    cache_location_camera = camera.location if camera is not None else window.camera.location
    cache_size_screen = window.logicalResolution

    cache_size = _calculate_size(size, cache_size_screen, scale)
    cache_location = _calculate_location(location, cache_size_screen)

    cache_location = [cache_location[0] + cache_location_camera[0], cache_location[1] + cache_location_camera[1]]

    if pivot == Pivot2D.Center:
        cache_location = [cache_location[0] - int(cache_size[0] // 2), cache_location[1] - int(cache_size[1] // 2)]
    elif pivot == Pivot2D.TopRightSide:
        cache_location[1] -= cache_size[1]
    elif pivot == Pivot2D.LowerLeftSide:
        cache_location[0] -= cache_size[0]
    elif pivot == Pivot2D.LowerRightSide:
        cache_location = [cache_location[0] - cache_size[0], cache_location[1] - cache_size[1]]

    if cache_size[0] * -1 < cache_location[0] < cache_size_screen[0] and cache_size[1] * -1 < cache_location[1] < cache_size_screen[1]:
        render = True
    else:
        tt = edges(calculate_square_vertices(cache_location, cache_size, rotation))
        win_tt = edges([(0, 0), (0, window.resolution[1]), window.resolution, (window.resolution[0], 0)])

        render = False

        for num in range(4):
            for num2 in range(4):
                if line_intersection(tt[num][0], tt[num][1], win_tt[num2][0], win_tt[num2][1]):
                    render = True

    return [render, cache_location, cache_size]

def _calculate_line(start, end, size, window, camera) -> list[bool, list[int, int], list[int, int], int]:
    cache_location_camera = camera.location if camera is not None else window.camera.location
    cache_size_screen = window.resolution

    cache_size = _calculate_size([size, 0], cache_size_screen, [1, 1])
    cache_start = _calculate_location(start, cache_size_screen)
    cache_end = _calculate_location(end, cache_size_screen)

    cache_start = [cache_start[0] + cache_location_camera[0], cache_start[1] + cache_location_camera[1]]
    cache_end = [cache_end[0] + cache_location_camera[0], cache_end[1] + cache_location_camera[1]]

    if (cache_size[0] * -1 < cache_start[0] < cache_size_screen[0] and (cache_size[0] * -1) < cache_start[1] < cache_size_screen[1]) or ((cache_size[0] * -1) < cache_end[0] < cache_size_screen[0] and (cache_size[0] * -1) < cache_end[1] < cache_size_screen[1]):
        render = True
    else:
        win_tt = edges([(0, 0), (0, window.resolution[1]), window.resolution, (window.resolution[0], 0)])

        render = False

        for num in range(4):
            if line_intersection(cache_start, cache_end, win_tt[num][0], win_tt[num][1]):
                render = True

    return [render, cache_start, cache_end, cache_size[0]]
