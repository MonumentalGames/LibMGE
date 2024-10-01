from .Common import _temp, AllEvents
from .Constants import All

__all__ = ["keyboard", "KeyboardText", "KeyboardClick", "KeyboardState"]

def KeyboardText() -> str:
    for ev in AllEvents():
        if ev.type == 771:
            return ev.text.text.decode()

def KeyboardClick() -> int:
    for ev in AllEvents():
        if ev.type == 768:
            return ev.key.keysym.sym

def KeyboardState(key=All) -> bool | list:
    if key == -1:
        return _temp.KeyboardState
    if 0 < key < 500:
        return bool(_temp.KeyboardState[key])
    return False

def keyboard(key: int | list, multiple_click=False) -> bool | list:
    if key == -1:
        if any(KeyboardState(-1)):
            return True
        return False
    key = [key] if type(key) == int else key
    for k in key:
        if KeyboardState(k):
            if _temp.KeyboardCache[k] or multiple_click:
                _temp.KeyboardCache[k] = False
                return True
        else:
            _temp.KeyboardCache[k] = True
