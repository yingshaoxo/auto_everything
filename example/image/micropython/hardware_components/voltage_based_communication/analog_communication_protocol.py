# this code will not work because you can not buy a micro_controller that has digital_to_analog_voltage_converter. in old time, the nes game player, has such device which can send analog voltage as video signal to TV. the modern computer chip basically get cut to garbage, so you can not send and receive simple 0~5v voltage as data.
from time import sleep_us
from machine import PWM
from machine import ADC

def anolog_communication_output_initialization(pin_clock, pin_data):
    pin_clock.init(pin_clock.OUT)
    pin_clock.low()
    pin_data.init(pin_data.OUT)
    pin_data.low()

def anolog_communication_output_write_bytes(pin_clock, pin_data, bytes_data, delay_in_us=20):
    #write(data + bytes([0x04]))
    #duty cycle range is 0-65535
    adds = int(65535 / 255 / 2)
    pwm0 = PWM(pin_data)
    pwm0.freq(125000)
    for a_byte_number in bytes_data:
        pwm0.duty_u16(int((a_byte_number/255) * 65535) + adds)
        pin_clock.high()
        sleep_us(delay_in_us)
        pin_clock.low()
        sleep_us(delay_in_us)
    pwm0.deinit()

def anolog_communication_input_initialization(pin_clock, pin_data):
    pin_clock.init(pin_clock.IN)
    pin_data.init(pin_data.IN)

def anolog_communication_input_read_bytes(pin_clock, pin_data, length=1024):
    a_adc = ADC(pin_data)
    a_list = []
    a_byte = 0x00
    while len(a_list) < length:
        clock_value = 1
        while clock_value == 1:
            clock_value = pin_clock.value()
        while clock_value == 0:
            clock_value = pin_clock.value()
        a_byte = int((a_adc.read_u16()/65535) * 255)
        a_list.append(a_byte)
        if a_byte == 0x04:
            break
    return bytes(a_list)

"""
# sender
import analog_communication_protocol as communicator
from machine import Pin

pin_clock = Pin(26)
pin_data = Pin(27)
communicator.anolog_communication_output_initialization(pin_clock, pin_data)

the_data = b"what is your name?"
the_data = the_data + bytes([0x04])
communicator.anolog_communication_output_write_bytes(pin_clock, pin_data, the_data)
"""

"""
# receiver
import analog_communication_protocol as communicator
from machine import Pin

pin_clock = Pin(26)
pin_data = Pin(27)
communicator.anolog_communication_input_initialization(pin_clock, pin_data)
while True:
    data = communicator.anolog_communication_input_read_bytes(pin_clock, pin_data)
    if data != None:
        if data[-1] == 0x04:
            data = data[:-1]
            with open("test.txt", "ab") as f:
                f.write(data + b"\n")
"""
