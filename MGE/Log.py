from typing import NoReturn

__all__ = ["Log", "LogDebug", "LogInfo", "LogWarn", "LogError", "LogCritical"]

class _ConsoleColors:
    Reset = "\033[0m"
    Gray = "\033[90m"
    Red = "\033[91m"
    Green = "\033[92m"
    Yellow = "\033[93m"
    Blue = "\033[94m"
    Purple = "\033[95m"
    Cyan = "\033[96m"
    White = "\033[97m"

def Log(msg=""):
    print(f"{_ConsoleColors.Gray}{msg}{_ConsoleColors.Reset}")

def LogDebug(msg=""):
    print(f"{_ConsoleColors.Yellow}Debug{_ConsoleColors.Reset}: {msg}")

def LogInfo(msg=""):
    print(f"{_ConsoleColors.Green}Info{_ConsoleColors.Reset}: {_ConsoleColors.Gray}{msg}{_ConsoleColors.Reset}")

def LogWarn(msg=""):
    print(f"{_ConsoleColors.Yellow}Warning{_ConsoleColors.Reset}: {msg}")

def LogError(msg=""):
    print(f"{_ConsoleColors.Red}Error{_ConsoleColors.Reset}: {msg}")

def LogCritical(msg="", long_msg="", exit_code=1) -> NoReturn:
    print(f"{_ConsoleColors.Red}Critical Error{_ConsoleColors.Reset}: {msg}")
    if long_msg:
        Log(long_msg)
    raise SystemExit(exit_code)
