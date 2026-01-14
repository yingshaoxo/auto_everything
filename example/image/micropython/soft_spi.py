# this module written by doubao ai
from time import sleep_us


class SoftSPI:
    def __init__(self, sck, mosi, miso, delay=0):
        if sck is None or mosi is None:
            raise ValueError("SCK and MOSI pins must be specified for SoftSPI")

        self.sck = sck
        self.sck.init(Pin.OUT_PP)
        self.sck.low()

        self.mosi = mosi
        self.mosi.init(Pin.OUT_PP)
        self.mosi.low()

        self.miso = miso
        if self.miso is not None:
            self.miso.init(Pin.IN, Pin.PULL_NONE)

        # Calculate delay for clock timing (1/(2*baudrate) = half clock cycle)
        # Convert to microseconds for sleep_us (1e6 us = 1 second)
        #self.clock_delay = int((1 / (2 * baudrate)) * 1e6) if baudrate > 0 else 0
        self.clock_delay = delay

    def _clock_pulse(self, out_bit=None):
        # Step 1: Set MOSI level (if writing)
        if out_bit is not None:
            self.mosi.value(out_bit)

        # Step 2: Short delay to stabilize signal before clock edge
        if self.clock_delay > 0:
            sleep_us(self.clock_delay)

        # Step 3: Raise SCK (rising edge - slave latches MOSI, master samples MISO)
        self.sck.high()

        # Step 4: Delay to ensure stable reading
        if self.clock_delay > 0:
            sleep_us(self.clock_delay)

        # Step 5: Read MISO bit (if available)
        in_bit = self.miso.value() if self.miso is not None else 0

        # Step 6: Lower SCK (falling edge)
        self.sck.low()

        return in_bit

    def write(self, data):
        if isinstance(data, int):
            data = [data]

        for byte in data:
            for bit_idx in range(7, -1, -1):  # 7 = MSB, 0 = LSB
                out_bit = (byte >> bit_idx) & 0x01  # Extract single bit
                self._clock_pulse(out_bit)

    def read(self, n_bytes):
        if self.miso is None:
            raise RuntimeError("MISO pin not specified - cannot read data")

        result = bytearray()
        for _ in range(n_bytes):
            byte = 0
            for bit_idx in range(7, -1, -1):  # MSB first
                in_bit = self._clock_pulse()  # No write, only read
                byte |= (in_bit << bit_idx)   # Build byte from bits
            result.append(byte)
        return result

    def write_readinto(self, write_buf, read_buf):
        if len(write_buf) != len(read_buf):
            raise ValueError("Write and read buffers must have same length")
        if self.miso is None:
            raise RuntimeError("MISO pin not specified - cannot read data")

        for i in range(len(write_buf)):
            write_byte = write_buf[i]
            read_byte = 0
            # Transmit/receive one byte (MSB first)
            for bit_idx in range(7, -1, -1):
                out_bit = (write_byte >> bit_idx) & 0x01
                in_bit = self._clock_pulse(out_bit)
                read_byte |= (in_bit << bit_idx)
            read_buf[i] = read_byte


class Simple_Output_Soft_SPI:
    def __init__(self, sck, mosi, miso=None, delay=0):
        self.sck = sck
        self.sck.init(Pin.OUT_PP)
        self.sck.low()

        self.mosi = mosi
        self.mosi.init(Pin.OUT_PP)
        self.mosi.low()

        self.miso = miso
        if self.miso is not None:
            self.miso.init(Pin.IN, Pin.PULL_NONE)

        #self.delay = 1 / (2 * baudrate) if baudrate > 0 else 0
        self.delay = delay

    def _write_bit(self, bit):
        self.mosi.value(bit)
        if self.delay > 0:
            sleep_us(int(self.delay * 1e6))
        self.sck.high()
        if self.delay > 0:
            sleep_us(int(self.delay * 1e6))
        self.sck.low()

    def write(self, data):
        if isinstance(data, int):
            data = [data]

        for byte in data:
            for bit_idx in range(7, -1, -1):
                bit = (byte >> bit_idx) & 0x01
                self._write_bit(bit)

#if __name__ == "__main__":
#    TFT_CLK_PIN = Pin('X1')
#    TFT_MOSI_PIN = Pin('X2')
#
#    spiTFT = Simple_Output_Soft_SPI(baudrate=600000, sck=TFT_CLK_PIN, mosi=TFT_MOSI_PIN)
#
#    spiTFT.write(0x55)
#    spiTFT.write([0xAA, 0x01])
