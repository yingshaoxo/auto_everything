from auto_everything.image import Image
from auto_everything.ml import ML

image = Image()
image_transformer = ML().Yingshaoxo_Image_Transformer()

source_image_path = "/home/yingshaoxo/Downloads/hero.png"
no_hd_image = image.read_image_from_file(source_image_path)

#edge_line = image_transformer.get_edge_lines_of_a_image_by_using_yingshaoxo_method(no_hd_image, min_color_distance=20, smooth_value=0, spread=True)
#edge_line.save_image_to_file_path("/home/yingshaoxo/Downloads/edge.png")

#no_hd_image = image_transformer.scale_up_animation_image_by_using_yingshaoxo_method(no_hd_image)
no_hd_image = image_transformer.scale_up_image_by_using_yingshaoxo_method(no_hd_image)
no_hd_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero_test.png")
