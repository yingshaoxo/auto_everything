from machine import Pin, ADC
import time

# 4-wire Resistive Touchscreen
# normally your touch screen has pins like: x1,y1,x2,y2
# how do I know that? x1 and x2 should be a single line, 0 resistence. y1 and y2 should be a single line, 0 resistence.
# x1->0v, x2->5v, get y2 value; y1->0v, y2->5v, get x2 value;

# here i use pi pico with micropython1.15 as example.

X1_PIN = 16  # Digital
X2_PIN = 26  # ADC1
Y1_PIN = 17  # Digital
Y2_PIN = 27  # ADC2

def get_raw_touch():
    time.sleep_us(100)  # interval

    # --- read X axis ---
    # X1=3.3V, X2=GND
    x1_p = Pin(X1_PIN, Pin.OUT)
    x2_p = Pin(X2_PIN, Pin.OUT)
    x1_p.value(0)
    x2_p.value(1)

    # Y axis set to high resistence, so only big volatage can cross it
    y1_p = Pin(Y1_PIN, Pin.IN, None)
    y2_p = Pin(Y2_PIN, Pin.IN, None)

    time.sleep_us(100)

    adc_y = ADC(Pin(Y2_PIN))
    x_val = adc_y.read_u16()
    adc_y = None

    # clear X axis setting
    x1_p = Pin(X1_PIN, Pin.IN, None)
    x2_p = Pin(X2_PIN, Pin.IN, None)

    time.sleep_us(100)  # interval

    # --- read Y axis ---
    # Y1=3.3V, Y2=GND
    y1_p = Pin(Y1_PIN, Pin.OUT)
    y2_p = Pin(Y2_PIN, Pin.OUT)
    y1_p.value(0)
    y2_p.value(1)

    # X axis set to high resistence, so only big volatage can cross it
    x1_p = Pin(X1_PIN, Pin.IN, None)
    x2_p = Pin(X2_PIN, Pin.IN, None)

    time.sleep_us(100)

    adc_x = ADC(Pin(X2_PIN))
    y_val = adc_x.read_u16()
    adc_x = None

    # clear Y axis setting
    y1_p = Pin(Y1_PIN, Pin.IN, None)
    y2_p = Pin(Y2_PIN, Pin.IN, None)

    return y_val, x_val

def convert_to_resolution_y_and_x(raw_y, raw_x):
    # you may found the y range has to bind to x range to have 100% accuracy. but i think it is a hardware bug. for example, when 20<x<30,2000<y<3000, when 200<x<240,2000<y<30000.
    min_y = 4600
    max_y = 27555
    min_x = 4700
    max_x = 24555
    y_value = int(((raw_y - min_y) / (max_y - min_y)) * 320)
    x_value = int(((raw_x - min_x) / (max_x - min_x)) * 240)
    return max(0, min(319, y_value)), max(0, min(239, x_value))

while True:
    raw_y, raw_x = get_raw_touch()
    #if 500 < raw_x < 63000 or 4500 < raw_y < 63000:
    y, x = convert_to_resolution_y_and_x(raw_y, raw_x)
    print("Y: {:3d} | X: {:3d}".format(raw_y, raw_x))
    print("Y: {:3d} | X: {:3d}".format(y, x))
    print()
    time.sleep(1)
