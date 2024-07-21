__versionList__ = [0, 9, 8, 0]

# Alpha, Beta
__versionData__ = {"version": f"{__versionList__[0]}.{__versionList__[1]}", "build": f"{__versionList__[2]}{f'.{__versionList__[3]}' if __versionList__[3] else ''}", "phase": "Alpha"}

__version__ = f"{__versionData__['version']}.{__versionData__['build']}"
