from ctypes import Structure, c_int, c_char_p, POINTER as _P
from .dll import DLL, find_path
try:
    from .sdl2 import SDL_version, SDL_RWops, SDL_Surface, SDL_Texture, SDL_Renderer
except:
    pass

IMAGEFunc = DLL(find_path("SDL2_image.dll")).bind_function

class IMG_Animation(Structure):
    _fields_ = [("w", c_int), ("h", c_int), ("count", c_int), ("frames", _P(_P(SDL_Surface))), ("delays", _P(c_int))]

def IMG_Linked_Version(): return IMAGEFunc("IMG_Linked_Version", None, _P(SDL_version))()

def IMG_Init(flags=0): return IMAGEFunc("IMG_Init", [c_int], c_int)(flags)
def IMG_Quit(): IMAGEFunc("IMG_Quit")()

def IMG_Load(file): return IMAGEFunc("IMG_Load", [c_char_p], _P(SDL_Surface))(file)
def IMG_Load_RW(file): return IMAGEFunc("IMG_Load_RW", [_P(SDL_RWops)], _P(SDL_Surface))(file)
def IMG_LoadTexture(renderer: SDL_Renderer, file): IMAGEFunc("IMG_LoadTexture", [_P(SDL_Renderer), c_char_p], _P(SDL_Texture))(renderer, file)

def IMG_isAVIF(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isAVIF", [_P(SDL_RWops)], c_int)(src))
def IMG_isICO(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isICO", [_P(SDL_RWops)], c_int)(src))
def IMG_isCUR(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isCUR", [_P(SDL_RWops)], c_int)(src))
def IMG_isBMP(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isBMP", [_P(SDL_RWops)], c_int)(src))
def IMG_isGIF(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isGIF", [_P(SDL_RWops)], c_int)(src))
def IMG_isJPG(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isJPG", [_P(SDL_RWops)], c_int)(src))
def IMG_isJXL(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isJXL", [_P(SDL_RWops)], c_int)(src))
def IMG_isLBM(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isLBM", [_P(SDL_RWops)], c_int)(src))
def IMG_isPCX(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isPCX", [_P(SDL_RWops)], c_int)(src))
def IMG_isPNG(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isPNG", [_P(SDL_RWops)], c_int)(src))
def IMG_isPNM(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isPNM", [_P(SDL_RWops)], c_int)(src))
def IMG_isSVG(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isSVG", [_P(SDL_RWops)], c_int)(src))
def IMG_isQOI(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isQOI", [_P(SDL_RWops)], c_int)(src))
def IMG_isTIF(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isTIF", [_P(SDL_RWops)], c_int)(src))
def IMG_isXCF(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isXCF", [_P(SDL_RWops)], c_int)(src))
def IMG_isXPM(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isXPM", [_P(SDL_RWops)], c_int)(src))
def IMG_isXV(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isXV", [_P(SDL_RWops)], c_int)(src))
def IMG_isWEBP(src: SDL_RWops) -> bool: return bool(IMAGEFunc("IMG_isWEBP", [_P(SDL_RWops)], c_int)(src))

def IMG_LoadAVIF_RW(src): return IMAGEFunc("IMG_LoadAVIF_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadICO_RW(src): return IMAGEFunc("IMG_LoadICO_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadCUR_RW(src): return IMAGEFunc("IMG_LoadCUR_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadBMP_RW(src): return IMAGEFunc("IMG_LoadBMP_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadGIF_RW(src): return IMAGEFunc("IMG_LoadGIF_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadJPG_RW(src): return IMAGEFunc("IMG_LoadJPG_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadJXL_RW(src): return IMAGEFunc("IMG_LoadJXL_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadLBM_RW(src): return IMAGEFunc("IMG_LoadLBM_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadPCX_RW(src): return IMAGEFunc("IMG_LoadPCX_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadPNG_RW(src): return IMAGEFunc("IMG_LoadPNG_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadPNM_RW(src): return IMAGEFunc("IMG_LoadPNM_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadSVG_RW(src): return IMAGEFunc("IMG_LoadSVG_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadQOI_RW(src): return IMAGEFunc("IMG_LoadQOI_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadTGA_RW(src): return IMAGEFunc("IMG_LoadTGA_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadTIF_RW(src): return IMAGEFunc("IMG_LoadTIF_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadXCF_RW(src): return IMAGEFunc("IMG_LoadXCF_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadXPM_RW(src): return IMAGEFunc("IMG_LoadXPM_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadXV_RW(src): return IMAGEFunc("IMG_LoadXV_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)
def IMG_LoadWEBP_RW(src): return IMAGEFunc("IMG_LoadWEBP_RW", [_P(SDL_RWops)], _P(SDL_Surface))(src)

def IMG_LoadSizedSVG_RW(src, width, height): return IMAGEFunc("IMG_LoadSizedSVG_RW", [_P(SDL_RWops), c_int, c_int], _P(SDL_Surface))(src, width, height)

def IMG_ReadXPMFromArray(xpm): return IMAGEFunc("IMG_ReadXPMFromArray", [_P(c_char_p)], _P(SDL_Surface))(xpm)
def IMG_ReadXPMFromArrayToRGB888(xpm): return IMAGEFunc("IMG_ReadXPMFromArrayToRGB888", [_P(c_char_p)], _P(SDL_Surface))(xpm)

def IMG_SavePNG(surface, file): return IMAGEFunc("IMG_SavePNG", [_P(SDL_Surface), c_char_p], c_int)(surface, file)
def IMG_SaveJPG(surface, file, quality): return IMAGEFunc("IMG_SaveJPG", [_P(SDL_Surface), c_char_p, c_int], c_int)(surface, file, quality)
# NOTE: Not available in official macOS binaries

def IMG_LoadAnimation(file): return IMAGEFunc("IMG_LoadAnimation", [c_char_p], _P(IMG_Animation))(file)
def IMG_LoadAnimation_RW(src): return IMAGEFunc("IMG_LoadAnimation_RW", [_P(SDL_RWops), c_int], _P(IMG_Animation))(src, 1)
def IMG_FreeAnimation(anim): return IMAGEFunc("IMG_FreeAnimation", [_P(IMG_Animation)])(anim)
