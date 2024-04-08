from auto_everything.disk import Disk
disk = Disk()

source_image_path = "/home/yingshaoxo/Downloads/atlantis_space.png"
target_image_path = disk.join_paths(disk.get_directory_path(source_image_path), "new.png")

try:
    """
    pillow function, you may not want to use
    """
    from auto_everything.image import MyPillow

    mypillow = MyPillow()

    an_image = mypillow.read_image_from_file(file_path=source_image_path)

    bytes_io_image = mypillow.force_decrease_image_file_size(an_image, limit_in_kb=50)

    mypillow.save_bytes_io_image_to_file_path(bytes_io_image=bytes_io_image, file_path=target_image_path)



    from auto_everything.image import Image
    image = Image()

    a_image = image.read_image_from_file(source_image_path)
    a_image.print(width=70)
except Exception as e:
    # In the end, we will use HSL color system, because it allows you to compare color in a easy way
    print(e)

    from auto_everything.image import Image
    image = Image()

    import auto_everything.additional.pypng as pypng

    height, width, raw_data = pypng.read_png_from_file(source_image_path)

    a_image = image.create_an_image(height, width)
    a_image.raw_data = raw_data

    a_image.print(width=70)

    a_image.resize(512, 512)
    pypng.save_png_to_file(a_image, target_image_path)
    a_image.save_image_to_file_path(target_image_path+".txt")
    a_image.save_image_to_file_path(target_image_path+".json")

    input("Want to load them back?")
    a_image = image.read_image_from_file(target_image_path+".json")
    a_image.print()
    a_image = image.read_image_from_file(target_image_path+".txt")
    a_image.print()

    #import matplotlib.pyplot as plt
    #import numpy as np
    #plt.imshow(np.array(a_image.raw_data))
    #plt.show()
