from ctypes import c_int, POINTER as _P
from .dll import DLL, find_path
try:
    from .sdl2 import Uint8, Sint16, SDL_Renderer, SDL_Surface
except:
    pass

GFXFunc = DLL(find_path("SDL2_gfx.dll")).bind_function

def pixelRGBA(renderer, x, y, r, g, b, a): return GFXFunc("pixelRGBA", [_P(SDL_Renderer), Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, r, g, b, a)

def rectangleRGBA(renderer, x1, y1, x2, y2, r, g, b, a): return GFXFunc("rectangleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x1, y1, x2, y2, r, g, b, a)
def roundedRectangleRGBA(renderer, x1, y1, x2, y2, rad, r, g, b, a): return GFXFunc("roundedRectangleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x1, y1, x2, y2, rad, r, g, b, a)

def boxRGBA(renderer, x1, y1, x2, y2, r, g, b, a): return GFXFunc("boxRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x1, y1, x2, y2, r, g, b, a)
def roundedBoxRGBA(renderer, x1, y1, x2, y2, rad, r, g, b, a): return GFXFunc("roundedBoxRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x1, y1, x2, y2, rad, r, g, b, a)

def lineRGBA(renderer, x1, y1, x2, y2, r, g, b, a): return GFXFunc("lineRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x1, y1, x2, y2, r, g, b, a)
def aalineRGBA(renderer, x1, y1, x2, y2, r, g, b, a): return GFXFunc("aalineRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x1, y1, x2, y2, r, g, b, a)
def thickLineRGBA(renderer, x1, y1, x2, y2, width, r, g, b, a): return GFXFunc("thickLineRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x1, y1, x2, y2, width, r, g, b, a)

def circleRGBA(renderer, x, y, rad, r, g, b, a): return GFXFunc("circleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rad, r, g, b, a)
def arcRGBA(renderer, x, y, rad, start, end, r, g, b, a): return GFXFunc("arcRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rad, start, end, r, g, b, a)
def aacircleRGBA(renderer, x, y, rad, r, g, b, a): return GFXFunc("aacircleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rad, r, g, b, a)
def filledCircleRGBA(renderer, x, y, rad, r, g, b, a): return GFXFunc("filledCircleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rad, r, g, b, a)

def ellipseRGBA(renderer, x, y, rx, ry, r, g, b, a): return GFXFunc("ellipseRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rx, ry, r, g, b, a)
def aaellipseRGBA(renderer, x, y, rx, ry, r, g, b, a): return GFXFunc("aaellipseRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rx, ry, r, g, b, a)
def filledEllipseRGBA(renderer, x, y, rx, ry, r, g, b, a): return GFXFunc("filledEllipseRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rx, ry, r, g, b, a)

def pieRGBA(renderer, x, y, rad, start, end, r, g, b, a): return GFXFunc("pieRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rad, start, end, r, g, b, a)
def filledPieRGBA(renderer, x, y, rad, start, end, r, g, b, a): return GFXFunc("filledPieRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, x, y, rad, start, end, r, g, b, a)

def polygonRGBA(renderer, vx, vy, n, r, g, b, a): return GFXFunc("polygonRGBA", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, vx, vy, n, r, g, b, a)
def aapolygonRGBA(renderer, vx, vy, n, r, g, b, a): return GFXFunc("aapolygonRGBA", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, vx, vy, n, r, g, b, a)
def filledPolygonRGBA(renderer, vx, vy, n, r, g, b, a): return GFXFunc("filledPolygonRGBA", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int)(renderer, vx, vy, n, r, g, b, a)
def texturedPolygon(renderer, vx, vy, n, texture, texture_dx, texture_dy): return GFXFunc("texturedPolygon", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, _P(SDL_Surface), c_int, c_int], c_int)(renderer, vx, vy, n, texture, texture_dx, texture_dy)

def rotateSurface90Degrees(src, num) -> SDL_Surface: return GFXFunc("rotateSurface90Degrees", [_P(SDL_Surface), c_int], _P(SDL_Surface))(src, num)
