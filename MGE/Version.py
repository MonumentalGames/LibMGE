import platform
import pygame
from os import system

from .Platform import Platform

__version_data__ = {"version": "0.2", "build": "0", "phase": "Stable"}

__version__ = f"{__version_data__['version']}.{__version_data__['build']}"

def version_print():
    if __version_data__["phase"] == "Stable":
        cache_print = "MGE"
    else:
        cache_print = f"{__version_data__['phase']}-MGE"
    if Platform.system == "Windows":
        system("cls")
    elif Platform.system == "Linux":
        system("clear")
    print(f"{cache_print} {__version__} (pygame {pygame.version.ver} | Python {platform.python_version()})")
