"""ILI9341 LCD/Touch module."""
"""
modified by: yingshaoxo.xyz
"""
from time import sleep
from math import cos, sin, pi, radians
#from sys import implementation
from framebuf import FrameBuffer, RGB565  # type: ignore
from io import BytesIO
import gc


class Display(object):
    "Serial interface for 16-bit color (5-6-5 RGB) IL9341 display."

    def __init__(self, spi, cs, dc, rst,
                 width=240, height=320, rotation=0, no_font=False):
        """Initialize OLED.

        Args:
            spi (Class Spi):  SPI interface for OLED
            cs (Class Pin):  Chip select pin
            dc (Class Pin):  Data/Command pin
            rst (Class Pin):  Reset pin
            width (int): Screen width (default 240)
            height (int): Screen height (default 320)
            rotation (int): Rotation must be 0 default, 90. 180 or 270
        """
        self.consts = { "NOP": 0x00, "SWRESET": 0x01, "RDDID": 0x04, "RDDST": 0x09, "SLPIN": 0x10, "SLPOUT": 0x11, "PTLON": 0x12, "NORON": 0x13, "RDMODE": 0x0A, "RDMADCTL": 0x0B, "RDPIXFMT": 0x0C, "RDIMGFMT": 0x0D, "RDSELFDIAG": 0x0F, "INVOFF": 0x20, "INVON": 0x21, "GAMMASET": 0x26, "DISPLAY_OFF": 0x28, "DISPLAY_ON": 0x29, "SET_COLUMN": 0x2A, "SET_PAGE": 0x2B, "WRITE_RAM": 0x2C, "READ_RAM": 0x2E, "PTLAR": 0x30, "VSCRDEF": 0x33, "MADCTL": 0x36, "VSCRSADD": 0x37, "PIXFMT": 0x3A, "WRITE_DISPLAY_BRIGHTNESS": 0x51, "READ_DISPLAY_BRIGHTNESS": 0x52, "WRITE_CTRL_DISPLAY": 0x53, "READ_CTRL_DISPLAY": 0x54, "WRITE_CABC": 0x55, "READ_CABC": 0x56, "WRITE_CABC_MINIMUM": 0x5E, "READ_CABC_MINIMUM": 0x5F, "FRMCTR1": 0xB1, "FRMCTR2": 0xB2, "FRMCTR3": 0xB3, "INVCTR": 0xB4, "DFUNCTR": 0xB6, "PWCTR1": 0xC0, "PWCTR2": 0xC1, "PWCTRA": 0xCB, "PWCTRB": 0xCF, "VMCTR1": 0xC5, "VMCTR2": 0xC7, "RDID1": 0xDA, "RDID2": 0xDB, "RDID3": 0xDC, "RDID4": 0xDD, "GMCTRP1": 0xE0, "GMCTRN1": 0xE1, "DTCA": 0xE8, "DTCB": 0xEA, "POSC": 0xED, "ENABLE3G": 0xF2, "PUMPRC": 0xF7 }
        self.ROTATE = { 0: 0x88, 90: 0xE8, 180: 0x48, 270: 0x28 }

        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = width
        self.height = height
        if rotation not in self.ROTATE.keys():
            raise RuntimeError('Rotation must be 0, 90, 180 or 270.')
        else:
            self.rotation = self.ROTATE[rotation]

        # Initialize GPIO pins and set implementation specific methods
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)
        self.reset()
        # Send initialization commands
        self.write_cmd(self.consts["SWRESET"])  # Software reset
        sleep(.1)
        self.write_cmd(self.consts["PWCTRB"], 0x00, 0xC1, 0x30)  # Pwr ctrl B
        self.write_cmd(self.consts["POSC"], 0x64, 0x03, 0x12, 0x81)  # Pwr on seq. ctrl
        self.write_cmd(self.consts["DTCA"], 0x85, 0x00, 0x78)  # Driver timing ctrl A
        self.write_cmd(self.consts["PWCTRA"], 0x39, 0x2C, 0x00, 0x34, 0x02)  # Pwr ctrl A
        self.write_cmd(self.consts["PUMPRC"], 0x20)  # Pump ratio control
        self.write_cmd(self.consts["DTCB"], 0x00, 0x00)  # Driver timing ctrl B
        self.write_cmd(self.consts["PWCTR1"], 0x23)  # Pwr ctrl 1
        self.write_cmd(self.consts["PWCTR2"], 0x10)  # Pwr ctrl 2
        self.write_cmd(self.consts["VMCTR1"], 0x3E, 0x28)  # VCOM ctrl 1
        self.write_cmd(self.consts["VMCTR2"], 0x86)  # VCOM ctrl 2
        self.write_cmd(self.consts["MADCTL"], self.rotation)  # Memory access ctrl
        self.write_cmd(self.consts["VSCRSADD"], 0x00)  # Vertical scrolling start address
        self.write_cmd(self.consts["PIXFMT"], 0x55)  # COLMOD: Pixel format
        self.write_cmd(self.consts["FRMCTR1"], 0x00, 0x18)  # Frame rate ctrl
        self.write_cmd(self.consts["DFUNCTR"], 0x08, 0x82, 0x27)
        self.write_cmd(self.consts["ENABLE3G"], 0x00)  # Enable 3 gamma ctrl
        self.write_cmd(self.consts["GAMMASET"], 0x01)  # Gamma curve selected
        self.write_cmd(self.consts["GMCTRP1"], 0x0F, 0x31, 0x2B, 0x0C, 0x0E, 0x08, 0x4E,
                       0xF1, 0x37, 0x07, 0x10, 0x03, 0x0E, 0x09, 0x00)
        self.write_cmd(self.consts["GMCTRN1"], 0x00, 0x0E, 0x14, 0x03, 0x11, 0x07, 0x31,
                       0xC1, 0x48, 0x08, 0x0F, 0x0C, 0x31, 0x36, 0x0F)
        self.write_cmd(self.consts["SLPOUT"])  # Exit sleep
        sleep(.1)
        self.write_cmd(self.consts["DISPLAY_ON"])  # Display on
        sleep(.1)
        self.clear()

        del self.consts

        if no_font == False:
            gc.collect()
            self.yingshaoxo_init()
            gc.collect()
        gc.collect()

    def yingshaoxo_init(self):
        # font related
        try:
            from auto_everything.font_ import get_ascii_8_times_16_points_data
        except Exception as e:
            try:
                from font_ import get_ascii_8_times_16_points_data
            except Exception as e:
                print(e)
                from mini_font_ import get_ascii_8_times_16_points_data
        self.get_ascii_8_times_16_points_data = get_ascii_8_times_16_points_data

        self.font_cache = {}
        self.the_2d_text_cache = None
        self.the_force_redraw_2d_text_index_set = set()

    def reset(self):
        self.rst(0)
        sleep(.05)
        self.rst(1)
        sleep(.05)

    def write_cmd(self, command, *args):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        # Handle any passed data
        if len(args) > 0:
            self.write_data(bytearray(args))

    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def color565(self, r, g, b):
        """Return RGB565 color value.

        Args:
            r (int): Red value.
            g (int): Green value.
            b (int): Blue value.
        """
        return ((r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3).to_bytes(2, "big")

    def draw_buffer(self, x0, y0, x1, y1, data):
        """Write a rectangle of data to display.

        Args:
            x0 (int):  Starting X position.
            y0 (int):  Starting Y position.
            x1 (int):  Ending X position.
            y1 (int):  Ending Y position.
            data (bytes): Data buffer to write.
        """
        self.write_cmd(0x2A,
                       x0 >> 8, x0 & 0xff, x1 >> 8, x1 & 0xff)
        self.write_cmd(0x2B,
                       y0 >> 8, y0 & 0xff, y1 >> 8, y1 & 0xff)
        self.write_cmd(0x2C)
        self.write_data(data)

    def clear(self, color=None, hlines=4):
        """Clear display.

        Args:
            color (Optional int): RGB565 color value (Default: 0 = Black).
            hlines (Optional int): # of horizontal lines per chunk (Default: 8)
        Note:
            hlines can be 1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 160.
            Higher values may result in memory allocation errors.
        """
        w = self.width
        h = self.height
        assert hlines > 0 and h % hlines == 0, ("hlines must be a non-zero factor of height.")

        # Clear display
        if color == None:
            color = self.color565(0,0,0)
        if type(color) == bytes:
            line = color * (w * hlines)
        else:
            line = color.to_bytes(2, 'big') * (w * hlines)

        for y in range(0, h, hlines):
            self.draw_buffer(0, y, w - 1, y + hlines - 1, line)

    def draw_pixel(self, x, y, color):
        """Draw a single pixel.

        Args:
            x (int): X position.
            y (int): Y position.
            color (int): RGB565 color value.
        """
        if self.is_off_grid(x, y, x, y):
            return
        #self.draw_buffer(x, y, x, y, color.to_bytes(2, 'big'))
        self.draw_buffer(x, y, x, y, color)

    def pixel_list_to_bytes_buffer(self, pixel_list):
        data = BytesIO(b'')
        for pixel in pixel_list:
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            data.write(((r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3).to_bytes(2, "big"))
        data.seek(0)
        return data.read()

    def draw_image(self, image, height=None, width=None):
        if height == None:
            height = self.height
        if width == None:
            width = self.width
        data = BytesIO(b'')
        #data = bytearrary(height * width) # bytearray has bug in here, it can't make bytes 'big'
        for row_index, row in enumerate(image):
            base_index = row_index * width
            for column_index, pixel in enumerate(row):
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                data.write(((r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3).to_bytes(2, "big"))
        data.seek(0)
        self.draw_buffer(0, 0, width-1, height-1, data.read())

    def draw_image_quick(self, image, height=None, width=None, step=8):
        if height == None:
            height = self.height
        if width == None:
            width = self.width
        step_length = step
        index = 0
        for row_index, row in enumerate(image):
            if row_index < index:
                continue
            data = BytesIO(b'')
            for i in range(step_length):
                real_index = row_index+i
                if real_index >= height:
                    break
                data.write(self.pixel_list_to_bytes_buffer(image[real_index]))
            index += step_length
            data.seek(0)
            self.draw_buffer(0, row_index, width-1, row_index+step_length-1, data.read())

    def cache_font_at_boot_time(self):
        r, g, b = 255,255,255
        white = self.color565(r,g,b)
        r, g, b = 0,0,0
        black = self.color565(r,g,b)

        all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        for char in all_chars:
            char_points_data = self.get_ascii_8_times_16_points_data(char)
            data = BytesIO(b'')
            for row_index, row in enumerate(char_points_data):
                for column_index, element in enumerate(row):
                    if element == 1:
                        data.write(white)
                    else:
                        data.write(black)
            data.seek(0)
            self.font_cache[char] = data.read()

    def get_char_bytes_by_char(self, char):
        if char in self.font_cache:
            return self.font_cache[char]
        else:
            r, g, b = 255,255,255
            white = self.color565(r,g,b)
            r, g, b = 0,0,0
            black = self.color565(r,g,b)

            char_points_data = self.get_ascii_8_times_16_points_data(char)
            data = BytesIO(b'')
            for row_index, row in enumerate(char_points_data):
                for column_index, element in enumerate(row):
                    if element == 1:
                        data.write(white)
                    else:
                        data.write(black)
            data.seek(0)
            return data.read()

    def draw_2d_text(self, text_2d_array, height=None, width=None):
        #call self.cache_font_at_boot_time() first
        #text_2d_array = root_container.render_as_text()
        self.clear()

        if height == None:
            height = self.height
        if width == None:
            width = self.width

        text_list = []
        for row in text_2d_array:
            text_list += row

        rows_number = int(height // 16)
        columns_number = int(width // 8)

        for row_index in range(rows_number):
            top = row_index * 16
            for column_index in range(columns_number):
                left = column_index * 8

                if len(text_list) == 0:
                    return

                #char = text_list[0]
                #text_list = text_list[1:]
                char = text_list.pop(0)

                if char == "\n":
                    char = " "

                if char == " ":
                    continue

                a_char_bytes = self.get_char_bytes_by_char(char)
                self.draw_buffer(left, top, left+8-1, top+16-1, a_char_bytes)
                del a_char_bytes

        gc.collect()

    def draw_1d_text(self, a_text, height=None, width=None):
        if height == None:
            height = self.height
        if width == None:
            width = self.width

        full_screen_char_number = int(((height/16)*(width/8)))
        a_text = a_text[-full_screen_char_number:]
        a_text = a_text + (full_screen_char_number-len(a_text))*" "

        rows_number = int(height // 16)
        columns_number = int(width // 8)

        the_char_index = 0
        for row_index in range(rows_number):
            top = row_index * 16
            for column_index in range(columns_number):
                left = column_index * 8
                the_char_index += 1

                if ((the_char_index - 1) < 0) or ((the_char_index - 1) >= len(a_text)):
                    break
                char = a_text[the_char_index - 1]

                if char == "\n":
                    char = " "

                if self.the_2d_text_cache == None:
                    if char == " ":
                        continue

                if self.the_2d_text_cache != None:
                    if (the_char_index - 1) >= len(self.the_2d_text_cache):
                        break
                    if self.the_2d_text_cache[the_char_index-1] == char:
                        continue

                a_char_bytes = self.get_char_bytes_by_char(char)
                self.draw_buffer(left, top, left+8-1, top+16-1, a_char_bytes)
                del a_char_bytes

        gc.collect()

        del self.the_2d_text_cache
        gc.collect()
        self.the_2d_text_cache = a_text

    def draw_ellipse(self, x0, y0, a, b, color):
        """Draw an ellipse.

        Args:
            x0, y0 (int): Coordinates of center point.
            a (int): Semi axis horizontal.
            b (int): Semi axis vertical.
            color (int): RGB565 color value.
        """
        a2 = a * a
        b2 = b * b
        twoa2 = a2 + a2
        twob2 = b2 + b2
        x = 0
        y = b
        px = 0
        py = twoa2 * y
        # Plot initial points
        self.draw_pixel(x0 + x, y0 + y, color)
        self.draw_pixel(x0 - x, y0 + y, color)
        self.draw_pixel(x0 + x, y0 - y, color)
        self.draw_pixel(x0 - x, y0 - y, color)
        # Region 1
        p = round(b2 - (a2 * b) + (0.25 * a2))
        while px < py:
            x += 1
            px += twob2
            if p < 0:
                p += b2 + px
            else:
                y -= 1
                py -= twoa2
                p += b2 + px - py
            self.draw_pixel(x0 + x, y0 + y, color)
            self.draw_pixel(x0 - x, y0 + y, color)
            self.draw_pixel(x0 + x, y0 - y, color)
            self.draw_pixel(x0 - x, y0 - y, color)
        # Region 2
        p = round(b2 * (x + 0.5) * (x + 0.5) +
                  a2 * (y - 1) * (y - 1) - a2 * b2)
        while y > 0:
            y -= 1
            py -= twoa2
            if p > 0:
                p += a2 - py
            else:
                x += 1
                px += twob2
                p += a2 - py + px
            self.draw_pixel(x0 + x, y0 + y, color)
            self.draw_pixel(x0 - x, y0 + y, color)
            self.draw_pixel(x0 + x, y0 - y, color)
            self.draw_pixel(x0 - x, y0 - y, color)

    def is_off_grid(self, xmin, ymin, xmax, ymax):
        """Check if coordinates extend past display boundaries."""
        if xmin < 0:
            print('x-coordinate: {0} below minimum of 0.'.format(xmin))
            return True
        if ymin < 0:
            print('y-coordinate: {0} below minimum of 0.'.format(ymin))
            return True
        if xmax >= self.width:
            print('x-coordinate: {0} above maximum of {1}.'.format(
                xmax, self.width - 1))
            return True
        if ymax >= self.height:
            print('y-coordinate: {0} above maximum of {1}.'.format(
                ymax, self.height - 1))
            return True
        return False

    def sleep(self, enable=True):
        """Enters or exits sleep mode.

        Args:
            enable (bool): True (default)=Enter sleep mode, False=Exit sleep
        """
        if enable:
            self.write_cmd(0x10)
        else:
            self.write_cmd(0x11)
