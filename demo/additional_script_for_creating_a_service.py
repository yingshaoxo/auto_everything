from auto_everything.base import Terminal, IO
import time

t = Terminal()
io = IO()

while 1:
    try:
        if not t.is_running("firefox"):
            #io.log("no running")
            t.run_program("firefox")

        if not t.is_running("terminator"):
            t.run_program("terminator")

        time.sleep(1)
    except Exception as e:
        log(e)
