#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python
from auto_everything.terminal import Terminal

py = Python()
t = Terminal()


class Do:
    def experiment(self):
        t.run(
        """
            jupyter-lab . &
        """
        )

py.fire(Do)
py.make_it_global_runnable(executable_name="Do")
