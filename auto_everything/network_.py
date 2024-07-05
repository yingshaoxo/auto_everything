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
    def __init__(self, device_path):
        """
        device_path: string
            '/dev/ttyACM0'
        """
        import os
        import fcntl
        self.os = os
        self.fcntl = fcntl

        self.device_path = device_path

    def read(self, callback_function):
        fd = self.os.open(self.device_path, self.os.O_RDWR | self.os.O_NOCTTY | self.os.O_NDELAY)
        self.fcntl.fcntl(fd, self.fcntl.F_SETFL, 0)
        try:
            while True:
                data = self.os.read(fd, 128)
                if data:
                    callback_function(data)
        except Exception as e:
            os.close(fd)
            raise e

    def write(self, data):
        SERIAL_PORT = self.device_path
        BAUD_RATE = 9600

        fd = self.os.open(SERIAL_PORT, self.os.O_RDWR | self.os.O_NOCTTY | self.os.O_NDELAY)

        attrs = self.fcntl.tcgetattr(fd)
        attrs[1] = attrs[1] & ~(termios.ICANON | termios.ECHO | termios.ISIG)
        attrs[1] = attrs[1] | termios.CS8
        attrs[1] = attrs[1] & ~termios.ICANON
        attrs[1] = attrs[1] & ~termios.ECHO
        attrs[1] = attrs[1] & ~termios.ISIG
        attrs[1] = attrs[1] & ~termios.IXON
        attrs[2] = attrs[2] & ~termios.CRTSCTS
        attrs[3] = BAUD_RATE
        self.fcntl.tcsetattr(fd, self.fcntl.TCSANOW, attrs)

        try:
            self.os.write(fd, data)
            #read_data = self.os.read(fd, 100)
        except Exception as e:
            self.os.close(fd)
            raise e


if __name__ == "__main__":
    uart = Universal_Asynchronous_Receiver_And_Transmitter(device_path="/dev/ttyACM0")
    uart.read(print)
