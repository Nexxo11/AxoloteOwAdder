from cx_Freeze import setup, Executable
import sys

with open("ver.txt", "r") as f:
    version = f.read().strip()

build_exe_options = {
    "packages": [
        "configparser",
        "tkinter",
        "dearpygui.dearpygui",
        "os",
        "shutil",
        "requests",
        "json",
    ],
    "excludes": [],
    "include_files": [
        ("icon.ico", "icon.ico"),
        ("translations/en.json", "translations/en.json"),
        ("translations/es.json", "translations/es.json"),
        ("translations/fr.json", "translations/fr.json"),
        ("translations/pt.json", "translations/pt.json"),
        ("assets/refresh.png", "assets/refresh.png"),
        ("ver.txt", "ver.txt"),
        ("path.ini", "path.ini")
    ]
}

# Configuración dependiente del SO
base = None
target_name = "AxoloteOwAdder"

if sys.platform == "win32":
    base = "Win32GUI"
    target_name = "AxoloteOwAdder.exe"
    icon = "icon.ico"
else:
    base = None
    target_name = "AxoloteOwAdder"
    icon = None

executables = [
    Executable(
        "main.py",    
        base=base,
        target_name=target_name,
        icon=icon
    )
]

setup(
    name="AxoloteOwAdder",
    version=version,
    description="Aplicación para añadir Overworlds",
    options={"build_exe": build_exe_options},
    executables=executables
)