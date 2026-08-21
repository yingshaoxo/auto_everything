# yingshaoxo: I'm using "pyboard v1.1 plus(Frequency 168MHz, SRAM 192KB, Flash 1MB) micropython board" and "2.4inch SPI ili9341 320x240 lcd".
# with micropython1.15

print("Booted.")
from gc import mem_free
print("Has memory of", mem_free()/1024, "KB.")
from time import sleep
sleep(3) #let keyboard init
# use LED to debug when no console/shell/terminal/bash
# from pyb import LED def light(): led = LED(2) while True: led.on() sleep(1) led.off()
sleep(1)
#from pyb import freq
#freq(168000000)
print("Ready")

def string_encode(a_string):
    return str(a_string).replace("\n","%0a").replace("=","%3d")
def string_decode(a_string):
    return str(a_string).replace("%0a","\n").replace("%3d","=")


"""
# Setup the LCD Display module
"""
from pyb import Pin, SPI # for pyboard, it is pyb than machine
from ili9341 import Display

TFT_CS_PIN = "X5"
TFT_CLK_PIN = "X6"
TFT_MISO_PIN = "X7" # not need, no output data come from lcd
TFT_MOSI_PIN = "X8"

TFT_RST_PIN = "X3"
TFT_DC_PIN = "X4"

background_light = Pin("X2", Pin.OUT_PP)
background_light.high()
# this chip do not support ADC input, it is a bug

def create_display():
    spiTFT = SPI(1, SPI.MASTER, baudrate=51200000) # for pyboard, it can not specify sck, mosi, miso. and spi2 is used by SD card
    #spiTFT = Simple_Output_Soft_SPI(baudrate=0, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN), miso=Pin(TFT_MISO_PIN))
    display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN), height=320, width=240, rotation=180)
    return display
display = create_display()
print("Display ready.")

display.draw_1d_text("hi, you.")
display.clear()
#display.draw_pixel(150, 150, display.color565(255,0,255))

from gc import mem_free
print("Has memory of", mem_free()/1024, "KB.")


"""
# Handle 3x3 keyboard
"""
from pyb import ADC
keypad_pin = ADC(Pin("X1"))
pre_defined_button_dict = { '1': 155, '2': 308, '3': 434, '4': 560, '5': 680, '6': 790, '7': 869, '8': 943, '9': 1012, '10': 1080, '11': 1143, '12': 1230 }
def get_pressed_key():
    target_key = -1
    a_value = 0
    for i in range(8):
        a_value += keypad_pin.read()
    a_value = a_value/8
    if a_value > 3000:
        return target_key
    for key, center_value in pre_defined_button_dict.items():
        if ((center_value - 20) <= a_value <= (center_value + 20)):
            # key get pressed
            target_key = int(key)
            break
    return target_key


"""
# Handle terminal mobile phone
"""
from gc import collect
# 0 is normal mode, 1 is input_mode
input_mode = 1
screen_sleep = False
max_y = int(320/16) - 2
max_x = int(240/8)
light_cursor_flag = 0
cursor_position_y = 0
cursor_position_x = 0
terminal_text_2d_array = []
for y in range(max_y):
    row = []
    for x in range(max_x):
        row.append(" ")
    terminal_text_2d_array.append(row)
terminal_text_2d_array[0][0] = " "
input_target_list = [
"1abc()#", "2def[]@", "3g\bhi{}",
"4jkl<>", "5mno\n+-", "6pqr*/=",
"7stu'\"`", "8vwx:;", "9yz&|\\"
]
           #0_,.?!
temp_input_1 = -1
temp_input_tip = ""
temp_input_char = "\0"
one_line_input = ""

def render_to_1d_text_array():
    the_text = ""
    for one in terminal_text_2d_array:
        the_text += "".join(one)
    if input_mode == 0:
        the_text += "input: none"
    else:
        if temp_input_tip == "":
            the_text += "input: abc/123/,.?"
        else:
            the_text += temp_input_tip
    return the_text

def make_cursor_position_safe():
    global terminal_text_2d_array, cursor_position_y, cursor_position_x, max_y, max_x
    if cursor_position_y < 0:
        cursor_position_y = 0
    if cursor_position_x < 0:
        cursor_position_x = 0

    if cursor_position_x >= max_x:
        cursor_position_x = 0
        cursor_position_y += 1

    if cursor_position_y >= max_y:
        ## need to remove first line
        #new_row = []
        #for x in range(max_x):
        #    new_row.append(" ")
        #for y in range(max_y):
        #    old_index = y
        #    new_index = y+1
        #    if y+1 < max_y:
        #        terminal_text_2d_array[old_index] = terminal_text_2d_array[new_index]
        #terminal_text_2d_array[max_y-1] = new_row
        #cursor_position_y = max_y - 1
        #display.clear()
        temp_text = render_to_1d_text_array()
        display.draw_1d_text(temp_text)
        sleep(3)
        clear_screen()

    collect()

def render_and_refresh():
    # display_cache_on_screen
    global terminal_text_2d_array, cursor_position_y, cursor_position_x
    make_cursor_position_safe()
    terminal_text_2d_array[cursor_position_y][cursor_position_x] = "_"
    temp_text = render_to_1d_text_array()
    display.draw_1d_text(temp_text)

def put_char_into_screen_cache(a_char, to_one_line_input=False):
    global terminal_text_2d_array, cursor_position_y, cursor_position_x, max_y, max_x, one_line_input
    make_cursor_position_safe()

    if a_char == "\b":
        terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
        cursor_position_x -= 1
        terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
        if to_one_line_input:
            one_line_input = one_line_input[:-1]
    elif a_char == "\n":
        terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
        cursor_position_y += 1
        cursor_position_x = 0
    else:
        terminal_text_2d_array[cursor_position_y][cursor_position_x] = a_char
        cursor_position_x += 1
        if to_one_line_input:
            one_line_input += a_char

    make_cursor_position_safe()

def clear_screen(**args):
    global terminal_text_2d_array, cursor_position_y, cursor_position_x
    for y in range(0, max_y):
        new_row = []
        for x in range(max_x):
            new_row.append(" ")
        terminal_text_2d_array[y] = new_row
    cursor_position_y = 0
    cursor_position_x = 0
    display.clear()
    display.the_2d_text_cache = None
    collect()

def draw_pixel(y,x,r,g,b):
    display.draw_pixel(x, y, display.color565(r,g,b))

def print_char(a_char):
    put_char_into_screen_cache(a_char)
    render_and_refresh()

def input_char():
    while True:
        #a_char = get_keyboard_char()
        a_char = new_input(no_char_display=True)
        if a_char != "":
            return a_char

def new_print(a_string):
    for one in a_string:
        put_char_into_screen_cache(one)
    put_char_into_screen_cache("\n")
    render_and_refresh()

def real_print(a_string):
    new_print(a_string)

def get_command_list():
    try:
        from os import listdir
    except Exception as e:
        from uos import listdir
    commands_list = listdir("./applications")
    commands_list = [one[:-3] for one in commands_list if one.endswith(".py") and one[0] != '_']
    return commands_list

def run_shell_command(command):
    global display
    commands_list = get_command_list()
    target_command = command.split(" ")[0]
    target_arguments = " ".join(command.split(" ")[1:])
    if target_command in commands_list:
        with open("./applications/"+target_command+".py", "r") as f:
            some_code = f.read()
        some_code = 'terminal_arguments = "{}"\n'.format(target_arguments) + "print_char_ = print_char\n" + "input_char_ = input_char\n" + "print_ = new_print\n" + "real_print_ = real_print\n" + "input_ = new_input\n" + "display_ = display\n" + "run_command_ = run_shell_command\n" + "clear_screen_ = clear_screen\n" + "draw_pixel_ = draw_pixel\n" + some_code
        try:
            exec(some_code)
            return "ok"
        except Exception as e:
            return str(e)
    else:
        return "no"

def run_python_code(code):
    code = code.strip()
    if code == "":
        return ""

    shell_result = run_shell_command(code)
    if shell_result == "ok":
        return ""
    elif shell_result != "no":
        return shell_result

    try:
        return str(eval(code))
    except Exception as e:
        try:
            exec(code)
            return ""
        except Exception as e:
            return str(e)

def add_index_to_char_selection(a_string):
    new_string = ""
    for index, one in enumerate(a_string):
        new_string += str(index+1) + one + " | "
    return new_string

def handle_pressed_key(a_number, keyboard_input_char='\0', no_char_display=False):
    global terminal_text_2d_array, cursor_position_y, cursor_position_x, input_mode, temp_input_1, temp_input_tip, input_char, screen_sleep, one_line_input, temp_input_char
    if no_char_display == True:
        temp_input_char = ""
    should_return = None
    if keyboard_input_char == '\0':
        if a_number == -1:
            return

        if a_number == 10:
            if input_mode == 0:
                input_mode = 1
            else:
                input_mode = 0

        #if a_number == 12:
        #    screen_sleep = not screen_sleep
        #    if screen_sleep:
        #        display.sleep(True)
        #        background_light.low()
        #    else:
        #        display.sleep(False)
        #        background_light.high()
        #    return

        if input_mode == 0:
            # normal mode
            if a_number == 2:
                # up
                temp_input_char = "k"
            elif a_number == 8:
                # down
                temp_input_char = "j"
            elif a_number == 4:
                # left
                temp_input_char = "h"
            elif a_number == 6:
                # right
                temp_input_char = "l"
            elif a_number == 5:
                # insert a char
                temp_input_char = "a"
            elif a_number == 9:
                # insert a line
                temp_input_char = "o"
            elif a_number == 3:
                # delete
                temp_input_char = "x"
            elif a_number == 7:
                # delete a line
                temp_input_char = "d"
            elif a_number == 1:
                # esc and save
                temp_input_char = "$"
            elif a_number == 11:
                # find
                temp_input_char = "/"
        else:
            # english input mode
            if temp_input_1 == -1:
                if a_number == -1:
                    pass
                elif 1 <= a_number <= 9:
                    a_index = a_number - 1
                    temp_input_tip = "select: " + add_index_to_char_selection(input_target_list[a_index])
                elif a_number == 11:
                    temp_input_tip = "select: " + add_index_to_char_selection("0_,.?!")
                temp_input_1 = a_number
                temp_input_char = "\0"

                if a_number == 12:
                    # complete command
                    if " " not in one_line_input:
                        commands = get_command_list()
                        for one_1 in commands:
                            if one_1.startswith(one_line_input):
                                for one_2 in one_1[len(one_line_input):]:
                                    put_char_into_screen_cache(one_2, to_one_line_input=True)
                                temp_input_char = " "
                                temp_input_1 = -1
                                break
            else:
                if temp_input_1 == -1:
                    pass
                elif 1 <= temp_input_1 <= 9:
                    a_index = temp_input_1 - 1
                    if a_number-1 < len(input_target_list[a_index]):
                        temp_input_char = input_target_list[a_index][a_number-1]
                elif temp_input_1 == 11:
                    if (a_number == 11):
                        temp_input_char = " "
                    else:
                        if (a_number-1) < len("0_,.?!"):
                            temp_input_char = list("0_,.?!")[a_number-1]
                temp_input_tip = ""
                temp_input_1 = -1
    else:
        temp_input_char = keyboard_input_char

    if temp_input_char != "\0" and temp_input_char != "":
        if no_char_display == False:
            if temp_input_char == "\n":
                terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
                cursor_position_y += 1
                cursor_position_x = 0
                should_return = str(one_line_input)
                one_line_input = ""
                #cursor_position_y += 1
                #cursor_position_x = 0
            else:
                put_char_into_screen_cache(temp_input_char[0], to_one_line_input=True)
        else:
            should_return = temp_input_char

    render_and_refresh()
    return should_return

def print_heading_symbol(tip):
    for one in tip:
        put_char_into_screen_cache(one)
    render_and_refresh()

from soft_spi import Simple_Input_Soft_SPI
my_input_spi = Simple_Input_Soft_SPI(Pin("Y1"), Pin("Y2"))
def get_keyboard_char():
    my_input_spi.read_until_bytes([0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0])
    data = my_input_spi.read_bytes()
    if my_input_spi.end == 1:
        return ""
    if data != None:
        if data[-1] == 0x04:
            return data[:-1].decode("ascii").lower()
    return ""

def new_input(tip_string="", multiple_line=False, no_char_display=False):
    global a_char_from_keyboard
    print_heading_symbol(tip_string)
    while True:
        sleep(0.05)
        if a_char_from_keyboard == "":
            pressed_key = get_pressed_key()
            if pressed_key != -1:
                result = handle_pressed_key(pressed_key, no_char_display=no_char_display)
                if result != None:
                    return result
                from gc import mem_free
                print("Has memory of", mem_free()/1024, "KB.")
                sleep(0.05)
        else:
            temp_char = a_char_from_keyboard
            result = handle_pressed_key(a_number=-1, keyboard_input_char=temp_char, no_char_display=no_char_display)
            a_char_from_keyboard = ""
            if result != None:
                return result

a_char_from_keyboard = ""
from machine import Timer
a_timer = None
import _thread
def thread_task():
    # this is a fake thread, if main process has no sleep, this process will not go on. in another word, each time should only has one process is doing things.
    global a_char_from_keyboard, a_timer, my_input_spi
    def shit(t):
        my_input_spi.end = 1
    while True:
        a_timer = Timer(period=1000, mode=Timer.ONE_SHOT, callback=shit)
        a_char = get_keyboard_char()
        a_char_from_keyboard = a_char
        while a_char_from_keyboard != "":
            pass
        my_input_spi.end = 0
_thread.start_new_thread(thread_task, ())

while True:
    one_line = new_input(">").strip()
    result = run_python_code(one_line)
    new_print(result)
