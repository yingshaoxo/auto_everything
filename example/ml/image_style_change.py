from auto_everything.image import Image
from auto_everything.ml import ML

image = Image()
image_transformer = ML().Yingshaoxo_Image_Transformer()

source_image_path = "/home/yingshaoxo/Downloads/hero.png"
hero_image = image.read_image_from_file(source_image_path)

source_image_path = "/home/yingshaoxo/Downloads/freedom.png"
freedom_image = image.read_image_from_file(source_image_path)

new_image = image_transformer.change_image_style(freedom_image, hero_image)
new_image.save_image_to_file_path("/home/yingshaoxo/Downloads/new_image.png")
