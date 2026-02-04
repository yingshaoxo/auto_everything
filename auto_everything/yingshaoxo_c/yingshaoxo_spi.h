/* tested in arduino nano v3 (no wifi version, 2k memory, 30kb flash) */ 

#ifndef yingshaoxo_spi
#define yingshaoxo_spi

// fake spi input: d4(clock), d5(data)
#define yingshaoxo_spi_input_clock_pin 4
#define yingshaoxo_spi_input_data_pin 5
unsigned char yingshaoxo_spi_input_that_transmit_ends_with_04[68] = { '\0' };
unsigned int yingshaoxo_spi_input_has_been_initialized = 0;
void set_up_yingshaoxo_spi_input() {
    pinMode(13, OUTPUT); // LED
    pinMode(yingshaoxo_spi_input_clock_pin, INPUT);
    pinMode(yingshaoxo_spi_input_data_pin, INPUT);
    yingshaoxo_spi_input_has_been_initialized = 1;
}
int get_yingshaoxo_spi_input_binary_0_or_1() {
    int clock_value = 1;
    while (clock_value == 1) {
        clock_value = digitalRead(yingshaoxo_spi_input_clock_pin);
    }
    while (clock_value == 0) {
        clock_value = digitalRead(yingshaoxo_spi_input_clock_pin);
    }
    return digitalRead(yingshaoxo_spi_input_data_pin);
}
unsigned char get_yingshaoxo_spi_input_single_byte() {
    unsigned char a_byte = 0x00;
    int i = 7;
    for (i; i>=0; i--) {
        a_byte |= (get_yingshaoxo_spi_input_binary_0_or_1() << i);
    }
    return a_byte;
}
int get_yingshaoxo_spi_input_simple_bytes() {
    // data must start with 0x01, 0x02, end with 0x04
    // sender must delay for 20us. 1 second == 1000 ms; 1 ms = 1000us;
    // receive_data is valid only when return value > 0
    unsigned char a_byte = '\0';
    int i = 0;
    while (1) {
        a_byte = get_yingshaoxo_spi_input_single_byte();
        yingshaoxo_spi_input_that_transmit_ends_with_04[i] = a_byte;
        if (a_byte == 0x04) {
            yingshaoxo_spi_input_that_transmit_ends_with_04[i] = '\0';
            break;
        }
        if (i >= 63) {
            yingshaoxo_spi_input_that_transmit_ends_with_04[64] = '\0';
            return 0;
        }
        i += 1;
    }
    return i;
}
unsigned char yingshaoxo_spi_input_starting_0_and_1_array[16] = { 0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0 };
unsigned char yingshaoxo_spi_input_temp_0_and_1_array[16] = { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };
int _get_yingshaoxo_spi_input_is_two_list_equal() {
    int result = 1;
    int i = 0;
    while (i < 16) {
        if (yingshaoxo_spi_input_starting_0_and_1_array[i] != yingshaoxo_spi_input_temp_0_and_1_array[i]) {
            result = 0;
            break;
        }
        i += 1;
    }
    return result;
}
int get_yingshaoxo_spi_input_bytes(unsigned char end_byte) {
    // data must start with 0x01, 0x02
    int fucking_index = 0;
    int shit_index = 0;
    unsigned char a_byte = '\0';
    int start = 0;
    int i = 0;
    while (1) {
        if (start == 0) {
            while (1) {
                int value = get_yingshaoxo_spi_input_binary_0_or_1();
                yingshaoxo_spi_input_temp_0_and_1_array[fucking_index] = value;
                fucking_index += 1;
                if (fucking_index >= 16) {
                    if (_get_yingshaoxo_spi_input_is_two_list_equal() == 1) {
                        start = 1;
                        break;
                    }

                    fucking_index = 15;
                    shit_index = 1;
                    while (shit_index < 16) {
                        yingshaoxo_spi_input_temp_0_and_1_array[shit_index-1] = yingshaoxo_spi_input_temp_0_and_1_array[shit_index];
                        shit_index += 1;
                    }
                }
            }
        } else {
            a_byte = get_yingshaoxo_spi_input_single_byte();
            yingshaoxo_spi_input_that_transmit_ends_with_04[i] = a_byte;
            if (a_byte == end_byte) {
                yingshaoxo_spi_input_that_transmit_ends_with_04[i] = '\0';
                break;
            }
            if (i >= 63) {
                yingshaoxo_spi_input_that_transmit_ends_with_04[64] = '\0';
                break;
            }
            i += 1;
        }
    }
    return i;
}
int get_yingshaoxo_spi_input(unsigned long timeout) {
    // the other side will send 0x01 as "00000001", which means this client will first receive 0, ends with 1.
    /*
    >>> io.bytes_to_binary_zero_and_one(bytes([0x00 | (1 << 0x07)]))
    ['10000000']
    >>> io.bytes_to_binary_zero_and_one(bytes([0x00 | (1 << 0x06)]))
    ['01000000']
    >>> io.bytes_to_binary_zero_and_one(bytes([0x00 | (1 << 0x05)]))
    ['00100000']
    */
    if (yingshaoxo_spi_input_has_been_initialized == 0) {
        // call set_up_yingshaoxo_spi_input() first
        return 0;
    }

    unsigned long start_time = millis(); //millisecond, 1000 = 1 second
    int index = 0;
    int clock_value = 0;
    int data_value = 1;
    unsigned char temp_byte = 0x00;
    int temp_binary_counting = 7;

    while (1) {
        while (clock_value == 0) {
            clock_value = digitalRead(yingshaoxo_spi_input_clock_pin);
            if ((millis()-start_time) > timeout) { yingshaoxo_spi_input_that_transmit_ends_with_04[index+1] = '\0'; return index; }
        }
        while (clock_value == 1) {
            clock_value = digitalRead(yingshaoxo_spi_input_clock_pin);
            if ((millis()-start_time) > timeout) { yingshaoxo_spi_input_that_transmit_ends_with_04[index+1] = '\0'; return index; }
        }

        data_value = digitalRead(yingshaoxo_spi_input_data_pin);
        digitalWrite(13, !digitalRead(13)); //LED

        // temo_binary_counting: 7,6,5,...,0
        temp_byte |= (data_value << temp_binary_counting);
        temp_binary_counting -= 1;
        if (temp_binary_counting < 0) {
            temp_binary_counting = 7;

            if (temp_byte == 0x04) {
                yingshaoxo_spi_input_that_transmit_ends_with_04[index] = '\0';
                return index;
            }

            yingshaoxo_spi_input_that_transmit_ends_with_04[index] = temp_byte;
            temp_byte = 0x00;
            index += 1;

            if (index >= 63) {
                yingshaoxo_spi_input_that_transmit_ends_with_04[64] = '\0';
                return 64;
            }
        }
    }
}

// fake spi output: d2(clock), d3(data)
#define yingshaoxo_spi_output_clock_pin 2
#define yingshaoxo_spi_output_data_pin 3
unsigned int yingshaoxo_spi_output_has_been_initialized = 0;
void set_up_yingshaoxo_spi_output() {
    pinMode(13, OUTPUT); // LED
    pinMode(yingshaoxo_spi_output_clock_pin, OUTPUT);
    pinMode(yingshaoxo_spi_output_data_pin, OUTPUT);
    digitalWrite(yingshaoxo_spi_output_clock_pin, LOW);
    digitalWrite(yingshaoxo_spi_output_data_pin, LOW);
    yingshaoxo_spi_output_has_been_initialized = 1;
}
void send_yingshaoxo_spi_a_byte(unsigned char a_byte, int delay_in_millisecond) {
    int temp_0_or_1 = 0;
    unsigned char temp_binary_index = 0;
    while (1) {
        temp_0_or_1 = a_byte & (1 << (7-temp_binary_index));
        digitalWrite(yingshaoxo_spi_output_data_pin, temp_0_or_1);
        digitalWrite(yingshaoxo_spi_output_clock_pin, LOW);
        if (delay_in_millisecond == 0) {
            delay_in_us(2);
        } else {
            delay(delay_in_millisecond);
        }
        digitalWrite(yingshaoxo_spi_output_clock_pin, HIGH);
        if (delay_in_millisecond == 0) {
            delay_in_us(2);
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
void send_yingshaoxo_spi_output(unsigned char *data, int delay_in_millisecond) {
    if (yingshaoxo_spi_output_has_been_initialized == 0) {
        // call set_up_yingshaoxo_spi_output() first
        return;
    }
    send_yingshaoxo_spi_a_byte(0x01, delay_in_millisecond);
    send_yingshaoxo_spi_a_byte(0x02, delay_in_millisecond);
    unsigned int index = 0;
    unsigned char a_byte = 0x00;
    while (1) {
        a_byte = data[index];
        send_yingshaoxo_spi_a_byte(a_byte, delay_in_millisecond);
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
    send_yingshaoxo_spi_a_byte(0x04, delay_in_millisecond);
}

#endif

/*
void setup() {
    set_up_yingshaoxo_spi_input();
    set_up_yingshaoxo_spi_output();
}

void loop() {
    //int result_index = get_yingshaoxo_spi_input(2000);
    //if (result_index >= 1) {
    //    clear_the_screen();
    //    smart_print_string(0, 0, yingshaoxo_spi_input_that_transmit_ends_with_04);
    //}

    send_yingshaoxo_spi_output("hi, you!", 1);
    delay(1000);

    //int result_index = get_yingshaoxo_spi_input_bytes(0x04);
    //if (result_index >= 0) {
    //    clear_the_screen();
    //    smart_print_string(0, 0, yingshaoxo_spi_input_that_transmit_ends_with_04);
    //}
}
*/ 



/*
class Simple_Output_Soft_SPI:
    def __init__(self, sck, mosi):
        self.sck = sck
        self.sck.init(self.sck.OUT)
        self.sck.low()
        self.mosi = mosi
        self.mosi.init(self.mosi.OUT)
        self.mosi.low()

    def _write_bit(self, bit):
        # python do not need delay, because it is slow. delay after each clock signal
        self.mosi.value(bit)
        self.sck.high()
        self.sck.low()

    def write(self, data):
        if isinstance(data, int):
            data = [data]
        for byte in data:
            for bit_idx in range(7, -1, -1):
                # write 0x01 as 00000001, the other side first receive 0, then 1.
                bit = (byte >> bit_idx) & 0x01
                self._write_bit(bit)


class Simple_Input_Soft_SPI:
    def __init__(self, sck, miso):
        self.sck = sck
        self.sck.init(self.sck.IN)
        self.miso = miso
        self.miso.init(self.miso.IN)

    def read_0_or_1(self):
        clock_value = 1
        while clock_value == 1:
            clock_value = self.sck.value()
        while clock_value == 0:
            clock_value = self.sck.value()
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
        return bytes(a_list)


"""
from machine import Pin
from soft_spi import Simple_Input_Soft_SPI, Simple_Output_Soft_SPI
my_input_spi = Simple_Input_Soft_SPI(Pin(20), Pin(21))
my_output_spi = Simple_Output_Soft_SPI(Pin(18), Pin(19))

my_output_spi.write(bytes([0x01, 0x02]) + b"what is your name?" + bytes([0x04]))

# while True:
#     my_input_spi.read_until_bytes([0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0])
#     data = my_input_spi.read_bytes()
#     print(data)
"""
*/
