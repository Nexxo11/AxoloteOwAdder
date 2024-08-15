from cx_Freeze import setup, Executable

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
        ("src/translate.json", "src/translate.json"),
        ("src/ver.txt", "src/ver.txt")
    ]
}

executables = [
    Executable(
        "ui.py",    
        base="Win32GUI",  
        icon="icon.ico"
    )
]

setup(
    name="AxoloteOwAdder",
    version="0.3.3",
    description="Aplicación para añadir Overworlds",
    options={"build_exe": build_exe_options},
    executables=executables
)
