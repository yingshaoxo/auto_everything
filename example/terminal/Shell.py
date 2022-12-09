#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
import os, re
import tty, termios, sys

from auto_everything.python import Python
from auto_everything.terminal import Terminal

py = Python()
t = Terminal(debug=False)

MODE = None

"""
def my_shell(type=None):
    if type == "x":
        def command_line_transforming(command):
            return "proxychains4 " + command
    else:
        def command_line_transforming(command):
            return command

    t.debug = False
    print("Welcome!\n\nLet's begin the journey by type your command here:\n")
    print("> ", end="")
    while True:
        try:
            command = input("")
            t.run(command_line_transforming(command=command))
            print()
            print("> ", end="")
        except Exception as e:
            print(e)
"""

def get_char():
    #https://www.physics.udel.edu/~watson/scen103/ascii.html

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return char

def delete_one_char():
    sys.stdout.write("\b")
    sys.stdout.write(" ")
    sys.stdout.write("\b")
    sys.stdout.flush()

def print_without_new_line(text):
    print(text, end="", flush=True)
    """
    out = sys.stdout
    if out.isatty():
        out.write(char)
    out.flush()
    """

def print_with_new_line(text=""):
    print(text, end="\n", flush=True)

def command_process(command):
    global MODE

    command = command.strip()

    if command == "exit":
        exit()
    elif command == "x":
        MODE = "x"
        return

    if MODE == "x":
        command = f"proxychains4 {command}"

    t.run(command)

def my_shell():
    # how to measure if a shell program is working properly? Can use it to use vim.
    os.system("clear")

    print_with_new_line("Welcome!\n\nLet's begin the journey by type your command here:\n")
    print_without_new_line("> ")

    command = ""
    while True:
        try:
            char = get_char()
            char_id = ord(char)

            # Print each char on the screen
            print_without_new_line(char)
            if char.isprintable():
                command += char

            # if char_id in [3, 4, 26, 27]:
            #     # Exit on ctrl-c, ctrl-d , ctrl-z, or ESC
            #     break
            if char_id in [3, 4]:
                # Exit on ctrl-c, ctrl-d
                break
            if char_id == 12:
                # Clear screen when press ctrl-l
                t.run("clear")
                print_without_new_line("> ")
            if char_id == 127:
                delete_one_char()
                command = command.strip("\n ")
                command = command[:-1]
            if char_id == 10 or char_id == 13:
                print_with_new_line()

                # Hit enter key, so we run the command
                command = command.strip("\n ")
                if len(command) > 0:
                    command_process(command=command)
                command = ""

                print_with_new_line()
                print_without_new_line("> ")
        except Exception as e:
            print(e)


py.make_it_global_runnable(executable_name="Shell")
py.fire(my_shell)
