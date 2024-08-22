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
from image_ import Container

content_container = Container(text="Hi you.\n\nHere should have an application list that you can click to open.")
def handle_tab_click(tab_name):
    if tab_name == "Files":
        content_container.text="Files view\n\nWhere you can modify files on your disk."
    elif tab_name == "Browser":
        content_container.text="Browser view\n\nWhere you can visit websites."
    elif tab_name == "Terminal":
        content_container.text="Terminal view\n\nWhere you can use command lines."

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
                    on_click_function=lambda x: handle_tab_click("Files")
                ),
                Container(
                    width=0.33,
                    text="Browser",
                    on_click_function=lambda x: handle_tab_click("Browser")
                ),
                Container(
                    width=0.33,
                    text="Terminal",
                    on_click_function=lambda x: handle_tab_click("Terminal")
                ),
            ]
        ),
        Container(
            height=0.9,
            width=1.0,
            rows=True,
            children=[
                content_container
            ]
        ),
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
    display.draw_ellipse(x, y, 10, 10, display.color565(255,0,255))

    # Click and rendering
    root_container.click(y, x)
    the_rendering()

spi2 = SoftSPI(baudrate=9000, polarity=1, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(8))
touch = Touch(spi2, height=height, width=width, cs=Pin(9), int_pin=Pin(14), int_handler=handle_touchscreen_press)
