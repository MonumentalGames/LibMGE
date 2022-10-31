import platform

from .Platform import Platform

from .MGE import Program, Cache, MGE_ver

from .Camera import Camera
from .Internal_Window import Internal_Window

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

print(f"Beta-MGE {MGE_ver} (pygame {MGE.Program.pygame.version.ver} | Python {platform.python_version()})\n")
