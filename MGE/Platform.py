from os import environ
from platform import system

class Platform:
    system = ""

if system() == "Windows":
    Platform.system = "Windows"
elif system() == "Linux":
    if 'ANDROID_BOOTLOGO' in environ:
        Platform.system = "Android"
    else:
        Platform.system = "Linux"
else:
    Platform.system = system()
