# need root permission

import os
import time

from auto_everything.terminal import Terminal
terminal = Terminal()
gate = 50

while True:
    power_percent = int(terminal.run_command("cat /sys/class/power_supply/BAT0/capacity"))
    print("battery power left: ", power_percent, "%")
    if power_percent < 50:
        #terminal.run("hibernate") # won't work
        #os.system("hibernate") # won't work
        terminal.run("systemctl hibernate")

    time.sleep(60)
