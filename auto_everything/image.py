from typing import Any
import json


class Image:
    """
    This class will represent image as 2D list. For example [[r,g,b,a], [r,g,b,a]] means two RGBA point.
    And with this image, you could do crop, put_on_top operations.
    """
    """
    It is a pure image based library. or RGBA 2-dimensional array based library. The final output and middle representation is pure number and arrays. We can add sub_picture to the top of another picture in a specified position. Anything photoshop_like image editor could do, we could do. Anything a 3D game engine could do, we could do.
    """
    def __init__(self, data=None):
        self.raw_data = None

        if data == None:
            self.raw_data = self.create_an_image(1, 1)
        else:
            self.raw_data = data

    def __getitem__(self, idx):
        return self.raw_data[idx]

    def __str__(self):
        text = "An yingshaoxo image object with shape of: "
        text += str(self.get_shape()) + " (height, width)"
        text += "\n"
        text += "The base first RGBA element is: "
        text += str(self.raw_data[0][0])
        return text

    def create_an_image(self, height, width):
        data = []
        for row_index in range(0, height):
            one_row = []
            for column_index in range(0, width):
                one_row.append([255, 255, 255, 255])
            data.append(one_row)
        return Image(data=data)

    def get_shape(self):
        """
        return [height, width]
        """
        rows = len(self.raw_data)
        if rows == 0:
            return [0, 0]
        else:
            return [rows, len(self.raw_data[0])]

    def read_image_from_file(self, file_path):
        if file_path.endswith(".png") or file_path.endswith(".jpg"):
            print("Since png or jpg is too complex to implement, we strongly recommand you to save raw_data as text, for example, 'hi.png.json', then do a text level compression.")
            from PIL import Image as _Image
            the_image = _Image.open(file_path)
            height, width = the_image.size[1], the_image.size[0]

            new_image = self.create_an_image(height=height, width=width)

            """
            data = []
            for pixel in the_image.convert('RGBA').getdata():
                data.append(list(pixel))
            """
            data = the_image.convert('RGBA').getdata()

            for row_index in range(0, height):
                base_index = row_index * width
                for column_index in range(0, width):
                    new_image.raw_data[row_index][column_index] = list(data[base_index + column_index])

            return new_image
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return Image(json.loads(f.read()))

    def save_image_to_file_path(self, file_path):
        if file_path.endswith(".png") or file_path.endswith(".jpg"):
            print("Since png or jpg is too complex to implement, we strongly recommand you to save raw_data as text, for example, 'hi.png.json', then do a text level compression.")
            from PIL import Image as _Image
            import numpy
            the_image = _Image.fromarray(numpy.uint8(self.raw_data))
            the_image.save(file_path)
        else:
            """
            For image, maybe convert it to ascii is a good compression idea
            """
            raw_data = json.dumps(self.raw_data, ensure_ascii=False)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(raw_data)


class Animation:
    """
    This class will play Image list as Video, or export them as video file.
    For example, play 20 images per second.
    """


class GUI:
    """
    This class will use Image class to represent graphic user interface, and also provide a top componet infomation list
    Which contains the touchable area for each component. For example, it has a function called "touch(y,x) -> image_id"
    """
    pass


class MyPillow():
    """
    python3 -m pip install --upgrade Pillow
    """
    def __init__(self):
        from io import BytesIO
        from PIL import Image
        self._Image = Image
        self._BytesIO = BytesIO

        from auto_everything.disk import Disk
        self._disk = Disk()

    def read_image_from_file(self, file_path: str):
        return self._Image.open(file_path)

    def read_image_from_bytes_io(self, bytes_io: Any):
        return self._Image.open(bytes_io)

    def read_image_from_base64_string(self, base64_string: str):
        return self.read_image_from_bytes_io(self._disk.base64_to_bytesio(base64_string=base64_string))

    def save_image_to_file_path(self, image: Any, file_path: str):
        image.save(file_path)

    def save_bytes_io_image_to_file_path(self, bytes_io_image: Any, file_path: str):
        with open(file_path, "wb") as f:
            f.write(bytes_io_image.getbuffer())

    def get_image_bytes_size(self, image):
        image = image.convert('RGB')
        out = self._BytesIO()
        image.save(out, format="jpeg")
        return out.tell()

    def decrease_the_size_of_an_image(self, image: Any, quality=None) -> Any:
        image = image.convert('RGB')
        out = self._BytesIO()
        if quality is None:
            image.save(out, format="jpeg")
        else:
            image.save(out, format="jpeg", optimize=True, quality=quality)
        out.seek(0)
        return out

    def force_decrease_image_file_size(self, image: Any, limit_in_kb: int=1024) -> Any:
        """
        :param image: PIL image
        :param limit: kb
        :return: bytes_io
        """
        image = image.convert('RGB')
        OK = False
        quality = 100
        out = self._BytesIO()
        while (OK is False):
            out = self._BytesIO()
            image.save(out, format="jpeg", optimize=True, quality=quality)
            size = self._disk.get_file_size(path=None, bytes_size=out.tell(), level="KB")
            if size is None:
                break
            quality -= 3
            if size <= limit_in_kb or quality <= 3:
                OK = True
        out.seek(0)
        return out


if __name__ == "__main__":
    from auto_everything.disk import Disk
    disk = Disk()
    image = Image()
    a_image = image.read_image_from_file(disk._expand_user("~/Downloads/cat.jpg"))
    print(a_image.get_shape())
    print(a_image[0][0])
    print(a_image)
    a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/ok111.png.json")
