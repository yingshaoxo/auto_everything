from time import sleep, time
import os

class Terminal_App():
    def __init__(self, height=320, width=240):
        self.height = height
        self.width = width

        self.char_height = 16
        self.char_width = 8
        self.text_height = int(self.height / self.char_height)
        self.text_width = int(self.width / self.char_width)
        self.text = [" "] * self.text_height * self.text_width

        #init_text = "Hi"
        #init_text += "\n\ncontent_view has height and width of:\n"
        #init_text += "{height}, {width}".format(height=height, width=width)
        #self._draw_text(0, 0, init_text)
        self.y = 0
        self.x = 1
        self.current_line_buffer = []
        self.envirnoment_variable_dict = {}

        self._start_line_print()

    def _get_1d_index_from_2d_index(self, y, x):
        return y*self.text_width + x

    def _draw_text(self, y, x, text):
        done = False
        char_index = 0
        text_length = len(text)
        for y_index in range(y, self.text_height):
            for x_index in range(x, self.text_width):
                index = self._get_1d_index_from_2d_index(y_index, x_index)
                if char_index >= text_length:
                    done = True
                    break
                a_char = text[char_index]
                char_index += 1
                if a_char == "\n":
                    break
                self.text[index] = a_char
            x = 0
            if done == True:
                break

    def render_as_text(self):
        self._draw_text(self.y, self.x, "_")
        return "".join(self.text)

    def handle_touch_function(self, y, x):
        print("sub_app_click:", y, x)
        #self.text = "y:{}, x:{}".format(y, x)

    def handle_keyboard_function(self, char):
        print("sub_app get key press:", char)
        #self.text = "{}".format(char)
        if len(char) == 1:
            if char == "\n":
                self._draw_text(self.y, self.x, " ")
                self.x = 0
                self.y += 1

                result = self._run_command("".join(self.current_line_buffer))
                result = result.strip()
                self._draw_text(self.y, self.x, result)

                self.current_line_buffer = []
                self.y += self._get_real_text_height_of_text(result)
                self.x = 0
                self._start_line_print()
                return
            self.current_line_buffer.append(char)
            self._draw_text(self.y, self.x, char)
            if self.x > self.text_width:
                self.y += 1
                self.x = 0
            else:
                self.x += 1
        else:
            if char == "Del":
                self.current_line_buffer.pop()
                self._draw_text(self.y, self.x, " ")
                self._draw_text(self.y, self.x-1, " ")
                if self.x > 0:
                    self.x -= 1

    def handle_resize(self, new_height, new_width):
        pass

    def handle_exit(self):
        # has timeout of 5 seconds
        pass

    def _get_real_text_height_of_text(self, a_text):
        the_height = 0
        lines = a_text.split("\n")
        for line in lines:
            if (len(line) % self.text_width) == 0:
                the_height += int(len(line) / self.text_width)
            else:
                the_height += int(len(line) / self.text_width) + 1
        return the_height

    def _start_line_print(self):
        head_text = "{}$ ".format(os.getcwd())
        self._draw_text(self.y, 0, head_text)
        self.x = len(head_text)

    def _run_command(self, command):
        command = command.strip()
        if command == "ls":
            return "\n".join(os.listdir("."))
        elif command == "uname":
            return "yingshaoxo micropython phone linux system 1.0 2024"
        try:
            result = str(eval(command, globals(), locals()))
        except Exception as e:
            result = str(e)
        return result
