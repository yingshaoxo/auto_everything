print("Booted.")
from time import sleep, time
sleep(5)
print("Ready")
try:
    from machine import freq
    freq(70000000) #lower cpu frequency to save power
except Exception as e:
    print(e)


"""
# Setup the LCD Display module
"""
from fake_ili9488 import Ili9488_Display as Display
from machine import Pin, SPI

TFT_CLK_PIN = const(2)
TFT_MOSI_PIN = const(3)
TFT_MISO_PIN = const(4)
TFT_CS_PIN = const(5)

TFT_DC_PIN = const(0)
TFT_RST_PIN = const(1)

height=480
width=320

def create_display():
    baudrate = 60000000
    spiTFT = SPI(0, baudrate=baudrate, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN), miso=Pin(TFT_MISO_PIN))
    display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN),
                      height=height, width=width)
    return display

display = create_display()
print("Display ready.")



"""
# Setup the GUI module that comes from python package 'auto_everything', the author is yingshaoxo
"""
from image_ import Container, Container_Helper
container_helper = Container_Helper()


content_container = Container(text="Hi you.\n\nHere should have an application list that you can click to open.")
render_as_text_component_backup = content_container._render_as_text_component_list
def handle_tab_click(tab_name):
    if tab_name == "Files":
        content_container.text="Files view\n\nWhere you can modify files on your disk."
        content_container._render_as_text_component_list = render_as_text_component_backup
        show_or_hide_keyboard(False)
    elif tab_name == "Browser":
        content_container.text="Browser view\n\nWhere you can visit websites."
        content_container._render_as_text_component_list = render_as_text_component_backup
        show_or_hide_keyboard(False)
    elif tab_name == "Terminal":
        #content_container.text="Terminal view\n\nWhere you can use command lines."
        content_container.text=""
        from applications.terminal import Terminal_App
        sub_window_height = None
        sub_window_width = None
        for child in container_helper.iterate_child_container(root_container):
            if child.information.get("id") == "content_box":
                print(child.real_property_dict)
                sub_window_height = child.real_property_dict["height"]
                sub_window_width = child.real_property_dict["width"]
                break

        terminal_app = Terminal_App(height=sub_window_height, width=sub_window_width)

        def handle_child_click(a_container, y, x):
            terminal_app.handle_touch_function(y, x)
        content_container.on_click_function=handle_child_click

        def handle_child_key_press(char):
            terminal_app.handle_keyboard_function(char)
        keyboard_callback_function_dict["terminal_app"] = handle_child_key_press

        def new_render_as_text_component_function(*arguments):
            content_container.text = terminal_app.render_as_text()
            if len(arguments) == 3:
                _, top_, left_ = arguments
            elif len(arguments) == 2:
                top_, left_ = arguments
            elif len(arguments) == 0:
                top_, left_ = 0, 0
            return render_as_text_component_backup(top_, left_)
        content_container._render_as_text_component_list = new_render_as_text_component_function
        show_or_hide_keyboard(True)


keyboard_callback_function_dict = {}
def handle_keyboard_press(a_container, y, x):
    the_char = a_container.text
    if the_char == " " or the_char == "":
        return
    #print("get key press:", the_char)
    if the_char == "Space":
        the_char = " "
    elif the_char == "Enter":
        the_char = "\n"
    for a_function in keyboard_callback_function_dict.values():
        try:
            a_function(the_char)
        except Exception as e:
            print(e)

from applications._keyboard import A_Keyboard
a_keyboard = A_Keyboard()
def get_keyboard_container():
    component_list = []

    def handle_special_keyboard_press(a_element, y, x):
        a_char = a_keyboard.handle_touch_function(y,x)
        handle_keyboard_press(Container(text=a_char), y, x)

    component_list.append(
        Container(
            height=6/8,
            width=1.0,
            rows=False,
            columns=True,
            children=[
                Container(height=1.0, width=0.15),
                Container(
                    height=1.0, width=0.7, rows=True,
                    text=a_keyboard.render_as_text(),
                    center_text=False,
                    on_click_function=handle_special_keyboard_press
                ),
                Container(height=1.0, width=0.15)
            ]
        )
    )

    component_list.append(
        Container(
            height=8,
            width=1.0,
            rows=True,
            columns=False,
        )
    )

    command_text = """
Esc Tab Space Del Enter
    """.strip()
    command_component_list = []
    for token in command_text.split(" "):
        command_component_list.append(
            Container(
                height=1.0,
                width=1/5,
                rows=True,
                columns=False,
                text=token,
                on_click_function=handle_keyboard_press
            )
        )
    component_list.append(
        Container(
            height=1/8,
            width=1.0,
            rows=False,
            columns=True,
            children=command_component_list
        )
    )

    component_list.append(
        Container(
            height=1/8,
            width=1.0,
            rows=False,
            columns=True,
            text="keyboard",
            on_click_function=lambda *x: show_or_hide_keyboard()
        )
    )

    keyboard_container = Container(
        height=0.2,
        width=1.0,
        rows=True,
        children=component_list
    )
    return keyboard_container

keyboard_is_showing = False
keyboard_container = get_keyboard_container()
bottom_keyboard_trigger = Container(
    height=0.05, width=1.0,
    children=[
        Container(
            height=16,
            width=1.0,
            rows=True,
            columns=False,
        ),
        Container(height=16, text="keyboard", on_click_function=lambda *x: show_or_hide_keyboard())
    ]
)
def show_or_hide_keyboard(status=None):
    global keyboard_is_showing
    if status == None:
        status = not keyboard_is_showing
        keyboard_is_showing = status
    if status == True:
        keyboard_container.height = 0.3
        root_container.children[1].height = 0.6
        root_container.children[2] = keyboard_container
        keyboard_is_showing = status
    else:
        bottom_keyboard_trigger.height = 0.05
        root_container.children[1].height = 0.85
        root_container.children[2] = bottom_keyboard_trigger
        keyboard_is_showing = status


root_container = Container(
    height=1.0,
    width=1.0,
    rows=True,
    children=[
        Container(
            height=0.1,
            width=1.0,
            columns=True,
            children=[
                Container(
                    width=0.33,
                    text="Files",
                    on_click_function=lambda *x: handle_tab_click("Files")
                ),
                Container(
                    width=0.33,
                    text="Browser",
                    on_click_function=lambda *x: handle_tab_click("Browser")
                ),
                Container(
                    width=0.33,
                    text="Terminal",
                    on_click_function=lambda *x: handle_tab_click("Terminal")
                ),
            ]
        ),
        Container(
            height=0.85,
            width=1.0,
            rows=True,
            information={"id": "content_box"},
            children=[
                content_container
            ]
        ),
        bottom_keyboard_trigger
    ]
)

root_container.parent_height=height
root_container.parent_width=width


def the_rendering():
    print()
    print("start rendering...")
    start_point = time()
    text_1d_string = root_container.render_as_text(pure_text=True, one_dimention_text=True)
    end_point = time()
    print("render time use: ", (end_point-start_point), "seconds")
    print("rendering finished...")
    print()

    print("start_drawing...")
    start_point = time()
    display.draw_1d_text(text_1d_string)
    end_point = time()
    print("draw time use: ", (end_point-start_point), "seconds")
    print("drawing_done.")

the_rendering()


"""
# Set up the TFT touch module, which normally a built_in feature of the LCD (ili9341 or ili9488) you buy
"""
from time import sleep, time
from xpt2046 import Touch
from machine import Pin, SoftSPI

def handle_touchscreen_press(x, y):
    """Process touchscreen press events."""
    #y = (display.height - 1) - y
    x = (display.width - 1) - x
    # Display coordinates
    print("clicked: ", y, x)

    # Draw dot circle
    display.draw_pixel(x, y, display.color565(255,0,255))
    display.draw_ellipse(x, y, 5, 5, display.color565(255,0,255))

    # Click and rendering
    root_container.click(y, x)
    the_rendering()

spi2 = SoftSPI(baudrate=9000, polarity=1, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(8))
touch = Touch(spi2, height=height, width=width, cs=Pin(9), int_pin=Pin(14), int_handler=handle_touchscreen_press)
