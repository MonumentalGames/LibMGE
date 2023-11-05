import ctypes

__all__ = ["MousePress", "MouseRelease", "MouseClick", "MouseScroll",
           "KeyboardPress", "KeyboardRelease", "KeyboardClick"]

_MouseEvent = {1: [0x0002, 0x0004], 2: [0x0020, 0x0040], 3: [0x0008, 0x0010], 4: [0x0002, 0x0004], 5: [0x0002, 0x0004]}
_KeyboardEvent = {}

def MousePress(button):
    pass

def MouseRelease(button):
    pass

def MouseClick(button):
    pass

def MouseScroll(scroll):
    pass

def KeyboardPress(key):
    pass

def KeyboardRelease(key):
    pass

def KeyboardClick(key):
    pass
