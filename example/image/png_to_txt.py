from auto_everything.disk import Disk
disk = Disk()

source_image_path = "/home/yingshaoxo/Downloads/water.png"
target_image_path = disk.join_paths(disk.get_directory_path(source_image_path), "new.png")

from auto_everything.image import Image
image = Image()

a_image = image.read_image_from_file(source_image_path)
a_image.print(width=70)

#a_image.resize(512, 512)
a_image = a_image.get_simplified_image()
a_image.save_image_to_file_path(target_image_path+".txt", extreme=True)
a_image.save_image_to_file_path(target_image_path+".json")
a_image.save_image_to_file_path(target_image_path)

input("Want to load them back?")
a_image_1 = image.read_image_from_file(target_image_path+".json").copy()
a_image_1.print()
a_image_2 = image.read_image_from_file(target_image_path+".txt").copy()
a_image_2.print()
a_image_2.save_image_to_file_path(target_image_path)

print(str(a_image_1.raw_data) == str(a_image_2.raw_data))
