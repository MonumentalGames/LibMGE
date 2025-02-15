from platform import system, version

_system = system()
if _system.lower() == "windows" and int(version().split(".")[2]) >= 22000:
    _colors = True
else:
    _colors = False

__all__ = ["ConsoleColors", "Log", "LogDebug", "LogInfo", "LogWarn", "LogError", "LogCritical"]

class ConsoleColors:
    Reset = "\033[0m" if _colors else ""
    Bold = "\033[1m" if _colors else ""
    Gray = "\033[90m" if _colors else ""
    Red = "\033[91m" if _colors else ""
    Green = "\033[92m" if _colors else ""
    Yellow = "\033[93m" if _colors else ""
    Blue = "\033[94m" if _colors else ""
    Purple = "\033[95m" if _colors else ""
    Cyan = "\033[96m" if _colors else ""
    White = "\033[97m" if _colors else ""

def Log(msg, color=ConsoleColors.Gray, end="\n"):
    print(f"{color}{msg}{ConsoleColors.Reset}", end=end)

def LogDebug(msg, end="\n"):
    print(f"{ConsoleColors.Yellow}Debug{ConsoleColors.Reset}: {msg}", end=end)

def LogInfo(msg, end="\n"):
    print(f"{ConsoleColors.Green}Info{ConsoleColors.Reset}: {ConsoleColors.Gray}{msg}{ConsoleColors.Reset}", end=end)

def LogWarn(msg, end="\n"):
    print(f"{ConsoleColors.Yellow}Warning{ConsoleColors.Reset}: {msg}", end=end)

def LogError(msg, end="\n"):
    print(f"{ConsoleColors.Red}Error{ConsoleColors.Reset}: {msg}", end=end)

def LogCritical(msg, long_msg="", exit_code=1):
    print(f"{ConsoleColors.Red}Critical Error{ConsoleColors.Reset}: {msg}")
    if long_msg:
        Log(long_msg)
    raise SystemExit(exit_code)
