from ctypes import c_int, c_uint, c_long, c_char_p, c_void_p, byref, POINTER as _P
from .dll import DLL, find_path
from .sdl2 import Uint16, Uint32, SDL_bool, SDL_RWops, SDL_version, SDL_Color, SDL_Surface

class SDLFuncCache(object):
    def __init__(self, name, args=None, returns=None, added=None):
        self.name = name
        self.args = args
        self.returns = returns
        self.added = added

dll = DLL(find_path("SDL2_ttf.dll"))
TTFFunc = dll.bind_function

TTF_STYLE_NORMAL = 0x00
TTF_STYLE_BOLD = 0x01
TTF_STYLE_ITALIC = 0x02
TTF_STYLE_UNDERLINE = 0x04
TTF_STYLE_STRIKETHROUGH = 0x08

TTF_Direction = c_int
TTF_DIRECTION_LTR = 0
TTF_DIRECTION_RTL = 1
TTF_DIRECTION_TTB = 2
TTF_DIRECTION_BTT = 3

# Some additional definitions from HarfBuzz for SetDirection/SetScript
hb_direction_t = c_int
HB_DIRECTION_INVALID = 0
HB_DIRECTION_LTR = 4
HB_DIRECTION_RTL = 5
HB_DIRECTION_TTB = 6
HB_DIRECTION_BTT = 7

class TTF_Font(c_void_p):
    pass

_funcdefs = [
    SDLFuncCache("TTF_OpenFontIndex", [c_char_p, c_int, c_long], _P(TTF_Font)),
    SDLFuncCache("TTF_OpenFontRW", [_P(SDL_RWops), c_int, c_int], _P(TTF_Font)),
    SDLFuncCache("TTF_OpenFontIndexRW", [_P(SDL_RWops), c_int, c_int, c_long], _P(TTF_Font)),
    SDLFuncCache("TTF_OpenFontDPI", [c_char_p, c_int, c_uint, c_uint], _P(TTF_Font)),
    SDLFuncCache("TTF_OpenFontIndexDPI", [c_char_p, c_int, c_long, c_uint, c_uint], returns=_P(TTF_Font)),
    SDLFuncCache("TTF_OpenFontDPIRW", [_P(SDL_RWops), c_int, c_int, c_uint, c_uint], returns=_P(TTF_Font)),
    SDLFuncCache("TTF_OpenFontIndexDPIRW", [_P(SDL_RWops), c_int, c_int, c_long, c_uint, c_uint], returns=_P(TTF_Font)),
    SDLFuncCache("TTF_SetFontSize", [_P(TTF_Font), c_int], c_int),
    SDLFuncCache("TTF_SetFontSizeDPI", [_P(TTF_Font), c_int, c_uint, c_uint], c_int),
    SDLFuncCache("TTF_GetFontStyle", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_SetFontStyle", [_P(TTF_Font), c_int], None),
    SDLFuncCache("TTF_GetFontOutline", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_SetFontOutline", [_P(TTF_Font), c_int], None),
    SDLFuncCache("TTF_GetFontHinting", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_SetFontHinting", [_P(TTF_Font), c_int], None),
    SDLFuncCache("TTF_GetFontWrappedAlign", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_SetFontWrappedAlign", [_P(TTF_Font), c_int], None),
    SDLFuncCache("TTF_FontHeight", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_FontAscent", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_FontDescent", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_FontLineSkip", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_GetFontKerning", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_SetFontKerning", [_P(TTF_Font), c_int]),
    SDLFuncCache("TTF_FontFaces", [_P(TTF_Font)], c_long),
    SDLFuncCache("TTF_FontFaceIsFixedWidth", [_P(TTF_Font)], c_int),
    SDLFuncCache("TTF_FontFaceFamilyName", [_P(TTF_Font)], c_char_p),
    SDLFuncCache("TTF_FontFaceStyleName", [_P(TTF_Font)], c_char_p),
    SDLFuncCache("TTF_GlyphIsProvided", [_P(TTF_Font), Uint16], c_int),
    SDLFuncCache("TTF_GlyphIsProvided32", [_P(TTF_Font), Uint32], c_int),
    SDLFuncCache("TTF_SizeText", [_P(TTF_Font), c_char_p, _P(c_int), _P(c_int)], c_int),
    SDLFuncCache("TTF_SizeUTF8", [_P(TTF_Font), c_char_p, _P(c_int), _P(c_int)], c_int),
    SDLFuncCache("TTF_RenderText_Shaded", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color], returns=_P(SDL_Surface)),
    SDLFuncCache("TTF_RenderUTF8_Shaded", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color], returns=_P(SDL_Surface)),
    SDLFuncCache("TTF_RenderText_Shaded_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color, Uint32], returns=_P(SDL_Surface)),
    SDLFuncCache("TTF_RenderUTF8_Shaded_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color, Uint32], returns=_P(SDL_Surface)),
    SDLFuncCache("TTF_RenderText_Blended", [_P(TTF_Font), c_char_p, SDL_Color], _P(SDL_Surface)),
    SDLFuncCache("TTF_RenderUTF8_Blended", [_P(TTF_Font), c_char_p, SDL_Color], _P(SDL_Surface)),
    SDLFuncCache("TTF_RenderText_Blended_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, Uint32], returns=_P(SDL_Surface)),
    SDLFuncCache("TTF_RenderUTF8_Blended_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, Uint32], returns=_P(SDL_Surface)),
    SDLFuncCache("TTF_SetDirection", [c_int], c_int),
    SDLFuncCache("TTF_SetScript", [c_int], c_int),
    SDLFuncCache("TTF_SetFontDirection", [_P(TTF_Font), TTF_Direction], c_int),
    SDLFuncCache("TTF_SetFontScriptName", [_P(TTF_Font), c_char_p], c_int),
    SDLFuncCache("TTF_GetFontKerningSize", [_P(TTF_Font), c_int, c_int], c_int),
]
_ctypes = {}
for f in _funcdefs:
    _ctypes[f.name] = TTFFunc(f.name, f.args, f.returns)

def TTF_Linked_Version():
    return TTFFunc("TTF_Linked_Version", None, _P(SDL_version))().contents

def TTF_GetFreeTypeVersion(major, minor, patch):
    return TTFFunc("TTF_GetFreeTypeVersion", [_P(c_int), _P(c_int), _P(c_int)])(major, minor, patch)

def TTF_Init():
    return TTFFunc("TTF_Init", None, c_int)()

def TTF_WasInit():
    return TTFFunc("TTF_WasInit", None, c_int)()

def TTF_Quit():
    return TTFFunc("TTF_Quit")()


def TTF_OpenFont(file, ptsize):
    return TTFFunc("TTF_OpenFont", [c_char_p, c_int], _P(TTF_Font))(file.encode(), ptsize)

def TTF_CloseFont(font):
    return TTFFunc("TTF_CloseFont", [_P(TTF_Font)])(font)

def TTF_OpenFontRW(src, freesrc, ptsize):
    return _ctypes["TTF_OpenFontRW"](src, freesrc, ptsize)



def TTF_SetFontSize(font, ptsize):
    return _ctypes["TTF_SetFontSize"](font, ptsize)


def TTF_GetFontStyle(font):
    return _ctypes["TTF_GetFontStyle"](font)

def TTF_SetFontStyle(font, style):
    return _ctypes["TTF_SetFontStyle"](font, style)

def TTF_GetFontOutline(font):
    return _ctypes["TTF_GetFontOutline"](font)

def TTF_SetFontOutline(font, outline):
    return _ctypes["TTF_SetFontOutline"](font, outline)


def TTF_FontHeight(font):
    return _ctypes["TTF_FontHeight"](font)

def TTF_FontAscent(font):
    return _ctypes["TTF_FontAscent"](font)

def TTF_FontDescent(font):
    return _ctypes["TTF_FontDescent"](font)

def TTF_FontLineSkip(font):
    return _ctypes["TTF_FontLineSkip"](font)

def TTF_GetFontKerning(font):
    return _ctypes["TTF_GetFontKerning"](font)

def TTF_SetFontKerning(font, allowed):
    return _ctypes["TTF_SetFontKerning"](font, allowed)

def TTF_FontFaces(font):
    return _ctypes["TTF_FontFaces"](font)

def TTF_FontFaceIsFixedWidth(font):
    return _ctypes["TTF_FontFaceIsFixedWidth"](font)

def TTF_FontFaceFamilyName(font):
    return _ctypes["TTF_FontFaceFamilyName"](font)

def TTF_FontFaceStyleName(font):
    return _ctypes["TTF_FontFaceStyleName"](font)

def TTF_GlyphIsProvided(font, ch):
    return _ctypes["TTF_GlyphIsProvided"](font, ch)

def TTF_GlyphIsProvided32(font, ch):
    return _ctypes["TTF_GlyphIsProvided32"](font, ch)


def TTF_SizeText(font, text, w, h):
    return _ctypes["TTF_SizeText"](font, text, w, h)

def TTF_SizeUTF8(font, text):
    w, h = c_long(0), c_long(0)
    _ctypes["TTF_SizeUTF8"](font, text, byref(w), byref(h))
    return w.value, h.value

def TTF_RenderText_Shaded(font, text, fg, bg):
    return _ctypes["TTF_RenderText_Shaded"](font, text, fg, bg)

def TTF_RenderUTF8_Shaded(font, text, fg, bg):
    return _ctypes["TTF_RenderUTF8_Shaded"](font, text, fg, bg)

def TTF_RenderText_Shaded_Wrapped(font, text, fg, bg, wrapLength):
    return _ctypes["TTF_RenderText_Shaded_Wrapped"](font, text, fg, bg, wrapLength)

def TTF_RenderUTF8_Shaded_Wrapped(font, text, fg, bg, wrapLength):
    return _ctypes["TTF_RenderUTF8_Shaded_Wrapped"](font, text, fg, bg, wrapLength)


def TTF_RenderText_Blended(font, text, fg):
    return _ctypes["TTF_RenderText_Blended"](font, text.encode(), fg).contents

def TTF_RenderUTF8_Blended(font, text, fg):
    return _ctypes["TTF_RenderUTF8_Blended"](font, text, fg)

def TTF_RenderText_Blended_Wrapped(font, text, fg, wrapLength):
    return _ctypes["TTF_RenderText_Blended_Wrapped"](font, text, fg, wrapLength)

def TTF_RenderUTF8_Blended_Wrapped(font, text, fg, wrapLength):
    return _ctypes["TTF_RenderUTF8_Blended_Wrapped"](font, text, fg, wrapLength)


def TTF_SetScript(script):
    return _ctypes["TTF_SetScript"](script)

def TTF_SetFontDirection(font, direction):
    return _ctypes["TTF_SetFontDirection"](font, direction)

def TTF_SetFontScriptName(font, script):
    return _ctypes["TTF_SetFontScriptName"](font, script)

def TTF_GetFontKerningSize(font, prev_index, index):
    return _ctypes["TTF_GetFontKerningSize"](font, prev_index, index)

