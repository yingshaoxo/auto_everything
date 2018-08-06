import os
import time
import threading


# This is for using my parent package
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from base import Terminal, Python
t = Terminal()
py = Python()

sys.path.pop(0)


class GUI():
    def __init__(self):
        t.install_package("python3-xlib")
        py.install_package("pyautogui")

        import pyautogui as autogui
        self.autogui = autogui
        self.autogui.FAILSAFE = False

    def traning(self):
        self.autogui.moveTo(0, 0)


if __name__ == "__main__":
    gui = GUI()
    gui.test()
