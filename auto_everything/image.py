from io import BytesIO
from PIL import Image

from auto_everything.disk import Disk
disk = Disk()


class MyPillow():
    def read_image_from_file(self, file_path: str):
        return Image.open(file_path)

    def read_image_from_bytes_io(self, bytes_io: BytesIO):
        return Image.open(bytes_io)

    def read_image_from_base64_string(self, base64_string: str):
        return self.read_image_from_bytes_io(disk.base64_to_bytesio(base64_string=base64_string))

    def save_image_to_file_path(self, image: Image.Image, file_path: str):
        image.save(file_path)

    def save_bytes_io_image_to_file_path(self, bytes_io_image: BytesIO, file_path: str):
        with open(file_path, "wb") as f:
            f.write(bytes_io_image.getbuffer())

    def get_image_bytes_size(self, image):
        image = image.convert('RGB')
        out = BytesIO()
        image.save(out, format="jpeg")
        return out.tell()

    def decrease_the_size_of_an_image(self, image: Image.Image, quality=None) -> BytesIO:
        image = image.convert('RGB')
        out = BytesIO()
        if quality is None:
            image.save(out, format="jpeg")
        else:
            image.save(out, format="jpeg", optimize=True, quality=quality)
        out.seek(0)
        return out

    def force_decrease_image_file_size(self, image: Image.Image, limit_in_kb: int=1024) -> BytesIO:
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
            quality -= 3
            if size <= limit_in_kb or quality <= 3:
                OK = True
        out.seek(0)
        return out
