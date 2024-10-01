from platform import python_version, version
from ._sdl.sdl2 import SDL_GetPlatform, SDL_GetVersion, SDL_GetNumRenderDrivers, SDL_RendererInfo, SDL_GetRenderDriverInfo
from ._sdl.sdlimage import IMG_Linked_Version
from ._sdl.sdlmixer import Mix_Linked_Version
from ._sdl.sdlttf import TTF_Linked_Version
from .Constants import RenderDriver as _RenderDriver
from .Log import LogCritical

__all__ = ["Platform"]

def compare_versions(version1, version2):
    for ver1, ver2 in zip(version1, version2):
        if ver1 < ver2:
            return -1
        elif ver1 > ver2:
            return 1
    return 0

class Platform:
    system = ""
    system_version = 0
    python_version = python_version()
    drivers = []

    class SDL:
        SDL_version_list = [0, 0, 0]
        SDL_version = ""

        SDLGFX_version_list = [0, 0, 0]
        SDLGFX_version = ""

        SDLIMAGE_version_list = [0, 0, 0]
        SDLIMAGE_version = ""

        SDLMIXER_version_list = [0, 0, 0]
        SDLMIXER_version = ""

        SDLTTF_version_list = [0, 0, 0]
        SDLTTF_version = ""

_systems = ["Windows", "Mac OS X", "Linux", "iOS", "Android"]
_compatible_systems = ["Windows"]

_min_versions_SDL = {"sdl": [2, 26, 0], "sdlgfx": [0, 0, 0], "sdlimage": [2, 0, 0], "sdlmixer": [2, 6, 0], "sdlttf": [2, 20, 0]}

Platform.system = SDL_GetPlatform()
if Platform.system not in _compatible_systems:
    LogCritical(f"incompatible {Platform.system} system")
if Platform.system.lower() == "windows":
    Platform.system_version = int(version().split(".")[2])

class RenderDriver:
    def __init__(self):
        self.id = self.name = self.hardware = self.software = self.bufferTexture = self.targetTexture = None

    def __repr__(self):
        return f"<%s.%s %s at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.name,
            id(self)
        )

for driver_index in range(SDL_GetNumRenderDrivers()):
    driver_info = SDL_RendererInfo()
    if SDL_GetRenderDriverInfo(driver_index, driver_info) == 0:
        _driver = RenderDriver()
        _driver.id = driver_index
        _driver.name = driver_info.name.decode('utf-8')
        _driver.hardware = bool(driver_info.flags & 0x00000002)
        _driver.software = bool(driver_info.flags & 0x00000001)
        _driver.bufferTexture = bool(driver_info.flags & 0x00000004)
        _driver.targetTexture = bool(driver_info.flags & 0x00000008)
        Platform.drivers.append(_driver)
        if _driver.name == "direct3d":
            _RenderDriver.Direct3d = _driver.id
        elif _driver.name == "direct3d11":
            _RenderDriver.Direct3d11 = _driver.id
        elif _driver.name == "direct3d12":
            _RenderDriver.Direct3d12 = _driver.id
        elif _driver.name == "opengl":
            _RenderDriver.OpenGL = _driver.id
        elif _driver.name == "software":
            _RenderDriver.Software = _driver.id

_SDL_Version = SDL_GetVersion()
Platform.SDL.SDL_version_list = [_SDL_Version.major, _SDL_Version.minor, _SDL_Version.patch]
Platform.SDL.SDL_version = ".".join(map(str, Platform.SDL.SDL_version_list))
if compare_versions(Platform.SDL.SDL_version_list, _min_versions_SDL["sdl"]) < 0:
    LogCritical()

Platform.SDL.SDLGFX_version_list = [0, 0, 0]
Platform.SDL.SDLGFX_version = ".".join(map(str, Platform.SDL.SDLGFX_version_list))
if compare_versions(Platform.SDL.SDLGFX_version_list, _min_versions_SDL["sdlgfx"]) < 0:
    LogCritical()

_SDL_Version = IMG_Linked_Version().contents
Platform.SDL.SDLIMAGE_version_list = [_SDL_Version.major, _SDL_Version.minor, _SDL_Version.patch]
Platform.SDL.SDLIMAGE_version = ".".join(map(str, Platform.SDL.SDLIMAGE_version_list))
if compare_versions(Platform.SDL.SDLIMAGE_version_list, _min_versions_SDL["sdlimage"]) < 0:
    LogCritical()

_SDL_Version = Mix_Linked_Version()
Platform.SDL.SDLMIXER_version_list = [_SDL_Version.major, _SDL_Version.minor, _SDL_Version.patch]
Platform.SDL.SDLMIXER_version = ".".join(map(str, Platform.SDL.SDLMIXER_version_list))
if compare_versions(Platform.SDL.SDLMIXER_version_list, _min_versions_SDL["sdlmixer"]) < 0:
    LogCritical()

_SDL_Version = TTF_Linked_Version()
Platform.SDL.SDLTTF_version_list = [_SDL_Version.major, _SDL_Version.minor, _SDL_Version.patch]
Platform.SDL.SDLTTF_version = ".".join(map(str, Platform.SDL.SDLTTF_version_list))
if compare_versions(Platform.SDL.SDLTTF_version_list, _min_versions_SDL["sdlttf"]) < 0:
    LogCritical()
