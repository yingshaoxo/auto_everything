# code translated by doubao ai
from machine import Pin, SPI
import time

class LCD_12864_ST7920():
    def __init__(self, a_spi, cs_pin):
        """ see README.md """
        self.spi = a_spi
        self.cs = Pin(cs_pin, Pin.OUT)
        self.cs.low()

        # LCD parameters
        self.width = 128
        self.height = 64

        # Frame buffer (1024 bytes, initialized to 0)
        self.frame_buffer = bytearray(1024)

        # Initialize LCD
        self.initialize()

    def _send_byte(self, eight_bits):
        self.spi.write(eight_bits)

    def write_command(self, command):
        self.cs.high()  # CS/RS high for command

        self._send_byte(0xF8)
        self._send_byte(command & 0xF0)        # High 4 bits
        self._send_byte((command << 4) & 0xF0) # Low 4 bits

        time.sleep_us(100)  # Short delay (faster than ms for SPI)
        self.cs.low()

    def write_data(self, data):
        self.cs.high()  # CS/RS high for data

        self._send_byte(0xFA)
        self._send_byte(data & 0xF0)        # High 4 bits
        self._send_byte((data << 4) & 0xF0) # Low 4 bits

        time.sleep_us(100)
        self.cs.low()

    def initialize(self):
        # Reset sequence with proper timing
        time.sleep_ms(100)

        # Basic instruction set
        self.write_command(0x30)
        time.sleep_ms(20)

        # Display on, cursor off
        self.write_command(0x0C)
        time.sleep_ms(20)

        # Clear text screen
        self.write_command(0x01)
        time.sleep_ms(200)

        # Enable graphic mode
        self.write_command(0x34)
        time.sleep_ms(20)
        self.write_command(0x36)
        time.sleep_ms(20)
        self.write_command(0x30)

    def clear_text_screen(self):
        self.write_command(0x01)
        time.sleep_ms(10)

    def clear_graphic_screen(self):
        # Clear frame buffer
        for i in range(1024):
            self.frame_buffer[i] = 0

        # Clear physical LCD
        self.write_command(0x34)  # Extended instruction set
        for y_pair in range(32):
            for x_byte in range(16):
                self.write_command(0x80 + y_pair)
                self.write_command(0x80 + x_byte)
                self.write_data(0x00)
                self.write_data(0x00)
        self.write_command(0x36)  # Graphic display on
        self.write_command(0x30)  # Basic instruction set

    def print_string(self, y, x, text):
        if y == 0:
            self.write_command(0x80 + x)
        elif y == 1:
            self.write_command(0x90 + x)
        elif y == 2:
            self.write_command(0x88 + x)
        elif y == 3:
            self.write_command(0x98 + x)

        for char in text:
            self.write_data(ord(char))
            time.sleep_us(100)

    def print_bytes_string(self, y, x, bytes_string):
        if y == 0:
            self.write_command(0x80 + x)
        elif y == 1:
            self.write_command(0x90 + x)
        elif y == 2:
            self.write_command(0x88 + x)
        elif y == 3:
            self.write_command(0x98 + x)

        for one in bytes_string:
            self.write_data(one)
            time.sleep_us(100)

    def draw_pixel(self, y, x, value):
        """0=off, 1=on"""
        # Coordinate validation
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        # Calculate pixel position in frame buffer
        x_byte = x // 16
        x_bit = x % 16
        y_screen = y // 32  # 0=upper, 1=lower
        y_line = y % 32

        # Calculate byte index
        base = y_screen * 32 * 16
        word_offset = y_line * 16 + x_byte * 2
        byte_index = base + word_offset

        # Update frame buffer
        if x_bit < 8:
            mask = 1 << (7 - x_bit)
            if value == 1:
                self.frame_buffer[byte_index] |= mask
            else:
                self.frame_buffer[byte_index] &= ~mask
        else:
            mask = 1 << (15 - x_bit)
            if value == 1:
                self.frame_buffer[byte_index + 1] |= mask
            else:
                self.frame_buffer[byte_index + 1] &= ~mask

    def update_graphic_screen(self):
        """must call this function after draw_point()"""
        temp_idx = 0

        self.write_command(0x34)  # Extended instruction set
        self.write_command(0x36)  # Graphic display on

        # Upper screen (y=0~31)
        for y_line in range(32):
            self.write_command(0x80 | y_line)
            self.write_command(0x80)  # Horizontal start (upper)
            for x_byte in range(8):
                self.write_data(self.frame_buffer[temp_idx])
                temp_idx += 1
                self.write_data(self.frame_buffer[temp_idx])
                temp_idx += 1

        # Lower screen (y=32~63)
        for y_line in range(32):
            self.write_command(0x80 | y_line)
            self.write_command(0x88)  # Horizontal start (lower)
            for x_byte in range(8):
                self.write_data(self.frame_buffer[temp_idx])
                temp_idx += 1
                self.write_data(self.frame_buffer[temp_idx])
                temp_idx += 1

        self.write_command(0x30)  # Back to basic instruction set

    def draw_pixel_directly(self, y, x, value):
        """Draw pixel directly to LCD (bypasses full buffer update)"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        # Calculate position
        x_byte = x // 16
        x_bit = x % 16
        y_screen = y // 32
        y_line = y % 32

        # Calculate byte index
        base = y_screen * 32 * 16
        word_offset = y_line * 16 + x_byte * 2
        byte_index = base + word_offset

        # Get current bytes
        high_byte = self.frame_buffer[byte_index]
        low_byte = self.frame_buffer[byte_index + 1]

        # Update bytes
        if x_bit < 8:
            mask = 1 << (7 - x_bit)
            if value == 1:
                high_byte |= mask
            else:
                high_byte &= ~mask
        else:
            mask = 1 << (15 - x_bit)
            if value == 1:
                low_byte |= mask
            else:
                low_byte &= ~mask

        # Save back to buffer
        self.frame_buffer[byte_index] = high_byte
        self.frame_buffer[byte_index + 1] = low_byte

        # Write directly to LCD
        self.write_command(0x34)
        self.write_command(0x36)

        self.write_command(0x80 | y_line)
        self.write_command(0x80 + x_byte + (8 * y_screen))

        self.write_data(high_byte)
        self.write_data(low_byte)

        self.write_command(0x30)


if __name__ == "__main__":
    # SPI Configuration (Pico Hardware SPI)
    TFT_CLK_PIN = 2  # E -> SCK
    TFT_MOSI_PIN = 3 # RW -> MOSI
    TFT_MISO_PIN = 4 # Not used (ST7920 is write-only)
    TFT_CS_PIN = 5   # RS -> CS
    baudrate = 10000000  # 10MHz max for Pico SPI

    # Create hardware SPI instance
    # Note: Pico SPI write() requires bytearray, so we wrap it for compatibility
    class HardwareSPIWrapper:
        def __init__(self, spi):
            self.spi = spi

        def write(self, data):
            """Wrapper to match Simple_Output_Soft_SPI write() interface"""
            if isinstance(data, int):
                self.spi.write(bytearray([data]))
            else:
                self.spi.write(bytearray(data))

    # Initialize SPI
    spi_hw = SPI(0, baudrate=baudrate, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN), miso=Pin(TFT_MISO_PIN))
    spi_wrapper = HardwareSPIWrapper(spi_hw)

    # Create LCD instance
    lcd = LCD_12864_ST7920(spi_wrapper, TFT_CS_PIN)

    # Test the LCD (same functionality as original setup)
    def test_lcd():
        # Clear screens
        lcd.clear_text_screen()
        lcd.clear_graphic_screen()

        # Print text
        lcd.print_string(0, 0, "Hi! (SPI 10MHz)")

        # Draw 8x8 square
        for y in range(28, 36):
            for x in range(60, 68):
                lcd.draw_pixel(y, x, 1)
        lcd.update_graphic_screen()

        # Draw single pixel directly
        lcd.draw_pixel_directly(22, 98, 1)
        print("LCD test completed!")

    test_lcd()
