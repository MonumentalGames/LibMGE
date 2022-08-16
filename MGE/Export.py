import os

# C:\Users\lucas\AppData\Local\Programs\Python\Python39\python.exe .\ctOS\System\setup.py build
def Export_exe(project, name, version, description):

    user = os.getlogin()
    loc_project = f"C:/Users/{user}/Documents/Monumental_Games/Engine/Projects/{project}"
    script = f"{loc_project}/main.py"
    ico = f"{loc_project}/images/icon.ico"

    setup = "import sys \n" \
            "from cx_Freeze import setup, Executable \n" \
            "\n" \
            "build_exe_options = {'packages': ['os', 'platform'], 'includes': ['pygame', 'MGE']} \n" \
            "\n" \
            "base = None \n" \
            "if sys.platform == 'win32': \n" \
            "    base = 'Win32GUI' \n" \
            "\n" \
            "target = Executable( \n" \
            f"    script='{script}', \n" \
            "    base=base, \n" \
            f"    icon='{ico}' \n" \
            "    ) \n" \
            "\n" \
            "setup( \n" \
            f"    name='{name}', \n" \
            f"    version='{version}', \n" \
            f"    description='{description}', \n" \
            "    options={'build_exe': build_exe_options}, \n" \
            "    executables=[target] \n" \
            "    ) \n"

    with open('./../DataFiles/setup.py', 'w') as arquivo:
        arquivo.write(setup)
        arquivo.close()

    #os.system(f"C:\\Users\\{user}\\AppData\\Local\\Programs\\Python\\Python39\\python.exe .\\ctOS\\System\\setup.py build")

    with open('./../DataFiles/setup.py', 'w') as arquivo:
        arquivo.write("None\nMGE12.0.0.1")
        arquivo.close()

    print(setup)

#Export_exe(0, 0, 0, 0)
