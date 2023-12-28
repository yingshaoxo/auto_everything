from auto_everything.image import MyPillow
from auto_everything.disk import Disk

mypillow = MyPillow()
disk = Disk()

source_image_path = "/home/yingshaoxo/Downloads/atlantis_space.png"
an_image = mypillow.read_image_from_file(file_path=source_image_path)
bytes_io_image = mypillow.force_decrease_image_file_size(an_image, limit_in_kb=50)

mypillow.save_bytes_io_image_to_file_path(bytes_io_image=bytes_io_image, file_path=disk.join_paths(disk.get_directory_path(source_image_path), "new.jpg"))
