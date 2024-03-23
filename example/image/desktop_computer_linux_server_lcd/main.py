import os
import sys  # for exit
import mmap # shared memory

frame_buffer_number = 'fb0'   # device created by the device driver

# get width and height
f = open(f"/sys/class/graphics/{frame_buffer_number}/virtual_size", "r")
width_and_height = f.read()
width_string, height_string = width_and_height.split(',')
width = int(width_string) # width
height = int(height_string) # height
f.close()

# get bits per pixel
f = open(f"/sys/class/graphics/{frame_buffer_number}/bits_per_pixel", "r")
bpp = int(f.read())
if not bpp in (16, 32):
    print("Unsupported bpp")
    sys.exit()
f.close()

# open framebuffer and map it onto a python bytearray
frame_buffer_device = open(f"/dev/{frame_buffer_number}", mode='r+b') # open R/W
frame_buffer_memory_map = mmap.mmap(frame_buffer_device.fileno(), width * height * bpp//8, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)

color = 255
frame_buffer_memory_map.write(color.to_bytes(1, byteorder='little') * width * height * 3)

# Close the framebuffer device and mmap
frame_buffer_memory_map.close()
frame_buffer_device.close()


"""
# May not work example

#from PIL import Image

# Open the JPEG/PNG file using PIL
image = Image.open('./hero.png')  # Replace 'image.jpg' with the path to your image file
image = image.convert('RGB')  # Convert image to RGB format

# Get the width and height of the image
width, height = image.size

# Open the framebuffer device
frame_buffer_memory_map_device = open('/dev/fb0', 'r+')

# Create mmap to access the framebuffer
frame_buffer_memory_map = mmap.mmap(fb_device.fileno(), 0)

# Set the framebuffer size and color depth
frame_buffer_memory_map.resize(width * height * 3)  # Assuming 24-bit color depth (RGB)

# Copy the image pixel data to the framebuffer
for y in range(height):
    for x in range(width):
        #r, g, b = image.getpixel((x, y))
        r, g, b = 255, 255, 255

        # Calculate the offset in framebuffer memory
        offset = (y * width + x) * 3

        # Write the pixel data to the framebuffer mmap
        frame_buffer_memory_map[offset + 0] = r
        frame_buffer_memory_map[offset + 1] = g
        frame_buffer_memory_map[offset + 2] = b

# Clear the framebuffer
#os.system('clear')
"""
