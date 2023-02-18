from .Platform import Platform

if Platform.system == "Windows" or Platform.system == "Linux" or Platform.system == "MacOs":
    from screeninfo import get_monitors
elif Platform.system == "Android":
    pass

def monitor_resolution(monitor_name="primary"):
    if Platform.system == "Windows" or Platform.system == "Linux" or Platform.system == "MacOs":
        if monitor_name == "primary":
            for monitor in get_monitors():
                if monitor.is_primary:
                    return f"{monitor.height}, {monitor.width}"
        else:
            for monitor in get_monitors():
                if monitor.name == monitor_name:
                    return f"{monitor.height}, {monitor.width}"
    elif Platform.system == "Android":
        pass
    else:
        pass
