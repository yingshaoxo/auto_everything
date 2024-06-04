from auto_everything.image import Image
from time import time as now

image = Image()

source_image_path = "/home/yingshaoxo/Downloads/hero.png"
an_image = image.read_image_from_file(source_image_path)
an_image_backup = an_image.copy()
height, width = an_image.get_shape()
an_image = an_image.resize(height*2, width*2)
an_image.print()
an_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero1_original.png")
print("original image output done")
print()

start = now()
mosaic_image = an_image.copy().to_mosaic(kernel_number=12)
mosaic_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_mosaic.png")
print("mosaic image output done")
end = now()
print("time use:", end-start)
print()

start = now()
simplified_image_2 = an_image.copy().get_simplified_image(level=7, extream_color_number=50)
simplified_image_2.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_simplified2.png")
print("simplified2 image output done")
end = now()
print("time use:", end-start)
print()

start = now()
quick_mode = an_image.copy().get_simplified_image_in_a_quick_way(level=15)
quick_mode.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_quick_mode.png")
print("quick_mode image output done")
end = now()
print("time use:", end-start)
print()

start = now()
white_and_black = an_image.copy().to_white_and_black()
white_and_black.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_white_and_black.png")
#white_and_black.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_white_and_black.png.txt")
print("white_and_black image output done")
end = now()
print("time use:", end-start)
print()

start = now()
simplified_image_1 = an_image.copy().get_simplified_image_in_a_slow_way(ratio=0.7)
simplified_image_1.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_simplified.png")
print("simplified1 image output done")
end = now()
print("time use:", end-start)
print()

