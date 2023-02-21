import platform
import pygame
from os import system

__version_data__ = {"version": "0.1", "build": "27", "phase": "Beta"}

__version__ = f"{__version_data__['version']}.{__version_data__['build']}"

def version_print():
    if __version_data__["phase"] == "Stable":
        cache_print = "MGE"
    else:
        cache_print = f"{__version_data__['phase']}-MGE"
    system("cls")
    print(f"{cache_print} {__version__} (pygame {pygame.version.ver} | Python {platform.python_version()})")
