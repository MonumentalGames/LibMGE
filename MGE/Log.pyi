from typing import Never

class ConsoleColors:
    Reset:str
    Bold:str
    Gray:str
    Red:str
    Green:str
    Yellow:str
    Blue:str
    Purple:str
    Cyan:str
    White:str

def Log(msg:str, color:str=ConsoleColors.Gray, end:str="\n"): ...

def LogDebug(msg:str, end:str="\n"): ...

def LogInfo(msg:str, end:str="\n"): ...

def LogWarn(msg:str, end:str="\n"): ...

def LogError(msg:str, end:str="\n"): ...

def LogCritical(msg:str, long_msg:str="", exit_code:int=1) -> Never: ...
