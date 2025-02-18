import os
import sys
from ctypes import CDLL
from platform import system
from ..Log import LogError, LogCritical, ConsoleColors

def nullFunction(*args):
    return

def get_depsPath(file_name: str | list):
    file_name = file_name if isinstance(file_name, str) else file_name[0]
    potential_paths = [
        os.path.abspath(f"./{file_name}"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), file_name)),
        os.path.abspath(os.path.join(os.path.dirname(__file__), f"../{file_name}")),
    ]
    for path in potential_paths:
        if os.path.exists(path):
            return path
    LogError(f"{file_name} not found")
    return None

class DLL(object):
    def __init__(self, path=None):
        self._dll = None if path is None else CDLL(path)

    def bindFunction(self, func_name, args=None, returns=None):
        if self._dll is None:
            return None if func_name is None else nullFunction
        else:
            if func_name is None:
                return nullFunction
            func = getattr(self._dll, func_name, None)
            if not func:
                LogError(f"{func_name}")
                return nullFunction
            func.argtypes, func.restype = args, returns
            return func

def get_sdl_func(lib_name):
    extensions = {
        'win32': 'dll',
        'windows': 'dll',
        'darwin': 'dylib',
        'linux': 'so',
        'linux2': 'so',
        'android': 'so'
    }
    return DLL(get_depsPath(f"{lib_name}.{extensions.get(system().lower(), 'so')}")).bindFunction

SDLFunc = get_sdl_func("SDL2")
GFXFunc = get_sdl_func("SDL2_gfx")
IMAGEFunc = get_sdl_func("SDL2_image")
MIXERFunc = get_sdl_func("SDL2_mixer")
TTFFunc = get_sdl_func("SDL2_ttf")

if None in (SDLFunc(None), GFXFunc(None), IMAGEFunc(None), MIXERFunc(None), TTFFunc(None)):
    if sys.argv and sys.argv[0] in (f"{sys.prefix}\\Scripts\\mge.exe", f"{sys.prefix}\\Scripts\\mge"):
        raise SystemExit(1)
    else:
        LogCritical("Error when importing SDL2 libraries", f"MGE dependencies not found. Run '{ConsoleColors.Bold}MGE deps install{ConsoleColors.Reset}' to install them")
