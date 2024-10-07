from ..Log import *
from ..Version import __version__, __versionData__
from tempfile import gettempdir
from platform import system
import os
import sys
import urllib.request
import json
import zipfile

__all__ = ["main", "install"]

def install():
    print("Checking compatibility")

    _system = system().lower()

    with urllib.request.urlopen(f"https://deps.libmge.org/?version={__version__}&release={__versionData__['phase']}&os={_system}") as response:
        data = response.read().decode('utf-8')

    data = json.loads(data)

    if 'error' in data:
        LogCritical(data["error"]["title"], data["error"]["message"])
    else:
        print(f"Downloading dependencies from {data['download']}")

        temp_zip_path = os.path.join(gettempdir(), 'deps.zip')

        urllib.request.urlretrieve(data['download'], temp_zip_path)

        print(f"Extracting files")

        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(f"{os.path.abspath(os.path.dirname(__file__))}/../")

        Log("Successfully installed")

def main():
    if len(sys.argv) < 2:
        return

    command = sys.argv[1].lower()

    if command == "version":
        print(f"{'MGE' if __versionData__['phase'] == 'Stable' else __versionData__['phase'] + '-MGE'} {__version__}")

    elif command == "deps" and len(sys.argv) >= 3:
        subcommand = sys.argv[2].lower()

        if subcommand == "install":
            install()
        elif subcommand == "versions":
            from ..Platform import Platform
            LogInfo(f"SDL - {Platform.SDL.SDL_version}")
            LogInfo(f"SDLGFX - {Platform.SDL.SDLGFX_version}")
            LogInfo(f"SDLIMAGE - {Platform.SDL.SDLIMAGE_version}")
            LogInfo(f"SDLTTF - {Platform.SDL.SDLTTF_version}")
            LogInfo(f"SDLMIXER - {Platform.SDL.SDLMIXER_version}")
