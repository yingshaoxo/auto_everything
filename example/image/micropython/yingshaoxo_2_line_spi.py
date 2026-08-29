from time import sleep_us, ticks_ms


class Yingshaoxo_2_line_serial_protocol_interface:
    def __init__(self, clock_pin, data_pin, delay_in_us=120, timeout_in_ms=1000):
        # you can delete the timeout_in_ms code, and use outside timer to do the timeout control, for example, set self.end=0
        self.clock_pin = clock_pin
        self.clock_pin.init(self.clock_pin.IN)
        self.clock_pin.low()
        self.data_pin = data_pin
        self.data_pin.init(self.data_pin.IN)
        self.data_pin.low()
        self.delay_in_us = delay_in_us
        self.timeout_in_ms = timeout_in_ms
        self.end = 0

    def _write_bit(self, bit):
        self.data_pin.value(bit)
        self.clock_pin.high()
        sleep_us(self.delay_in_us)
        self.clock_pin.low()
        sleep_us(self.delay_in_us)

    def write(self, data):
        if isinstance(data, int):
            data = [data]

        # ready for output
        self.clock_pin.init(self.clock_pin.OUT)
        self.data_pin.init(self.data_pin.OUT)

        # notify the data sending
        self.clock_pin.high()
        sleep_us(self.delay_in_us)
        self.clock_pin.low()
        sleep_us(self.delay_in_us)

        # send data
        for byte in data:
            for bit_idx in range(7, -1, -1):
                # write 0x01 as 00000001, the other side first receive 0, then 1.
                bit = (byte >> bit_idx) & 0x01
                self._write_bit(bit)
        self.data_pin.value(0)

        # back to input
        self.clock_pin.low()
        self.clock_pin.init(self.clock_pin.IN)
        self.data_pin.init(self.data_pin.IN)

    def read_0_or_1(self):
        clock_value = 1
        while clock_value == 1:
            clock_value = self.clock_pin.value()
            if self.end == 1:
                return 0
            if (ticks_ms() - self.start_time) > self.timeout_in_ms:
                return 0
        while clock_value == 0:
            clock_value = self.clock_pin.value()
            if self.end == 1:
                return 0
            if (ticks_ms() - self.start_time) > self.timeout_in_ms:
                return 0
        return self.data_pin.value()

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
            if (ticks_ms() - self.start_time) > self.timeout_in_ms:
                return 0x00

    def wait_the_receive_signal(self):
        while self.clock_pin.value() != 1:
            if self.end == 1:
                return 0
        while self.clock_pin.value() != 0:
            if self.end == 1:
                return 0

    def read_bytes(self, length=59, end_with=0x04):
        # sender should at least delay for 1 millisecond
        self.start_time = ticks_ms()
        a_list = []
        a_byte = 0x00
        while len(a_list) < length:
            a_byte = self.read_a_byte()
            a_list.append(a_byte)
            if a_byte == 0x04:
                break
            if self.end == 1:
                return bytes(a_list)
            if (ticks_ms() - self.start_time) > self.timeout_in_ms:
                #return bytes(a_list)
                return None
        return bytes(a_list)


if __name__ == "__main__":
    from machine import Pin
    from time import sleep
    #from yingshaoxo_2_line_spi import Yingshaoxo_2_line_serial_protocol_interface
    my_serial_protocol_interface = Yingshaoxo_2_line_serial_protocol_interface(Pin(20), Pin(21))

    my_serial_protocol_interface.write(bytes([0x01, 0x02]) + b"what is your name?" + bytes([0x04]))
    my_serial_protocol_interface.wait_the_receive_signal()
    data = my_serial_protocol_interface.read_bytes()
    print(data)

    #while True:
    #    my_serial_protocol_interface.wait_the_receive_signal()
    #    data = my_serial_protocol_interface.read_bytes()
    #    print(data)
    #    my_serial_protocol_interface.write(bytes([0x01, 0x02]) + b"yingshaoxo" + bytes([0x04]))
