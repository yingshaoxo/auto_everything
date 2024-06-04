from auto_everything.image import Image
from time import time as now

image = Image()

source_image_path = "/home/yingshaoxo/Downloads/hero.png"
an_image = image.read_image_from_file(source_image_path)
an_image_backup = an_image.copy()
height, width = an_image.get_shape()
an_image.print()
an_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero1_original.png")
print("original image output done")

small_image = an_image.copy()
small_image.resize(30, 30)
small_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero1_30x30.png")
print("30x30 image output done")

start = now()
an_image = an_image.get_simplified_image_in_a_slow_way()
an_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2_simplified.png")
print("simplified image output done")
end = now()
print("time use:", end-start)

import auto_everything.additional.hqx as hqx
an_image = hqx.yingshaoxo_image_scalling_up_by_using_hqx3(an_image)
an_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero3_hqx3.png")
print("hqx3 hd image output done")

from auto_everything.ml import ML
image_transformer = ML().Yingshaoxo_Image_Transformer()

hd_image = image_transformer.scale_up_animation_image_by_using_yingshaoxo_method(an_image_backup)
hd_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero4_yingshaoxo_animation.png")
print("yingshaoxo animation hd image output done")

hd_image = image_transformer.scale_up_animation_image(an_image_backup)
hd_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero5_opencv_animation.png")
print("opencv animation hd image output done")

hd_image = image_transformer.scale_up_image(an_image_backup)
hd_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero6_opencv_normal.png")
print("opencv normal hd image output done")

hd_image = image_transformer.scale_up_image_by_using_yingshaoxo_method(an_image_backup)
hd_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero7_yingshaoxo_normal.png")
hd_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero7_yingshaoxo_normal.png.txt", extreme=True)
print("yingshaoxo normal hd image output done")


print("\n\n\nNow, open the new bigger image, and put your eyes far away from screen. You should see a super_resolution image if you have Myopia.")

print("If you want higher resolution of image, you could use hqx3 algorithm to do it, it is just about 200KB size of code. You don't need a GPU to do it, because normally hqx3 is used in old machine NES emulator for scaling the image up.")
