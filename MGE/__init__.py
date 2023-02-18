import platform
from os import system

from .Platform import Platform

from .MGE import Program, Cache, MGE_ver

from .Camera import Camera
from .Internal_Window import Internal_Window
from .Outside_Window import Outside_Window, messagebox

from .Text import ObjectText, text_box
from .Object2D import Object2D
from .Line import Line

from .Material import Material
from .Texture import Texture
from .Image import Image
from .Sprite import Sprite

from .Mesh import *

from .Mouse import mouse_button, mouse_position, mouse_set_position, mouse_set_visible
from .Keyboard import keyboard

from .Button import *

from .Audio import audio

from .Monitors import monitor_resolution

__version__ = f"{MGE_ver.version}.{MGE_ver.build}"

if True:
    if MGE_ver.phase == "Stable":
        cache_print = "MGE"
    elif MGE_ver.phase == "Alpha":
        cache_print = "Alpha-MGE"
    elif MGE_ver.phase == "Beta":
        cache_print = "Beta-MGE"
    else:
        cache_print = f"{MGE_ver.phase}-MGE"
    system("cls")
    print(f"{cache_print} {__version__} (pygame {MGE.Program.pygame.version.ver} | Python {platform.python_version()})")
