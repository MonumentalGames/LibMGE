import platform

from .MGE import *
from .Text import ObjectText, text_box
from .Object2D import Object2D
from .Line import Line

from .Material import Material
from .Texture import Texture
from .Image import Image
from .Sprite import Sprite

from .Mouse import mouse_button, mouse_position
from .Keyboard import *

print(f"Beta-MGE {ver} (Python {platform.python_version()})\n")
