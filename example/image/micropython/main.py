print("Booted.")
from time import sleep
sleep(5)
print("Ready")


"""
# Setup the SD card
"""
from machine import Pin, SPI
p32 = Pin(32, Pin.OUT, value=1) # light up a pin to power sd card module with 3.3V

import os
import sdcard # use 'from machine import SDCard; import vfs' will raise problems. the SD card I am using is a 2GB one with fat16 format.

spi = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
try:
    sd = sdcard.SDCard(spi,Pin(21))
    print("mounting...")
    os.mount(sd,"/sda")
    print(os.listdir("/sda"))
    print("Done")
except Exception as e:
    print(e)


"""
# Setup the LCD Display module
"""
from ili9341 import Display, color565
from machine import Pin, SPI

TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(23)
TFT_MISO_PIN = const(19)
TFT_CS_PIN = const(5)

TFT_RST_PIN = const(25)
TFT_DC_PIN = const(26)

def create_display():
    spiTFT = SPI(2, baudrate=51200000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN))
    return display

display = create_display()
print("Display ready.")


"""
# Set up the TFT touch module, which normally a built_in feature of the LCD (ili9341) you buy
"""
from time import sleep, time
from xpt2046 import Touch

def handle_touchscreen_press(x, y):
    """Process touchscreen press events."""
    #y = (display.height - 1) - y
    x = (display.width - 1) - x
    # Display coordinates
    print("clicked: ", y, x)
    
    # Draw dot
    display.draw_pixel(x, y, color565(255,0,255))
    display.draw_ellipse(x, y, 10, 10, color565(255,0,255))

    # Click and rendering
    root_container.click(y, x)
    the_rendering()

spi2 = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
touch = Touch(spi2, cs=Pin(15), int_pin=Pin(33), int_handler=handle_touchscreen_press)

"""
while True:
    result = touch.raw_touch()
    if result != None:
        x, y = touch.normalize(*result)
        handle_touchscreen_press(x, y)
    sleep(0.025)
"""


"""
# Setup the GUI module that comes from python package 'auto_everything', the author is yingshaoxo
"""
from image import GUI, Container

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
display.cache_font_at_boot_time()
print("end boot")
print()

the_rendering()


'''
# sd test

from machine import Pin, SPI
p32 = Pin(32, Pin.OUT, value=1) # light up a pin to power sd card module with 3.3V

import os
import sdcard # use 'from machine import SDCard; import vfs' will raise problems

spi = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
sd = sdcard.SDCard(spi,Pin(21))
print("mounting...")
os.mount(sd,"/sda")
print(os.listdir("/sda"))
print("Done")
'''

'''
#send PWM squre wave

import machine
from time import sleep

pin22 = machine.Pin(22, machine.Pin.OUT)
#"""
pwm22 = machine.PWM(pin22)
pwm22.freq(10)
pwm22.duty(0)
sleep(1)

value = 1023
while True:
    pwm22.duty(value)
    print(value/1023)
    sleep(3)
    value = value - int((value * 0.2))
    if value < 50:
        value = 1023
        #pwm22.duty(0)
        #break
'''


'''
#read anolog value

from time import sleep
from machine import Pin, ADC
adc = ADC(Pin(39))
adc.atten(ADC.ATTN_11DB)

the_number_list = []
def anolog_to_voltage(number):
    global the_number_list
    the_number_list.append(number / 4096 * 3.3)
    if len(the_number_list) >= 20:
        the_number_list = the_number_list[-20:]
    return sum(the_number_list)/len(the_number_list)

while True:
    print(anolog_to_voltage(adc.read()))
    sleep(0.1)
'''

"""
#button and led

from machine import Pin
import time

LED=Pin(2,Pin.OUT) #构建LED对象,开始熄灭
KEY=Pin(0,Pin.IN,Pin.PULL_UP) #构建KEY对象
state=0  #LED引脚状态

#LED状态翻转函数
def fun(KEY):
    global state
    time.sleep_ms(10) #消除抖动
    if KEY.value()==0: #确认按键被按下
        state = not state
        LED.value(state)

KEY.irq(fun,Pin.IRQ_FALLING) #定义中断，下降沿触发
"""
