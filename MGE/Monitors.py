from screeninfo import get_monitors

def monitor_resolution(monitor_name="primary"):
    if monitor_name == "primary":
        for monitor in get_monitors():
            if monitor.is_primary:
                return f"{monitor.height}, {monitor.width}"
    else:
        for monitor in get_monitors():
            if monitor.name == monitor_name:
                return f"{monitor.height}, {monitor.width}"
