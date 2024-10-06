import os
from ctypes import CDLL
from ..Log import LogError, LogCritical

def nullFunction(*args):
    return

def get_depsPath(file_name: str | list):
    file_name = file_name if type(file_name) == str else file_name[0]
    if os.path.exists(f"{os.path.abspath('./')}/{file_name}"):
        dll_path = os.path.abspath(f'./{file_name}')
    elif os.path.exists(f"{os.path.abspath(os.path.dirname(__file__))}/{file_name}"):
        dll_path = f"{os.path.abspath(os.path.dirname(__file__))}/{file_name}"
    elif os.path.exists(f"{os.path.abspath(os.path.dirname(__file__))}/../{file_name}"):
        dll_path = f"{os.path.abspath(os.path.dirname(__file__))}/../{file_name}"
    else:
        LogError(f"{file_name} not found")
        return None
    return dll_path

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

SDLFunc = DLL(get_depsPath("SDL2.dll")).bindFunction
GFXFunc = DLL(get_depsPath("SDL2_gfx.dll")).bindFunction
IMAGEFunc = DLL(get_depsPath("SDL2_image.dll")).bindFunction
MIXERFunc = DLL(get_depsPath("SDL2_mixer.dll")).bindFunction
TTFFunc = DLL(get_depsPath("SDL2_ttf.dll")).bindFunction

if None in (SDLFunc(None), GFXFunc(None), IMAGEFunc(None), MIXERFunc(None), TTFFunc(None)):
    LogCritical(f"Error when importing SDL2 libraries", "MGE dependencies not found. Run 'MGE deps install' to install them")
