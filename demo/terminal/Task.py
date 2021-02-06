#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python
from auto_everything.terminal import Terminal
from auto_everything.disk import Store

store = Store("task")
py = Python()
t = Terminal()


class Task():
    def add(self, comment):
        l = store.get("list", [])
        l.append(comment)
        store.set("list", l)
        print(comment)

    def done(self, index):
        l = store.get("list", [])
        del l[index]
        store.set("list", l)

    def list(self):
        l = store.get("list", [])
        for i, v in enumerate(l):
            print(f"{i}: {v}")


py.fire(Task)
py.make_it_global_runnable(executable_name="Task")
