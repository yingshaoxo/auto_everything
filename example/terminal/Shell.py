#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
import os, re
import tty, termios, sys

from typing import Any

from auto_everything.python import Python
from auto_everything.terminal import Terminal
from auto_everything.disk import Store

py = Python()
t = Terminal(debug=False)

store = Store("auto_everything_shell")
history_command_list_store_key = "history_command_list"
final_search_result_store_key = "final_search_result"

MODE = None

def search_a_command(text: str) -> list[str]:
    keyword_list = text.split(" ")
    history_command_list: list[str] = store.get(history_command_list_store_key, [])

    match_commands = []
    for command in history_command_list:
        ok = True
        for keyword in keyword_list:
            if keyword not in command:
                ok = False
                break
        if ok:
            match_commands.append(command)

    return match_commands

def add_a_command_to_history(command: str):
    command = command.strip()
    history_command_list: list[str] = store.get(history_command_list_store_key, [])
    if command not in history_command_list:
        history_command_list.append(command)
        store.set(history_command_list_store_key, history_command_list)
        
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

def print_with_new_line(text:Any=""):
    print(text, end="\n", flush=True)

def monitor_the_terminal_keyboard(callback_function_that_takes_input_string, exit_ascii_code:list[int]=[10, 12]):
    command = ""
    while True:
        try:
            char = get_char()
            char_id = ord(char)

            if char_id in [27, 91]: #unknown
                continue
            if char_id in [68, 65, 67, 66]: #arrow left,up,right,down
                continue
            if char_id in exit_ascii_code:
                break

            # Print each char on the screen
            print_without_new_line(char)
            if char.isprintable():
                command += char

            if char_id in [3, 4]:
                # Exit on ctrl-c, ctrl-d
                break
            if char_id == 12:
                # Clear screen when press ctrl-l
                break
            if char_id == 16:
                # Ctrl+p
                break
            if char_id == 127:
                # Delete key
                delete_one_char()
                command = command.strip("\n ")
                command = command[:-1]
            if char_id == 10 or char_id == 13:
                break

            callback_function_that_takes_input_string(command)
        except Exception as e:
            print(e)

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
    add_a_command_to_history(command=command)

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

            # print_with_new_line(char_id)
            # if char_id in [3, 4]:
            #     # Exit on ctrl-c, ctrl-d
            #     break
            # continue

            if char_id in [27, 91]: #unknown
                continue
            if char_id in [68, 65, 67, 66]: #arrow left,up,right,down
                continue

            # Print each char on the screen
            print_without_new_line(char)
            if char.isprintable():
                command += char

            if char_id in [3, 4]:
                # Exit on ctrl-c, ctrl-d
                break
            if char_id == 12:
                # Clear screen when press ctrl-l
                t.run("clear")
                print_without_new_line("> ")
            if char_id == 16:
                # Ctrl+P to make a search for history commands
                result = ""
                def search_it(the_command):
                    t.run("clear")

                    result = "\n".join(search_a_command(the_command))
                    store.set(final_search_result_store_key, result)
                    print_without_new_line(result)

                    print_without_new_line("\n\n" + "__________" + "\n\n")

                    print_without_new_line("> Search: " + the_command )

                t.run("clear")
                print_without_new_line("> Search: ")
                monitor_the_terminal_keyboard(
                    search_it
                )

                t.run("clear")
                print_with_new_line(store.get(final_search_result_store_key, ""))
                print_with_new_line()
                print_without_new_line("> ")
            if char_id == 127:
                # Delete key
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
