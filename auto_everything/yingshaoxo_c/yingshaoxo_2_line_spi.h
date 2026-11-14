/* tested in arduino nano v3 (no wifi version, 2k memory, 30kb flash) */ 

#ifndef yingshaoxo_2_line_spi
#define yingshaoxo_2_line_spi

// fake spi input: d2(clock), d3(data)
#define yingshaoxo_2_line_clock_pin 2
#define yingshaoxo_2_line_data_pin 3
int yingshaoxo_2_line_spi_has_been_initialized = 0;
unsigned char yingshaoxo_2_line_spi_input_that_transmit_ends_with_04[68] = { '\0' };
void set_up_yingshaoxo_2_line_spi() {
    pinMode(13, OUTPUT); // LED
    pinMode(yingshaoxo_2_line_clock_pin, INPUT);
    pinMode(yingshaoxo_2_line_data_pin, INPUT);
    yingshaoxo_2_line_spi_has_been_initialized = 1;
}
void set_up_2_line_spi_as_input() {
    pinMode(yingshaoxo_2_line_clock_pin, INPUT);
    pinMode(yingshaoxo_2_line_data_pin, INPUT);
}
int wait_the_receive_signal() {
    while (digitalRead(yingshaoxo_2_line_clock_pin) != 1) {
    }
    while (digitalRead(yingshaoxo_2_line_clock_pin) != 0) {
    }
}
int get_yingshaoxo_2_line_spi_input(unsigned long timeout_in_ms) {
    // the other side will send 0x01 as "00000001", which means this client will first receive 0, ends with 1.
    /*
    >>> io.bytes_to_binary_zero_and_one(bytes([0x00 | (1 << 0x07)]))
    ['10000000']
    >>> io.bytes_to_binary_zero_and_one(bytes([0x00 | (1 << 0x06)]))
    ['01000000']
    >>> io.bytes_to_binary_zero_and_one(bytes([0x00 | (1 << 0x05)]))
    ['00100000']
    */

    if (yingshaoxo_2_line_spi_has_been_initialized == 0) {
        // call set_up_yingshaoxo_2_line_spi() first
        return 0;
    }

    unsigned long start_time = millis(); //millisecond, 1000 = 1 second
    int index = 0;
    int clock_value = 0;
    int data_value = 1;
    unsigned char temp_byte = 0x00;
    int temp_binary_counting = 7;

    while (1) {
        while (clock_value == 1) {
            clock_value = digitalRead(yingshaoxo_2_line_clock_pin);
            if ((millis()-start_time) > timeout_in_ms) { yingshaoxo_2_line_spi_input_that_transmit_ends_with_04[index+1] = '\0'; return index; }
        }
        while (clock_value == 0) {
            clock_value = digitalRead(yingshaoxo_2_line_clock_pin);
            if ((millis()-start_time) > timeout_in_ms) { yingshaoxo_2_line_spi_input_that_transmit_ends_with_04[index+1] = '\0'; return index; }
        }

        data_value = digitalRead(yingshaoxo_2_line_data_pin);
        digitalWrite(13, !digitalRead(13)); //LED

        // temo_binary_counting: 7,6,5,...,0
        temp_byte |= (data_value << temp_binary_counting);
        temp_binary_counting -= 1;
        if (temp_binary_counting < 0) {
            temp_binary_counting = 7;

            if (temp_byte == 0x04) {
                yingshaoxo_2_line_spi_input_that_transmit_ends_with_04[index] = '\0';
                return index;
            }

            yingshaoxo_2_line_spi_input_that_transmit_ends_with_04[index] = temp_byte;
            temp_byte = 0x00;
            index += 1;

            if (index >= 63) {
                yingshaoxo_2_line_spi_input_that_transmit_ends_with_04[64] = '\0';
                return 64;
            }
        }
    }
}

void set_up_2_line_spi_as_output() {
    pinMode(yingshaoxo_2_line_clock_pin, OUTPUT);
    pinMode(yingshaoxo_2_line_data_pin, OUTPUT);
    digitalWrite(yingshaoxo_2_line_clock_pin, LOW);
    digitalWrite(yingshaoxo_2_line_data_pin, LOW);
}
void send_yingshaoxo_2_line_spi_a_byte(unsigned char a_byte, int delay_in_millisecond) {
    int temp_0_or_1 = 0;
    unsigned char temp_binary_index = 0;
    while (1) {
        temp_0_or_1 = a_byte & (1 << (7-temp_binary_index));
        digitalWrite(yingshaoxo_2_line_data_pin, temp_0_or_1);
        digitalWrite(yingshaoxo_2_line_clock_pin, HIGH);
        if (delay_in_millisecond == 0) {
            //delay_in_us(2);
            //delayMicroseconds(2); // not working
        } else {
            delay(delay_in_millisecond);
        }
        digitalWrite(yingshaoxo_2_line_clock_pin, LOW);
        if (delay_in_millisecond == 0) {
            //delay_in_us(2);
            //delayMicroseconds(2); // not working
        } else {
            delay(delay_in_millisecond);
        }
        digitalWrite(13, !digitalRead(13)); // LED
        temp_binary_index += 1;
        if (temp_binary_index >= 8) {
            break;
        }
    }
}
void send_yingshaoxo_2_line_spi_output(unsigned char *data, int delay_in_millisecond) {
    if (yingshaoxo_2_line_spi_has_been_initialized == 0) {
        // call set_up_yingshaoxo_2_line_spi() first
        return 0;
    }

    // ready for output
    set_up_2_line_spi_as_output();

    // notify the data sending
    digitalWrite(yingshaoxo_2_line_clock_pin, HIGH);
    if (delay_in_millisecond == 0) {
        //delay_in_us(2);
    } else {
        delay(delay_in_millisecond);
    }
    digitalWrite(yingshaoxo_2_line_clock_pin, LOW);
    if (delay_in_millisecond == 0) {
        //delay_in_us(2);
    } else {
        delay(delay_in_millisecond);
    }

    // send data
    send_yingshaoxo_2_line_spi_a_byte(0x01, delay_in_millisecond);
    send_yingshaoxo_2_line_spi_a_byte(0x02, delay_in_millisecond);
    unsigned int index = 0;
    unsigned char a_byte = 0x00;
    while (1) {
        a_byte = data[index];
        send_yingshaoxo_2_line_spi_a_byte(a_byte, delay_in_millisecond);
        index += 1;
        if (a_byte == '\0') {
            break;
        }
        if (a_byte == 0x04) {
            break;
        }
        if (index >= 63) {
            break;
        }
    }
    send_yingshaoxo_2_line_spi_a_byte(0x04, delay_in_millisecond);

    // back to input
    set_up_2_line_spi_as_input();
}

#endif

/*
void setup() {
    set_up_yingshaoxo_2_line_spi();
}

void loop() {
    send_yingshaoxo_2_line_spi_output("hi, you!", 1);
    int result_index = get_yingshaoxo_2_line_spi_input(1000);
    if (result_index >= 0) {
        clear_the_screen();
        smart_print_string(0, 0, yingshaoxo_2_line_spi_input_that_transmit_ends_with_04);
    }
}
*/ 



/*
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

*/
