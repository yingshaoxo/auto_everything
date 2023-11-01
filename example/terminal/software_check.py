from auto_everything.terminal import Terminal

terminal = Terminal()

if (terminal.software_exists("git")):
    print("git exists")

if (terminal.software_exists("freedom")):
    print("freedom not exists")
