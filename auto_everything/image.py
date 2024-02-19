import json
try:
    from auto_everything.font_ import get_ascii_8_times_16_points_data
except Exception as e:
    from font_ import get_ascii_8_times_16_points_data


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
            row = [None] * width
            for column_index in range(0, width):
                row[column_index] = color
            data.append(row)
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
            data.append(list(row))
        return Image(data)

    def _resize_an_list(self, a_list, old_length, new_length):
        # for downscale, you use "sub_window_length == int(old_size/new_size)", for each sub_window pixels, you only take the first pixel
        # for upscale, you use "it == int(new_size/old_size)", for each old pixel, you times that pixel by it, if the final pixels data is not meet the required length, we add transparent black color at the bottom
        new_list = []

        if old_length == new_length:
            return a_list
        if old_length > new_length:
            # downscale
            new_list = [None] * new_length
            sub_window_length = int(old_length/new_length)
            index = 0
            counting = 0
            while True:
                first_element = a_list[index]
                new_list[counting] = first_element
                counting += 1
                if counting >= new_length:
                    break
                index += sub_window_length
                if index >= old_length:
                    break
        else:
            # upscale
            new_list = []
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
        """
        data_2 = []
        for column in list(zip(*data)):
            data_2.append(self._resize_an_list(column, old_height, height))
        self.raw_data = list(zip(*data_2))
        """
        data_2 = []
        old_width = len(data[0])
        initialized = False
        for column_index in range(old_width):
            temp_column_list = [None] * old_height
            for row_index in range(old_height):
                element = data[row_index][column_index]
                temp_column_list[row_index] = element
            column_list = self._resize_an_list(temp_column_list, old_height, height)
            if initialized == False:
                data_2 += [[one] for one in column_list]
                initialized = True
            else:
                for index, one in enumerate(column_list):
                    data_2[index].append(one)

        self.raw_data = data_2

    def paste_image_on_top_of_this_image(self, another_image, top, left, height, width):
        """
        paste another image to current image based on (top, left, height, width) position in current image
        """
        base_image_height, base_image_width = self.get_shape()
        another_image_height, another_image_width = another_image.get_shape()
        if another_image_height > base_image_height or another_image_width > base_image_width:
            # overflow_situation: another image bigger than original image
            #raise Exception("The another image height and width should smaller than base image.")
            pass

        if another_image_height != height or another_image_width != width:
            another_image = another_image.copy()
            another_image.resize(height, width)

        y_start = top
        y_end = top + height
        x_start = left
        x_end = left + width

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
            old_data_length = len(old_data)
            new_data = [None] * old_data_length
            for index, one in enumerate(another_image[y_index-y_start][:old_data_length]):
                if one[3] == 0:
                    new_data[index] = old_data[index]
                else:
                    new_data[index] = one
            self.raw_data[y_index][x_start: x_end] = new_data

    def read_image_from_file(self, file_path):
        if file_path.endswith(".png") or file_path.endswith(".jpg"):
            try:
                from PIL import Image as _Image
            except Exception as e:
                print(e)
                print("Since png or jpg is too complex to implement, we strongly recommand you to save raw_data as text, for example, 'hi.png.json', then do a text level compression.")

            the_image = _Image.open(file_path)
            height, width = the_image.size[1], the_image.size[0]

            new_image = self.create_an_image(height=height, width=width)

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
            try:
                from PIL import Image as _Image
                import numpy
                the_image = _Image.fromarray(numpy.uint8(self.raw_data))
                the_image.save(file_path)
            except Exception as e:
                print(e)
                print("Since png or jpg is too complex to implement, we strongly recommand you to save raw_data as text, for example, 'hi.png.json', then do a text level compression.")
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


char_image_container_cache = {} # 'size+char' as key, image_container as value


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

        self.real_property_dict["one_row_height"] = 0
        self.real_property_dict["one_column_width"] = 0
        """

        self.old_propertys = []
        self.cache_image = None

        if on_click_function != None:
            self.on_click_function = on_click_function
        else:
            def on_click():
                return

            self.on_click_function = on_click

    def _is_ascii(self, char):
        #return all(ord(c) < 128 for c in s)
        return ord(char) < 128

    def _convert_text_to_container_list(self, text, parent_height, parent_width, on_click_function):
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
            #if line_index != 0:
            #    children.append(Container(height=8, width=parent_width)) # line sperator

            text_row_container = Container(height=the_height, width=parent_width, children=[], columns=True)

            for char in line:
                if not self._is_ascii(char):
                    char = " "
                char_points_data = get_ascii_8_times_16_points_data(char)
                for row_index, row in enumerate(char_points_data):
                    for column_index, element in enumerate(row):
                        if element == 1:
                            char_points_data[row_index][column_index] = self.text_color
                        else:
                            char_points_data[row_index][column_index] = self.color

                char_id = f"{self.text_size}+{char}"
                if char_id not in char_image_container_cache:
                    char_image = Image().create_an_image(height=16, width=8, color=self.color)
                    char_image.raw_data = char_points_data
                    char_image.resize(height=the_height, width=the_width)
                    char_image_container = Container(image=char_image, height=the_height, width=the_width, columns=True)
                    char_image_container_cache[char_id] = char_image_container
                else:
                    char_image_container = char_image_container_cache[char_id]

                char_image_container.on_click_function = on_click_function
                text_row_container.children.append(char_image_container)

            children.append(text_row_container)

        return children

    def _get_propertys_of_a_container(self, one_container):
        return json.dumps([one_container.height, one_container.width, one_container.rows, one_container.columns, one_container.color, id(one_container.image), one_container.text, one_container.parent_height, one_container.parent_width, one_container.real_property_dict])

    def _loop_all_components_in_tree_to_see_if_its_child_got_changed(self, root_container):
        queue = [root_container]
        while len(queue) > 0:
            one_container = queue[0]
            queue = queue[1:]
            queue += one_container.children

            new_propertys = self._get_propertys_of_a_container(one_container)
            if new_propertys != one_container.old_propertys:
                #one_container.old_propertys = new_propertys
                return True
        return False

    def render(self):
        """
        returns a real container that uses fixed pixel values
        """
        if self._loop_all_components_in_tree_to_see_if_its_child_got_changed(self) == False:
            return self.cache_image
        else:
            self.old_propertys = self._get_propertys_of_a_container(self)

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
            image_height, image_width = temp_image.get_shape()
            if image_height != real_height or image_width != real_width:
                temp_image.resize(real_height, real_width)
            real_image = temp_image
        else:
            real_image = Image()
            real_image = real_image.create_an_image(real_height, real_width, self.color)

        if self.text != "":
            self.children = self._convert_text_to_container_list(self.text, parent_height=real_height, parent_width=real_width, on_click_function=self.on_click_function)
            self.rows = True

        #real_height, real_width = real_image.get_shape()
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
            left = 0
            for one_row_container in self.children:
                one_row_container.parent_height = self.real_property_dict["height"]
                one_row_container.parent_width = self.real_property_dict["width"]
                real_one_row_image = one_row_container.render()

                one_row_height, one_row_width = real_one_row_image.get_shape()
                real_image.paste_image_on_top_of_this_image(real_one_row_image, top=top, left=left, height=one_row_height, width=one_row_width)
                one_row_container.real_property_dict["left_top_y"] = top
                one_row_container.real_property_dict["left_top_x"] = left
                one_row_container.real_property_dict["right_bottom_y"] = top + one_row_height
                one_row_container.real_property_dict["right_bottom_x"] = one_row_width

                top += one_row_height
        elif self.columns == True:
            left = 0
            top = 0
            for one_column_container in self.children:
                one_column_container.parent_height = self.real_property_dict["height"]
                one_column_container.parent_width = self.real_property_dict["width"]
                real_one_column_image = one_column_container.render()

                one_column_height, one_column_width = real_one_column_image.get_shape()
                real_image.paste_image_on_top_of_this_image(real_one_column_image, top=top, left=left, height=one_column_height, width=one_column_width)
                one_column_container.real_property_dict["left_top_y"] = top
                one_column_container.real_property_dict["left_top_x"] = left
                one_column_container.real_property_dict["right_bottom_y"] = one_column_height
                one_column_container.real_property_dict["right_bottom_x"] = left+one_column_width

                left += one_column_width

        self.cache_image = real_image
        return real_image

    def _render_as_text_component_list(self, top_=0, left_=0):
        """
        try to get global absolute position of those components by only doing resize. (do not use paste_image_on_top_of_this_image function.)
        so that we could simply return those components as a list, let the lcd render those things directly will speed up the process. use 'paste_image_on_top_of_this_image' is kind of slow
        """
        data_list = []

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
            data_list.append({
                "top": top_,
                "left": left_,
                "height": real_height,
                "width": real_width,
                "image": self.image.copy(),
            })
        else:
            data_list.append({
                "top": top_,
                "left": left_,
                "height": real_height,
                "width": real_width,
                "text": self.text,
            })

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
            left = 0
            for one_row_container in self.children:
                one_row_container.parent_height = self.real_property_dict["height"]
                one_row_container.parent_width = self.real_property_dict["width"]
                temp_list = one_row_container._render_as_text_component_list(top_ + top, left_ + left)

                one_row_height = temp_list[0]["height"]
                one_row_width = temp_list[0]["width"]
                one_row_container.real_property_dict["left_top_y"] = top
                one_row_container.real_property_dict["left_top_x"] = left
                one_row_container.real_property_dict["right_bottom_y"] = top + one_row_height
                one_row_container.real_property_dict["right_bottom_x"] = one_row_width

                data_list += temp_list

                top += one_row_height
        elif self.columns == True:
            left = 0
            top = 0
            for one_column_container in self.children:
                one_column_container.parent_height = self.real_property_dict["height"]
                one_column_container.parent_width = self.real_property_dict["width"]
                temp_list = one_column_container._render_as_text_component_list(top_ + top, left_ + left)

                one_column_height = temp_list[0]["height"]
                one_column_width = temp_list[0]["width"]
                one_column_container.real_property_dict["left_top_y"] = top
                one_column_container.real_property_dict["left_top_x"] = left
                one_column_container.real_property_dict["right_bottom_y"] = one_column_height
                one_column_container.real_property_dict["right_bottom_x"] = left + one_column_width

                data_list += temp_list

                left += one_column_width

        return data_list

    def render_as_text(self, text_height=16, text_width=8, pure_text=False):
        component_list = self._render_as_text_component_list()

        char_number_in_one_row = int(self.real_property_dict["width"] // 8)
        rows_number = int(self.real_property_dict["height"] // 16)

        # raw_data = [[" "] * char_number_in_one_row] * rows_number # this will make bugs, if you change one row, every row will get changed
        raw_data = []
        for row_index in range(rows_number):
            one_row = [" "] * char_number_in_one_row
            raw_data.append(one_row)

        for component in component_list:
            top = component["top"]
            left = component["left"]
            height = component["height"]
            width = component["width"]

            real_top = int(top // text_height)
            real_height = int(height // text_height)

            real_left = int(left // text_width)
            real_width = int(width // text_width)

            if "image" in component:
                # image
                image = component["image"]
            else:
                # text
                text = component["text"]
                if text == "":
                    continue
                char_list = list(text)
                for row_index in range(real_top, real_top+real_height):
                    for column_index in range(real_left, real_left+real_width):
                        if len(char_list) == 0:
                            break
                        char = char_list[0]
                        char_list = char_list[1:]
                        if char == "\n":
                            break
                        raw_data[row_index][column_index] = char

        if pure_text == False:
            return raw_data
        else:
            text = ""
            for row in raw_data:
                text += "".join(row) + "\n"
            return text

    def _convert_2d_text_to_image(self, text):
        if type(text) == list:
            text = ""
            for row in text_2d_array:
                text += "".join(row) + "\n"
        root_container = Container(text=text)
        root_container.parent_height=self.real_property_dict["height"]
        root_container.parent_width=self.real_property_dict["width"]
        image = root_container.render()
        return image

    def click(self, y, x):
        """
        When user click a point, we find the root container they click, then we loop that root container to find out which child container that user click...
        """
        if len(self.children) == 0:
            print(self.text)
            self.on_click_function()
            return True

        clicked = False
        if self.rows == True:
            top = 0
            for one_row_container in self.children:
                left_top_y = one_row_container.real_property_dict.get("left_top_y")
                left_top_x = one_row_container.real_property_dict.get("left_top_x")
                right_bottom_y = one_row_container.real_property_dict.get("right_bottom_y")
                right_bottom_x = one_row_container.real_property_dict.get("right_bottom_x")

                if left_top_y != None and left_top_x != None and right_bottom_y != None and right_bottom_x != None:
                    if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                        clicked = clicked or one_row_container.click(y-top, x)
                        break

                top += one_row_container.real_property_dict["height"]
        elif self.columns == True:
            left = 0
            for one_column_container in self.children:
                left_top_y = one_column_container.real_property_dict.get("left_top_y")
                left_top_x = one_column_container.real_property_dict.get("left_top_x")
                right_bottom_y = one_column_container.real_property_dict.get("right_bottom_y")
                right_bottom_x = one_column_container.real_property_dict.get("right_bottom_x")

                if left_top_y != None and left_top_x != None and right_bottom_y != None and right_bottom_x != None:
                    if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                        clicked = clicked or one_column_container.click(y, x-left)
                        break

                left += one_column_container.real_property_dict["width"]

        if clicked == False:
            left_top_y = self.real_property_dict.get("left_top_y")
            left_top_x = self.real_property_dict.get("left_top_x")
            right_bottom_y = self.real_property_dict.get("right_bottom_y")
            right_bottom_x = self.real_property_dict.get("right_bottom_x")
            if left_top_y != None and left_top_x != None and right_bottom_y != None and right_bottom_x != None:
                if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                    # clicked at this container, but no children matchs, the point is at background
                    self.on_click_function()
                    return True

        return clicked

    def advance_click(self, touch_start, touch_move, touch_end, y, x):
        pass


class GUI(Container):
    """
    This class will use Image class to represent graphic user interface, and also provide a top componet infomation list
    Which contains the touchable area for each component. For example, it has a function called "touch(y,x) -> image_id"

    We have to render the graph whenever the widget/component tree get changed

    The component tree is not a tree, it is a 2d array (matrix), it was combined with rows and columns. Normally row width got change according to parent window change, but height is fixed. It is similar to flutter or web broswer. Those elements inside those list is components. You can call self.render() to render that component matrix.

    In here, for User Interface, the parent big window would always be a rectangle, for example, 54*99 (1080*1980).

    The core feature should be:
    1. when children height or width beyound parent container, use a scroll bar automatically in either y or x direction. (in css, it is overflow-y or overflow-x)
    2. auto re-render a child container when one of global variable they use got changed. and for other container that did not change, we use cached image. someone call this feature "hot reload when variable got changed" (Or when user make change on some variable, or if the user call render function, we loop the container tree, see which container's property got changed, if so, we do a re_render. starts from top containers, level down, if re_rendered, only render its children for once) (Or you could use __setattr__(self, name, value) hook in python class, when a property got changed, you call render. def __setattr__(self, name, value): self.__dict__[name] = value)
    3. when user click a point, the GUI class should know which container the user clicked. so we can call on_click_function in that container.
    4. consider give a special paramater to render() function, let it return a list of rectangle that represent those changed part of the screen. So the LCD can render those pixel block very quickly. (for other UI rendering engine, they could just use changed pixel for screen update)
    """
    def __init__(self, *arguments, **key_arguments):
        super().__init__(*arguments, **key_arguments)


#class TextGUI():
#    """
#    Now, think about this: a character will take 8*16 pixels. 320*240 screen could show 40 * 15 = 600 characters. You can treat characters as pixels. Then you only have to handle 600 rectangles. So in your memory, you should have a 600 elements 2d list as graphic buffer.
#    For a terminal, it only has to have print_char function. So it you have LCD char buffer, for each time, you just have to move the top_left point of those char buffers. Just treat it like a one stream display flow (Don't forget the new line).
#    """
#    def __init__(self, height, width):
#        char_number_in_one_row = int(width // 8)
#        rows_number = int(height // 16)
#
#        self.raw_data = [[" "] * char_number_in_one_row] * rows_number


try:
    from typing import Any

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
except Exception as e:
    pass


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
