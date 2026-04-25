# yingshaoxo: I'm using "yd_rp2040_lite_pi_pico(2M Flash, 264KB Memory) micropython board"
# pico only has 264KB memory
# with micropython1.15

print("Booted.")
from time import sleep, time
sleep(1)
print("Ready\n")
from machine import freq
freq(240000000)
from gc import collect, mem_free


from machine import Pin
from soft_spi import Simple_Output_Soft_SPI
simple_output = Simple_Output_Soft_SPI(Pin(16), Pin(17), 200)
def send_command(data):
    simple_output.write(bytes([0x01, 0x02]) + data.encode("utf-8") + bytes([0x04]))

from soft_spi import Simple_Input_Soft_SPI
my_input_spi = Simple_Input_Soft_SPI(Pin(14), Pin(15))
def get_keyboard_char():
    my_input_spi.read_until_bytes([0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0])
    data = my_input_spi.read_bytes()
    if data != None:
        if data[-1] == 0x04:
            try:
                return data[:-1].decode("utf-8").lower()
            except Exception as e:
                print(e)
                return ""
    return ""


global_print_cache = ""

class Display():
    def clear(self):
        send_command("clear_screen:")
        sleep(0.25)
display = Display()

def clear_screen():
    display.clear()

def print_char(a_char):
    send_command("print_char:"+a_char)
    sleep(0.05)

def input_char():
    while True:
        a_char = get_keyboard_char()
        if a_char != "":
            return a_char

def print_char_with_y_and_x(y, x, a_char):
    send_command("print_char_with_y_and_x:{y},{x},{a_char}".format(y=y,x=x,a_char=a_char))

def draw_a_pixel(y, x, r, g, b):
    send_command("draw_a_pixel:{},{},{},{},{}".format(y,x,r,g,b))

def new_print(a_string):
    global global_print_cache
    global_print_cache += a_string + "\n"

def real_print(a_string):
    if type(a_string) == bytes:
        a_string = a_string.decode("utf-8")
    a_string = "\n"+a_string
    send_command("print_string:"+a_string)
    sleep(0.2)

def new_input(a_string):
    if len(a_string) != 0:
        real_print(a_string)
    one_line_input = ""
    while True:
        a_char = get_keyboard_char()
        if a_char == "\b":
            one_line_input = one_line_input[:-1]
            print_char("\b")
            continue
        if a_char == "\n":
            return one_line_input
        if a_char != "":
            one_line_input += a_char
            print_char(a_char)

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
        some_code = 'terminal_arguments = "{}"\n'.format(target_arguments) + "print_char_ = print_char\n" + "input_char_ = input_char\n" + "print_ = new_print\n" + "real_print_ = real_print\n" + "input_ = new_input\n" + "display_ = display\n" + "run_command_ = run_shell_command\n" + some_code
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

screen_text = "welcome yingshaoxo python linux shell!"
def handle_one_input_char(a_char):
    global screen_text
    if a_char == "\b":
        screen_text = screen_text[:-1]
        screen_text = show_text_on_screen(screen_text, delete_one=True)
    else:
        screen_text += a_char
        screen_text = show_text_on_screen(screen_text)
    if type(value) == str:
        simple_output.write(bytes([0x01, 0x02]) + a_char.encode("utf-8") + bytes([0x04]))
    collect()
    print("current memory: ", mem_free()/1024, "KB.")

print(screen_text)
while True:
    text_data = new_input(">")
    result = run_python_code(text_data)
    real_print("\n" + result + "\n")
    collect()
