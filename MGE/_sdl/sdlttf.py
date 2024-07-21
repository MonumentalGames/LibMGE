from ctypes import c_int, c_uint, c_long, c_char_p, c_void_p, byref, POINTER as _P
from .dll import DLL, find_path
try:
    from .sdl2 import Uint16, Uint32, SDL_RWops, SDL_version, SDL_Color, SDL_Surface
except:
    pass

TTFFunc = DLL(find_path("SDL2_ttf.dll")).bind_function

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

hb_direction_t = c_int
HB_DIRECTION_INVALID = 0
HB_DIRECTION_LTR = 4
HB_DIRECTION_RTL = 5
HB_DIRECTION_TTB = 6
HB_DIRECTION_BTT = 7

class TTF_Font(c_void_p):
    pass

def TTF_Linked_Version(): return TTFFunc("TTF_Linked_Version", None, _P(SDL_version))().contents
def TTF_GetFreeTypeVersion(major, minor, patch): return TTFFunc("TTF_GetFreeTypeVersion", [_P(c_int), _P(c_int), _P(c_int)])(major, minor, patch)

def TTF_Init(): return TTFFunc("TTF_Init", None, c_int)()
def TTF_WasInit(): return TTFFunc("TTF_WasInit", None, c_int)()
def TTF_Quit(): return TTFFunc("TTF_Quit")()

def TTF_OpenFont(file, ptsize): return TTFFunc("TTF_OpenFont", [c_char_p, c_int], _P(TTF_Font))(file.encode(), ptsize)
def TTF_OpenFontDPI(file, ptsize, hdpi, vdpi): return TTFFunc("TTF_OpenFontDPI", [c_char_p, c_int, c_uint, c_uint], _P(TTF_Font))(file, ptsize, hdpi, vdpi)
def TTF_OpenFontRW(src, freesrc, ptsize): return TTFFunc("TTF_OpenFontRW", [_P(SDL_RWops), c_int, c_int], _P(TTF_Font))(src, freesrc, ptsize)
def TTF_OpenFontDPIRW(src, freesrc, ptsize, hdpi, vdpi): return TTFFunc("TTF_OpenFontDPIRW", [_P(SDL_RWops), c_int, c_int, c_uint, c_uint], returns=_P(TTF_Font))(src, freesrc, ptsize, hdpi, vdpi)
def TTF_CloseFont(font): return TTFFunc("TTF_CloseFont", [_P(TTF_Font)])(font)

def TTF_SetFontSize(font, ptsize): return TTFFunc("TTF_SetFontSize", [_P(TTF_Font), c_int], c_int)(font, ptsize)
def TTF_SetFontSizeDPI(font, ptsize, hdpi, vdpi): return TTFFunc("TTF_SetFontSizeDPI", [_P(TTF_Font), c_int, c_uint, c_uint], c_int)(font, ptsize, hdpi, vdpi)

def TTF_GetFontStyle(font): return TTFFunc("TTF_GetFontStyle", [_P(TTF_Font)], c_int)(font)
def TTF_SetFontStyle(font, style): return TTFFunc("TTF_SetFontStyle", [_P(TTF_Font), c_int], None)(font, style)

def TTF_GetFontOutline(font): return TTFFunc("TTF_GetFontOutline", [_P(TTF_Font)], c_int)(font)
def TTF_SetFontOutline(font, outline): return TTFFunc("TTF_SetFontOutline", [_P(TTF_Font), c_int], None)(font, outline)

def TTF_FontHeight(font): return TTFFunc("TTF_FontHeight", [_P(TTF_Font)], c_int)(font)
def TTF_FontAscent(font): return TTFFunc("TTF_FontAscent", [_P(TTF_Font)], c_int)(font)
def TTF_FontDescent(font): return TTFFunc("TTF_FontDescent", [_P(TTF_Font)], c_int)(font)
def TTF_FontLineSkip(font): return TTFFunc("TTF_FontLineSkip", [_P(TTF_Font)], c_int)(font)

def TTF_GetFontKerning(font): return TTFFunc("TTF_GetFontKerning", [_P(TTF_Font)], c_int)(font)
def TTF_SetFontKerning(font, allowed): return TTFFunc("TTF_SetFontKerning", [_P(TTF_Font), c_int])(font, allowed)

def TTF_FontFaces(font): return TTFFunc("TTF_FontFaces", [_P(TTF_Font)], c_long)(font)
def TTF_FontFaceIsFixedWidth(font): return TTFFunc("TTF_FontFaceIsFixedWidth", [_P(TTF_Font)], c_int)(font)
def TTF_FontFaceFamilyName(font): return TTFFunc("TTF_FontFaceFamilyName", [_P(TTF_Font)], c_char_p)(font)
def TTF_FontFaceStyleName(font): return TTFFunc("TTF_FontFaceStyleName", [_P(TTF_Font)], c_char_p)(font)

def TTF_GlyphIsProvided(font, ch): return TTFFunc("TTF_GlyphIsProvided", [_P(TTF_Font), Uint16], c_int)(font, ch)
def TTF_GlyphIsProvided32(font, ch): return TTFFunc("TTF_GlyphIsProvided32", [_P(TTF_Font), Uint32], c_int)(font, ch)

def TTF_SizeText(font, text):
    w, h = c_long(0), c_long(0)
    TTFFunc("TTF_SizeText", [_P(TTF_Font), c_char_p, _P(c_int), _P(c_int)], c_int)(font, text, byref(w), byref(h))
    # return _ctypes["TTF_SizeText"](font, text, w, h)
    return w.value, h.value
def TTF_SizeUTF8(font, text):
    w, h = c_long(0), c_long(0)
    TTFFunc("TTF_SizeUTF8", [_P(TTF_Font), c_char_p, _P(c_int), _P(c_int)], c_int)(font, text, byref(w), byref(h))
    return w.value, h.value

def TTF_RenderText_Shaded(font, text, fg, bg): return TTFFunc("TTF_RenderText_Shaded", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color], returns=_P(SDL_Surface))(font, text, fg, bg)
def TTF_RenderUTF8_Shaded(font, text, fg, bg): return TTFFunc("TTF_RenderUTF8_Shaded", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color], returns=_P(SDL_Surface))(font, text, fg, bg)

def TTF_RenderText_Shaded_Wrapped(font, text, fg, bg, wrapLength): return TTFFunc("TTF_RenderText_Shaded_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color, Uint32], returns=_P(SDL_Surface))(font, text, fg, bg, wrapLength)
def TTF_RenderUTF8_Shaded_Wrapped(font, text, fg, bg, wrapLength): return TTFFunc("TTF_RenderUTF8_Shaded_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color, Uint32], returns=_P(SDL_Surface))(font, text, fg, bg, wrapLength)

def TTF_RenderText_Blended(font, text, fg): return TTFFunc("TTF_RenderText_Blended", [_P(TTF_Font), c_char_p, SDL_Color], _P(SDL_Surface))(font, text.encode(), fg).contents
def TTF_RenderUTF8_Blended(font, text, fg): return TTFFunc("TTF_RenderUTF8_Blended", [_P(TTF_Font), c_char_p, SDL_Color], _P(SDL_Surface))(font, text, fg)

def TTF_RenderText_Blended_Wrapped(font, text, fg, wrapLength): return TTFFunc("TTF_RenderText_Blended_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, Uint32], returns=_P(SDL_Surface))(font, text, fg, wrapLength)
def TTF_RenderUTF8_Blended_Wrapped(font, text, fg, wrapLength): return TTFFunc("TTF_RenderUTF8_Blended_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, Uint32], returns=_P(SDL_Surface))(font, text, fg, wrapLength)

def TTF_SetScript(script): return TTFFunc("TTF_SetScript", [c_int], c_int)(script)
def TTF_SetDirection(direction): return TTFFunc("TTF_SetDirection", [c_int], c_int)(direction)
def TTF_SetFontDirection(font, direction): return TTFFunc("TTF_SetFontDirection", [_P(TTF_Font), TTF_Direction], c_int)(font, direction)

def TTF_SetFontScriptName(font, script): return TTFFunc("TTF_SetFontScriptName", [_P(TTF_Font), c_char_p], c_int)(font, script)
def TTF_GetFontKerningSize(font, prev_index, index): return TTFFunc("TTF_GetFontKerningSize", [_P(TTF_Font), c_int, c_int], c_int)(font, prev_index, index)
