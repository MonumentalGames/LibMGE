import sys

__all__ = ["sdl2", "sdlgfx", "sdlimage", "sdlttf", "sdlmixer"]

try:
    from . import sdl2
    from . import sdlgfx
    from . import sdlimage
    from . import sdlttf
    from . import sdlmixer
except:
    sys.exit("error when importing sdl2")
