from auto_everything.image_ import Image
from time import time as now

image = Image()

source_image_path = "/home/yingshaoxo/Downloads/pillow.bmp"
an_image = image.read_image_from_file(source_image_path)
an_image_backup = an_image.copy()
height, width = an_image.get_shape()
an_image.print()
an_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero1_original.png")
print("original image output done")
print()

start = now()

#image_2 = an_image.get_6_color_simplified_image(free_mode=True, kernel=11)
image_2 = an_image.get_simplified_image_based_on_edge_and_average_color()
image_2.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_pure_color.png")
print("pure color image output done")

end = now()
print("time use:", end-start)
print()
