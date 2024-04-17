from auto_everything.image import Image
from auto_everything.ml import ML

image = Image()
image_transformer = ML().Yingshaoxo_Image_Transformer()

source_image_path = "/home/yingshaoxo/Downloads/hero.png"
no_hd_image = image.read_image_from_file(source_image_path)

#no_hd_image = image_transformer.scale_up_normal_image(no_hd_image)
no_hd_image = image_transformer.scale_up_animation_image(no_hd_image)
no_hd_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero_fake_hd.png")
