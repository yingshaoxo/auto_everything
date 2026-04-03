"""
# for my keyboard, it has 61 buttons, each button only got 2 pins. when you press, it connects.

1.each button has two pin, one is at up side called pin1, another is at down side called pin2.
2.for row_x, all button pin1 is connected.
3.for column_x, all button pin2 is connected.
4.if row1 has 3v power, when you click a button, i can know what button you clicked by check the column input for each column. (if you pressed a button, that column will become 1, otherwise, 0.)
5.in mathmatics, column is x number, row is y number.
6.maybe I should put shift and ctrl in a splited row, so you can press it while hit other key.
"""
from machine import Pin
from time import sleep

column_pin_list = []
for column_pin_number in range(2,15+1):
    column_pin_list.append(Pin(column_pin_number, Pin.IN, Pin.PULL_DOWN))

row_pin_list = []
for row_pin_number in range(20, 25+1):
    row_pin_list.append(Pin(row_pin_number, Pin.OUT))

def get_a_raw_key_press(only_unpressed=True):
    for row_index, row_pin in enumerate(row_pin_list):
        # set other row to 0
        for temp_row_index, temp_row_pin in enumerate(row_pin_list):
            temp_row_pin.value(0)
        # set the target row to 1
        row_pin.value(1)
        for column_index, column_pin in enumerate(column_pin_list):
            if column_pin.value() == 1:
                # if pin is 1, it is pressed in this special case
                if only_unpressed == True:
                    while True:
                        if column_pin.value() == 0:
                            break
                return "{},{}".format(row_index, column_index)
        row_pin.value(0)
    return ""

key_table = {
    "0,0": 'Escape',
    "1,0": '`',
    "1,1": '1',
    "1,2": '2',
    "1,3": '3',
    "1,4": '4',
    "1,5": '5',
    "1,6": '6',
    "1,7": '7',
    "1,8": '8',
    "1,9": '9',
    "1,10": '0',
    "1,11": '-',
    "1,12": '=',
    "1,13": 'BackSpace',
    "2,0": 'Tab',
    "2,1": 'q',
    "2,2": 'w',
    "2,3": 'e',
    "2,4": 'r',
    "2,5": 't',
    "2,6": 'y',
    "2,7": 'u',
    "2,8": 'i',
    "2,9": 'o',
    "2,10": 'p',
    "2,11": '[',
    "2,12": ']',
    "2,13": '\\',
    "3,0": 'Caps_Lock',
    "3,1": 'a',
    "3,2": 's',
    "3,3": 'd',
    "3,4": 'f',
    "3,5": 'g',
    "3,6": 'h',
    "3,7": 'j',
    "3,8": 'k',
    "3,9": 'l',
    "3,10": ';',
    "3,11": "'",
    "3,12": "Return",
    "4,0": "Shift_L",
    "4,1": "z",
    "4,2": "x",
    "4,3": "c",
    "4,4": "v",
    "4,5": "b",
    "4,6": "n",
    "4,7": "m",
    "4,8": ",",
    "4,9": ".",
    "4,10": "/",
    "4,11": "Shift_R",
    "5,0": "Control_L",
    "5,1": "Super_L",
    "5,2": "Alt_L",
    "5,5": "space",
    "5,8": "Alt_R",
    "5,9": "Menu",
    "5,10": "Control_R",
    "5,11": "Left",
    "5,12": "Up",
    "5,13": "Right",
}
key_table2 = {
    "1,0": '~',
    "1,1": '!',
    "1,2": '@',
    "1,3": '#',
    "1,4": '$',
    "1,5": '%',
    "1,6": '^',
    "1,7": '&',
    "1,8": '*',
    "1,9": '(',
    "1,10": ')',
    "1,11": '_',
    "1,12": '+',
    "2,1": 'Q',
    "2,2": 'W',
    "2,3": 'E',
    "2,4": 'R',
    "2,5": 'T',
    "2,6": 'Y',
    "2,7": 'U',
    "2,8": 'I',
    "2,9": 'O',
    "2,10": 'P',
    "2,11": '{',
    "2,12": '}',
    "2,13": '|',
    "3,1": 'A',
    "3,2": 'S',
    "3,3": 'D',
    "3,4": 'F',
    "3,5": 'G',
    "3,6": 'H',
    "3,7": 'J',
    "3,8": 'K',
    "3,9": 'L',
    "3,10": ':',
    "3,11": '"',
    "4,1": "Z",
    "4,2": "X",
    "4,3": "C",
    "4,4": "V",
    "4,5": "B",
    "4,6": "N",
    "4,7": "M",
    "4,8": "<",
    "4,9": ">",
    "4,10": "?",
    "5,12": "Down",
}
shift_pin = Pin(26, Pin.PULL_DOWN)
use_which_key_table = 0
def get_key_press():
    global use_which_key_table
    raw_key = get_a_raw_key_press()
    result = key_table.get(raw_key)
    if result == "Caps_Lock":
        if use_which_key_table == 1:
            use_which_key_table = 0
        else:
            use_which_key_table = 1

    if shift_pin.value() == 1:
        use_which_key_table = 1
    else:
        use_which_key_table = 0

    if use_which_key_table == 0:
        temp_table = key_table
    else:
        temp_table = key_table2

    if raw_key in temp_table:
        result = temp_table[raw_key]
        return result
    return ""

def get_pressed_raw_character():
    value = get_key_press()
    if value == "BackSpace":
        value = "\b"
    if value == "Return":
        value = "\n"
    if value == "space":
        value = " "
    if value == "Tab":
        value = "    "
    if value != "":
        if (value != "") and ("Shift" not in value):
            print(value, end="")
            return value
    return ""

from machine import Pin
from soft_spi import Simple_Output_Soft_SPI
simple_output = Simple_Output_Soft_SPI(Pin(16), Pin(17))

while True:
    try:
        value = get_pressed_raw_character()
        if value != "":
            #simple_output.write(value.encode("ascii"))
            simple_output.write(bytes([0x01, 0x02]) + value.encode("ascii") + bytes([0x04]))
        sleep(0.01)
    except Exception as e:
        print(e)
