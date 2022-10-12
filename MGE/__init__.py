import platform

from .MGE import Program, Internal_Screen, Cache, MGE_ver

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

print(f"Beta-MGE {MGE_ver} (Python {platform.python_version()})\n")
