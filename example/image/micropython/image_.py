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
        new_list = []

        if old_length == new_length:
            return a_list
        if old_length > new_length:
            # downscale
            new_list = [None] * new_length
            sub_window_length = old_length/new_length
            index = 0
            counting = 0
            while True:
                first_element = a_list[int(round(index))]
                new_list[counting] = first_element
                counting += 1
                if counting >= new_length:
                    break
                index += sub_window_length
                if index >= old_length:
                    break
        else:
            # upscale
            sub_window_length = new_length/old_length
            new_list = [None] * new_length
            for i in range(new_length):
                old_index = int(i / sub_window_length)
                new_list[i] = a_list[old_index]

        return new_list

    def resize(self, height, width):
        """
        The image resize or pixel iteration in python is 60 times slower than c version, so don't use it as much as possible
        """
        if type(height) != int or type(width) != int:
            raise Exception("The height and width should be integer.")

        old_height, old_width = self.get_shape()
        if old_height == height and old_width == width:
            return self

        # handle width
        data = []
        for row in self.raw_data:
            data.append(self._resize_an_list(row, old_width, width))

        # handle height
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
        return self

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
        import json
        with open(file_path, "r", encoding="utf-8") as f:
            return Image(json.loads(f.read()))

    def save_image_to_file_path(self, file_path):
        """
        For image, maybe convert it to ascii is a good compression idea
        """
        import json
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
    def __init__(self, height=1.0, width=1.0, children=[], rows=None, columns=None, color=[255,255,255,255], image=None, text="", text_color=[0,0,0,255], text_size=1, parent_height=None, parent_width=None, on_click_function=None, information={}):
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
        information: will pass to self.information as a {} dict
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
        self.information = information

        self.real_property_dict = {}

        self.old_propertys = []
        self.cache_image = None

        if on_click_function != None:
            self.on_click_function = on_click_function
        else:
            def on_click(element=None, y=None, x=None):
                return

            self.on_click_function = on_click


        self.get_ascii_8_times_16_points_data = None

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

    def render_as_text(self, text_height=16, text_width=8, pure_text=False, one_dimention_text=False):
        component_list = self._render_as_text_component_list()

        char_number_in_one_row = int(self.real_property_dict["width"] / 8)
        rows_number = int(self.real_property_dict["height"] / 16)

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

            real_top = int(top / text_height)
            real_height = int(height / text_height) # max line number for this container

            real_left = int(left / text_width)
            real_width = int(width / text_width) # max character number per row

            if "image" in component:
                # image
                image = component["image"]
            else:
                # text
                text = component["text"]
                if text == "":
                    continue

                if "\n" in text:
                    center_text = False
                    horizontal_padding_space_number = 0
                else:
                    center_text = True
                    horizontal_padding_space_number = int((real_width - len(text))/2)

                lines = text.split("\n")
                actual_text_lines = len(lines) + sum([len(line)/real_width for line in lines])
                vertical_padding_line_number = int((real_height-actual_text_lines) / 2)

                index = 0
                text_length = len(text)
                for row_index in range(real_top, real_top+real_height):
                    if vertical_padding_line_number > 0:
                        # for center text
                        vertical_padding_line_number -= 1
                        continue
                    for column_index in range(real_left, real_left+real_width):
                        if horizontal_padding_space_number > 0:
                            # for center text
                            horizontal_padding_space_number -= 1
                            continue
                        if index >= text_length:
                            break
                        char = text[index]
                        index += 1
                        if char == "\n":
                            break
                        raw_data[row_index][column_index] = char

        if pure_text == False:
            return raw_data
        else:
            text = ""
            for row in raw_data:
                if one_dimention_text == False:
                    text += "".join(row) + "\n"
                else:
                    text += "".join(row)
            return text

    def click(self, y, x):
        """
        When user click a point, we find the root container they click, then we loop that root container to find out which child container that user click...
        """
        if len(self.children) == 0:
            print(self.text)
            try:
                self.on_click_function(self, y, x)
            except Exception as e:
                try:
                    self.on_click_function()
                except Exception as e2:
                    print(e)
                    print(e2)
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
                    try:
                        self.on_click_function(self, y, x)
                    except Exception as e:
                        try:
                            self.on_click_function()
                        except Exception as e2:
                            print(e)
                            print(e2)
                    return True

        return clicked

    def advance_click(self, touch_start, touch_move, touch_end, y, x):
        pass


class Container_Helper:
    # Help you handle container related operations
    def iterate_child_container(self, root_container):
        # So that you can get a container that has some id in information, and get its real height and width in "node.real_property_dict"
        queue = [root_container]
        while (len(queue) != 0):
            child = queue.pop()
            if len(child.children) != 0:
                queue += child.children.copy()
            yield child
