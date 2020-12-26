#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal

py = Python()
t = Terminal()


class Tools():
    def cd(self, to_where):
        """
        change directory
        """
        if to_where == "auto":
            t.run_program("terminator --working-directory='~/Codes/Python/auto_everything'")
        elif to_where == "pyask":
            t.run_program("terminator --working-directory='~/Codes/PyAsk'")
        elif to_where == "blog":
            t.run("""
sudo mkdir /media/newhd
sudo umount /dev/sda3
sudo mount /dev/sda3 /media/newhd

terminator --working-directory='/media/newhd/home/yingshaoxo/Codes/Python/ysblogger'
            """)
        elif to_where == "tenxun":
            t.run("""
            #ssh-copy-id root@182.211.142.181
            terminator -x "ssh root@182.211.142.181"
            """)


py.make_it_runnable()
py.fire(Tools)
