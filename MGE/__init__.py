from .Platform import Platform

from .MGE import Program
from .Global_Cache import Cache

from .Camera import Camera
from .Internal_Window import Internal_Window
#from .Outside_Window import Outside_Window, messagebox

from .Text import ObjectText, text_box
from .Object2D import Object2D
from .Line import Line

from .Material import Material
from .Texture import Texture
from .Image import Image
from .Sprite import Sprite

from .Mesh import Mesh

from .Mouse import mouse_button, mouse_position, mouse_set_position, mouse_set_visible
from .Keyboard import keyboard

from .Button import Button

from .Audio import Audio

from .Monitors import monitor_resolution

from .Version import __version__, __version_data__

Program.init()
