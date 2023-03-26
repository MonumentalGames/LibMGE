import sys
from os import environ
from platform import system
from pygame._sdl2 import get_drivers

class Platform:
    system = ""
    drivers = []

for driver in get_drivers():
    Platform.drivers.append(driver)

if system() == "Windows":
    Platform.system = "Windows"
elif system() == "Linux":
    if 'ANDROID_BOOTLOGO' in environ:
        Platform.system = "Android"
        sys.exit("Error ('Unsupported Platform')")
    else:
        Platform.system = "Linux"
else:
    Platform.system = system()
