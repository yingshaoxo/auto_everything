"""
Fake ILI9488 LCD/Touch module.

I don't know what kind of LED driver board it is using.

Seems like the init_code has backdoor code. It changes quickly.


author: yingshaoxo@gmail.com
"""


from ili9341 import *


try:
    bytes().fromhex("A9")
    def hex_string_to_bytes(hex_string):
        return bytes().fromhex(hex_string)
except Exception as e:
    import ubinascii
    def hex_string_to_bytes(hex_string):
        return ubinascii.unhexlify(hex_string)


class Ili9488_Display(Display):
    def __init__(self, spi, cs, dc, rst, width=320, height=480, rotation=0):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = width
        self.height = height
        if rotation not in self.ROTATE.keys():
            raise Exception('Rotation must be 0, 90, 180 or 270.')
        else:
            self.rotation = self.ROTATE[rotation]

        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)
        self.reset = self.reset_mpy
        self.write_cmd = self.write_cmd_mpy
        self.write_data = self.write_data_mpy

        self.reset()

        # Send initialization commands, it may diff depends on what password your LED driver board productor set. They are bad guys.
        init_backdoor_data = [['command', '0xF7'], ['data', '0xA9'], ['data', '0x51'], ['data', '0x2C'], ['data', '0x82'], ['command', '0xC0'], ['data', '0x11'], ['data', '0x09'], ['command', '0xC1'], ['data', '0x41'], ['command', '0xC5'], ['data', '0x00'], ['data', '0x0A'], ['data', '0x80'], ['command', '0xB1'], ['data', '0xB0'], ['data', '0x11'], ['command', '0xB4'], ['data', '0x02'], ['command', '0xB6'], ['data', '0x02'], ['data', '0x42'], ['command', '0xB7'], ['data', '0xc6'], ['command', '0xBE'], ['data', '0x00'], ['data', '0x04'], ['command', '0xE9'], ['data', '0x00'], ['command', '0x36'], ['data', '0x68'], ['command', '0x3A'], ['data', '0x66'], ['command', '0xE0'], ['data', '0x00'], ['data', '0x07'], ['data', '0x10'], ['data', '0x09'], ['data', '0x17'], ['data', '0x0B'], ['data', '0x41'], ['data', '0x89'], ['data', '0x4B'], ['data', '0x0A'], ['data', '0x0C'], ['data', '0x0E'], ['data', '0x18'], ['data', '0x1B'], ['data', '0x0F'], ['command', '0xE1'], ['data', '0x00'], ['data', '0x17'], ['data', '0x1A'], ['data', '0x04'], ['data', '0x0E'], ['data', '0x06'], ['data', '0x2F'], ['data', '0x45'], ['data', '0x43'], ['data', '0x02'], ['data', '0x0A'], ['data', '0x09'], ['data', '0x32'], ['data', '0x36'], ['data', '0x0F'], ['command', '0x11']]
        for key,value in init_backdoor_data:
            value = hex_string_to_bytes(value.split("0x")[1])[0]
            if key == "command":
                self.write_cmd(value)
            else:
                self.write_data(bytearray([value]))
        sleep(.1)
        self.write_cmd(0x21)
        self.write_cmd(0x29)
        sleep(0.1)
        self.write_cmd(0x36, 0x08) #set rotation to 0 degree
        sleep(0.1)
        self.clear()

        self.yingshaoxo_init()

    def color666(self, r, g, b):
        r_666 = (r & 0xF8) | (r >> 5)
        g_666 = (g & 0xF8) | (g >> 5)
        b_666 = (b & 0xF8) | (b >> 5)
        return bytes([r_666, g_666, b_666])

    def color565(self, r, g, b):
        return self.color666(r,g,b)

    def clear(self, color=None):
        # clear screen
        w = self.width
        h = self.height
        if color == None:
            color = self.color666(0,0,0)
        if type(color) == bytes:
            line = color * (w * 8)
        else:
            raise Exception("This shitty LCD driver only support rgb666")
        for y in range(0, h, 8):
            self.draw_buffer(0, y, w - 1, y + 7, line)

    def draw_pixel(self, x, y, color):
        """Draw a single pixel.
        Args:
            x (int): X position.
            y (int): Y position.
            color (bytes): RGB666 color value.
        """
        if self.is_off_grid(x, y, x, y):
            return
        self.draw_buffer(x, y, x, y, color)
