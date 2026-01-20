# code translated by doubao ai
from machine import Pin
import time

TFT_CLK_PIN = 2
TFT_MOSI_PIN = 3
TFT_MISO_PIN = 4
TFT_CS_PIN = 5

TFT_RS_PIN = TFT_CS_PIN    # Arduino D7 -> Pico GPIO7 (chip select)
TFT_RW_PIN = TFT_MOSI_PIN    # Arduino D8 -> Pico GPIO8 (serial data input)
TFT_E_PIN = TFT_CLK_PIN     # Arduino D9 -> Pico GPIO9 (serial clock)

# LCD parameters
height = 64
width = 128

rs = Pin(TFT_RS_PIN, Pin.OUT)
rw = Pin(TFT_RW_PIN, Pin.OUT)
e = Pin(TFT_E_PIN, Pin.OUT)

# Global frame buffer (1024 bytes, initialized to 0)
the_lcd_fixed_frame_buffer = bytearray(1024)  # More efficient than list in MicroPython

# ------------------- Core LCD communication functions -------------------
def send_byte(eight_bits):
    """Send 8 bits to LCD via bit-bang (matches C send_byte function)"""
    for i in range(8):
        # Set data pin (RW) high/low based on current bit
        if (eight_bits << i) & 0x80:
            rw.value(1)
        else:
            rw.value(0)
        # Toggle clock pin (E)
        e.value(0)
        e.value(1)

def write_command(command):
    """Write command to LCD (matches C write_command function)"""
    rs.value(1)  # chip_select_1

    send_byte(0xf8)
    send_byte(command & 0xf0)
    send_byte((command << 4) & 0xf0)

    time.sleep_ms(1)
    rs.value(0)  # chip_select_0

def write_data(character):
    """Write data to LCD (matches C write_data function)"""
    rs.value(1)  # chip_select_1

    send_byte(0xfa)
    send_byte(character & 0xf0)
    send_byte((character << 4) & 0xf0)

    time.sleep_ms(1)
    rs.value(0)  # chip_select_0

# ------------------- Text display functions -------------------
def print_string(y, x, a_string):
    if y == 0:
        write_command(0x80 + x)
    elif y == 1:
        write_command(0x90 + x)
    elif y == 2:
        write_command(0x88 + x)
    elif y == 3:
        write_command(0x98 + x)
    for char in a_string:
        write_data(ord(char))
        time.sleep_ms(1)

def clear_the_screen():
    write_command(0x01)

# ------------------- Graphic display functions -------------------
def clear_graphic_screen():
    # Clear frame buffer first
    for i in range(1024):
        the_lcd_fixed_frame_buffer[i] = 0
    # Clear physical LCD
    write_command(0x34)  # Extended instruction set
    for y_pair in range(32):
        for x_byte in range(16):
            write_command(0x80 + y_pair)
            write_command(0x80 + x_byte)
            write_data(0x00)
            write_data(0x00)
    write_command(0x36)  # Graphic display on
    write_command(0x30)  # Basic instruction set

def draw_pixel(y, x, value):
    # Coordinate validity check
    if x < 0 or x >= 128 or y < 0 or y >= 64:
        return
    # Calculate pixel position in frame buffer
    x_byte = x // 16
    x_bit = x % 16
    y_byte = y // 32
    y_bit = y % 32
    # Calculate byte index
    base = y_byte * 32 * 16
    word_offset = y_bit * 16 + x_byte * 2
    byte_index = base + word_offset
    # Update frame buffer
    if x_bit < 8:
        # High byte (first 8 bits)
        mask = 1 << (7 - x_bit)
        if value == 1:
            the_lcd_fixed_frame_buffer[byte_index] |= mask
        else:
            the_lcd_fixed_frame_buffer[byte_index] &= ~mask
    else:
        # Low byte (last 8 bits)
        mask = 1 << (15 - x_bit)
        if value == 1:
            the_lcd_fixed_frame_buffer[byte_index + 1] |= mask
        else:
            the_lcd_fixed_frame_buffer[byte_index + 1] &= ~mask

def update_graphic_screen():
    """call this after draw_pixel() to see something"""
    temp_idx = 0  # Index pointer for frame buffer (replaces C pointer)
    write_command(0x34)  # Extended instruction set
    write_command(0x36)  # Graphic display on
    # Upper screen (y=0~31)
    for y_bit in range(32):
        write_command(0x80 | y_bit)
        write_command(0x80)  # Horizontal start address (upper)
        for x_byte in range(8):
            write_data(the_lcd_fixed_frame_buffer[temp_idx])
            temp_idx += 1
            write_data(the_lcd_fixed_frame_buffer[temp_idx])
            temp_idx += 1
    # Lower screen (y=32~63)
    for y_bit in range(32):
        write_command(0x80 | y_bit)
        write_command(0x88)  # Horizontal start address (lower)
        for x_byte in range(8):
            write_data(the_lcd_fixed_frame_buffer[temp_idx])
            temp_idx += 1
            write_data(the_lcd_fixed_frame_buffer[temp_idx])
            temp_idx += 1
    write_command(0x30)  # Back to basic instruction set

def draw_pixel_directly(y, x, value):
    """Draw pixel directly to LCD"""
    if x < 0 or x >= 128 or y < 0 or y >= 64:
        return
    # Calculate position
    x_byte = x // 16
    x_bit = x % 16
    y_screen = y // 32
    y_line = y % 32
    base = y_screen * 32 * 16
    word_offset = y_line * 16 + x_byte * 2
    byte_index = base + word_offset
    # Get current bytes
    target_byte_high = the_lcd_fixed_frame_buffer[byte_index]
    target_byte_low = the_lcd_fixed_frame_buffer[byte_index + 1]
    # Update bytes
    if x_bit < 8:
        mask = 1 << (7 - x_bit)
        if value == 1:
            target_byte_high |= mask
        else:
            target_byte_high &= ~mask
    else:
        mask = 1 << (15 - x_bit)
        if value == 1:
            target_byte_low |= mask
        else:
            target_byte_low &= ~mask
    # Save back to frame buffer
    the_lcd_fixed_frame_buffer[byte_index] = target_byte_high
    the_lcd_fixed_frame_buffer[byte_index + 1] = target_byte_low
    # Write to LCD
    write_command(0x34)
    write_command(0x36)
    write_command(0x80 | y_line)
    write_command(0x80 + x_byte + (8 * y_screen))
    write_data(target_byte_high)
    write_data(target_byte_low)
    write_command(0x30)

# ------------------- Initialization -------------------
def set_LCD_pin_to_low():
    e.value(0)
    rw.value(0)
    rs.value(0)

def initialize_LCD():
    # Set pin modes (done at top in MicroPython, just set low here)
    set_LCD_pin_to_low()
    time.sleep_ms(1000)  # 1 second delay
    write_command(0x30)
    time.sleep_ms(20)
    write_command(0x0c)
    time.sleep_ms(20)
    write_command(0x01)
    time.sleep_ms(200)

# ------------------- Main setup (matches C setup) -------------------
def setup():
    initialize_LCD()
    clear_the_screen()
    clear_graphic_screen()
    print("initlized successfully")

    print_string(0, 0, "Hi!")

    # Draw a small cube (8x8 pixel square)
    for y in range(28, 36):
        for x in range(60, 68):
            draw_pixel(y, x, 1)
    update_graphic_screen()

    # Draw one pixel directly
    draw_pixel_directly(22, 98, 1)

setup()
