import pygame

Key_Map = {
    "all": -1,
    "1": 49,
    "2": 50,
    "3": 51,
    "4": 52,
    "5": 53,
    "6": 54,
    "7": 55,
    "8": 56,
    "9": 57,
    "0": 48,
    "a": 97,
    "b": 98,
    "c": 99,
    "d": 100,
    "e": 101,
    "f": 102,
    "g": 103,
    "h": 104,
    "i": 105,
    "j": 106,
    "k": 107,
    "l": 108,
    "m": 109,
    "n": 110,
    "o": 111,
    "p": 112,
    "q": 113,
    "r": 114,
    "s": 115,
    "t": 116,
    "u": 117,
    "v": 118,
    "w": 119,
    "x": 120,
    "y": 121,
    "z": 122,
    "esc": 27,
    "back": 8,
    "up": 273,
    "down": 274,
    "left": 276,
    "right": 275,
    "space": 32,
    "return": 13,
    "shift": (1073742049, 1073742053),
    "left_shift": 1073742049,
    "right_shift": 1073742053,
    "ctrl": 306,
    "left_ctrl": 306,
    "right_ctrl": 305,
    "alt": 308,
    "left_alt": 308,
    "right_alt": 307,
    "f1": 1073741882,
    "f2": 1073741883,
    "f3": 1073741884,
    "f4": 1073741885,
    "f5": 1073741886,
    "f6": 1073741887,
    "f7": 1073741888,
    "f8": 1073741889,
    "f9": 1073741890,
    "f10": 1073741891,
    "f11": 1073741892,
    "f12": 1073741893
}

def keyboard(key):
    key = str(key).lower()
    event_key = pygame.key.get_pressed()

    if key == "all":
        return any(event_key)

    if key in Key_Map:
        if isinstance(Key_Map[key], int):
            return event_key[Key_Map[key]]
        else:
            return any(event_key[k] for k in Key_Map[key])

    return False
