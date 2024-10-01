from .Log import LogCritical
from ._sdl import sdl2

__all__ = ("Monitors", "Monitor", "_update_monitors_datas")

class Monitor:
    def __init__(self, index: int, name: str, resolution: tuple[int, int], frame_rate: float):
        self.__Monitor_Id__ = index
        self.name = name
        self.resolution = resolution
        self.frameRate = frame_rate

Monitors: list[Monitor] = []

def _update_monitors_datas():
    ret = sdl2.SDL_GetNumVideoDisplays()
    if ret < 0:
        LogCritical("no monitor found")
    for num in range(ret):
        name = sdl2.SDL_GetDisplayName(num)
        display_mode = sdl2.SDL_GetCurrentDisplayMode(num)
        Monitors.append(Monitor(num, name, (display_mode.w, display_mode.h), display_mode.refresh_rate))
