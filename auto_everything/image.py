from PIL import Image
from io import BytesIO

from auto_everything.disk import Disk
disk = Disk()


class MyPillow():
    def read_image_from_bytes_io(self, bytes_io):
        return Image.open(bytes_io)

    def save_image_to_file_path(self, image, file_path):
        """
        foamat = [jpeg, png]
        """
        image.save(file_path)

    def get_image_bytes_size(self, image):
        image = image.convert('RGB')
        out = BytesIO()
        image.save(out, format="jpeg")
        return out.tell()

    def decrease_the_size_of_an_image(self, image, quality=None):
        image = image.convert('RGB')
        out = BytesIO()
        if quality is None:
            image.save(out, format="jpeg")
        else:
            image.save(out, format="jpeg", optimize=True, quality=quality)
        out.seek(0)
        return out

    def force_decrease_image_file_size(self, image, limit_in_kb: int=1024):
        """
        :param image: PIL image
        :param limit: kb
        :return: bytes_io
        """
        image = image.convert('RGB')
        OK = False
        quality = 100
        out = BytesIO()
        while (OK is False):
            out = BytesIO()
            image.save(out, format="jpeg", optimize=True, quality=quality)
            size = disk.get_file_size(path=None, bytes_size=out.tell(), level="KB")
            if size is None:
                break
            quality -= 10
            if size <= limit_in_kb or quality <= 10:
                OK = True
        out.seek(0)
        return out
