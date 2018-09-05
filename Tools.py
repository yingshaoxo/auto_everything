#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal
py = Python()
t = Terminal()

class Tools():
    def push(self, comment):
        self.__clear()

        commands = """
git add .
git commit -m "{}"
git push origin
        """.format(comment)
        t.run(commands)

    def __clear(self):
        commands = """
sudo rm -fr dist
sudo rm -fr build
sudo rm -fr test.py
sudo rm -fr nohup.out
sudo rm -fr whatsup.log
sudo rm -fr auto_everything.egg-info
sudo rm auto_everything/Base.pyc
sudo rm auto_everything/__init__.pyc
sudo rm -fr auto_everything/nohup.out
sudo rm -fr auto_everything/__pycache__
        """
        t.run(commands)

py.make_it_runnable()
py.fire(Tools)
