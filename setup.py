'''
Setup file using cx_Freeze. NOTE:cx_Freeze is not included in the 
requirements.txt file because it is not nessicary for running the
program itself. 

To install cx_Freeze:
pip install cx_Freeze

To run this file:
python setup.py build
'''

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PassMan",
        version = "0.1",
        description = "Password Manager",
        options = {"build_exe": build_exe_options},
        executables = [Executable("passman.py", base=base, icon='icon.ico')])
