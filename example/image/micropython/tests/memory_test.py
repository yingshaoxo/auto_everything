def get_a_fake_image_in_memory():
    import gc
    a_image = []
    height = 320
    width = 240
    print("old memory:", gc.mem_free()/1000, "kb")
    start_memory = gc.mem_free()/1000
    for y in range(height):
        row = []
        for x in range(width):
            row.append([255,255,255,255])
        a_image.append(row)
    end_memory = gc.mem_free()/1000
    print("memory use for a picture:", int(start_memory - end_memory), "kb")
    return a_image

def test():
    from gc import mem_free
    print("current memory: ", mem_free()/1024, "KB.")

    counting = 0
    try:
        image_list = []
        for i in range(98):
            counting += 1
            print("\n\npicture ", counting, " test:")
            image_list.append(get_a_fake_image_in_memory())
    except Exception as e:
        print("memory allocation failed at picture ", counting)
        print(e)

test()
