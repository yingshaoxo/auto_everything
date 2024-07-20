from struct import unpack


class BMP:
    # author: rocketeerLi, https://blog.csdn.net/rocketeerLi/article/details/84929516
    def __init__(self, filePath) :
        file = open(filePath, "rb")
        # Read the first 14 bytes of bmp file.
        self.bfType = unpack("<h", file.read(2))[0]       # 0x4d42 corresponding to BM indicates that this is a bitmap format supported by Windows.
        self.bfSize = unpack("<i", file.read(4))[0]       # Bitmap file size
        self.bfReserved1 = unpack("<h", file.read(2))[0]  # Reserved field must be set to 0 
        self.bfReserved2 = unpack("<h", file.read(2))[0]  # Reserved field must be set to 0 
        self.bfOffBits = unpack("<i", file.read(4))[0]    # How many bytes should be offset from the file header to the bitmap data (the bitmap header and palette length are not fixed, so this parameter is needed).
        # Read the first 40 bytes of bitmap information of bmp file.
        self.biSize = unpack("<i", file.read(4))[0]       # Number of bytes required
        self.biWidth = unpack("<i", file.read(4))[0]      # Width of the image in pixels
        self.biHeight = unpack("<i", file.read(4))[0]     # Height unit pixel of the image
        self.biPlanes = unpack("<h", file.read(2))[0]     # Description The number of color planes is always set to 1.
        self.biBitCount = unpack("<h", file.read(2))[0]   # Indicate the number of bits

        self.biCompression = unpack("<i", file.read(4))[0]  # Data type of image compression
        self.biSizeImage = unpack("<i", file.read(4))[0]    # Image size
        self.biXPelsPerMeter = unpack("<i", file.read(4))[0]# Horizontal resolution
        self.biYPelsPerMeter = unpack("<i", file.read(4))[0]# Vertical resolution
        self.biClrUsed = unpack("<i", file.read(4))[0]      # Number of color indexes in the color table actually used
        self.biClrImportant = unpack("<i", file.read(4))[0] # Number of color indexes that have an important influence on image display

        if self.biBitCount != 24:
            raise Exception("We need 24bit rgb bmp than:" + str(self.biBitCount) + "bit" + "\n" + "We also need you select 'Do not write color space information' under 'Compatibility Options' when exporting BMP from GIMP.")

        # handle color_space offset
        if self.biClrUsed == 0:
            self.bfOffBits = self.biSize + 14
        else:
            self.bfOffBits = self.biSize + 14 + (self.biClrUsed * 4)
        file.seek(self.bfOffBits)

        # read data
        self.bmp_data = []
        for height in range(self.biHeight) :
            bmp_data_row = []
            # Four-byte padding bit detection
            count = 0
            for width in range(self.biWidth) :
                bmp_data_row.append([unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0]])
                count = count + 3
            # BMP four-byte alignment principle
            while count % 4 != 0 :
                file.read(1)
                count = count + 1
            self.bmp_data.append(bmp_data_row)
        self.bmp_data.reverse()
        file.close()

        self.rgb_data = [None] * self.biHeight
        for row in range(self.biHeight) :
            one_row = [None] * self.biWidth
            for col in range(self.biWidth) :
                b = self.bmp_data[row][col][0]
                g = self.bmp_data[row][col][1]
                r = self.bmp_data[row][col][2]
                one_row[col] = [r,g,b,255]
            self.rgb_data[row] = one_row


def read_bmp_from_file(path):
    """
    return (height, width, raw_data)

    The newest GIMP or online png to bmp converter, they have used a bug version of bmp c++ library, so the bmp image you get from those sources will be broken in columns. If you use oldest ffmpeg to convert mp4 to bmp images, it would work fine.
    """
    img = BMP(path)

    height, width = img.biHeight, img.biWidth
    data = img.rgb_data

    return height, width, data


__all__ = [
    "BMP",
    "read_bmp_from_file",
]
