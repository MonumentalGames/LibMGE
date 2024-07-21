from ..Log import LogCritical

__all__ = ["sdl2", "sdlgfx", "sdlimage", "sdlttf", "sdlmixer"]

_errors = []

try:
    from . import sdl2
except:
    _errors.append(0)

try:
    from . import sdlgfx
except:
    _errors.append(1)

try:
    from . import sdlimage
except:
    _errors.append(2)

try:
    from . import sdlttf
except:
    _errors.append(3)

try:
    from . import sdlmixer
except:
    _errors.append(4)

if len(_errors) != 0:
    LogCritical(f"error when importing sdl2")
