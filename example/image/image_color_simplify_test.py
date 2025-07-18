from auto_everything.image_ import Image
from time import time as now

image = Image()

source_image_path = "/home/yingshaoxo/Downloads/dnf.bmp"#water.png"
an_image = image.read_image_from_file(source_image_path)
an_image_backup = an_image.copy()
height, width = an_image.get_shape()
an_image.print()
an_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero1_original.png")
print("original image output done")
print()

start = now()

# todo: use old color. So far, this is not that good, it should use one of the old color than creating a new average color
# todo: use better edge line. And the quality of this function highly related to the edge line detection function, but my version is not that good, maybe use hsv's h value to detect edge line would be better
image_2 = an_image.get_simplified_image_based_on_mean_square_and_edge_line()
image_2.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_pure_color.png")
print("pure color image output done")

end = now()
print("time use:", end-start)
print()
