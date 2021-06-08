#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python
from auto_everything.terminal import Terminal

py = Python()
t = Terminal()


class Open:
    def worklog(self):
        t.run(
            """
        cd ~/work/worklog
        code .
        """
        )

    def this(self):
        t.run(
            """
        xdg-open .
        """
        )


py.fire(Open)
py.make_it_global_runnable(executable_name="Open")
