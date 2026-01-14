# yingshaoxo: I'm using "pyboard v1.1 plus(Frequency 168MHz, SRAM 192KB, Flash 1MB) micropython board" and "2.4inch SPI ili9341 320x240 lcd".
# with micropython1.15

print("Booted.")
from gc import mem_free
print("Has memory of", mem_free()/1024, "KB.")
from time import sleep
sleep(1)
from pyb import LED
def light():
    # use this to debug when no console/shell/terminal/bash
    led = LED(2)
    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)
print("Ready")


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
#display.draw_pixel(150, 150, display.color565(255,0,255))

from gc import mem_free
print("Has memory of", mem_free()/1024, "KB.")


"""
# Handle 3x3 keyboard
"""
from pyb import ADC
keypad_pin = ADC(Pin("A0"))
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
input_mode = 0
screen_sleep = False
max_y = int(320/16) - 1
max_x = int(240/8)
enable_light_cursor = False
light_cursor_flag = 0
cursor_position_y = 0
cursor_position_x = 1
terminal_text_2d_array = []
for y in range(max_y):
    row = []
    for x in range(max_x):
        row.append(" ")
    terminal_text_2d_array.append(row)
terminal_text_2d_array[0][0] = ">"
input_target_list = ["1abc()#", "2def[]@", "3g\bhi{}", "4jkl<>", "5mno\n+-", "6pqr*/=", "7stu'\"`", "8vwx:;", "9yz&|\\"]
"""
1abc()#   2def[]@   3g\bhi{}
4jkl<>    5mno\n+-  6pqr*/=
7stu'\"`   8vwx:;    9yz&|\\
          0_,.?!
"""
temp_input_1 = -1
temp_input_tip = ""
input_char = "\0"
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
        # need to remove first line
        new_row = []
        for x in range(max_x):
            new_row.append(" ")
        for y in range(max_y):
            old_index = y
            new_index = y+1
            if y+1 < max_y:
                terminal_text_2d_array[old_index] = terminal_text_2d_array[new_index]
        terminal_text_2d_array[max_y-1] = new_row
        cursor_position_y = max_y - 1

    collect()

def put_char_into_screen(a_char):
    global terminal_text_2d_array, cursor_position_y, cursor_position_x, max_y, max_x
    make_cursor_position_safe()

    if a_char == "\b":
        terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
        cursor_position_x -= 1
        terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
    elif a_char == "\n":
        terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
        cursor_position_y += 1
        cursor_position_x = 0
    else:
        terminal_text_2d_array[cursor_position_y][cursor_position_x] = a_char
        cursor_position_x += 1

    make_cursor_position_safe()

def new_print(a_string):
    for one in a_string:
        put_char_into_screen(one)
    put_char_into_screen("\n")

def run_shell_command(command):
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
        some_code = 'terminal_arguments = "{}"\n'.format(target_arguments) + "print_ = new_print\n" + some_code
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

def handle_pressed_key(a_number):
    global terminal_text_2d_array, cursor_position_y, cursor_position_x, input_mode, temp_input_1, temp_input_tip, input_char, screen_sleep, one_line_input
    if a_number == -1:
        return

    if a_number == 10:
        if input_mode == 0:
            input_mode = 1
        else:
            input_mode = 0

    if a_number == 12:
        screen_sleep = not screen_sleep
        if screen_sleep:
            display.sleep(True)
            background_light.low()
        else:
            display.sleep(False)
            background_light.high()
        return

    if input_mode == 0:
        # normal mode
        if a_number == 2:
            # up
            pass
        elif a_number == 8:
            # down
            pass
        elif a_number == 4:
            # left
            pass
        elif a_number == 6:
            # right
            pass
        elif a_number == 5:
            # ok
            pass
    else:
        # input mode
        if temp_input_1 == -1:
            if a_number == -1:
                pass
            elif 1 <= a_number <= 9:
                a_index = a_number - 1
                temp_input_tip = "select: " + input_target_list[a_index]
            elif a_number == 11:
                temp_input_tip = "select: 0_,.?!"
            temp_input_1 = a_number
            input_char = "\0"
        else:
            if temp_input_1 == -1:
                pass
            elif 1 <= temp_input_1 <= 9:
                a_index = temp_input_1 - 1
                if a_number-1 < len(input_target_list[a_index]):
                    input_char = input_target_list[a_index][a_number-1]
            elif temp_input_1 == 11:
                if (a_number == 11):
                    input_char = " "
                else:
                    if (a_number-1) < len("0_,.?!"):
                        input_char = list("0_,.?!")[a_number-1]
            temp_input_tip = ""
            temp_input_1 = -1

    if input_char != "\0" and input_char != "":
        if input_char == "\b":
            if cursor_position_x >= 2:
                terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
                cursor_position_x -= 1
                terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
            else:
                pass
            one_line_input = one_line_input[:-1]
        elif input_char == "\n":
            terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
            cursor_position_y += 1
            cursor_position_x = 0
            result = run_python_code(one_line_input)
            one_line_input = ""
            for one in result:
                put_char_into_screen(one)
            cursor_position_y += 1
            cursor_position_x = 0
            put_char_into_screen(">")
        else:
            put_char_into_screen(input_char[0])
            one_line_input += input_char[0]

    terminal_text_2d_array[cursor_position_y][cursor_position_x] = "_"
    temp_text = render_to_1d_text_array()
    display.draw_1d_text(temp_text)

while True:
    pressed_key = get_pressed_key()
    if pressed_key != -1:
        handle_pressed_key(pressed_key)
        from gc import mem_free
        print("Has memory of", mem_free()/1024, "KB.")
        sleep(0.1)
    sleep(0.1)

    if enable_light_cursor:
        if light_cursor_flag == 0:
            terminal_text_2d_array[cursor_position_y][cursor_position_x] = "_"
            display.draw_1d_text(render_to_1d_text_array())
        elif light_cursor_flag == 7:
            terminal_text_2d_array[cursor_position_y][cursor_position_x] = " "
            display.draw_1d_text(render_to_1d_text_array())
        light_cursor_flag += 1
        if light_cursor_flag >= 12:
            light_cursor_flag = 0
