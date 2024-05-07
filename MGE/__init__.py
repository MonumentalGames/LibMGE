from .Common import update, init, SetLogicClock, GetLogicClock, AllEvents, QuitEvent, WindowEvents, OpenUrl, AutoCalcs2D
from .Log import *
from .Audio import Music, Sound
from .Platform import Platform
from .Constants import *
from .Camera import Camera
from .Window import Window, CreateGlWindow
from .InternalWindow import InternalWindow
from .Monitors import Monitors, Monitor
from .Text import ObjectText, ObjectInputTextLine, ObjectInputPassLine, ObjectInputTextBox
from .Object2D import Object2D
from .Line import Line
from .Material import Material
from .Texture import Texture
from .Image import *
from .Color import Color
from .Mesh import Mesh2D, CreateMeshPlane
from .Mouse import *
from .Keyboard import keyboard
from .GameController import *
from .Button import *
from .Time import *
from .Version import __version__, __version_data__, __version_list__

print(f"{'MGE' if __version_data__['phase'] == 'Stable' else __version_data__['phase'] + '-MGE'} {__version__} (SDL {Platform.SDL.SDL_version} | Python {Platform.python_version})")
