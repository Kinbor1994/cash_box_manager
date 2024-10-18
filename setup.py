import os
import sys
from cx_Freeze import setup, Executable

def find_data_file(filename): 
    if getattr(sys, "frozen", False):
            datadir = os.path.dirname(sys.executable) 
    else:
            datadir = os.path.dirname("./") 
    return os.path.join(datadir, filename)




# Liste des dépendances à inclure
packages = [
    'babel',
    'bcrypt',
    'pyparsing',
    "PySide6.QtCore", 
    "PySide6.QtGui", 
    "PySide6.QtWidgets",
    "PySide6.QtCharts",
    'qt_material',
    'qtawesome',
    'requests',
    'setuptools',
    'shiboken6',
    'sqlalchemy',
    'typing_extensions',
    'urllib3',
]

# Inclure les fichiers non-Python nécessaires à votre application
include_files = [
    find_data_file("config.json"), 
    find_data_file("initial_balance.json"),
    find_data_file("db.db"), 
    find_data_file("resources/icons/icon_3.ico"), 
    find_data_file("initial_balance.json"),  
]

# Définir les options de construction
build_options = {
    'packages': packages,
    'include_files': include_files,
    'excludes': ['tkinter'],
    "optimize": 1,
    "silent": True,
    "include_msvcr": True,
}

# Créer l'exécutable principal
exe = Executable(
    script='main.py',
    base='Win32GUI' if sys.platform == 'win32' else None,
    target_name='cbm_setup.exe',
    icon=find_data_file('resources/icons/icon_3.ico'),  
)

setup(
    name='CASHBOXMANAGERBYBOREL',
    version='1.0',
    description='Logiciel de gestion de caisse.',
    options={'build_exe': build_options},
    executables=[exe]
)

