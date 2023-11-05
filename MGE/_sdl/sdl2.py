import sys
from ctypes import *
from ctypes import POINTER as _P
from .dll import DLL, find_path

Sint8 = c_int8
Uint8 = c_uint8
Sint16 = c_int16
Uint16 = c_uint16
Sint32 = c_int32
Uint32 = c_uint32
Sint64 = c_int64
Uint64 = c_uint64

SDL_bool = c_int
SDL_FALSE = 0
SDL_TRUE = 1

SDL_LIL_ENDIAN = 1234
SDL_BIG_ENDIAN = 4321
SDL_BYTEORDER = SDL_LIL_ENDIAN if sys.byteorder == "little" else SDL_BIG_ENDIAN

dll = DLL(find_path("SDL2.dll"))
SDLFunc = dll.bind_function

SDLFunc("SDL_SetMainReady")()

SDL_INIT_TIMER = 0x00000001
SDL_INIT_AUDIO = 0x00000010
SDL_INIT_VIDEO = 0x00000020
SDL_INIT_JOYSTICK = 0x00000200
SDL_INIT_HAPTIC = 0x00001000
SDL_INIT_GAMECONTROLLER = 0x00002000
SDL_INIT_EVENTS = 0x00004000
SDL_INIT_SENSOR = 0x00008000
SDL_INIT_NOPARACHUTE = 0x00100000
SDL_INIT_EVERYTHING = (SDL_INIT_TIMER | SDL_INIT_AUDIO | SDL_INIT_VIDEO | SDL_INIT_EVENTS | SDL_INIT_JOYSTICK | SDL_INIT_HAPTIC | SDL_INIT_GAMECONTROLLER | SDL_INIT_SENSOR)

SDL_Init = SDLFunc("SDL_Init", [c_uint32], c_int)
SDL_InitSubSystem = SDLFunc("SDL_InitSubSystem", [c_uint32], c_int)
SDL_QuitSubSystem = SDLFunc("SDL_QuitSubSystem", [c_uint32])
SDL_WasInit = SDLFunc("SDL_WasInit", [c_uint32], c_uint32)
SDL_Quit = SDLFunc("SDL_Quit")

class SDL_version(Structure):
    _fields_ = [("major", Uint8), ("minor", Uint8), ("patch", Uint8)]

def SDL_GetVersion() -> SDL_version:
    version = SDL_version()
    SDLFunc("SDL_GetVersion", [_P(SDL_version)])(version)
    return version

SDL_GetRevision = SDLFunc("SDL_GetRevision", None, c_char_p)

def SDL_GetPlatform():
    return SDLFunc("SDL_GetPlatform", None, c_char_p)().decode()

SDL_LOG_PRIORITY_INFO = 3
SDL_LOG_PRIORITY_WARN = 4
SDL_LOG_PRIORITY_ERROR = 5
SDL_LOG_PRIORITY_CRITICAL = 6

def SDL_LogMessage(priority, msg):
    SDLFunc("SDL_LogMessage", [c_int, c_int, c_char_p])(0, priority if 3 <= priority <= 6 else 3, msg.encode())

SDL_MESSAGEBOX_ERROR = 0x00000010
SDL_MESSAGEBOX_WARNING = 0x00000020
SDL_MESSAGEBOX_INFORMATION = 0x00000040

def SDL_ShowSimpleMessageBox(flags, title, msg):
    return SDLFunc("SDL_ShowSimpleMessageBox", [Uint32, c_char_p, c_char_p, c_char_p], c_int)(flags, title.encode(), msg.encode(), None)

HWND = c_void_p
HDC = c_void_p
HINSTANCE = c_void_p

class _wininfo(Structure):
    _fields_ = [("window", HWND), ("hdc", HDC), ("hinstance", HINSTANCE)]

class _winrtinfo(Structure):
    _fields_ = [("window", c_void_p)]

class _x11info(Structure):
    """Window information for X11."""
    _fields_ = [("display", c_void_p), ("window", c_ulong)]

class _dfbinfo(Structure):
    _fields_ = [("dfb", c_void_p), ("window", c_void_p), ("surface", c_void_p)]

class _cocoainfo(Structure):
    _fields_ = [("window", c_void_p)]

class _uikitinfo(Structure):
    _fields_ = [("window", c_void_p), ("framebuffer", Uint32), ("colorbuffer", Uint32), ("resolveFramebuffer", Uint32)]

class _wl(Structure):
    _fields_ = [("display", c_void_p), ("surface", c_void_p), ("shell_surface", c_void_p), ("egl_window", c_void_p),
                ("xdg_surface", c_void_p), ("xdg_toplevel", c_void_p), ("xdg_popup", c_void_p), ("xdg_positioner", c_void_p)]

class _mir(Structure):
    _fields_ = [("connection", c_void_p), ("surface", c_void_p)]

class _android(Structure):
    _fields_ = [("window", c_void_p), ("surface", c_void_p)]

class _os2(Structure):
    _fields_ = [("hwnd", HWND), ("hwndFrame", HWND)]

class _vivante(Structure):
    _fields_ = [("display", c_void_p), ("window", c_void_p)]

class _kmsdrm(Structure):
    _fields_ = [("dev_index", c_int), ("drm_fd", c_int), ("gbm_dev", c_void_p)]

class _info(Union):
    _fields_ = [("win", _wininfo), ("winrt", _winrtinfo), ("x11", _x11info), ("dfb", _dfbinfo), ("cocoa", _cocoainfo), ("uikit", _uikitinfo),
                ("wl", _wl), ("mir", _mir), ("android", _android), ("os2", _os2), ("vivante", _vivante), ("kmsdrm", _kmsdrm), ("dummy", (Uint8 * 64))]

class SDL_SysWMinfo(Structure):
    _fields_ = [("version", SDL_version), ("subsystem", c_int), ("info", _info)]

class _hidden(Union):
    pass

class SDL_RWops(Structure):
    pass

SDL_RWops._fields_ = [("size", CFUNCTYPE(Sint64, _P(SDL_RWops))),
                      ("seek", CFUNCTYPE(Sint64, _P(SDL_RWops), Sint64, c_int)),
                      ("read", CFUNCTYPE(c_size_t, _P(SDL_RWops), c_void_p, c_size_t, c_size_t)),
                      ("write", CFUNCTYPE(c_size_t, _P(SDL_RWops), c_void_p, c_size_t, c_size_t)),
                      ("close", CFUNCTYPE(c_int, _P(SDL_RWops))),
                      ("type", Uint32), ("hidden", _hidden)]

SDL_RWFromFile = SDLFunc("SDL_RWFromFile", [c_char_p, c_char_p], _P(SDL_RWops))

SDL_PowerState = c_int
SDL_POWERSTATE_UNKNOWN = 0
SDL_POWERSTATE_ON_BATTERY = 1
SDL_POWERSTATE_NO_BATTERY = 2
SDL_POWERSTATE_CHARGING = 3
SDL_POWERSTATE_CHARGED = 4

def SDL_GetPowerInfo():
    seconds, percent = c_int(), c_int()
    ret = SDLFunc("SDL_GetPowerInfo", [_P(c_int), _P(c_int)], SDL_PowerState)(byref(seconds), byref(percent))
    seconds, percent = seconds.value, percent.value
    return seconds if seconds >= 0 else None, percent if percent >= 0 else None, ret

class SDL_Locale(Structure):
    _fields_ = [("_language", c_char_p), ("_country", c_char_p)]

    @property
    def language(self):
        return self._language.decode() if self._language is not None else self._language

    @property
    def country(self):
        return self._country.decode() if self._country is not None else self._country

def SDL_GetPreferredLocales():
    locales = []
    loc_size = sizeof(SDL_Locale)
    p = SDLFunc("SDL_GetPreferredLocales", None, c_void_p)()
    while True:
        loc = cast(p, _P(SDL_Locale))
        if not loc or loc.contents.language is None:
            break
        locales.append(loc.contents)
        p = p + loc_size
    return locales

SDL_SetClipboardText = SDLFunc("SDL_SetClipboardText", [c_char_p], c_int)
SDL_GetClipboardText = SDLFunc("SDL_GetClipboardText", None, c_char_p)
SDL_HasClipboardText = SDLFunc("SDL_HasClipboardText", None, SDL_bool)

SDL_OpenURL = SDLFunc("SDL_OpenURL", [c_char_p], c_int)

# -- audio --
AUDIO_U16LSB = 0x0010
AUDIO_S16LSB = 0x8010
AUDIO_U16MSB = 0x1010
AUDIO_S16MSB = 0x9010
AUDIO_S32LSB = 0x8020
AUDIO_S32MSB = 0x9020
AUDIO_F32LSB = 0x8120
AUDIO_F32MSB = 0x9120

AUDIO_U16SYS = AUDIO_U16LSB if SDL_BYTEORDER == SDL_LIL_ENDIAN else AUDIO_U16MSB
AUDIO_S16SYS = AUDIO_S16LSB if SDL_BYTEORDER == SDL_LIL_ENDIAN else AUDIO_S16MSB
AUDIO_S32SYS = AUDIO_S32LSB if SDL_BYTEORDER == SDL_LIL_ENDIAN else AUDIO_S32MSB
AUDIO_F32SYS = AUDIO_F32LSB if SDL_BYTEORDER == SDL_LIL_ENDIAN else AUDIO_F32MSB

SDL_MIX_MAXVOLUME = 128
SDL_AUDIOCVT_MAX_FILTERS = 9

# -- video --
class SDL_Point(Structure):
    _fields_ = [("x", c_int), ("y", c_int)]

    def __init__(self, x=0, y=0):
        super(SDL_Point, self).__init__()
        self.x, self.y = x, y

    def __repr__(self):
        return f"SDL_Point(x={self.x}, y={self.y})"

    def __copy__(self):
        return SDL_Point(self.x, self.y)

class SDL_FPoint(Structure):
    _fields_ = [("x", c_float), ("y", c_float)]

    def __init__(self, x=0.0, y=0.0):
        super(SDL_FPoint, self).__init__()
        self.x, self.y = x, y

    def __repr__(self):
        return f"SDL_FPoint(x={self.x}, y={self.y})"

    def __copy__(self):
        return SDL_FPoint(self.x, self.y)

class SDL_Rect(Structure):
    _fields_ = [("x", c_int), ("y", c_int), ("w", c_int), ("h", c_int)]

    def __init__(self, x=0, y=0, w=0, h=0):
        super(SDL_Rect, self).__init__()
        self.x, self.y, self.w, self.h = x, y, w, h

    def __repr__(self):
        return f"SDL_Rect(x={self.x}, y={self.y}, w={self.w}, h={self.h})"

    def __copy__(self):
        return SDL_Rect(self.x, self.y, self.w, self.h)

class SDL_FRect(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("w", c_float), ("h", c_float)]

    def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0):
        super(SDL_FRect, self).__init__()
        self.x, self.y, self.w, self.h = x, y, w, h

    def __repr__(self):
        return f"SDL_FRect(x={self.x}, y={self.y}, w={self.w}, h={self.h})"

    def __copy__(self):
        return SDL_FRect(self.x, self.y, self.w, self.h)

# pixels
SDL_PIXELTYPE_ARRAYU8 = 7
SDL_PIXELTYPE_PACKED16 = 5
SDL_PIXELTYPE_PACKED32 = 6

SDL_PACKEDORDER_ARGB = 3
SDL_PACKEDORDER_RGBA = 4

SDL_ARRAYORDER_RGB = 1
SDL_PACKEDLAYOUT_4444 = 2
SDL_PACKEDLAYOUT_8888 = 6

def SDL_DEFINE_PIXELFORMAT(ptype, order, layout, bits, pbytes):
    return (1 << 28) | (ptype << 24) | (order << 20) | (layout << 16) | (bits << 8) | (pbytes << 0)

SDL_PIXELFORMAT_RGB24 = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_ARRAYU8, SDL_ARRAYORDER_RGB, 0, 24, 3)
SDL_PIXELFORMAT_ARGB4444 = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_ARGB, SDL_PACKEDLAYOUT_4444, 16, 2)
SDL_PIXELFORMAT_RGBA4444 = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_RGBA, SDL_PACKEDLAYOUT_4444, 16, 2)
SDL_PIXELFORMAT_ARGB8888 = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_ARGB, SDL_PACKEDLAYOUT_8888, 32, 4)
SDL_PIXELFORMAT_RGBA8888 = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_RGBA, SDL_PACKEDLAYOUT_8888, 32, 4)

class SDL_Color(Structure):
    _fields_ = [("r", Uint8), ("g", Uint8), ("b", Uint8), ("a", Uint8)]
    def __init__(self, r=255, g=255, b=255, a=255):
        super(SDL_Color, self).__init__()
        self.r, self.g, self.b, self.a = r, g, b, a

    def __repr__(self):
        return "SDL_Color(r=%d, g=%d, b=%d, a=%d)" % (self.r, self.g, self.b, self.a)

    def __copy__(self):
        return SDL_Color(self.r, self.g, self.b, self.a)

class SDL_Palette(Structure):
    _fields_ = [("ncolors", c_int), ("colors", _P(SDL_Color)), ("version", Uint32), ("refcount", c_int)]

class SDL_PixelFormat(Structure):
    pass

SDL_PixelFormat._fields_ = [
    ("format", Uint32), ("palette", _P(SDL_Palette)), ("BitsPerPixel", Uint8), ("BytesPerPixel", Uint8), ("padding", Uint8 * 2),
    ("Rmask", Uint32), ("Gmask", Uint32), ("Bmask", Uint32), ("Amask", Uint32), ("Rloss", Uint8), ("Gloss", Uint8), ("Bloss", Uint8),
    ("Aloss", Uint8), ("Rshift", Uint8), ("Gshift", Uint8), ("Bshift", Uint8), ("Ashift", Uint8), ("refcount", c_int), ("next", _P(SDL_PixelFormat))]

SDL_AllocFormat = SDLFunc("SDL_AllocFormat", [Uint32], _P(SDL_PixelFormat))
SDL_FreeFormat = SDLFunc("SDL_FreeFormat", [_P(SDL_PixelFormat)])

# surface
class SDL_Surface(Structure):
    _fields_ = [("flags", Uint32), ("format", _P(SDL_PixelFormat)), ("w", c_int), ("h", c_int), ("pitch", c_int),
                ("pixels", c_void_p), ("userdata", c_void_p), ("list_blitmap", c_void_p), ("refcount", c_int)]

SDL_CreateRGBSurface = SDLFunc("SDL_CreateRGBSurface", [Uint32, c_int, c_int, c_int, Uint32, Uint32, Uint32, Uint32], returns=_P(SDL_Surface))
SDL_CreateRGBSurfaceWithFormat = SDLFunc("SDL_CreateRGBSurfaceWithFormat", [Uint32, c_int, c_int, c_int, Uint32], returns=_P(SDL_Surface))
SDL_CreateRGBSurfaceFrom = SDLFunc("SDL_CreateRGBSurfaceFrom", [c_void_p, c_int, c_int, c_int, c_int, Uint32, Uint32, Uint32, Uint32], returns=_P(SDL_Surface))
SDL_CreateRGBSurfaceWithFormatFrom = SDLFunc("SDL_CreateRGBSurfaceWithFormatFrom", [c_void_p, c_int, c_int, c_int, c_int, Uint32], returns=_P(SDL_Surface))

SDL_SetSurfaceColorMod = SDLFunc("SDL_SetSurfaceColorMod", [_P(SDL_Surface), Uint8, Uint8, Uint8], c_int)
SDL_GetSurfaceColorMod = SDLFunc("SDL_GetSurfaceColorMod", [_P(SDL_Surface), _P(Uint8), _P(Uint8), _P(Uint8)], c_int)
SDL_SetSurfaceAlphaMod = SDLFunc("SDL_SetSurfaceAlphaMod", [_P(SDL_Surface), Uint8], c_int)
SDL_GetSurfaceAlphaMod = SDLFunc("SDL_GetSurfaceAlphaMod", [_P(SDL_Surface), _P(Uint8)], c_int)

SDL_MapRGB = SDLFunc("SDL_MapRGB", [_P(SDL_PixelFormat), Uint8, Uint8, Uint8], Uint32)
SDL_MapRGBA = SDLFunc("SDL_MapRGBA", [_P(SDL_PixelFormat), Uint8, Uint8, Uint8, Uint8], Uint32)

SDL_FreeSurface = SDLFunc("SDL_FreeSurface", [_P(SDL_Surface)])
SDL_DuplicateSurface = SDLFunc("SDL_DuplicateSurface", [_P(SDL_Surface)], _P(SDL_Surface))
SDL_ConvertSurface = SDLFunc("SDL_ConvertSurface", [_P(SDL_Surface), _P(SDL_PixelFormat), Uint32], _P(SDL_Surface))
SDL_ConvertSurfaceFormat = SDLFunc("SDL_ConvertSurfaceFormat", [_P(SDL_Surface), Uint32, Uint32], _P(SDL_Surface))
SDL_FillRect = SDLFunc("SDL_FillRect", [_P(SDL_Surface), _P(SDL_Rect), Uint32], c_int)
SDL_UpperBlit = SDLFunc("SDL_UpperBlit", [_P(SDL_Surface), _P(SDL_Rect), _P(SDL_Surface), _P(SDL_Rect)], returns=c_int)
SDL_BlitSurface = SDL_UpperBlit
SDL_UpperBlitScaled = SDLFunc("SDL_UpperBlitScaled", [_P(SDL_Surface), _P(SDL_Rect), _P(SDL_Surface), _P(SDL_Rect)], returns=c_int)
SDL_BlitScaled = SDL_UpperBlitScaled

# Window
SDL_WindowFlags = c_int

SDL_WindowEventID = c_int

SDL_DisplayEventID = c_int
SDL_DISPLAYEVENT_NONE = 0
SDL_DISPLAYEVENT_ORIENTATION = 1
SDL_DISPLAYEVENT_CONNECTED = 2
SDL_DISPLAYEVENT_DISCONNECTED = 3

SDL_DisplayOrientation = c_int
SDL_ORIENTATION_UNKNOWN = 0
SDL_ORIENTATION_LANDSCAPE = 1
SDL_ORIENTATION_LANDSCAPE_FLIPPED = 2
SDL_ORIENTATION_PORTRAIT = 3
SDL_ORIENTATION_PORTRAIT_FLIPPED = 4

SDL_FlashOperation = c_int
SDL_FLASH_CANCEL = 0
SDL_FLASH_BRIEFLY = 1
SDL_FLASH_UNTIL_FOCUSED = 2

SDL_HitTestResult = c_int
SDL_HITTEST_NORMAL = 0
SDL_HITTEST_DRAGGABLE = 1
SDL_HITTEST_RESIZE_TOPLEFT = 2
SDL_HITTEST_RESIZE_TOP = 3
SDL_HITTEST_RESIZE_TOPRIGHT = 4
SDL_HITTEST_RESIZE_RIGHT = 5
SDL_HITTEST_RESIZE_BOTTOMRIGHT = 6
SDL_HITTEST_RESIZE_BOTTOM = 7
SDL_HITTEST_RESIZE_BOTTOMLEFT = 8
SDL_HITTEST_RESIZE_LEFT = 9

SDL_WINDOWPOS_UNDEFINED_MASK = 0x1FFF0000
SDL_WINDOWPOS_UNDEFINED_DISPLAY = lambda x: (SDL_WINDOWPOS_UNDEFINED_MASK | x)
SDL_WINDOWPOS_UNDEFINED = SDL_WINDOWPOS_UNDEFINED_DISPLAY(0)
SDL_WINDOWPOS_ISUNDEFINED = lambda x: ((x & 0xFFFF0000) == SDL_WINDOWPOS_UNDEFINED_MASK)

SDL_WINDOWPOS_CENTERED_MASK = 0x2FFF0000
SDL_WINDOWPOS_CENTERED_DISPLAY = lambda x: (SDL_WINDOWPOS_CENTERED_MASK | x)
SDL_WINDOWPOS_CENTERED = SDL_WINDOWPOS_CENTERED_DISPLAY(0)
SDL_WINDOWPOS_ISCENTERED = lambda x: ((x & 0xFFFF0000) == SDL_WINDOWPOS_CENTERED_MASK)

ShapeModeDefault = 0
ShapeModeBinarizeAlpha = 1
ShapeModeReverseBinarizeAlpha = 2
ShapeModeColorKey = 3

SDL_GLContext = c_void_p

SDL_GLattr = c_int
SDL_GL_RED_SIZE = 0
SDL_GL_GREEN_SIZE = 1
SDL_GL_BLUE_SIZE = 2
SDL_GL_ALPHA_SIZE = 3
SDL_GL_BUFFER_SIZE = 4
SDL_GL_DOUBLEBUFFER = 5
SDL_GL_DEPTH_SIZE = 6
SDL_GL_STENCIL_SIZE = 7
SDL_GL_ACCUM_RED_SIZE = 8
SDL_GL_ACCUM_GREEN_SIZE = 9
SDL_GL_ACCUM_BLUE_SIZE = 10
SDL_GL_ACCUM_ALPHA_SIZE = 11
SDL_GL_STEREO = 12
SDL_GL_MULTISAMPLEBUFFERS = 13
SDL_GL_MULTISAMPLESAMPLES = 14
SDL_GL_ACCELERATED_VISUAL = 15
SDL_GL_RETAINED_BACKING = 16
SDL_GL_CONTEXT_MAJOR_VERSION = 17
SDL_GL_CONTEXT_MINOR_VERSION = 18
SDL_GL_CONTEXT_EGL = 19
SDL_GL_CONTEXT_FLAGS = 20
SDL_GL_CONTEXT_PROFILE_MASK = 21
SDL_GL_SHARE_WITH_CURRENT_CONTEXT = 22
SDL_GL_FRAMEBUFFER_SRGB_CAPABLE = 23
SDL_GL_CONTEXT_RELEASE_BEHAVIOR = 24
SDL_GL_CONTEXT_RESET_NOTIFICATION = 25
SDL_GL_CONTEXT_NO_ERROR = 26
SDL_GL_FLOATBUFFERS = 27

class SDL_Window(c_void_p):
    pass

class SDL_DisplayMode(Structure):
    _fields_ = [("format", Uint32),
                ("w", c_int),
                ("h", c_int),
                ("refresh_rate", c_int),
                ("driverdata", c_void_p)
                ]

    def __init__(self, format_=0, w=0, h=0, refresh_rate=0):
        super(SDL_DisplayMode, self).__init__()
        self.format = format_
        self.w = w
        self.h = h
        self.refresh_rate = refresh_rate

    def __repr__(self):
        s = "SDL_DisplayMode({0}x{1} @ {2}Hz)"
        return s.format(self.w, self.h, self.refresh_rate)

    def __eq__(self, mode):
        return self.format == mode.format and self.w == mode.w and \
            self.h == mode.h and self.refresh_rate == mode.refresh_rate

    def __ne__(self, mode):
        return self.format != mode.format or self.w != mode.w or \
            self.h != mode.h or self.refresh_rate != mode.refresh_rate

class SDL_WindowShapeParams(Union):
    _fields_ = [("binarizationCutoff", Uint8), ("colorKey", SDL_Color)]

class SDL_WindowShapeMode(Structure):
    _fields_ = [("mode", c_int), ("parameters", SDL_WindowShapeParams)]

    def __init__(self, mode=ShapeModeDefault, parameters=SDL_WindowShapeParams()):
        super(SDL_WindowShapeMode, self).__init__()
        self.mode, self.parameters = mode, parameters

SDL_CreateShapedWindow = SDLFunc("SDL_CreateShapedWindow", [c_char_p, c_uint, c_uint, c_uint, c_uint, Uint32], returns=_P(SDL_Window))
SDL_IsShapedWindow = SDLFunc("SDL_IsShapedWindow", [_P(SDL_Window)], SDL_bool)
SDL_SetWindowShape = SDLFunc("SDL_SetWindowShape", [_P(SDL_Window), _P(SDL_Surface), _P(SDL_WindowShapeMode)], returns=c_int)
SDL_GetShapedWindowMode = SDLFunc("SDL_GetShapedWindowMode", [_P(SDL_Window), _P(SDL_WindowShapeMode)], c_int)
SDL_GetNumVideoDrivers = SDLFunc("SDL_GetNumVideoDrivers", None, c_int)
SDL_GetVideoDriver = SDLFunc("SDL_GetVideoDriver", [c_int], c_char_p)

def SDL_VideoInit(driver_name=None):
    return SDLFunc("SDL_VideoInit", [c_char_p], c_int)(driver_name)

def SDL_VideoQuit():
    SDLFunc("SDL_VideoQuit")()

SDL_GetCurrentVideoDriver = SDLFunc("SDL_GetCurrentVideoDriver", None, c_char_p)

def SDL_GetNumVideoDisplays() -> int:
    return SDLFunc("SDL_GetNumVideoDisplays", None, c_int)()

def SDL_GetDisplayName(display_index: int) -> str | None:
    ret = SDLFunc("SDL_GetDisplayName", [c_int], c_char_p)(display_index)
    if isinstance(ret, bytes):
        return ret.decode()
    return ret

SDL_GetDisplayBounds = SDLFunc("SDL_GetDisplayBounds", [c_int, _P(SDL_Rect)], c_int)
SDL_GetDisplayUsableBounds = SDLFunc("SDL_GetDisplayUsableBounds", [c_int, _P(SDL_Rect)], c_int)
SDL_GetDisplayDPI = SDLFunc("SDL_GetDisplayDPI", [c_int, _P(c_float), _P(c_float), _P(c_float)], returns=c_int)
SDL_GetDisplayOrientation = SDLFunc("SDL_GetDisplayOrientation", [c_int], SDL_DisplayOrientation)
SDL_GetNumDisplayModes = SDLFunc("SDL_GetNumDisplayModes", [c_int], c_int)

SDL_GetDisplayMode = SDLFunc("SDL_GetDisplayMode", [c_int, c_int, _P(SDL_DisplayMode)], c_int)

SDL_GetDesktopDisplayMode = SDLFunc("SDL_GetDesktopDisplayMode", [c_int, _P(SDL_DisplayMode)], c_int)

def SDL_GetCurrentDisplayMode(displayIndex: int, mode: SDL_DisplayMode | None = None) -> int | SDL_DisplayMode:
    if mode is None:
        mode = SDL_DisplayMode()
    er = SDLFunc("SDL_GetCurrentDisplayMode", [c_int, _P(SDL_DisplayMode)], c_int)(displayIndex, mode)
    return er if er < 0 else mode

SDL_GetClosestDisplayMode = SDLFunc("SDL_GetClosestDisplayMode", [c_int, _P(SDL_DisplayMode), _P(SDL_DisplayMode)], returns=_P(SDL_DisplayMode))
SDL_GetPointDisplayIndex = SDLFunc("SDL_GetPointDisplayIndex", [_P(SDL_Point)], c_int)
SDL_GetRectDisplayIndex = SDLFunc("SDL_GetRectDisplayIndex", [_P(SDL_Rect)], c_int)
SDL_GetWindowDisplayIndex = SDLFunc("SDL_GetWindowDisplayIndex", [_P(SDL_Window)], c_int)
SDL_SetWindowDisplayMode = SDLFunc("SDL_SetWindowDisplayMode", [_P(SDL_Window), _P(SDL_DisplayMode)], c_int)
SDL_GetWindowDisplayMode = SDLFunc("SDL_GetWindowDisplayMode", [_P(SDL_Window), _P(SDL_DisplayMode)], c_int)

def SDL_CreateWindow(title: str, x: int, y: int, w: int, h: int, flags) -> SDL_Window | None:
    return SDLFunc("SDL_CreateWindow", [c_char_p, c_int, c_int, c_int, c_int, Uint32], _P(SDL_Window))(title.encode() if type(title) == str else title, x, y, w, h, flags)

def SDL_GetWindowID(window: SDL_Window) -> int:
    return SDLFunc("SDL_GetWindowID", [_P(SDL_Window)], Uint32)(window)

SDL_GetWindowFromID = SDLFunc("SDL_GetWindowFromID", [Uint32], _P(SDL_Window))

SDL_GetWindowFlags = SDLFunc("SDL_GetWindowFlags", [_P(SDL_Window)], Uint32)

SDL_SetWindowTitle = SDLFunc("SDL_SetWindowTitle", [_P(SDL_Window), c_char_p])

def SDL_GetWindowTitle(window: SDL_Window):
    return SDLFunc("SDL_GetWindowTitle", [_P(SDL_Window)], c_char_p)(window).decode()

SDL_SetWindowIcon = SDLFunc("SDL_SetWindowIcon", [_P(SDL_Window), _P(SDL_Surface)])

SDL_SetWindowPosition = SDLFunc("SDL_SetWindowPosition", [_P(SDL_Window), c_int, c_int])
SDL_GetWindowPosition = SDLFunc("SDL_GetWindowPosition", [_P(SDL_Window), _P(c_int), _P(c_int)])

SDL_SetWindowSize = SDLFunc("SDL_SetWindowSize", [_P(SDL_Window), c_int, c_int])

def SDL_GetWindowSize(window: SDL_Window):
    w, h = c_int(), c_int()
    SDLFunc("SDL_GetWindowSize", [_P(SDL_Window), _P(c_int), _P(c_int)])(window, w, h)
    return w.value, h.value

SDL_SetWindowMinimumSize = SDLFunc("SDL_SetWindowMinimumSize", [_P(SDL_Window), c_int, c_int])
SDL_GetWindowMinimumSize = SDLFunc("SDL_GetWindowMinimumSize", [_P(SDL_Window), _P(c_int), _P(c_int)])
SDL_SetWindowMaximumSize = SDLFunc("SDL_SetWindowMaximumSize", [_P(SDL_Window), c_int, c_int])
SDL_GetWindowMaximumSize = SDLFunc("SDL_GetWindowMaximumSize", [_P(SDL_Window), _P(c_int), _P(c_int)])

SDL_SetWindowBordered = SDLFunc("SDL_SetWindowBordered", [_P(SDL_Window), SDL_bool])
SDL_SetWindowResizable = SDLFunc("SDL_SetWindowResizable", [_P(SDL_Window), SDL_bool])
SDL_SetWindowAlwaysOnTop = SDLFunc("SDL_SetWindowAlwaysOnTop", [_P(SDL_Window), SDL_bool])

SDL_SetWindowFullscreen = SDLFunc("SDL_SetWindowFullscreen", [_P(SDL_Window), Uint32], c_int)

SDL_ShowWindow = SDLFunc("SDL_ShowWindow", [_P(SDL_Window)])
SDL_HideWindow = SDLFunc("SDL_HideWindow", [_P(SDL_Window)])

# oi
SDL_RaiseWindow = SDLFunc("SDL_RaiseWindow", [_P(SDL_Window)])

SDL_MaximizeWindow = SDLFunc("SDL_MaximizeWindow", [_P(SDL_Window)])
SDL_MinimizeWindow = SDLFunc("SDL_MinimizeWindow", [_P(SDL_Window)])

SDL_RestoreWindow = SDLFunc("SDL_RestoreWindow", [_P(SDL_Window)])

def SDL_GetWindowOpacity(window: SDL_Window):
    opacity = c_float()
    SDLFunc("SDL_GetWindowOpacity", [_P(SDL_Window), _P(c_float)], c_int)(window, opacity)
    return opacity.value

SDL_SetWindowOpacity = SDLFunc("SDL_SetWindowOpacity", [_P(SDL_Window), c_float], c_int)

SDL_GetWindowSurface = SDLFunc("SDL_GetWindowSurface", [_P(SDL_Window)], _P(SDL_Surface))

SDL_SetWindowInputFocus = SDLFunc("SDL_SetWindowInputFocus", [_P(SDL_Window)], c_int)

SDL_FlashWindow = SDLFunc("SDL_FlashWindow", [_P(SDL_Window), SDL_FlashOperation], c_int)
SDL_DestroyWindow = SDLFunc("SDL_DestroyWindow", [_P(SDL_Window)])

SDL_IsScreenSaverEnabled = SDLFunc("SDL_IsScreenSaverEnabled", None, SDL_bool)
SDL_EnableScreenSaver = SDLFunc("SDL_EnableScreenSaver")
SDL_DisableScreenSaver = SDLFunc("SDL_DisableScreenSaver")

SDL_GetWindowWMInfo = SDLFunc("SDL_GetWindowWMInfo", [_P(SDL_Window), _P(SDL_SysWMinfo)], SDL_bool)

SDL_GL_LoadLibrary = SDLFunc("SDL_GL_LoadLibrary", [c_char_p], c_int)
SDL_GL_GetProcAddress = SDLFunc("SDL_GL_GetProcAddress", [c_char_p], c_void_p)
SDL_GL_UnloadLibrary = SDLFunc("SDL_GL_UnloadLibrary")
SDL_GL_ExtensionSupported = SDLFunc("SDL_GL_ExtensionSupported", [c_char_p], SDL_bool)
SDL_GL_ResetAttributes = SDLFunc("SDL_GL_ResetAttributes")
SDL_GL_SetAttribute = SDLFunc("SDL_GL_SetAttribute", [SDL_GLattr, c_int], c_int)
SDL_GL_GetAttribute = SDLFunc("SDL_GL_GetAttribute", [SDL_GLattr, _P(c_int)], c_int)
SDL_GL_CreateContext = SDLFunc("SDL_GL_CreateContext", [_P(SDL_Window)], SDL_GLContext)
SDL_GL_MakeCurrent = SDLFunc("SDL_GL_MakeCurrent", [_P(SDL_Window), SDL_GLContext], c_int)
SDL_GL_GetCurrentWindow = SDLFunc("SDL_GL_GetCurrentWindow", None, _P(SDL_Window))
SDL_GL_GetCurrentContext = SDLFunc("SDL_GL_GetCurrentContext", None, SDL_GLContext)
SDL_GL_GetDrawableSize = SDLFunc("SDL_GL_GetDrawableSize", [_P(SDL_Window), _P(c_int), _P(c_int)])
SDL_GL_SetSwapInterval = SDLFunc("SDL_GL_SetSwapInterval", [c_int], c_int)
SDL_GL_GetSwapInterval = SDLFunc("SDL_GL_GetSwapInterval", None, c_int)
SDL_GL_SwapWindow = SDLFunc("SDL_GL_SwapWindow", [_P(SDL_Window)])
SDL_GL_DeleteContext = SDLFunc("SDL_GL_DeleteContext", [SDL_GLContext])

# render
SDL_RendererFlags = c_int
SDL_RENDERER_SOFTWARE = 0x00000001
SDL_RENDERER_ACCELERATED = 0x00000002
SDL_RENDERER_PRESENTVSYNC = 0x00000004
SDL_RENDERER_TARGETTEXTURE = 0x00000008

SDL_ScaleMode = c_int
SDL_ScaleModeNearest = 0
SDL_ScaleModeLinear = 1
SDL_ScaleModeBest = 2

SDL_TextureAccess = c_int
SDL_TEXTUREACCESS_STATIC = 0
SDL_TEXTUREACCESS_STREAMING = 1
SDL_TEXTUREACCESS_TARGET = 2

SDL_TextureModulate = c_int
SDL_TEXTUREMODULATE_NONE = 0x00000000
SDL_TEXTUREMODULATE_COLOR = 0x00000001
SDL_TEXTUREMODULATE_ALPHA = 0x00000002

SDL_RendererFlip = c_int
SDL_FLIP_NONE = 0x00000000
SDL_FLIP_HORIZONTAL = 0x00000001
SDL_FLIP_VERTICAL = 0x00000002

class SDL_RendererInfo(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("flags", Uint32),
        ("num_texture_formats", Uint32),
        ("texture_formats", Uint32 * 16),
        ("max_texture_width", c_int),
        ("max_texture_height", c_int),
    ]

class SDL_Renderer(c_void_p):
    pass

class SDL_Texture(c_void_p):
    pass

SDL_GetNumRenderDrivers = SDLFunc("SDL_GetNumRenderDrivers", None, c_int)
SDL_GetRenderDriverInfo = SDLFunc("SDL_GetRenderDriverInfo", [c_int, _P(SDL_RendererInfo)], c_int)
SDL_CreateWindowAndRenderer = SDLFunc("SDL_CreateWindowAndRenderer", [c_int, c_int, Uint32, _P(_P(SDL_Window)), _P(_P(SDL_Renderer))], returns=c_int)

SDL_CreateRenderer = SDLFunc("SDL_CreateRenderer", [_P(SDL_Window), c_int, Uint32], _P(SDL_Renderer))
SDL_CreateSoftwareRenderer = SDLFunc("SDL_CreateSoftwareRenderer", [_P(SDL_Surface)], _P(SDL_Renderer))

SDL_GetRenderer = SDLFunc("SDL_GetRenderer", [_P(SDL_Window)], _P(SDL_Renderer))
SDL_RenderGetWindow = SDLFunc("SDL_RenderGetWindow", [_P(SDL_Renderer)], _P(SDL_Window))

SDL_SetRenderTarget = SDLFunc("SDL_SetRenderTarget", [_P(SDL_Renderer), _P(SDL_Texture)], c_int)
SDL_GetRenderTarget = SDLFunc("SDL_GetRenderTarget", [_P(SDL_Renderer)], _P(SDL_Texture))

SDL_GetRendererInfo = SDLFunc("SDL_GetRendererInfo", [_P(SDL_Renderer), _P(SDL_RendererInfo)], c_int)
SDL_GetRendererOutputSize = SDLFunc("SDL_GetRendererOutputSize", [_P(SDL_Renderer), _P(c_int), _P(c_int)], c_int)
SDL_CreateTexture = SDLFunc("SDL_CreateTexture", [_P(SDL_Renderer), Uint32, c_int, c_int, c_int], _P(SDL_Texture))
SDL_CreateTextureFromSurface = SDLFunc("SDL_CreateTextureFromSurface", [_P(SDL_Renderer), _P(SDL_Surface)], _P(SDL_Texture))

def SDL_QueryTexture(texture: SDL_Texture):
    flags = Uint32()
    access, w, h = (c_int(), c_int(), c_int())
    ret = SDLFunc("SDL_QueryTexture", [_P(SDL_Texture), _P(Uint32), _P(c_int), _P(c_int), _P(c_int)], returns=c_int)(texture, byref(flags), byref(access), byref(w), byref(h))
    if ret < 0:
        return None
    return flags.value, access.value, w.value, h.value

SDL_SetTextureColorMod = SDLFunc("SDL_SetTextureColorMod", [_P(SDL_Texture), Uint8, Uint8, Uint8], c_int)
SDL_GetTextureColorMod = SDLFunc("SDL_GetTextureColorMod", [_P(SDL_Texture), _P(Uint8), _P(Uint8), _P(Uint8)], c_int)
SDL_SetTextureAlphaMod = SDLFunc("SDL_SetTextureAlphaMod", [_P(SDL_Texture), Uint8], c_int)
SDL_GetTextureAlphaMod = SDLFunc("SDL_GetTextureAlphaMod", [_P(SDL_Texture), _P(Uint8)], c_int)
SDL_SetTextureScaleMode = SDLFunc("SDL_SetTextureScaleMode", [_P(SDL_Texture), SDL_ScaleMode], returns=c_int)
SDL_GetTextureScaleMode = SDLFunc("SDL_GetTextureScaleMode", [_P(SDL_Texture), _P(SDL_ScaleMode)], returns=c_int)
SDL_UpdateTexture = SDLFunc("SDL_UpdateTexture", [_P(SDL_Texture), _P(SDL_Rect), c_void_p, c_int], c_int)
SDL_UpdateYUVTexture = SDLFunc("SDL_UpdateYUVTexture", [_P(SDL_Texture), _P(SDL_Rect), _P(Uint8), c_int, _P(Uint8), c_int, _P(Uint8), c_int], returns=c_int)
SDL_UpdateNVTexture = SDLFunc("SDL_UpdateNVTexture", [_P(SDL_Texture), _P(SDL_Rect), _P(Uint8), c_int, _P(Uint8), c_int], returns=c_int)
SDL_RenderSetLogicalSize = SDLFunc("SDL_RenderSetLogicalSize", [_P(SDL_Renderer), c_int, c_int], c_int)
SDL_RenderGetLogicalSize = SDLFunc("SDL_RenderGetLogicalSize", [_P(SDL_Renderer), _P(c_int), _P(c_int)])
SDL_RenderSetViewport = SDLFunc("SDL_RenderSetViewport", [_P(SDL_Renderer), _P(SDL_Rect)], c_int)
SDL_RenderGetViewport = SDLFunc("SDL_RenderGetViewport", [_P(SDL_Renderer), _P(SDL_Rect)])
SDL_RenderSetScale = SDLFunc("SDL_RenderSetScale", [_P(SDL_Renderer), c_float, c_float], c_int)
SDL_RenderGetScale = SDLFunc("SDL_RenderGetScale", [_P(SDL_Renderer), _P(c_float), _P(c_float)])
SDL_SetRenderDrawColor = SDLFunc("SDL_SetRenderDrawColor", [_P(SDL_Renderer), Uint8, Uint8, Uint8, Uint8], c_int)
SDL_GetRenderDrawColor = SDLFunc("SDL_GetRenderDrawColor", [_P(SDL_Renderer), _P(Uint8), _P(Uint8), _P(Uint8), _P(Uint8)], returns=c_int)

SDL_RenderReadPixels = SDLFunc("SDL_RenderReadPixels", [_P(SDL_Renderer), _P(SDL_Rect), Uint32, c_void_p, c_int], returns=c_int)

SDL_RenderClear = SDLFunc("SDL_RenderClear", [_P(SDL_Renderer)], c_int)
SDL_RenderCopy = SDLFunc("SDL_RenderCopy", [_P(SDL_Renderer), _P(SDL_Texture), _P(SDL_Rect), _P(SDL_Rect)], returns=c_int)
SDL_RenderCopyExF = SDLFunc("SDL_RenderCopyExF", args=[_P(SDL_Renderer), _P(SDL_Texture), _P(SDL_Rect), _P(SDL_FRect), c_double, _P(SDL_FPoint), SDL_RendererFlip], returns=c_int)
SDL_RenderPresent = SDLFunc("SDL_RenderPresent", [_P(SDL_Renderer)])
SDL_DestroyTexture = SDLFunc("SDL_DestroyTexture", [_P(SDL_Texture)])
SDL_DestroyRenderer = SDLFunc("SDL_DestroyRenderer", [_P(SDL_Renderer)])
SDL_RenderSetVSync = SDLFunc("SDL_RenderSetVSync", [_P(SDL_Renderer), c_int], c_int)

# -- events --
# touch
SDL_TouchDeviceType = c_int
SDL_TOUCH_DEVICE_INVALID = -1,
SDL_TOUCH_DEVICE_DIRECT = 0
SDL_TOUCH_DEVICE_INDIRECT_ABSOLUTE = 1
SDL_TOUCH_DEVICE_INDIRECT_RELATIVE = 2

SDL_TOUCH_MOUSEID = 2**32 - 1  # defined as ((Uint32)-1), hope this is right
SDL_MOUSE_TOUCHID = 2**63 - 1  # defined as ((Sint64)-1), hope this is right

SDL_TouchID = Sint64
SDL_FingerID = Sint64
SDL_GestureID = Sint64

class SDL_Finger(Structure):
    _fields_ = [("id", SDL_FingerID), ("x", c_float), ("y", c_float), ("pressure", c_float)]

SDL_GetNumTouchDevices = SDLFunc("SDL_GetNumTouchDevices", None, c_int)
SDL_GetTouchDevice = SDLFunc("SDL_GetTouchDevice", [c_int], SDL_TouchID)
SDL_GetTouchName = SDLFunc("SDL_GetTouchName", [c_int], c_char_p)
SDL_GetTouchDeviceType = SDLFunc("SDL_GetTouchDeviceType", [SDL_TouchID], SDL_TouchDeviceType)
SDL_GetNumTouchFingers = SDLFunc("SDL_GetNumTouchFingers", [SDL_TouchID], c_int)
SDL_GetTouchFinger = SDLFunc("SDL_GetTouchFinger", [SDL_TouchID, c_int], _P(SDL_Finger))

SDL_RecordGesture = SDLFunc("SDL_RecordGesture", [SDL_TouchID], c_int)
SDL_SaveAllDollarTemplates = SDLFunc("SDL_SaveAllDollarTemplates", [_P(SDL_RWops)], c_int)
SDL_SaveDollarTemplate = SDLFunc("SDL_SaveDollarTemplate", [SDL_GestureID, _P(SDL_RWops)], c_int)
SDL_LoadDollarTemplates = SDLFunc("SDL_LoadDollarTemplates", [SDL_TouchID, _P(SDL_RWops)], c_int)

# keyboard
SDL_Scancode = c_int
SDL_Keycode = Sint32

SDL_GetKeyboardFocus = SDLFunc("SDL_GetKeyboardFocus", None, _P(SDL_Window))
SDL_GetKeyboardState = SDLFunc("SDL_GetKeyboardState", [_P(c_int)], _P(Uint8))

SDL_GetScancodeName = SDLFunc("SDL_GetScancodeName", [SDL_Scancode], c_char_p)
SDL_GetScancodeFromName = SDLFunc("SDL_GetScancodeFromName", [c_char_p], SDL_Scancode)

SDL_GetKeyName = SDLFunc("SDL_GetKeyName", [SDL_Keycode], c_char_p)
SDL_GetKeyFromName = SDLFunc("SDL_GetKeyFromName", [c_char_p], SDL_Keycode)
SDL_IsTextInputShown = SDLFunc("SDL_IsTextInputShown", None, SDL_bool)
SDL_SetTextInputRect = SDLFunc("SDL_SetTextInputRect", [_P(SDL_Rect)])

# mouse
SDL_MouseWheelDirection = c_int
SDL_MOUSEWHEEL_NORMAL = 0
SDL_MOUSEWHEEL_FLIPPED = 1

SDL_BUTTON = lambda X: (1 << ((X) - 1))
SDL_BUTTON_LEFT = 1
SDL_BUTTON_MIDDLE = 2
SDL_BUTTON_RIGHT = 3
SDL_BUTTON_X1 = 4
SDL_BUTTON_X2 = 5
SDL_BUTTON_LMASK = SDL_BUTTON(SDL_BUTTON_LEFT)
SDL_BUTTON_MMASK = SDL_BUTTON(SDL_BUTTON_MIDDLE)
SDL_BUTTON_RMASK = SDL_BUTTON(SDL_BUTTON_RIGHT)
SDL_BUTTON_X1MASK = SDL_BUTTON(SDL_BUTTON_X1)
SDL_BUTTON_X2MASK = SDL_BUTTON(SDL_BUTTON_X2)

class SDL_Cursor(c_void_p):
    pass

SDL_GetMouseFocus = SDLFunc("SDL_GetMouseFocus", None, _P(SDL_Window))
SDL_GetMouseState = SDLFunc("SDL_GetMouseState", [_P(c_int), _P(c_int)], Uint32)
SDL_GetRelativeMouseState = SDLFunc("SDL_GetRelativeMouseState", [_P(c_int), _P(c_int)], Uint32)
SDL_WarpMouseInWindow = SDLFunc("SDL_WarpMouseInWindow", [_P(SDL_Window), c_int, c_int])
SDL_CreateColorCursor = SDLFunc("SDL_CreateColorCursor", [_P(SDL_Surface), c_int, c_int], _P(SDL_Cursor))
SDL_CreateSystemCursor = SDLFunc("SDL_CreateSystemCursor", [c_int], _P(SDL_Cursor))
SDL_SetCursor = SDLFunc("SDL_SetCursor", [_P(SDL_Cursor)])
SDL_GetCursor = SDLFunc("SDL_GetCursor", None, _P(SDL_Cursor))
SDL_FreeCursor = SDLFunc("SDL_FreeCursor", [_P(SDL_Cursor)])
SDL_ShowCursor = SDLFunc("SDL_ShowCursor", [c_int], c_int)
SDL_CaptureMouse = SDLFunc("SDL_CaptureMouse", [SDL_bool], c_int)
SDL_GetGlobalMouseState = SDLFunc("SDL_GetGlobalMouseState", [_P(c_int), _P(c_int)], Uint32)
SDL_WarpMouseGlobal = SDLFunc("SDL_WarpMouseGlobal", [c_int, c_int], c_int)

# joystick
SDL_JoystickPowerLevel = c_int
SDL_JOYSTICK_POWER_UNKNOWN = -1
SDL_JOYSTICK_POWER_EMPTY = 0
SDL_JOYSTICK_POWER_LOW = 1
SDL_JOYSTICK_POWER_MEDIUM = 2
SDL_JOYSTICK_POWER_FULL = 3
SDL_JOYSTICK_POWER_WIRED = 4
SDL_JOYSTICK_POWER_MAX = 5

SDL_JoystickType = c_int
SDL_JOYSTICK_TYPE_UNKNOWN = 0
SDL_JOYSTICK_TYPE_GAMECONTROLLER = 1
SDL_JOYSTICK_TYPE_WHEEL = 2
SDL_JOYSTICK_TYPE_ARCADE_STICK = 3
SDL_JOYSTICK_TYPE_FLIGHT_STICK = 4
SDL_JOYSTICK_TYPE_DANCE_PAD = 5
SDL_JOYSTICK_TYPE_GUITAR = 6
SDL_JOYSTICK_TYPE_DRUM_KIT = 7
SDL_JOYSTICK_TYPE_ARCADE_PAD = 8
SDL_JOYSTICK_TYPE_THROTTLE = 9

SDL_IPHONE_MAX_GFORCE = 5.0

SDL_HAT_CENTERED = 0x00
SDL_HAT_UP = 0x01
SDL_HAT_RIGHT = 0x02
SDL_HAT_DOWN = 0x04
SDL_HAT_LEFT = 0x08
SDL_HAT_RIGHTUP = SDL_HAT_RIGHT | SDL_HAT_UP
SDL_HAT_RIGHTDOWN = SDL_HAT_RIGHT | SDL_HAT_DOWN
SDL_HAT_LEFTUP = SDL_HAT_LEFT | SDL_HAT_UP
SDL_HAT_LEFTDOWN = SDL_HAT_LEFT | SDL_HAT_DOWN

SDL_VIRTUAL_JOYSTICK_DESC_VERSION = 1

SDL_JoystickID = Sint32

CFUNC_Update = CFUNCTYPE(None, c_void_p)
CFUNC_SetPlayerIndex = CFUNCTYPE(None, c_void_p, c_int)
CFUNC_Rumble = CFUNCTYPE(c_int, c_void_p, Uint16, Uint16)
CFUNC_RumbleTriggers = CFUNCTYPE(c_int, c_void_p, Uint16, Uint16)
CFUNC_SetLED = CFUNCTYPE(c_int, c_void_p, Uint8, Uint8, Uint8)
CFUNC_SendEffect = CFUNCTYPE(c_int, c_void_p, c_void_p, c_int)

class SDL_JoystickGUID(Structure):
    _fields_ = [("data", (Uint8 * 16))]

class SDL_Joystick(c_void_p):
    pass

class SDL_VirtualJoystickDesc(Structure):
    _fields_ = [
        ("version", Uint16),
        ("type", Uint16),
        ("naxes", Uint16),
        ("nbuttons", Uint16),
        ("nhats", Uint16),
        ("vendor_id", Uint16),
        ("product_id", Uint16),
        ("padding", Uint16),
        ("button_mask", Uint32),
        ("axis_mask", Uint32),
        ("name", c_char_p),
        ("userdata", c_void_p),
        ("Update", CFUNC_Update),
        ("SetPlayerIndex", CFUNC_SetPlayerIndex),
        ("Rumble", CFUNC_Rumble),
        ("RumbleTriggers", CFUNC_RumbleTriggers),
        ("SetLED", CFUNC_SetLED),
        ("SendEffect", CFUNC_SendEffect),
    ]

SDL_LockJoysticks = SDLFunc("SDL_LockJoysticks", None, None)
SDL_UnlockJoysticks = SDLFunc("SDL_UnlockJoysticks", None, None)
SDL_NumJoysticks = SDLFunc("SDL_NumJoysticks", None, c_int)
SDL_JoystickNameForIndex = SDLFunc("SDL_JoystickNameForIndex", [c_int], c_char_p)
SDL_JoystickPathForIndex = SDLFunc("SDL_JoystickPathForIndex", [c_int], c_char_p)
SDL_JoystickGetDevicePlayerIndex = SDLFunc("SDL_JoystickGetDevicePlayerIndex", [c_int], c_int)
SDL_JoystickGetDeviceGUID = SDLFunc("SDL_JoystickGetDeviceGUID", [c_int], SDL_JoystickGUID)
SDL_JoystickGetDeviceVendor = SDLFunc("SDL_JoystickGetDeviceVendor", [c_int], Uint16)
SDL_JoystickGetDeviceProduct = SDLFunc("SDL_JoystickGetDeviceProduct", [c_int], Uint16)
SDL_JoystickGetDeviceProductVersion = SDLFunc("SDL_JoystickGetDeviceProductVersion", [c_int], Uint16)
SDL_JoystickGetDeviceType = SDLFunc("SDL_JoystickGetDeviceType", [c_int], SDL_JoystickType)
SDL_JoystickGetDeviceInstanceID = SDLFunc("SDL_JoystickGetDeviceInstanceID", [c_int], SDL_JoystickID)
SDL_JoystickOpen = SDLFunc("SDL_JoystickOpen", [c_int], _P(SDL_Joystick))
SDL_JoystickFromInstanceID = SDLFunc("SDL_JoystickFromInstanceID", [SDL_JoystickID], _P(SDL_Joystick))
SDL_JoystickFromPlayerIndex = SDLFunc("SDL_JoystickFromPlayerIndex", [c_int], _P(SDL_Joystick))
SDL_JoystickAttachVirtual = SDLFunc("SDL_JoystickAttachVirtual", [SDL_JoystickType, c_int, c_int, c_int], returns=c_int)
SDL_JoystickAttachVirtualEx = SDLFunc("SDL_JoystickAttachVirtualEx", [_P(SDL_VirtualJoystickDesc)], c_int)
SDL_JoystickDetachVirtual = SDLFunc("SDL_JoystickDetachVirtual", [c_int], c_int)
SDL_JoystickIsVirtual = SDLFunc("SDL_JoystickIsVirtual", [c_int], SDL_bool)
SDL_JoystickSetVirtualAxis = SDLFunc("SDL_JoystickSetVirtualAxis", [_P(SDL_Joystick), c_int, Sint16], returns=c_int)
SDL_JoystickSetVirtualButton = SDLFunc("SDL_JoystickSetVirtualButton", [_P(SDL_Joystick), c_int, Uint8], returns=c_int)
SDL_JoystickSetVirtualHat = SDLFunc("SDL_JoystickSetVirtualHat", [_P(SDL_Joystick), c_int, Uint8], c_int)
SDL_JoystickName = SDLFunc("SDL_JoystickName", [_P(SDL_Joystick)], c_char_p)
SDL_JoystickPath = SDLFunc("SDL_JoystickPath", [_P(SDL_Joystick)], c_char_p)
SDL_JoystickGetPlayerIndex = SDLFunc("SDL_JoystickGetPlayerIndex", [_P(SDL_Joystick)], c_int)
SDL_JoystickSetPlayerIndex = SDLFunc("SDL_JoystickSetPlayerIndex", [_P(SDL_Joystick), c_int])
SDL_JoystickGetGUID = SDLFunc("SDL_JoystickGetGUID", [_P(SDL_Joystick)], SDL_JoystickGUID)
SDL_JoystickGetVendor = SDLFunc("SDL_JoystickGetVendor", [_P(SDL_Joystick)], Uint16)
SDL_JoystickGetProduct = SDLFunc("SDL_JoystickGetProduct", [_P(SDL_Joystick)], Uint16)
SDL_JoystickGetProductVersion = SDLFunc("SDL_JoystickGetProductVersion", [_P(SDL_Joystick)], Uint16)
SDL_JoystickGetFirmwareVersion = SDLFunc("SDL_JoystickGetFirmwareVersion", [_P(SDL_Joystick)], Uint16)
SDL_JoystickGetSerial = SDLFunc("SDL_JoystickGetSerial", [_P(SDL_Joystick)], c_char_p)
SDL_JoystickGetType = SDLFunc("SDL_JoystickGetType", [_P(SDL_Joystick)], SDL_JoystickType)
SDL_JoystickGetGUIDFromString = SDLFunc("SDL_JoystickGetGUIDFromString", [c_char_p], SDL_JoystickGUID)
SDL_JoystickGetAttached = SDLFunc("SDL_JoystickGetAttached", [_P(SDL_Joystick)], SDL_bool)
SDL_JoystickInstanceID = SDLFunc("SDL_JoystickInstanceID", [_P(SDL_Joystick)], SDL_JoystickID)
SDL_JoystickNumAxes = SDLFunc("SDL_JoystickNumAxes", [_P(SDL_Joystick)], c_int)
SDL_JoystickNumBalls = SDLFunc("SDL_JoystickNumBalls", [_P(SDL_Joystick)], c_int)
SDL_JoystickNumHats = SDLFunc("SDL_JoystickNumHats", [_P(SDL_Joystick)], c_int)
SDL_JoystickNumButtons = SDLFunc("SDL_JoystickNumButtons", [_P(SDL_Joystick)], c_int)
SDL_JoystickUpdate = SDLFunc("SDL_JoystickUpdate")
SDL_JoystickEventState = SDLFunc("SDL_JoystickEventState", [c_int], c_int)
SDL_JoystickGetAxis = SDLFunc("SDL_JoystickGetAxis", [_P(SDL_Joystick), c_int], Sint16)
SDL_JoystickGetAxisInitialState = SDLFunc("SDL_JoystickGetAxisInitialState", [_P(SDL_Joystick), c_int, _P(Sint16)], returns=SDL_bool)
SDL_JoystickGetHat = SDLFunc("SDL_JoystickGetHat", [_P(SDL_Joystick), c_int], Uint8)
SDL_JoystickGetBall = SDLFunc("SDL_JoystickGetBall", [_P(SDL_Joystick), c_int, _P(c_int), _P(c_int)], c_int)
SDL_JoystickGetButton = SDLFunc("SDL_JoystickGetButton", [_P(SDL_Joystick), c_int], Uint8)
SDL_JoystickRumble = SDLFunc("SDL_JoystickRumble", [_P(SDL_Joystick), Uint16, Uint16, Uint32], returns=c_int)
SDL_JoystickRumbleTriggers = SDLFunc("SDL_JoystickRumbleTriggers", [_P(SDL_Joystick), Uint16, Uint16, Uint32], returns=c_int)
SDL_JoystickHasLED = SDLFunc("SDL_JoystickHasLED", [_P(SDL_Joystick)], SDL_bool)
SDL_JoystickHasRumble = SDLFunc("SDL_JoystickHasRumble", [_P(SDL_Joystick)], SDL_bool)
SDL_JoystickHasRumbleTriggers = SDLFunc("SDL_JoystickHasRumbleTriggers", [_P(SDL_Joystick)], SDL_bool)
SDL_JoystickSetLED = SDLFunc("SDL_JoystickSetLED", [_P(SDL_Joystick), Uint8, Uint8, Uint8], c_int)
SDL_JoystickSendEffect = SDLFunc("SDL_JoystickSendEffect", [_P(SDL_Joystick), c_void_p, c_int], c_int)
SDL_JoystickClose = SDLFunc("SDL_JoystickClose", [_P(SDL_Joystick)])
SDL_JoystickCurrentPowerLevel = SDLFunc("SDL_JoystickCurrentPowerLevel", [_P(SDL_Joystick)], returns=SDL_JoystickPowerLevel)

# controller
SDL_GameControllerBindType = c_int
SDL_CONTROLLER_BINDTYPE_NONE = 0
SDL_CONTROLLER_BINDTYPE_BUTTON = 1
SDL_CONTROLLER_BINDTYPE_AXIS = 2
SDL_CONTROLLER_BINDTYPE_HAT = 3

SDL_GameControllerType = c_int

SDL_GameControllerAxis = c_int
SDL_CONTROLLER_AXIS_INVALID = -1
SDL_CONTROLLER_AXIS_LEFTX = 0
SDL_CONTROLLER_AXIS_LEFTY = 1
SDL_CONTROLLER_AXIS_RIGHTX = 2
SDL_CONTROLLER_AXIS_RIGHTY = 3
SDL_CONTROLLER_AXIS_TRIGGERLEFT = 4
SDL_CONTROLLER_AXIS_TRIGGERRIGHT = 5
SDL_CONTROLLER_AXIS_MAX = 6

SDL_GameControllerButton = c_int

class _gchat(Structure):
    _fields_ = [("hat", c_int), ("hat_mask", c_int)]

class _gcvalue(Union):
    _fields_ = [("button", c_int), ("axis", c_int), ("hat", _gchat)]

class SDL_GameControllerButtonBind(Structure):
    _fields_ = [("bindType", SDL_GameControllerBindType), ("value", _gcvalue)]

class SDL_GameController(c_void_p):
    pass

SDL_GameControllerAddMappingsFromRW = SDLFunc("SDL_GameControllerAddMappingsFromRW", [_P(SDL_RWops), c_int], c_int)
SDL_GameControllerAddMappingsFromFile = lambda fname: SDL_GameControllerAddMappingsFromRW(SDL_RWFromFile(fname, b"rb"), 1)
SDL_GameControllerAddMapping = SDLFunc("SDL_GameControllerAddMapping", [c_char_p], c_int)
SDL_GameControllerNumMappings = SDLFunc("SDL_GameControllerNumMappings", None, c_int)
SDL_GameControllerMappingForIndex = SDLFunc("SDL_GameControllerMappingForIndex", [c_int], c_char_p)
SDL_GameControllerMapping = SDLFunc("SDL_GameControllerMapping", [_P(SDL_GameController)], c_char_p)
SDL_IsGameController = SDLFunc("SDL_IsGameController", [c_int], SDL_bool)
SDL_GameControllerNameForIndex = SDLFunc("SDL_GameControllerNameForIndex", [c_int], c_char_p)
SDL_GameControllerPathForIndex = SDLFunc("SDL_GameControllerPathForIndex", [c_int], c_char_p)
SDL_GameControllerTypeForIndex = SDLFunc("SDL_GameControllerTypeForIndex", [c_int], SDL_GameControllerType)
SDL_GameControllerMappingForDeviceIndex = SDLFunc("SDL_GameControllerMappingForDeviceIndex", [c_int], c_char_p)
SDL_GameControllerOpen = SDLFunc("SDL_GameControllerOpen", [c_int], _P(SDL_GameController))
SDL_GameControllerFromInstanceID = SDLFunc("SDL_GameControllerFromInstanceID", [SDL_JoystickID], returns=_P(SDL_GameController))
SDL_GameControllerFromPlayerIndex = SDLFunc("SDL_GameControllerFromPlayerIndex", [c_int], _P(SDL_GameController))
SDL_GameControllerName = SDLFunc("SDL_GameControllerName", [_P(SDL_GameController)], c_char_p)
SDL_GameControllerPath = SDLFunc("SDL_GameControllerPath", [_P(SDL_GameController)], c_char_p)
SDL_GameControllerGetType = SDLFunc("SDL_GameControllerGetType", [_P(SDL_GameController)], returns=SDL_GameControllerType)
SDL_GameControllerGetPlayerIndex = SDLFunc("SDL_GameControllerGetPlayerIndex", [_P(SDL_GameController)], c_int)
SDL_GameControllerSetPlayerIndex = SDLFunc("SDL_GameControllerSetPlayerIndex", [_P(SDL_GameController), c_int])
SDL_GameControllerGetVendor = SDLFunc("SDL_GameControllerGetVendor", [_P(SDL_GameController)], Uint16)
SDL_GameControllerGetProduct = SDLFunc("SDL_GameControllerGetProduct", [_P(SDL_GameController)], Uint16)
SDL_GameControllerGetProductVersion = SDLFunc("SDL_GameControllerGetProductVersion", [_P(SDL_GameController)], returns=Uint16)
SDL_GameControllerGetFirmwareVersion = SDLFunc("SDL_GameControllerGetFirmwareVersion", [_P(SDL_GameController)], returns=Uint16)
SDL_GameControllerGetSerial = SDLFunc("SDL_GameControllerGetSerial", [_P(SDL_GameController)], c_char_p)
SDL_GameControllerGetAttached = SDLFunc("SDL_GameControllerGetAttached", [_P(SDL_GameController)], SDL_bool)
SDL_GameControllerGetJoystick = SDLFunc("SDL_GameControllerGetJoystick", [_P(SDL_GameController)], _P(SDL_Joystick))
SDL_GameControllerEventState = SDLFunc("SDL_GameControllerEventState", [c_int], c_int)
SDL_GameControllerGetAxisFromString = SDLFunc("SDL_GameControllerGetAxisFromString", [c_char_p], SDL_GameControllerAxis)
SDL_GameControllerGetStringForAxis = SDLFunc("SDL_GameControllerGetStringForAxis", [SDL_GameControllerAxis], c_char_p)
SDL_GameControllerGetBindForAxis = SDLFunc("SDL_GameControllerGetBindForAxis", [_P(SDL_GameController), SDL_GameControllerAxis], returns=SDL_GameControllerButtonBind)
SDL_GameControllerHasAxis = SDLFunc("SDL_GameControllerHasAxis", [_P(SDL_GameController), SDL_GameControllerAxis], returns=SDL_bool)
SDL_GameControllerGetAxis = SDLFunc("SDL_GameControllerGetAxis", [_P(SDL_GameController), SDL_GameControllerAxis], Sint16)
SDL_GameControllerGetButtonFromString = SDLFunc("SDL_GameControllerGetButtonFromString", [c_char_p], SDL_GameControllerButton)
SDL_GameControllerGetStringForButton = SDLFunc("SDL_GameControllerGetStringForButton", [SDL_GameControllerButton], c_char_p)
SDL_GameControllerGetBindForButton = SDLFunc("SDL_GameControllerGetBindForButton", [_P(SDL_GameController), SDL_GameControllerButton], returns=SDL_GameControllerButtonBind)
SDL_GameControllerHasButton = SDLFunc("SDL_GameControllerHasButton", [_P(SDL_GameController), SDL_GameControllerButton], returns=SDL_bool)
SDL_GameControllerGetButton = SDLFunc("SDL_GameControllerGetButton", [_P(SDL_GameController), SDL_GameControllerButton], returns=Uint8)
SDL_GameControllerGetNumTouchpads = SDLFunc("SDL_GameControllerGetNumTouchpads", [_P(SDL_GameController)], c_int)
SDL_GameControllerGetNumTouchpadFingers = SDLFunc("SDL_GameControllerGetNumTouchpadFingers", [_P(SDL_GameController), c_int], returns=c_int)
SDL_GameControllerGetTouchpadFinger = SDLFunc("SDL_GameControllerGetTouchpadFinger", [_P(SDL_GameController), c_int, c_int, _P(Uint8), _P(c_float), _P(c_float), _P(c_float)], returns=c_int)
#SDL_GameControllerHasSensor = SDLFunc("SDL_GameControllerHasSensor", [_P(SDL_GameController), SDL_SensorType], returns=SDL_bool)
#SDL_GameControllerSetSensorEnabled = SDLFunc("SDL_GameControllerSetSensorEnabled", [_P(SDL_GameController), SDL_SensorType, SDL_bool], returns=c_int)
#SDL_GameControllerIsSensorEnabled = SDLFunc("SDL_GameControllerIsSensorEnabled", [_P(SDL_GameController), SDL_SensorType], returns=SDL_bool)
#SDL_GameControllerGetSensorDataRate = SDLFunc("SDL_GameControllerGetSensorDataRate", [_P(SDL_GameController), SDL_SensorType], returns=c_float)
#SDL_GameControllerGetSensorData = SDLFunc("SDL_GameControllerGetSensorData", [_P(SDL_GameController), SDL_SensorType, _P(c_float), c_int], returns=c_int)
#SDL_GameControllerGetSensorDataWithTimestamp = SDLFunc("SDL_GameControllerGetSensorDataWithTimestamp", [_P(SDL_GameController), SDL_SensorType, _P(Uint64), _P(c_float), c_int], returns=c_int)
SDL_GameControllerRumble = SDLFunc("SDL_GameControllerRumble", [_P(SDL_GameController), Uint16, Uint16, Uint32], returns=c_int)
SDL_GameControllerRumbleTriggers = SDLFunc("SDL_GameControllerRumbleTriggers", [_P(SDL_GameController), Uint16, Uint16, Uint32], returns=c_int)
SDL_GameControllerHasLED = SDLFunc("SDL_GameControllerHasLED", [_P(SDL_GameController)], SDL_bool)
SDL_GameControllerHasRumble = SDLFunc("SDL_GameControllerHasRumble", [_P(SDL_GameController)], SDL_bool)
SDL_GameControllerHasRumbleTriggers = SDLFunc("SDL_GameControllerHasRumbleTriggers", [_P(SDL_GameController)], returns=SDL_bool)
SDL_GameControllerSetLED = SDLFunc("SDL_GameControllerSetLED", [_P(SDL_GameController), Uint8, Uint8, Uint8], returns=c_int)
SDL_GameControllerSendEffect = SDLFunc("SDL_GameControllerSendEffect", [_P(SDL_GameController), c_void_p, c_int], returns=c_int)
SDL_GameControllerClose = SDLFunc("SDL_GameControllerClose", [_P(SDL_GameController)])

# events
SDL_RELEASED = 0
SDL_PRESSED = 1

SDL_EventType = c_int
SDL_FIRSTEVENT = 0
SDL_QUIT = 0x100
SDL_APP_TERMINATING = 0x101
SDL_APP_LOWMEMORY = 0x102
SDL_APP_WILLENTERBACKGROUND = 0x103
SDL_APP_DIDENTERBACKGROUND = 0x104
SDL_APP_WILLENTERFOREGROUND = 0x105
SDL_APP_DIDENTERFOREGROUND = 0x106
SDL_LOCALECHANGED = 0x107
SDL_DISPLAYEVENT = 0x150
SDL_WINDOWEVENT = 0x200
SDL_SYSWMEVENT = 0x201
SDL_KEYDOWN = 0x300
SDL_KEYUP = 0x301
SDL_TEXTEDITING = 0x302
SDL_TEXTINPUT = 0x303
SDL_KEYMAPCHANGED = 0x304
SDL_TEXTEDITING_EXT = 0x305
SDL_MOUSEMOTION = 0x400
SDL_MOUSEBUTTONDOWN = 0x401
SDL_MOUSEBUTTONUP = 0x402
SDL_MOUSEWHEEL = 0x403
SDL_JOYAXISMOTION = 0x600
SDL_JOYBALLMOTION = 0x601
SDL_JOYHATMOTION = 0x602
SDL_JOYBUTTONDOWN = 0x603
SDL_JOYBUTTONUP = 0x604
SDL_JOYDEVICEADDED = 0x605
SDL_JOYDEVICEREMOVED = 0x606
SDL_JOYBATTERYUPDATED = 0x607
SDL_CONTROLLERAXISMOTION = 0x650
SDL_CONTROLLERBUTTONDOWN = 0x651
SDL_CONTROLLERBUTTONUP = 0x652
SDL_CONTROLLERDEVICEADDED = 0x653
SDL_CONTROLLERDEVICEREMOVED = 0x654
SDL_CONTROLLERDEVICEREMAPPED = 0x655
SDL_CONTROLLERTOUCHPADDOWN = 0x656
SDL_CONTROLLERTOUCHPADMOTION = 0x657
SDL_CONTROLLERTOUCHPADUP = 0x658
SDL_CONTROLLERSENSORUPDATE = 0x659
SDL_FINGERDOWN = 0x700
SDL_FINGERUP = 0x701
SDL_FINGERMOTION = 0x702
SDL_DOLLARGESTURE = 0x800
SDL_DOLLARRECORD = 0x801
SDL_MULTIGESTURE = 0x802
SDL_CLIPBOARDUPDATE = 0x900
SDL_DROPFILE = 0x1000
SDL_DROPTEXT = 0x1001
SDL_DROPBEGIN = 0x1002
SDL_DROPCOMPLETE = 0x1003
SDL_AUDIODEVICEADDED = 0x1100
SDL_AUDIODEVICEREMOVED = 0x1101
SDL_SENSORUPDATE = 0x1200
SDL_RENDER_TARGETS_RESET = 0x2000
SDL_RENDER_DEVICE_RESET = 0x2001
SDL_POLLSENTINEL = 0x7F00
SDL_USEREVENT = 0x8000
SDL_LASTEVENT = 0xFFFF

SDL_eventaction = c_int
SDL_ADDEVENT = 0
SDL_PEEKEVENT = 1
SDL_GETEVENT = 2

SDL_TEXTEDITINGEVENT_TEXT_SIZE = 32
SDL_TEXTINPUTEVENT_TEXT_SIZE = 32

SDL_QUERY = -1
SDL_IGNORE = 0
SDL_DISABLE = 0
SDL_ENABLE = 1

class SDL_CommonEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32)]

class SDL_DisplayEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("display", Uint32),
        ("event", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
        ("padding3", Uint8),
        ("data1", Sint32),
    ]

class SDL_WindowEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("windowID", Uint32),
        ("event", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
        ("padding3", Uint8),
        ("data1", Sint32),
        ("data2", Sint32),
    ]

class SDL_Keysym(Structure):
    _fields_ = [("sym", SDL_Keycode), ("mod", Uint16), ("unused", Uint32)]

class SDL_KeyboardEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("windowID", Uint32),
        ("state", Uint8),
        ("repeat", Uint8),
        ("padding2", Uint8),
        ("padding3", Uint8),
        ("keysym", SDL_Keysym),
    ]

class SDL_TextEditingEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("windowID", Uint32),
        ("text", (c_char * SDL_TEXTEDITINGEVENT_TEXT_SIZE)),
        ("start", Sint32),
        ("length", Sint32),
    ]

class SDL_TextEditingExtEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("windowID", Uint32),
        ("text", c_char_p),
        ("start", Sint32),
        ("length", Sint32),
    ]

class SDL_TextInputEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32), ("windowID", Uint32), ("text", (c_char * SDL_TEXTINPUTEVENT_TEXT_SIZE))]

class SDL_MouseMotionEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("windowID", Uint32),
        ("which", Uint32),
        ("state", Uint32),
        ("x", Sint32),
        ("y", Sint32),
        ("xrel", Sint32),
        ("yrel", Sint32),
    ]

class SDL_MouseButtonEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("windowID", Uint32),
        ("which", Uint32),
        ("button", Uint8),
        ("state", Uint8),
        ("clicks", Uint8),
        ("padding1", Uint8),
        ("x", Sint32),
        ("y", Sint32),
    ]

class SDL_MouseWheelEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("windowID", Uint32),
        ("which", Uint32),
        ("x", Sint32),
        ("y", Sint32),
        ("direction", Uint32),
        ("preciseX", c_float),
        ("preciseY", c_float),
        ("mouseX", Sint32),
        ("mouseY", Sint32)
    ]

class SDL_JoyAxisEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", SDL_JoystickID),
        ("axis", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
        ("padding3", Uint8),
        ("value", Sint16),
        ("padding4", Uint16),
    ]

class SDL_JoyBallEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", SDL_JoystickID),
        ("ball", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
        ("padding3", Uint8),
        ("xrel", Sint16),
        ("yrel", Sint16),
    ]

class SDL_JoyHatEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", SDL_JoystickID),
        ("hat", Uint8),
        ("value", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
    ]

class SDL_JoyButtonEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", SDL_JoystickID),
        ("button", Uint8),
        ("state", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
    ]

class SDL_JoyDeviceEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32), ("which", Sint32)]

class SDL_JoyBatteryEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32), ("which", SDL_JoystickID), ("level", SDL_JoystickPowerLevel)]

class SDL_ControllerAxisEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", SDL_JoystickID),
        ("axis", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
        ("padding3", Uint8),
        ("value", Sint16),
        ("padding4", Uint16),
    ]

class SDL_ControllerButtonEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", SDL_JoystickID),
        ("button", Uint8),
        ("state", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
    ]

class SDL_ControllerDeviceEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32), ("which", Sint32)]

class SDL_ControllerTouchpadEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", SDL_JoystickID),
        ("touchpad", Sint32),
        ("finger", Sint32),
        ("x", c_float),
        ("y", c_float),
        ("pressure", c_float),
    ]

class SDL_ControllerSensorEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", SDL_JoystickID),
        ("sensor", Sint32),
        ("data", c_float * 3),
        ("timestamp_us", Uint64)
    ]

class SDL_AudioDeviceEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("which", Uint32),
        ("iscapture", Uint8),
        ("padding1", Uint8),
        ("padding2", Uint8),
        ("padding3", Uint8),
    ]

class SDL_TouchFingerEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("touchId", SDL_TouchID),
        ("fingerId", SDL_FingerID),
        ("x", c_float),
        ("y", c_float),
        ("dx", c_float),
        ("dy", c_float),
        ("pressure", c_float),
        ("windowID", Uint32)
    ]

class SDL_MultiGestureEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("touchId", SDL_TouchID),
        ("dTheta", c_float),
        ("dDist", c_float),
        ("x", c_float),
        ("y", c_float),
        ("numFingers", Uint16),
        ("padding", Uint16),
    ]

class SDL_DollarGestureEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("touchId", SDL_TouchID),
        ("gestureId", SDL_GestureID),
        ("numFingers", Uint32),
        ("error", c_float),
        ("x", c_float),
        ("y", c_float),
    ]

class SDL_DropEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32), ("file", c_char_p), ("windowID", Uint32)]

class SDL_SensorEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32), ("which", Sint32), ("data", (c_float * 6)), ("timestamp_us", Uint64)]

class SDL_QuitEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32)]

class SDL_OSEvent(Structure):
    _fields_ = [("type", Uint32), ("timestamp", Uint32)]

class SDL_UserEvent(Structure):
    _fields_ = [
        ("type", Uint32),
        ("timestamp", Uint32),
        ("windowID", Uint32),
        ("code", Sint32),
        ("data1", c_void_p),
        ("data2", c_void_p),
    ]

class SDL_Event(Union):
    _fields_ = [
        ("type", Uint32),
        ("common", SDL_CommonEvent),
        ("display", SDL_DisplayEvent),
        ("window", SDL_WindowEvent),
        ("key", SDL_KeyboardEvent),
        ("edit", SDL_TextEditingEvent),
        ("editExt", SDL_TextEditingExtEvent),
        ("text", SDL_TextInputEvent),
        ("motion", SDL_MouseMotionEvent),
        ("button", SDL_MouseButtonEvent),
        ("wheel", SDL_MouseWheelEvent),
        ("jaxis", SDL_JoyAxisEvent),
        ("jball", SDL_JoyBallEvent),
        ("jhat", SDL_JoyHatEvent),
        ("jbutton", SDL_JoyButtonEvent),
        ("jdevice", SDL_JoyDeviceEvent),
        ("jbattery", SDL_JoyBatteryEvent),
        ("caxis", SDL_ControllerAxisEvent),
        ("cbutton", SDL_ControllerButtonEvent),
        ("cdevice", SDL_ControllerDeviceEvent),
        ("ctouchpad", SDL_ControllerTouchpadEvent),
        ("csensor", SDL_ControllerSensorEvent),
        ("adevice", SDL_AudioDeviceEvent),
        ("sensor", SDL_SensorEvent),
        ("quit", SDL_QuitEvent),
        ("user", SDL_UserEvent),
        ("tfinger", SDL_TouchFingerEvent),
        ("mgesture", SDL_MultiGestureEvent),
        ("dgesture", SDL_DollarGestureEvent),
        ("drop", SDL_DropEvent),
        ("padding", (Uint8 * (56 if sizeof(c_void_p) <= 8 else (3 * sizeof(c_void_p)) if sizeof(c_void_p) > 16 else 64))),
    ]

SDL_PumpEvents = SDLFunc("SDL_PumpEvents")
SDL_PeepEvents = SDLFunc("SDL_PeepEvents", [_P(SDL_Event), c_int, SDL_eventaction, Uint32, Uint32], c_int)
