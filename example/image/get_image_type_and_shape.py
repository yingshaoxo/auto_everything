from auto_everything.additional import image_type_and_shape_detector

source_image_path = "/home/yingshaoxo/Downloads/water.jpg"
print(image_type_and_shape_detector.get_image_type(source_image_path))
print(image_type_and_shape_detector.get_image_shape(source_image_path))
