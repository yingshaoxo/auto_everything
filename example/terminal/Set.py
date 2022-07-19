#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python
from auto_everything.terminal import Terminal

py = Python()
t = Terminal()


class Mission():
    def light(self, num:float):
        num = num / 100
        t.run(f"""
xrandr --output DP-1 --brightness {num}
        """)


py.make_it_global_runnable(executable_name="Set")
py.fire(Mission)
