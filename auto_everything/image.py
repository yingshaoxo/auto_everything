from typing import Any
import json
from auto_everything.font_ import get_ascii_8_times_16_points_data


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

    def create_an_image(self, height, width, color=[255,255,255,255]):
        data = []
        for row_index in range(0, height):
            one_row = []
            for column_index in range(0, width):
                one_row.append(color)
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
            # overflow_situation: another image bigger than original image
            #raise Exception("The another image height and width should smaller than base image.")
            pass

        another_image = another_image.copy()
        another_image.resize(height, width)

        y_start = top
        y_end = top + height
        x_start = right
        x_end = right + width

        # overflow_situation: another image smaller than original image, but paste to outside
        if y_end > base_image_height:
            y_end = base_image_height
        if x_end > base_image_width:
            x_end = base_image_width

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
                if index < len(old_data):
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
        """
        I have a new idea about image representation:
            1. For lines, for example, circuits, you can only use stright line and two_point_with_radius_arc_line to define everything.
            2. For other colorful image, you can only use rectangle to define everything. Square is a special rectangle, especially 1x1 square, which normally means a point.
            3. For 3D world, is can also combined with basic shapes, for example, cube, cuboid, sphere.
        """
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


class Container:
    def __init__(self, height=1.0, width=1.0, children=[], rows=None, columns=None, color=[255,255,255,255], image=None, text="", text_color=[0,0,0,255], text_size=1, parent_height=None, parent_width=None, on_click_function=None):
        """
        height: "8" means "8px", "0.5" means "50% of its parent container"
        width: "20" means "20px", "0.2" means "20%"
        children: [Container(), ]
        rows: True
        columns: False
        color: [255,255,255,255]
        image: Image()
        text: ""
        text_color: [0,0,0,255]
        text_size: 1
        """
        if (type(height) != int and type(height) != float) or (type(width) != int and type(width) != float):
            raise Exception("Height and width for root window must be integer. For example, '20' or '100'")

        self.height = height
        self.width = width
        self.children = children
        self.rows = rows
        self.columns = columns
        self.color = color
        self.image = image
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.parent_height = parent_height
        self.parent_width = parent_width

        self.real_property_dict = {}
        """
        self.real_property_dict["left_top_y"] = 0
        self.real_property_dict["left_top_x"] = 0
        self.real_property_dict["right_bottom_y"] = height
        self.real_property_dict["right_bottom_x"] = width
        """

        self.old_propertys = []
        self.cache_image = None

        if on_click_function != None:
            self.on_click_function = on_click_function
        else:
            def on_click(*arg):
                print("Default click hander:")
                print(f"Click at {str(arg)}")
                info = {"height": self.height, "width": self.width, "color": self.color}
                print(json.dumps(info, indent=4))

            self.on_click_function = on_click

    def _convert_text_to_container_list(self, text, parent_height, parent_width):
        children = []

        the_height = 16 * self.text_size
        the_width = 8 * self.text_size
        maximum_character_number_per_row = int(parent_width / the_width)

        # let the text fill the parent_container
        new_text = ""
        for line in text.split("\n"):
            while len(line) > maximum_character_number_per_row:
                new_text += line[:maximum_character_number_per_row]
                new_text += "\n"
                line = line[maximum_character_number_per_row:]
            if len(line) != "":
                new_text += line
                new_text += "\n"
            new_text += "\n"
        text = new_text

        for line_index, line in enumerate(text.split("\n")):
            if line_index != 0:
                children.append(Container(height=8, width=1.0)) # line sperator

            text_row_container = Container(height=the_height, width=1.0, children=[], columns=True)

            for char in line:
                if not char.isascii():
                    char = " "
                char_points_data = get_ascii_8_times_16_points_data(char)
                for row_index, row in enumerate(char_points_data):
                    for column_index, element in enumerate(row):
                        if element == 1:
                            char_points_data[row_index][column_index] = self.text_color
                        else:
                            char_points_data[row_index][column_index] = self.color
                char_image = Image().create_an_image(height=16, width=8, color=self.color)
                char_image.raw_data = char_points_data
                char_image.resize(height=the_height, width=the_width)
                text_row_container.children.append(Container(image=char_image, height=the_height, width=the_width, columns=True))

            children.append(text_row_container)

        return children

    def render(self):
        """
        returns a real container that uses fixed pixel values
        """
        new_propertys = [self.height, self.width, self.children, self.rows, self.columns, self.color, self.image, self.text, self.parent_height, self.parent_width, self.real_property_dict]
        if new_propertys != self.old_propertys:
            self.old_propertys = new_propertys
        else:
            return self.cache_image

        real_image = None

        if (type(self.height) != int and type(self.height) != float) or (type(self.width) != int and type(self.width) != float):
            raise Exception("Height and width must be numbers. For example, 0.2 or 20. (0.2 means 20% of its parent)")

        real_height = None
        real_width = None

        if type(self.height) == float:
            if self.parent_height == None:
                raise Exception("parent_height shoudn't be None")
            real_height = int(self.parent_height * self.height)
        else:
            real_height = self.height

        if type(self.width) == float:
            if self.parent_width == None:
                raise Exception("parent_width shoudn't be None")
            real_width = int(self.parent_width * self.width)
        else:
            real_width = self.width

        if self.image != None:
            temp_image = self.image.copy()
            temp_image.resize(real_height, real_width)
            real_image = temp_image
        else:
            real_image = Image()
            real_image = real_image.create_an_image(real_height, real_width, self.color)

        if self.text != "":
            self.children = self._convert_text_to_container_list(self.text, parent_height=real_height, parent_width=real_width)
            self.rows = True
            #self.render().save_image_to_file_path(f"/home/yingshaoxo/Downloads/1.png")

        real_height, real_width = real_image.get_shape()
        self.real_property_dict["height"] = real_height
        self.real_property_dict["width"] = real_width

        if self.rows == None and self.columns == None:
            if self.text != "":
                self.columns = True
            else:
                self.rows = True
        if self.rows != True and self.columns != True:
            self.rows = True
        if self.rows == self.columns:
            raise Exception("You can either set rows to True or set columns to True, but not both.")

        if self.rows == True:
            top = 0
            right = 0
            for one_row_container in self.children:
                one_row_container.parent_height = self.real_property_dict["height"]
                one_row_container.parent_width = self.real_property_dict["width"]
                real_one_row_image = one_row_container.render()

                one_row_height, one_row_width = real_one_row_image.get_shape()
                #if (top + one_row_height) > real_height or (right + one_row_width) > real_width:
                    #break
                real_image.paste_image_on_top_of_this_image(real_one_row_image, top=top, right=right, height=one_row_height, width=one_row_width)
                one_row_container.real_property_dict["left_top_y"] = top
                one_row_container.real_property_dict["left_top_x"] = right
                one_row_container.real_property_dict["right_bottom_y"] = top + one_row_height
                one_row_container.real_property_dict["right_bottom_x"] = one_row_width

                top += one_row_height
        elif self.columns == True:
            right = 0
            top = 0
            for one_column_container in self.children:
                one_column_container.parent_height = self.real_property_dict["height"]
                one_column_container.parent_width = self.real_property_dict["width"]
                real_one_column_image = one_column_container.render()

                one_column_height, one_column_width = real_one_column_image.get_shape()
                #if (top + one_column_height) > real_height or (right + one_column_width) > real_width:
                    #break
                real_image.paste_image_on_top_of_this_image(real_one_column_image, top=top, right=right, height=one_column_height, width=one_column_width)
                one_column_container.real_property_dict["left_top_y"] = top
                one_column_container.real_property_dict["left_top_x"] = right
                one_column_container.real_property_dict["right_bottom_y"] = one_column_height
                one_column_container.real_property_dict["right_bottom_x"] = right+one_column_width

                right += one_column_width

        self.cache_image = real_image
        return real_image

    def click(self, y, x):
        """
        When user click a point, we find the root container they click, then we loop that root container to find out which child container that user click...
        """
        if len(self.children) == 0:
            self.on_click_function(y, x)
            return True

        clicked = False
        if self.rows == True:
            top = 0
            for one_row_container in self.children:
                real_one_row_image = one_row_container.render()
                one_row_height, one_row_width = real_one_row_image.get_shape()

                left_top_y = one_row_container.real_property_dict.get("left_top_y")
                left_top_x = one_row_container.real_property_dict.get("left_top_x")
                right_bottom_y = one_row_container.real_property_dict.get("right_bottom_y")
                right_bottom_x = one_row_container.real_property_dict.get("right_bottom_x")

                if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                    clicked = clicked or one_row_container.click(y-top, x)

                top += one_row_height
        elif self.columns == True:
            right = 0
            for one_column_container in self.children:
                real_one_column_image = one_column_container.render()
                one_column_height, one_column_width = real_one_column_image.get_shape()

                left_top_y = one_column_container.real_property_dict.get("left_top_y")
                left_top_x = one_column_container.real_property_dict.get("left_top_x")
                right_bottom_y = one_column_container.real_property_dict.get("right_bottom_y")
                right_bottom_x = one_column_container.real_property_dict.get("right_bottom_x")

                if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                    clicked = clicked or one_column_container.click(y, x-right)

                right += one_column_width

        if clicked == False:
            left_top_y = self.real_property_dict.get("left_top_y")
            left_top_x = self.real_property_dict.get("left_top_x")
            right_bottom_y = self.real_property_dict.get("right_bottom_y")
            right_bottom_x = self.real_property_dict.get("right_bottom_x")
            if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                # clicked at this container, but no children matchs, the point is at background
                self.on_click_function(y, x)
                return True

        return clicked


class GUI(Container):
    """
    This class will use Image class to represent graphic user interface, and also provide a top componet infomation list
    Which contains the touchable area for each component. For example, it has a function called "touch(y,x) -> image_id"

    We have to render the graph whenever the widget/component tree get changed

    The component tree is not a tree, it is a 2d array (matrix), it was combined with rows and columns. Normally row width got change according to parent window change, but height is fixed. It is similar to flutter or web broswer. Those elements inside those list is components. You can call self.render() to render that component matrix.

    In here, for User Interface, the parent big window would always be a rectangle, for example, 54*99 (1080*1980).

    The core feature should be:
    1. when children height or width beyound parent container, use a scroll bar automatically in either y or x direction. (in css, it is overflow-y or overflow-x)
    2. auto re-render a child container when one of global variable they use got changed. and for other container that did not change, we use cached image. someone call this feature "hot reload when variable got changed"
    3. when user click a point, the GUI class should know which container the user clicked. so we can call on_click_function in that container.
    """
    def __init__(self, *arguments, **key_arguments):
        super().__init__(*arguments, **key_arguments)


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
