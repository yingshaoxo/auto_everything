from auto_everything.base import Terminal, Python

t = Terminal()
py = Python()

@py.loop()
def do():
    if not t.is_running("firefox"):
        t.run_program("firefox")

do()
