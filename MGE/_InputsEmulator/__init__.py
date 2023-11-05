from ..Platform import Platform

__all__ = ["version",
           "MousePress", "MouseRelease", "MouseClick", "MouseScroll",
           "KeyboardPress", "KeyboardRelease", "KeyboardClick"]

if Platform.system == "Windows":
    from ._win32 import *
#elif Platform.system == "Linux":
#    from ._linux import *
else:
    from ._error import *

version = "0.1.0"
