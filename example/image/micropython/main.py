print("Booted.")

from ili9341 import Display, color565
from machine import Pin, SPI

TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(23)
TFT_MISO_PIN = const(19)
TFT_CS_PIN = const(5)

TFT_RST_PIN = const(25)
TFT_DC_PIN = const(26)

def create_display():
    #spiTFT = SPI(2, baudrate=40000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    spiTFT = SPI(2, baudrate=51200000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN))
    return display
        
display = create_display()
#display.fill_hrect(0, 0, 50, 50, color565(255, 0, 0))
print("Display ready.")


from image import GUI, Container


"""
def change_it_back(*args):
    the_text.text="never give up"
    print("fuck2")

the_text = Container(text="fuck it\nyou got everything you need right now, you don't have to worry about anything.", text_size=1, on_click_function=change_it_back)

def change_it(*args):
    the_text.text="yingshaoxo"
    print("fuck")

root_container = Container(
    height=1.0,
    width=1.0,
    rows=True,
    children=[
        Container(
            height=0.5,
            width=1.0,
            color=[0,255,255,255],
            columns=True,
            children=[
                Container(
                    height=1.0,
                    width=0.5,
                    color=[255,0,255,255],
                    rows=True,
                    children=[
                        the_text
                    ],
                ),
                Container(
                    height=1.0,
                    width=0.25,
                    color=[255,255,0,255],
                    on_click_function=lambda *x: print("hi you")
                ),
                Container(
                    height=1.0,
                    width=0.25,
                    color=[0,255,255,255],
                    on_click_function=change_it
                )
            ]
        ),
    ]
)
"""


#"""
root_container = Container(
    height=1.0,
    width=1.0,
    rows=True,
    color=[0,0,0,255],
    children=[
        Container(
            height=0.2,
            width=1.0,
            color=[255,255,0,255]
        ),
        Container(
            height=0.2,
            width=1.0,
            color=[255,0,255,255]
        ),
        Container(
            height=0.6,
            width=1.0,
            columns=True,
            children=[
                Container(
                    height=1.0,
                    width=0.5,
                    color=[255,0,0,255]
                ),
                Container(
                    height=1.0,
                    width=0.5,
                    color=[0,0,255,255]
                ),
            ]
        ),
    ]
)
#"""

print("start rendering...")
height = 128
width = 96
root_container.parent_height=height
root_container.parent_width=width
image = root_container.render()
print("rendering finished...")
print(image.get_shape())

print("start_drawing...")
#display.draw_image(image, height=height, width=width)
display.draw_image_quick(image, height=height, width=width, step=50)
print("drawing_done.")

    
'''
# sd test, failed
import machine
from time import sleep
import os

print("waiting")
sleep(3)
print("start")

# Slot 2 uses pins sck=18, cs=5, miso=19, mosi=23
# Slot 3 uses pins sck=14, cs=15, miso=12, mosi=13
sd = machine.SDCard(slot=2)#, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12), cs=machine.Pin(15))
os.mount(sd, "/sd")  # mount

print(os.listdir('/sd'))    # list directory contents

os.umount('/sd')     # eject
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