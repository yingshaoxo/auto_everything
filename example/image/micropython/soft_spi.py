from time import sleep_us


class Simple_Output_Soft_SPI:
    def __init__(self, sck, mosi, delay_in_us=20):
        self.sck = sck
        self.sck.init(self.sck.OUT)
        self.sck.low()
        self.mosi = mosi
        self.mosi.init(self.mosi.OUT)
        self.mosi.low()
        self.delay_in_us = delay_in_us

    def _write_bit(self, bit):
        self.mosi.value(bit)
        self.sck.high()
        sleep_us(self.delay_in_us)
        self.sck.low()
        sleep_us(self.delay_in_us)

    def write(self, data):
        if isinstance(data, int):
            data = [data]
        for byte in data:
            for bit_idx in range(7, -1, -1):
                # write 0x01 as 00000001, the other side first receive 0, then 1.
                bit = (byte >> bit_idx) & 0x01
                self._write_bit(bit)
        self.mosi.value(0)


class Simple_Input_Soft_SPI:
    def __init__(self, sck, miso):
        self.sck = sck
        self.sck.init(self.sck.IN)
        self.miso = miso
        self.miso.init(self.miso.IN)
        self.end = 0

    def read_0_or_1(self):
        clock_value = 1
        while clock_value == 1:
            clock_value = self.sck.value()
            if self.end == 1:
                return 0
        while clock_value == 0:
            clock_value = self.sck.value()
            if self.end == 1:
                return 0
        return self.miso.value()

    def read_a_byte(self):
        # will block/stuck program if no data. but quick.
        # sender should at least delay for 1 millisecond.
        a_byte = 0x00
        i = 7;
        get_value = 0
        while 1:
            get_value = self.read_0_or_1()
            a_byte |= (get_value << i)
            i -= 1
            if i < 0:
                return a_byte
            if self.end == 1:
                return 0x00

    def read_until_bytes(self, binary_0_and_1_list=[0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0]):
        # 0x01: 00000001, 0x02: 00000010
        length = len(binary_0_and_1_list)
        temp_list = []
        while 1:
            temp_list.append(self.read_0_or_1())
            if len(temp_list) == length:
                if temp_list == binary_0_and_1_list:
                    return
                temp_list.pop(0)
            if self.end == 1:
                return

    def read_bytes(self, length=59, end_with=0x04):
        # sender should at least delay for 1 millisecond
        # add this before function will increase accuracy: my_input_spi.read_until_bytes()
        a_list = []
        a_byte = 0x00
        while len(a_list) < length:
            a_byte = self.read_a_byte()
            a_list.append(a_byte)
            if a_byte == 0x04:
                break
            if self.end == 1:
                return bytes(a_list)
        return bytes(a_list)


class Complex_Input_Soft_SPI:
    def __init__(self, sck, miso):
        from time import time
        self.time = time

        self.sck = sck
        self.sck.init(self.sck.IN)
        self.miso = miso
        self.miso.init(self.miso.IN)

    def _8_number_to_byte(self, a_list):
        a_byte = 0x00
        i = 0
        while 1:
            a_byte |= (a_list[i] << (7-i))
            i += 1
            if i >= 8:
                break
        return a_byte

    def read_safely(self, timeout=5, start_byte=0x01, end_byte=0x04):
        # the sender should at least delay for 10 milliseconds between clock switch to let the pyboard to receive data.
        end_time = self.time() + timeout
        temp_byte_array = bytearray()
        receive_start = 0
        clock_value = 1
        the_0_or_1_queue = []
        the_0_or_1_queue_index = 0
        while 1:
            while clock_value == 1:
                clock_value = self.sck.value()
                if self.time() > end_time:
                    return bytes(temp_byte_array)
            while clock_value == 0:
                clock_value = self.sck.value()
                if self.time() > end_time:
                    return bytes(temp_byte_array)

            the_value = self.miso.value()

            if receive_start == 0:
                the_0_or_1_queue.append(the_value)
                if len(the_0_or_1_queue) == 8:
                    if (self._8_number_to_byte(the_0_or_1_queue) == start_byte):
                        receive_start = 1
                        the_0_or_1_queue_index = 0
                    else:
                        the_0_or_1_queue.pop(0)
            else:
                the_0_or_1_queue[the_0_or_1_queue_index] = the_value
                the_0_or_1_queue_index += 1
                if the_0_or_1_queue_index >= 8:
                    a_byte = self._8_number_to_byte(the_0_or_1_queue)
                    if (a_byte == end_byte):
                        return bytes(temp_byte_array)
                    else:
                        temp_byte_array.append(a_byte)
                    the_0_or_1_queue_index = 0


#if __name__ == "__main__":
#    TFT_CLK_PIN = Pin('X1')
#    TFT_MOSI_PIN = Pin('X2')
#
#    spiTFT = Simple_Output_Soft_SPI(sck=TFT_CLK_PIN, mosi=TFT_MOSI_PIN)
#
#    spiTFT.write(0x55)
#    spiTFT.write([0xAA, 0x01])


"""
from machine import Pin
from soft_spi import Simple_Input_Soft_SPI, Simple_Output_Soft_SPI
my_input_spi = Simple_Input_Soft_SPI(Pin(20), Pin(21))
my_output_spi = Simple_Output_Soft_SPI(Pin(18), Pin(19))

my_output_spi.write(bytes([0x01, 0x02]) + b"what is your name?" + bytes([0x04]))
# you can use a timer to keep sending data out in another threading

# while True:
#     my_input_spi.read_until_bytes([0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0])
#     data = my_input_spi.read_bytes()
#     print(data)
"""
