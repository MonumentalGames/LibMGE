
__all__ = ["Log", "LogDebug", "LogInfo", "LogWarn", "LogError", "LogCritical"]

reset = "\033[0m"
gray = "\033[90m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
purple = "\033[95m"
cyan = "\033[96m"
white = "\033[97m"

def Log(msg=""):
    print(f"{gray}{msg}{reset}")

def LogDebug(msg=""):
    print(f"{yellow}Debug{reset}: {msg}")

def LogInfo(msg=""):
    print(f"{green}Info{reset}: {gray}{msg}{reset}")

def LogWarn(msg=""):
    print(f"{yellow}Warning{reset}: {msg}")

def LogError(msg=""):
    print(f"{red}Error{reset}: {msg}")

def LogCritical(msg="", long_msg="", exit_code=1):
    print(f"{red}Critical Error{reset}: {msg}")
    if long_msg:
        Log(long_msg)
    raise SystemExit(exit_code)
