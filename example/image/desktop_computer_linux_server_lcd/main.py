def a_simple_test():
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
        exit()
    f.close()

    # open framebuffer and map it onto a python bytearray
    frame_buffer_device = open(f"/dev/{frame_buffer_number}", mode='r+b') # open R/W
    frame_buffer_memory_map = mmap.mmap(frame_buffer_device.fileno(), width * height * bpp//8, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)

    color = 255
    frame_buffer_memory_map.write(color.to_bytes(1, byteorder='little') * width * height * 3)

    # Close the framebuffer device and mmap
    frame_buffer_memory_map.close()
    frame_buffer_device.close()

class Frame_Buffer_Operator():
    def __init__(self, frame_buffer_name="fb0"):
        import mmap # map shared memory
        self.mmap = mmap
        self.frame_buffer_name = frame_buffer_name

        # get width and height
        f = open("/sys/class/graphics/{name}/virtual_size".format(name=self.frame_buffer_name), "r")
        width_and_height = f.read()
        width_string, height_string = width_and_height.split(',')
        self.width = int(width_string) # width
        self.height = int(height_string) # height
        f.close()

        # get bits per pixel
        f = open("/sys/class/graphics/{name}/bits_per_pixel".format(name=self.frame_buffer_name), "r")
        self.bpp = int(f.read())
        if not (self.bpp in [16, 32]):
            raise Exception("Unsupported bits per pixel, it should be in [16, 32]")
        f.close()

        self.frame_buffer_device = open("/dev/{name}".format(name=self.frame_buffer_name), mode='r+b') # open R/W
        self.frame_buffer_memory_map = self.mmap.mmap(self.frame_buffer_device.fileno(), self.width * self.height * self.bpp//8, self.mmap.MAP_SHARED, self.mmap.PROT_WRITE | self.mmap.PROT_READ)


    def close(self):
        # Close the framebuffer device and mmap when done
        self.frame_buffer_memory_map.close()
        self.frame_buffer_device.close()

    def write_image(self, a_image):
        a_image = a_image.copy()
        a_image = a_image.resize(self.height, self.width)

        height, width = a_image.get_shape()

        #data = bytearray(height*width*4)
        #index = 0
        #for y in range(height):
        #    for x in range(width):
        #        pixel = a_image.raw_data[y][x]
        #        r,g,b,a = pixel
        #        data[index+0] = r
        #        data[index+1] = g
        #        data[index+2] = b
        #        data[index+3] = a
        #        index += 4

        data_list = []
        for y in range(height):
            for x in range(width):
                pixel = a_image.raw_data[y][x]
                r,g,b,a = pixel
                data_list.append(r)
                data_list.append(g)
                data_list.append(b)
                data_list.append(a)
        data = bytes(data_list)

        self.frame_buffer_memory_map.write(data)

if __name__=="__main__":
    from auto_everything.image import Image
    image = Image()
    source_image_path = "/home/yingshaoxo/Downloads/water.png"
    a_image = image.read_image_from_file(source_image_path)
    #a_image = a_image.get_6_color_simplified_image(free_mode=True, animation_mode=True)

    frame_buffer_operator = Frame_Buffer_Operator()
    frame_buffer_operator.write_image(a_image)
