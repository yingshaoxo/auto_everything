# pico only has 264KB memory

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

TFT_RST_PIN = const(13)
TFT_DC_PIN = const(12)

def create_display():
    spiTFT = SPI(0, baudrate=60000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN))
    return display

display = create_display()
print("Display ready.")
display.draw_ellipse(30,30,10,10,display.color666(255,0,0))
sleep(5)



"""
# Setup the GUI module that comes from python package 'auto_everything', the author is yingshaoxo
"""
from image_ import GUI, Container

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
            height=0.2,
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
            height=0.6,
            width=1.0,
            columns=True,
            children=[
                the_text
            ]
        ),
        Container(
            height=0.2,
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


height = 320 #128 #256
width = 240 #96 #192
root_container.parent_height=height
root_container.parent_width=width

def the_rendering():
    print()
    print("start rendering...")
    start_point = time()
    text_2d_array = root_container.render_as_text()
    #image = root_container.render()
    end_point = time()
    print("time use: ", (end_point-start_point), "seconds")
    print("rendering finished...")
    print()

    print("start_drawing...")
    start_point = time()
    #display.clear()
    display.draw_2d_text(text_2d_array)
    #display.draw_image(image)
    end_point = time()
    print("time use: ", (end_point-start_point), "seconds")
    print("drawing_done.")

print("start boot")
#display.cache_font_at_boot_time()
print("end boot")
print()

the_rendering()
