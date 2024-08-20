# pico only has 264KB memory, hard to make it render 480x320 screen

print("Booted.")
from time import sleep, time
sleep(5)
print("Ready")


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
    spiTFT = SPI(0, baudrate=60000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN), miso=Pin(TFT_MISO_PIN))
    display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN),
                      height=height, width=width)
    return display

display = create_display()
print("Display ready.")
display.draw_ellipse(30,30,10,10,display.color666(255,0,0))
#a_char_bytes = display.get_char_bytes_by_char("1")
#display.draw_buffer(50, 50, 50+8-1, 50+16-1, a_char_bytes)
sleep(5)



"""
# Setup the GUI module that comes from python package 'auto_everything', the author is yingshaoxo
"""
from image_ import Container

def next_page_click():
    the_text.text="never give up"

the_text = Container(text="Hello everyone! \nThis micropython mobile phone example was made by yingshaoxo.\nYingshaoxo is the god, will you believe it?", text_size=1)

def previous_page_click():
    the_text.text="yingshaoxo"

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
                    width=0.2,
                    text="Menu"
                ),
                Container(
                    width=0.6,
                ),
                Container(
                    width=0.2,
                    text="Back"
                ),
            ]
        ),
        Container(
            height=0.8,
            width=1.0,
            columns=True,
            children=[
                the_text
            ]
        ),
        Container(
            height=0.1,
            width=1.0,
            columns=True,
            children=[
                Container(
                    height=1.0,
                    width=0.25,
                    text="Previous Page",
                    on_click_function=previous_page_click
                ),
                Container(
                    height=1.0,
                    width=0.5,
                ),
                Container(
                    height=1.0,
                    width=0.25,
                    text="Next Page",
                    on_click_function=next_page_click
                )
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
    text_2d_array = root_container.render_as_text()
    end_point = time()
    print("time use: ", (end_point-start_point), "seconds")
    print("rendering finished...")
    print()

    print("start_drawing...")
    start_point = time()
    display.draw_2d_text(text_2d_array)
    end_point = time()
    print("time use: ", (end_point-start_point), "seconds")
    print("drawing_done.")

print("start boot")
#display.cache_font_at_boot_time() #will get memory overflow
print("end boot")
print()

the_rendering()



"""
# Set up the TFT touch module, which normally a built_in feature of the LCD (ili9341) you buy
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
    
    # Draw dot
    display.draw_pixel(x, y, display.color565(255,0,255))
    display.draw_ellipse(x, y, 10, 10, display.color565(255,0,255))

    # Click and rendering
    root_container.click(y, x)
    #the_rendering()

spi2 = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(8))
#spi2 = SPI(0, baudrate=60000000, sck=Pin(6), mosi=Pin(7), miso=Pin(8))
touch = Touch(spi2, height=height, width=width, cs=Pin(9), int_pin=Pin(14), int_handler=handle_touchscreen_press)
