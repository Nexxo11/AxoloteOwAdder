from cx_Freeze import setup, Executable

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
        ("ver.txt", "ver.txt"),
        ("path.ini", "path.ini")
    ]
}

executables = [
    Executable(
        "main.py",    
        base="Win32GUI",  
        icon="icon.ico"
    )
]

setup(
    name="AxoloteOwAdder",
    version=version,
    description="Aplicación para añadir Overworlds",
    options={"build_exe": build_exe_options},
    executables=executables
)
