from typing import NoReturn
from platform import system, version

_system = system()
if _system.lower() == "windows" and int(version().split(".")[2]) >= 22000:
    _colors = True
else:
    _colors = False

__all__ = ["Log", "LogDebug", "LogInfo", "LogWarn", "LogError", "LogCritical"]

class _ConsoleColors:
    Reset = "\033[0m" if _colors else ""
    Gray = "\033[90m" if _colors else ""
    Red = "\033[91m" if _colors else ""
    Green = "\033[92m" if _colors else ""
    Yellow = "\033[93m" if _colors else ""
    Blue = "\033[94m" if _colors else ""
    Purple = "\033[95m" if _colors else ""
    Cyan = "\033[96m" if _colors else ""
    White = "\033[97m" if _colors else ""

def Log(msg: str = ""):
    print(f"{_ConsoleColors.Gray}{msg}{_ConsoleColors.Reset}")

def LogDebug(msg: str = ""):
    print(f"{_ConsoleColors.Yellow}Debug{_ConsoleColors.Reset}: {msg}")

def LogInfo(msg: str = ""):
    print(f"{_ConsoleColors.Green}Info{_ConsoleColors.Reset}: {_ConsoleColors.Gray}{msg}{_ConsoleColors.Reset}")

def LogWarn(msg: str = ""):
    print(f"{_ConsoleColors.Yellow}Warning{_ConsoleColors.Reset}: {msg}")

def LogError(msg: str = ""):
    print(f"{_ConsoleColors.Red}Error{_ConsoleColors.Reset}: {msg}")

def LogCritical(msg: str = "", long_msg: str = "", exit_code: int = 1) -> NoReturn:
    print(f"{_ConsoleColors.Red}Critical Error{_ConsoleColors.Reset}: {msg}")
    if long_msg:
        Log(long_msg)
    raise SystemExit(exit_code)
