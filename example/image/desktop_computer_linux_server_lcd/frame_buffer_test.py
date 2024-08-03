import os

# Define RGB values
red = b'\x00\x00\xff\x00'
green = b'\x00\xff\x00\x00'
blue = b'\xff\x00\x00\x00'

# Define screen resolution
width = 1920
height = 1080

# Open framebuffer for writing
fb = os.open("/dev/fb0", os.O_RDWR)

# Write RGB rows and columns to the framebuffer
for y in range(height):
    for x in range(width):
        os.lseek(fb, 4 * (y * width + x), os.SEEK_SET)
        if x < width // 3:
            os.write(fb, red)
        elif x < 2 * (width // 3):
            os.write(fb, green)
        else:
            os.write(fb, blue)

# Close the framebuffer
os.close(fb)
