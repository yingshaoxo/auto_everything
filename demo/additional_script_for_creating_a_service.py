from auto_everything.base import Terminal, IO, Python

t = Terminal()
io = IO()
py = Python()

@py.loop()
def do():
    if not t.is_running("firefox"):
        # io.log("no running")
        t.run_program("firefox")

do()
