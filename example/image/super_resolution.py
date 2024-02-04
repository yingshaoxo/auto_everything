from auto_everything.image import Image

image = Image()

source_image_path = "/home/yingshaoxo/Downloads/hero.png"
an_image = image.read_image_from_file(source_image_path)
height, width = an_image.get_shape()
an_image.resize(height*4, width*4)

an_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2.png")
print("Now, open the new bigger image, and put your eyes far away from screen. You should see a super_resolution image if you have Myopia.")
