import ctypes

user32 = ctypes.windll.user32

__all__ = ["MousePress", "MouseRelease", "MouseClick", "MouseScroll",
           "KeyboardPress", "KeyboardRelease", "KeyboardClick"]

_MouseEvent = {1: [0x0002, 0x0004], 2: [0x0020, 0x0040], 3: [0x0008, 0x0010], 4: [0x0002, 0x0004], 5: [0x0002, 0x0004]}
_KeyboardEvent = {}

def MousePress(button):
    button = 1 if button == -1 else button
    user32.mouse_event(_MouseEvent[button][0])

def MouseRelease(button):
    button = 1 if button == -1 else button
    user32.mouse_event(_MouseEvent[button][1])

def MouseClick(button):
    MousePress(button)
    MouseRelease(button)

def MouseScroll(scroll):
    user32.mouse_event(0x0800, 0, 0, scroll, 0)

def KeyboardPress(key):
    user32.keybd_event(key, user32.MapVirtualKeyA(key, 0), 0x0000 | 0x0001, 0)

def KeyboardRelease(key):
    user32.keybd_event(key, user32.MapVirtualKeyA(key, 0), 0x0002 | 0x0001, 0)

def KeyboardClick(key):
    KeyboardPress(key)
    KeyboardRelease(key)
