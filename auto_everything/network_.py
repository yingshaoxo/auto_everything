try:
    from auto_everything.network import *
except Exception as e:
    print(e)


"""
The network can be used to connect computers. But it could also used to connect people. Here I would only do something to help you to connect computers.


## Socket
It is based IP protocol, bytes data stream send from one computer to another.


## tx and rx two line Serial
This is used for two line communication, one line for send, another for read. If for one second, a line changes from 5V_to_0V or 0V_to_5V 9600 times, that means it is using 9600 Baud_Rate.

Some people also call this method "UART(Universal Asynchronous Receiver/Transmitter)" protocol.


## SPI(Serial Peripheral Interface)
SPI protocol can let you do communication for many devices, it needs at least 3 lines. clock line, input line, output line.

You can think SPI as an upgrade from tx,rx serial protocl. It has higher speed since it uses higher speed clock line to sync data communication.

It uses a line to select what device it wanted to communicate. If that line has 5 voltage, and that line is connected to that device, that means that device should do communication for that time. Other part is the same, they send 0 and 1 bytes data steam.

SPI 4 pins are: 1. sclk(serial clock that sends time signal) 2. mosi(master output, slave input) 3. miso(master input, slave output) 4. ss(slave select or chip select).

'Slaves' are some small devices, like microphone, speaker, keyboard, LED screen, 'Master' are the main computer. Serial clock sends clock data for every device to use, so those device can know when to detect if the line has 5 voltage or not. The whole communication speed is depend on the clock speed.

Every devices use same clock line, same mosi line, same miso line, only the select line is different, for each device, they have a unique select line. The select line 0 or 1 status can let the master device communicate to one and single one slave device at one time.

You could not rely on the clock signal line to do communication if you think mosi and miso as two line tx and rx serial communication.


## DIY your communicate method
It seems like, if you can use more line to do the communication at the same time, you would have higher communication speed. Or you can increase the send and receive speed if you like. For example, some poeple use optical fibre to send light as signals. But I think electricity also has high speed in short distance, you just don't have a quick enouth data sender and receiver.
"""


class Universal_Asynchronous_Receiver_And_Transmitter():
    def __init__(self, device_path, baudrate=9600):
        """
        device_path: string
            '/dev/ttyACM0'
            sudo usermod -a -G dialout <username>
        """
        import os
        import fcntl
        import termios
        import struct
        self.os = os
        self.fcntl = fcntl
        self.termios = termios
        self.struct = struct

        self.device_path = device_path
        self.baudrate = baudrate

        self.fd = self.os.open(self.device_path, self.os.O_RDWR | self.os.O_NOCTTY)
        #self.fd = self.os.open(self.device_path, self.os.O_RDWR | self.os.O_NOCTTY | self.os.O_NONBLOCK)

        self.set_baudrate(self.baudrate)

    def set_baudrate(self, baudrate=9600):
        """
        baudrate:

        B0        <==> 0x0000
        B50       <==> 0x0001
        B75       <==> 0x0002
        B110      <==> 0x0003
        B134      <==> 0x0004
        B150      <==> 0x0005
        B200      <==> 0x0006
        B300      <==> 0x0007
        B600      <==> 0x0008
        B1200     <==> 0x0009
        B1800     <==> 0x000a
        B2400     <==> 0x000b
        B4800     <==> 0x000c
        B9600     <==> 0x000d
        B19200    <==> 0x000e
        B38400    <==> 0x000f
        B57600    <==> 0x1001
        B115200   <==> 0x1002
        B230400   <==> 0x1003
        """
        """
            struct termios {
                tcflag_t c_iflag;        /* attrs[0], input mode flags */
                tcflag_t c_oflag;        /* output mode flags */
                tcflag_t c_cflag;        /* control mode flags */
                tcflag_t c_lflag;        /* local mode flags */
            };
        or
            iflag, oflag, cflag, lflag, ispeed, ospeed, cc = orig_attr
        """
        attrs = self.termios.tcgetattr(self.fd)

        # set up raw mode, otherwise '\r' will be '\n'
        try:
            attrs[0] = attrs[0] & ~(self.termios.INLCR | self.termios.IGNCR | self.termios.ICRNL | self.termios.IGNBRK)
            if hasattr(self.termios, 'IUCLC'):
                attrs[0] = attrs[0] & ~self.termios.IUCLC
            if hasattr(self.termios, 'PARMRK'):
                attrs[0] = attrs[0] & ~self.termios.PARMRK

            attrs[1] = attrs[1] & ~(self.termios.OPOST | self.termios.ONLCR | self.termios.OCRNL)

            attrs[2] = attrs[2] | (self.termios.CLOCAL | self.termios.CREAD)
            attrs[2] = attrs[2] & ~self.termios.CBAUD
            attrs[3] = attrs[3] & ~(self.termios.ICANON | self.termios.ECHO | self.termios.ECHOE | self.termios.ECHOK | self.termios.ECHONL | self.termios.ISIG | self.termios.IEXTEN)
        except Exception as e:
            print(e)

        # set baudrate
        the_baudrate_hex = getattr(self.termios, "B"+str(baudrate))
        attrs[2] = attrs[2] | the_baudrate_hex
        #attrs[2] = attrs[2] | self.termios.CS8 #8 bit

        self.termios.tcsetattr(self.fd, self.termios.TCSANOW, attrs)

    def read(self, size=1):
        # if no data, it will block the process
        return self.os.read(self.fd, size)

    def write(self, data):
        return self.os.write(self.fd, data)

    def close(self):
        self.os.close(self.fd)


class Serial():
    def __init__(self, port="/dev/ttyACM0", baudrate=9600, timeout=None):
        self.uart = Universal_Asynchronous_Receiver_And_Transmitter(port, baudrate)

        self.timeout = timeout

        self._start_read_process()

    def _start_read_process(self):
        from multiprocessing import Queue, Process
        import queue
        self.queue = queue

        def _get_input_data_stream(uart, read_queue, signal_queue):
            try:
                while True:
                    one_byte = uart.read(1)
                    if one_byte: # greater than 0, not None
                        read_queue.put(one_byte)
            except Exception as e:
                print(e)
                signal_queue.put("error")

        self.read_queue = Queue()
        self.signal_queue = Queue()

        self.read_process = Process(target=_get_input_data_stream, args=(self.uart, self.read_queue, self.signal_queue))
        self.read_process.daemon = True
        self.read_process.start()

    def _make_sure_the_reading_process_is_on(self):
        if not self.read_process.is_alive():
            self._start_read_process()

    def read(self, size=None):
        self._make_sure_the_reading_process_is_on()

        if size == None:
            if self.timeout == None:
                size = 1
            elif self.timeout != None:
                size = self.available()
                if size == 0:
                    return bytes()
        else:
            if size <= 0:
                raise Exception("can't read negative or 0 size")

        result = bytes()
        try:
            for i in range(size):
                try:
                    result += self.read_queue.get(True, self.timeout)
                    # will block, if timeout is None, block until data come, if timeout second is not None, read and return any data before timeout
                except self.queue.Empty:
                    break
        except Exception as e:
            print(e)
        return result

    def write(self, data):
        return self.uart.write(data)

    def inWaiting(self):
        # Return the number of bytes in the receive buffer.
        return self.read_queue.qsize()

    def available(self):
        # Return available bytes number for read()
        return self.inWaiting()

    def close(self):
        self.uart.close()
        if self.read_process.is_alive():
            self.read_process.kill()


if __name__ == "__main__":
    uart = Universal_Asynchronous_Receiver_And_Transmitter(device_path="/dev/ttyUSB0")
    #uart.read(print)
    #uart.write(b"abcd\n")
