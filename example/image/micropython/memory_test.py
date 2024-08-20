def get_a_fake_image_in_memory():
    import gc
    a_image = []
    height = 480
    width = 320
    print("all memory:", gc.mem_free()/1000, "kb")
    start_memory = gc.mem_free()/1000
    for y in range(height):
        row = []
        for x in range(width):
            row.append([255,255,255,255])
            #row.append(255)
        a_image.append(row)
    end_memory = gc.mem_free()/1000
    print("memory use for a picture:", int(start_memory - end_memory), "kb")
    return a_image

def test():
    image_list = []
    for i in range(1):
        image_list.append(get_a_fake_image_in_memory())

test()