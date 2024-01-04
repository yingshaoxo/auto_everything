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
            new_image = self.create_an_image(1, 1)
            self.raw_data = new_image.raw_data
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

    def copy(self):
        data = []
        for row in self.raw_data:
            data.append(row.copy())
        return Image(data)

    def _resize_an_list(self, a_list, old_length, new_length):
        # for downscale, you use "sub_window_length == int(old_size/new_size)", for each sub_window pixels, you only take the first pixel
        # for upscale, you use "it == int(new_size/old_size)", for each old pixel, you times that pixel by it, if the final pixels data is not meet the required length, we add transparent black color at the bottom
        new_list = []

        if old_length == new_length:
            return a_list
        if old_length > new_length:
            # downscale
            sub_window_length = int(old_length/new_length)
            index = 0
            counting = 0
            while True:
                first_element = a_list[index]
                new_list.append(first_element)
                counting += 1
                if counting >= new_length:
                    break
                index += sub_window_length
                if index >= old_length:
                    break
        else:
            # upscale
            sub_window_length = int(new_length/old_length)
            for one in a_list:
                new_list += [one] * sub_window_length
            new_list = new_list[:new_length]

            # add missing pixels at the bottom
            counting = sub_window_length * old_length
            new_list += [[0,0,0,0]] * (new_length - counting)

        return new_list

    def resize(self, height, width):
        if type(height) != int or type(width) != int:
            raise Exception("The height and width should be integer.")

        old_height, old_width = self.get_shape()
        if old_height == height and old_width == width:
            return

        # handle width
        data = []
        for row in self.raw_data:
            data.append(self._resize_an_list(row, old_width, width))

        # handle height
        data_2 = []
        old_width = len(data[0])
        initialized = False
        for column_index in range(old_width):
            temp_column_list = []
            for row_index in range(old_height):
                element = data[row_index][column_index]
                temp_column_list.append(element)
            column_list = self._resize_an_list(temp_column_list, old_height, height)
            if initialized == False:
                data_2 += [[one] for one in column_list]
                initialized = True
            else:
                for index, one in enumerate(column_list):
                    data_2[index].append(one)

        self.raw_data = data_2

    def paste_image_on_top_of_this_image(self, another_image, top, right, height, width):
        """
        paste another image to current image based on (top, right, height, width) position in current image
        """
        base_image_height, base_image_width = self.get_shape()
        another_image_height, another_image_width = another_image.get_shape()
        if another_image_height > base_image_height or another_image_width > base_image_width:
            raise Exception("The another image height and width should smaller to base image.")

        another_image = another_image.copy()
        another_image.resize(height, width)

        y_start = top
        y_end = top + height
        x_start = right
        x_end = right + width
        for y_index in range(y_start, y_end):
            #row = self.raw_data[y_index]
            #first_part = row[0:x_start]
            #second_part = row[x_end:]
            #new_row = first_part + another_image[y_index] + second_part
            #self.raw_data[y_index] = new_row

            #self.raw_data[y_index][x_start: x_end] = another_image[y_index-y_start]

            old_data = self.raw_data[y_index][x_start: x_end]
            new_data = []
            for index, one in enumerate(another_image[y_index-y_start]):
                if one[3] == 0:
                    new_data.append(old_data[index])
                else:
                    new_data.append(one)
            self.raw_data[y_index][x_start: x_end] = new_data

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
            #print("Since png or jpg is too complex to implement, we strongly recommand you to save raw_data as text, for example, 'hi.png.json', then do a text level compression.")
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
    pass


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

    #a_image = image.read_image_from_file(disk._expand_user("~/Downloads/cat.jpg"))
    #print(a_image.get_shape())
    #print(a_image[0][0])
    #print(a_image)
    #a_image.resize(96, 128)
    ##a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/cat2.png.json")
    #a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/cat2.png")

    a_image = image.read_image_from_file(disk._expand_user("~/Downloads/hero.png"))
    a_image.resize(512, 512)
    a_image.paste_image_on_top_of_this_image(a_image, 100, 27, 100, 100)
    a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2.png")
