import os
from ctypes import CDLL

from ..Log import LogError, LogCritical

def NullFunction(*args):
    return

def find_path(file_name: str | list):
    file_name = file_name if type(file_name) == str else file_name[0]
    if os.path.exists(f"{os.path.abspath('./')}/{file_name}"):
        dll_path = os.path.abspath(f'./{file_name}')
    elif os.path.exists(f"{os.path.abspath(os.path.dirname(__file__))}/../{file_name}"):
        dll_path = f"{os.path.abspath(os.path.dirname(__file__))}/../{file_name}"
    else:
        LogCritical(f"{file_name} not found", "", 1)
    return dll_path

class DLL(object):
    def __init__(self, path=None):
        self._dll = None if path is None else CDLL(path)

    def bind_function(self, func_name, args=None, returns=None):
        if self._dll is None:
            return NullFunction
        else:
            func = getattr(self._dll, func_name, None)
            if not func:
                LogError(f"{func_name}")
                return NullFunction
            func.argtypes, func.restype = args, returns
            return func
