from auto_everything.base import Terminal, Python

t = Terminal()
py = Python()

#browser = "firefox"
browser = "chromium"

@py.loop()
def do():
    if not t.is_running(browser):
        t.run_program(browser)

do()
