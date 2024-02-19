"""ILI9341 LCD/Touch module."""
from time import sleep
from math import cos, sin, pi, radians
from sys import implementation
from framebuf import FrameBuffer, RGB565  # type: ignore
from io import BytesIO


def color565(r, g, b):
    """Return RGB565 color value.

    Args:
        r (int): Red value.
        g (int): Green value.
        b (int): Blue value.
    """
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


class Display(object):
    """Serial interface for 16-bit color (5-6-5 RGB) IL9341 display.

    Note:  All coordinates are zero based.
    """

    # Command constants from ILI9341 datasheet
    NOP = const(0x00)  # No-op
    SWRESET = const(0x01)  # Software reset
    RDDID = const(0x04)  # Read display ID info
    RDDST = const(0x09)  # Read display status
    SLPIN = const(0x10)  # Enter sleep mode
    SLPOUT = const(0x11)  # Exit sleep mode
    PTLON = const(0x12)  # Partial mode on
    NORON = const(0x13)  # Normal display mode on
    RDMODE = const(0x0A)  # Read display power mode
    RDMADCTL = const(0x0B)  # Read display MADCTL
    RDPIXFMT = const(0x0C)  # Read display pixel format
    RDIMGFMT = const(0x0D)  # Read display image format
    RDSELFDIAG = const(0x0F)  # Read display self-diagnostic
    INVOFF = const(0x20)  # Display inversion off
    INVON = const(0x21)  # Display inversion on
    GAMMASET = const(0x26)  # Gamma set
    DISPLAY_OFF = const(0x28)  # Display off
    DISPLAY_ON = const(0x29)  # Display on
    SET_COLUMN = const(0x2A)  # Column address set
    SET_PAGE = const(0x2B)  # Page address set
    WRITE_RAM = const(0x2C)  # Memory write
    READ_RAM = const(0x2E)  # Memory read
    PTLAR = const(0x30)  # Partial area
    VSCRDEF = const(0x33)  # Vertical scrolling definition
    MADCTL = const(0x36)  # Memory access control
    VSCRSADD = const(0x37)  # Vertical scrolling start address
    PIXFMT = const(0x3A)  # COLMOD: Pixel format set
    WRITE_DISPLAY_BRIGHTNESS = const(0x51)  # Brightness hardware dependent!
    READ_DISPLAY_BRIGHTNESS = const(0x52)
    WRITE_CTRL_DISPLAY = const(0x53)
    READ_CTRL_DISPLAY = const(0x54)
    WRITE_CABC = const(0x55)  # Write Content Adaptive Brightness Control
    READ_CABC = const(0x56)  # Read Content Adaptive Brightness Control
    WRITE_CABC_MINIMUM = const(0x5E)  # Write CABC Minimum Brightness
    READ_CABC_MINIMUM = const(0x5F)  # Read CABC Minimum Brightness
    FRMCTR1 = const(0xB1)  # Frame rate control (In normal mode/full colors)
    FRMCTR2 = const(0xB2)  # Frame rate control (In idle mode/8 colors)
    FRMCTR3 = const(0xB3)  # Frame rate control (In partial mode/full colors)
    INVCTR = const(0xB4)  # Display inversion control
    DFUNCTR = const(0xB6)  # Display function control
    PWCTR1 = const(0xC0)  # Power control 1
    PWCTR2 = const(0xC1)  # Power control 2
    PWCTRA = const(0xCB)  # Power control A
    PWCTRB = const(0xCF)  # Power control B
    VMCTR1 = const(0xC5)  # VCOM control 1
    VMCTR2 = const(0xC7)  # VCOM control 2
    RDID1 = const(0xDA)  # Read ID 1
    RDID2 = const(0xDB)  # Read ID 2
    RDID3 = const(0xDC)  # Read ID 3
    RDID4 = const(0xDD)  # Read ID 4
    GMCTRP1 = const(0xE0)  # Positive gamma correction
    GMCTRN1 = const(0xE1)  # Negative gamma correction
    DTCA = const(0xE8)  # Driver timing control A
    DTCB = const(0xEA)  # Driver timing control B
    POSC = const(0xED)  # Power on sequence control
    ENABLE3G = const(0xF2)  # Enable 3 gamma control
    PUMPRC = const(0xF7)  # Pump ratio control

    ROTATE = {
        0: 0x88,
        90: 0xE8,
        180: 0x48,
        270: 0x28
    }

    def __init__(self, spi, cs, dc, rst,
                 width=240, height=320, rotation=0):
        """Initialize OLED.

        Args:
            spi (Class Spi):  SPI interface for OLED
            cs (Class Pin):  Chip select pin
            dc (Class Pin):  Data/Command pin
            rst (Class Pin):  Reset pin
            width (Optional int): Screen width (default 240)
            height (Optional int): Screen height (default 320)
            rotation (Optional int): Rotation must be 0 default, 90. 180 or 270
        """
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
        if implementation.name == 'circuitpython':
            self.cs.switch_to_output(value=True)
            self.dc.switch_to_output(value=False)
            self.rst.switch_to_output(value=True)
            self.reset = self.reset_cpy
            self.write_cmd = self.write_cmd_cpy
            self.write_data = self.write_data_cpy
        else:
            self.cs.init(self.cs.OUT, value=1)
            self.dc.init(self.dc.OUT, value=0)
            self.rst.init(self.rst.OUT, value=1)
            self.reset = self.reset_mpy
            self.write_cmd = self.write_cmd_mpy
            self.write_data = self.write_data_mpy
        self.reset()
        # Send initialization commands
        self.write_cmd(self.SWRESET)  # Software reset
        sleep(.1)
        self.write_cmd(self.PWCTRB, 0x00, 0xC1, 0x30)  # Pwr ctrl B
        self.write_cmd(self.POSC, 0x64, 0x03, 0x12, 0x81)  # Pwr on seq. ctrl
        self.write_cmd(self.DTCA, 0x85, 0x00, 0x78)  # Driver timing ctrl A
        self.write_cmd(self.PWCTRA, 0x39, 0x2C, 0x00, 0x34, 0x02)  # Pwr ctrl A
        self.write_cmd(self.PUMPRC, 0x20)  # Pump ratio control
        self.write_cmd(self.DTCB, 0x00, 0x00)  # Driver timing ctrl B
        self.write_cmd(self.PWCTR1, 0x23)  # Pwr ctrl 1
        self.write_cmd(self.PWCTR2, 0x10)  # Pwr ctrl 2
        self.write_cmd(self.VMCTR1, 0x3E, 0x28)  # VCOM ctrl 1
        self.write_cmd(self.VMCTR2, 0x86)  # VCOM ctrl 2
        self.write_cmd(self.MADCTL, self.rotation)  # Memory access ctrl
        self.write_cmd(self.VSCRSADD, 0x00)  # Vertical scrolling start address
        self.write_cmd(self.PIXFMT, 0x55)  # COLMOD: Pixel format
        self.write_cmd(self.FRMCTR1, 0x00, 0x18)  # Frame rate ctrl
        self.write_cmd(self.DFUNCTR, 0x08, 0x82, 0x27)
        self.write_cmd(self.ENABLE3G, 0x00)  # Enable 3 gamma ctrl
        self.write_cmd(self.GAMMASET, 0x01)  # Gamma curve selected
        self.write_cmd(self.GMCTRP1, 0x0F, 0x31, 0x2B, 0x0C, 0x0E, 0x08, 0x4E,
                       0xF1, 0x37, 0x07, 0x10, 0x03, 0x0E, 0x09, 0x00)
        self.write_cmd(self.GMCTRN1, 0x00, 0x0E, 0x14, 0x03, 0x11, 0x07, 0x31,
                       0xC1, 0x48, 0x08, 0x0F, 0x0C, 0x31, 0x36, 0x0F)
        self.write_cmd(self.SLPOUT)  # Exit sleep
        sleep(.1)
        self.write_cmd(self.DISPLAY_ON)  # Display on
        sleep(.1)
        self.clear()

        self.get_ascii_8_times_16_points_data = None
        self.font_cache = {}

    def draw_buffer(self, x0, y0, x1, y1, data):
        """Write a block of data to display.

        Args:
            x0 (int):  Starting X position.
            y0 (int):  Starting Y position.
            x1 (int):  Ending X position.
            y1 (int):  Ending Y position.
            data (bytes): Data buffer to write.
        """
        self.write_cmd(self.SET_COLUMN,
                       x0 >> 8, x0 & 0xff, x1 >> 8, x1 & 0xff)
        self.write_cmd(self.SET_PAGE,
                       y0 >> 8, y0 & 0xff, y1 >> 8, y1 & 0xff)
        self.write_cmd(self.WRITE_RAM)
        self.write_data(data)

    def cleanup(self):
        """Clean up resources."""
        self.clear()
        self.display_off()
        self.spi.deinit()
        print('display off')

    def clear(self, color=0, hlines=8):
        """Clear display.

        Args:
            color (Optional int): RGB565 color value (Default: 0 = Black).
            hlines (Optional int): # of horizontal lines per chunk (Default: 8)
        Note:
            hlines was introduced to deal with memory allocation on some
            boards.  Smaller values allocate less memory but take longer
            to execute.  hlines must be a factor of the display height.
            For example, for a 240 pixel height, valid values for hline
            would be 1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 160.
            Higher values may result in memory allocation errors.
        """
        w = self.width
        h = self.height
        assert hlines > 0 and h % hlines == 0, (
            "hlines must be a non-zero factor of height.")
        # Clear display
        if color:
            line = color.to_bytes(2, 'big') * (w * hlines)
        else:
            line = bytearray(w * 2 * hlines)
        for y in range(0, h, hlines):
            self.draw_buffer(0, y, w - 1, y + hlines - 1, line)

    def display_off(self):
        """Turn display off."""
        self.write_cmd(self.DISPLAY_OFF)

    def display_on(self):
        """Turn display on."""
        self.write_cmd(self.DISPLAY_ON)

    def draw_pixel(self, x, y, color):
        """Draw a single pixel.

        Args:
            x (int): X position.
            y (int): Y position.
            color (int): RGB565 color value.
        """
        if self.is_off_grid(x, y, x, y):
            return
        self.draw_buffer(x, y, x, y, color.to_bytes(2, 'big'))

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
        if self.get_ascii_8_times_16_points_data == None:
            try:
                from auto_everything.font_ import get_ascii_8_times_16_points_data
            except Exception as e:
                from font_ import get_ascii_8_times_16_points_data
            self.get_ascii_8_times_16_points_data = get_ascii_8_times_16_points_data

        r, g, b = 255,255,255
        white = ((r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3).to_bytes(2, "big")
        r, g, b = 0,0,0
        black = ((r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3).to_bytes(2, "big")

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

    def draw_2d_text(self, text_2d_array, height=None, width=None):
        #call self.cache_font_at_boot_time() first
        #text_2d_array = root_container.render_as_text()

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

                char = text_list[0]
                text_list = text_list[1:]

                if char == "\n":
                    char = " "
                if char not in self.font_cache:
                    char = " "

                self.draw_buffer(left, top, left+8-1, top+16-1, self.font_cache[char])

    def draw_ellipse(self, x0, y0, a, b, color):
        """Draw an ellipse.

        Args:
            x0, y0 (int): Coordinates of center point.
            a (int): Semi axis horizontal.
            b (int): Semi axis vertical.
            color (int): RGB565 color value.
        Note:
            The center point is the center of the x0,y0 pixel.
            Since pixels are not divisible, the axes are integer rounded
            up to complete on a full pixel.  Therefore the major and
            minor axes are increased by 1.
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
        """Check if coordinates extend past display boundaries.

        Args:
            xmin (int): Minimum horizontal pixel.
            ymin (int): Minimum vertical pixel.
            xmax (int): Maximum horizontal pixel.
            ymax (int): Maximum vertical pixel.
        Returns:
            boolean: False = Coordinates OK, True = Error.
        """
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

    def reset_cpy(self):
        """Perform reset: Low=initialization, High=normal operation.

        Notes: CircuitPython implemntation
        """
        self.rst.value = False
        sleep(.05)
        self.rst.value = True
        sleep(.05)

    def reset_mpy(self):
        """Perform reset: Low=initialization, High=normal operation.

        Notes: MicroPython implemntation
        """
        self.rst(0)
        sleep(.05)
        self.rst(1)
        sleep(.05)

    def scroll(self, y):
        """Scroll display vertically.

        Args:
            y (int): Number of pixels to scroll display.
        """
        self.write_cmd(self.VSCRSADD, y >> 8, y & 0xFF)

    def set_scroll(self, top, bottom):
        """Set the height of the top and bottom scroll margins.

        Args:
            top (int): Height of top scroll margin
            bottom (int): Height of bottom scroll margin
        """
        if top + bottom <= self.height:
            middle = self.height - (top + bottom)
            print(top, middle, bottom)
            self.write_cmd(self.VSCRDEF,
                           top >> 8,
                           top & 0xFF,
                           middle >> 8,
                           middle & 0xFF,
                           bottom >> 8,
                           bottom & 0xFF)

    def sleep(self, enable=True):
        """Enters or exits sleep mode.

        Args:
            enable (bool): True (default)=Enter sleep mode, False=Exit sleep
        """
        if enable:
            self.write_cmd(self.SLPIN)
        else:
            self.write_cmd(self.SLPOUT)

    def write_cmd_mpy(self, command, *args):
        """Write command to OLED (MicroPython).

        Args:
            command (byte): ILI9341 command code.
            *args (optional bytes): Data to transmit.
        """
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        # Handle any passed data
        if len(args) > 0:
            self.write_data(bytearray(args))

    def write_cmd_cpy(self, command, *args):
        """Write command to OLED (CircuitPython).

        Args:
            command (byte): ILI9341 command code.
            *args (optional bytes): Data to transmit.
        """
        self.dc.value = False
        self.cs.value = False
        # Confirm SPI locked before writing
        while not self.spi.try_lock():
            pass
        self.spi.write(bytearray([command]))
        self.spi.unlock()
        self.cs.value = True
        # Handle any passed data
        if len(args) > 0:
            self.write_data(bytearray(args))

    def write_data_mpy(self, data):
        """Write data to OLED (MicroPython).

        Args:
            data (bytes): Data to transmit.
        """
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def write_data_cpy(self, data):
        """Write data to OLED (CircuitPython).

        Args:
            data (bytes): Data to transmit.
        """
        self.dc.value = True
        self.cs.value = False
        # Confirm SPI locked before writing
        while not self.spi.try_lock():
            pass
        self.spi.write(data)
        self.spi.unlock()
        self.cs.value = True
