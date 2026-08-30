global_print_cache = ""

try:
    import os
    os.mkdir("./applications")
except Exception as e:
    pass

class Display():
    def clear(self):
        try:
            import os
            os.system("clear")
        except Exception as e:
            for i in range(10):
                print("\n")
display = Display()

def clear_screen():
    display.clear()

def print_char(a_char):
    print(a_char, end="", flush=True)

def real_print(a_string):
    print(a_string, end="", flush=True)

def input_char():
    import sys,tty,termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    except Exception as e:
        print(e)
        return ""
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ""

def new_print(a_string):
    global global_print_cache
    global_print_cache += a_string + "\n"

def new_input(a_string):
    return input(a_string)

def run_shell_command(command):
    global global_print_cache
    try:
        from os import listdir
    except Exception as e:
        from uos import listdir
    commands_list = listdir("./applications")
    commands_list = [one[:-3] for one in commands_list if one.endswith(".py") and one[0] != '_']
    del listdir
    target_command = command.split(" ")[0]
    target_arguments = " ".join(command.split(" ")[1:])
    if target_command in commands_list:
        with open("./applications/"+target_command+".py", "r") as f:
            some_code = f.read()
        some_code = 'terminal_arguments = "{}"\n'.format(target_arguments) + "input_char_ = input_char\n" + "print_char_ = print_char\n" + "print_ = new_print\n" + "real_print_ = real_print\n" + "input_ = new_input\n" + "display_ = display\n" + "run_command_ = run_shell_command\n" + "clear_screen_ = clear_screen\n" + some_code
        try:
            exec(some_code)
            temp = global_print_cache[:]
            global_print_cache = ""
            return temp.strip()
        except Exception as e:
            return str(e)
    else:
        return "no"

def run_python_code(code):
    code = code.strip()
    if code == "":
        return ""

    shell_result = run_shell_command(code)
    if shell_result != "no":
        return shell_result

    try:
        return str(eval(code))
    except Exception as e:
        try:
            exec(code)
            return ""
        except Exception as e:
            return str(e)

print("\nWelcome yingshaoxo python linux shell!")
while True:
    text_data = input(">")
    result = run_python_code(text_data)
    print(result)
    print()
