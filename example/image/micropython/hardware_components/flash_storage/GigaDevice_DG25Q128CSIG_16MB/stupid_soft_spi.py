class SoftSPI:
    def __init__(self, sck, mosi, miso, delay=0):
        # wrote by doubao ai
        self.sck = sck
        self.sck.init(self.sck.OUT)
        self.sck.low()

        self.mosi = mosi
        self.mosi.init(self.mosi.OUT)
        self.mosi.low()

        self.miso = miso
        if self.miso is not None:
            self.miso.init(self.miso.IN, self.miso.PULL_NONE)

        self.clock_delay = delay

    def _clock_pulse(self, out_bit=None):
        if out_bit is not None:
            self.mosi.value(out_bit)
        if self.clock_delay > 0:
            sleep_us(self.clock_delay)
        self.sck.high()
        if self.clock_delay > 0:
            sleep_us(self.clock_delay)
        in_bit = self.miso.value() if self.miso is not None else 0
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
        for i in range(len(write_buf)):
            write_byte = write_buf[i]
            read_byte = 0
            for bit_idx in range(7, -1, -1):
                out_bit = (write_byte >> bit_idx) & 0x01
                in_bit = self._clock_pulse(out_bit)
                read_byte |= (in_bit << bit_idx)
            read_buf[i] = read_byte
