__version_list__ = [0, 9, 7, 0]

# Alpha, Beta
__version_data__ = {"version": f"{__version_list__[0]}.{__version_list__[1]}", "build": f"{__version_list__[2]}{f'.{__version_list__[3]}' if __version_list__[3] else ''}", "phase": "Alpha"}

__version__ = f"{__version_data__['version']}.{__version_data__['build']}"
