from ..Log import *
from ..Version import __version__, __versionData__
from tempfile import gettempdir
from platform import system
import os
import sys
import urllib.request
import json
import urllib.request
from zipfile import ZipFile

__all__ = ["main", "depsInstall"]

def depsInstall():
    Log("Checking compatibility...", ConsoleColors.Reset)
    try:
        with urllib.request.urlopen(f"https://deps.libmge.org/?version={__version__}&release={__versionData__['phase']}&os={system().lower()}") as response:
            data = response.read().decode('utf-8')
    except:
        Log("")
        LogError("Compatibility check failed")
        Log("Installation aborted", ConsoleColors.Red)
        return
    else:
        data = json.loads(data)

    if 'error' in data:
        Log("")
        LogError(data["error"]["message"])
        Log("Installation aborted", ConsoleColors.Red)
        return
    else:
        url = data['download']
        temp_zip_path = os.path.join(gettempdir(), 'deps.zip')

        def download_with_progress(url, filename):
            Log(f"\rDownloading {url}...", ConsoleColors.Reset, '')
            with urllib.request.urlopen(url) as response:
                total_size = int(response.getheader('Content-Length').strip())
                downloaded_size = 0
                block_size = 1024  # 1 Kilobyte

                with open(filename, 'wb') as out_file:
                    while True:
                        buffer = response.read(block_size)
                        if not buffer:
                            break

                        downloaded_size += len(buffer)
                        out_file.write(buffer)

                        percent_complete = int(downloaded_size * 100 / total_size)
                        Log(f"\rDownloading {url} ({ConsoleColors.Yellow}{percent_complete}%{ConsoleColors.Reset}) {downloaded_size // 1024}Kb / {total_size // 1024}KB", ConsoleColors.Reset, '')

                Log("\nDownload complete", ConsoleColors.Green)

        try:
            download_with_progress(url, temp_zip_path)
        except:
            Log("")
            LogError("Failed to download file")
            Log("Installation aborted", ConsoleColors.Red)
            return

        Log("Extracting files...", ConsoleColors.Reset)

        try:
            with ZipFile(temp_zip_path, 'r') as zip_ref:
                zip_ref.extractall(f"{os.path.abspath(os.path.dirname(__file__))}/../")
        except:
            Log("")
            LogError("Failed to extract files")
            Log("Installation aborted", ConsoleColors.Red)
            return

        try:
            from .._sdl._dll_loader import nullFunction
        except:
            Log("Installation failed", ConsoleColors.Red)
        else:
            Log("Successfully installed", ConsoleColors.Green)

def help():
    Log("Usage:", ConsoleColors.Reset)
    Log(f"  MGE version         →  Show installed dependency versions", ConsoleColors.Reset)
    Log(f"  MGE help            →  Show this help message", ConsoleColors.Reset)
    Log(f"  MGE deps install    →  Install required dependencies", ConsoleColors.Reset)
    Log(f"  MGE deps versions   →  Show installed dependency versions", ConsoleColors.Reset, "\n\n")
    Log(f"{ConsoleColors.Cyan}Tip:{ConsoleColors.Reset} Run '{ConsoleColors.Bold}MGE deps install{ConsoleColors.Reset}' to ensure all dependencies are set up.", ConsoleColors.Reset)

def main():
    if len(sys.argv) < 2:
        Log("No command found.", ConsoleColors.Yellow, "\n\n")
        help()
        return

    command = sys.argv[1].lower()

    if command == "version":
        Log(f"{'MGE       ' if __versionData__['phase'] == 'Stable' else __versionData__['phase'] + '-MGE  '}→  {ConsoleColors.Green}{__version__}", ConsoleColors.Reset)

    elif command == "deps" and len(sys.argv) >= 3:
        subcommand = sys.argv[2].lower()

        if subcommand == "install":
            depsInstall()

        elif subcommand == "versions":
            try:
                from .._sdl._dll_loader import nullFunction
            except:
                Log(f"\n{ConsoleColors.Cyan}Tip:{ConsoleColors.Reset} Run '{ConsoleColors.Bold}MGE deps install{ConsoleColors.Reset}' to update missing or outdated dependencies.", ConsoleColors.Reset)
            else:
                from ..Platform import Platform
                Log(f"SDL       →  {ConsoleColors.Green}{Platform.SDL.SDL_version}", ConsoleColors.Reset)
                Log(f"SDLGFX    →  {ConsoleColors.Green}{Platform.SDL.SDLGFX_version}", ConsoleColors.Reset)
                Log(f"SDLIMAGE  →  {ConsoleColors.Green}{Platform.SDL.SDLIMAGE_version}", ConsoleColors.Reset)
                Log(f"SDLTTF    →  {ConsoleColors.Green}{Platform.SDL.SDLTTF_version}", ConsoleColors.Reset)
                Log(f"SDLMIXER  →  {ConsoleColors.Green}{Platform.SDL.SDLMIXER_version}", ConsoleColors.Reset)
                Log(f"{ConsoleColors.Cyan}Tip:{ConsoleColors.Reset} Run '{ConsoleColors.Bold}MGE deps install{ConsoleColors.Reset}' to update missing or outdated dependencies.", ConsoleColors.Reset)

        else:
            Log("No command found.", ConsoleColors.Yellow, "\n\n")
            help()

    elif command == "help":
        help()

    else:
        Log("No command found.", ConsoleColors.Yellow, "\n\n")
        help()
