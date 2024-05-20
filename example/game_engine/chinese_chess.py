from auto_everything.image import GUI, Container
from auto_everything.terminal import Terminal, Advanced_Terminal_User_Interface
terminal = Terminal()
advanced_terminal_interface = Advanced_Terminal_User_Interface()


class Chinese_Chess():
    def __init__(self, window_height=270*1.2, window_width=480*2):
        self.window_height = window_height
        self.window_width = window_width
        self.raw_data = [
            ["car", "horse", "elephant", "guard", "general", "guard", "elephant", "horse", "car"],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "cannon", ".", ".", ".", ".", ".", "cannon", "."],
            ["soldier", ".", "soldier", ".", "soldier", ".", "soldier", ".", "soldier"],
            ["soldier", ".", "soldier", ".", "soldier", ".", "soldier", ".", "soldier"],
            [".", "cannon", ".", ".", ".", ".", ".", "cannon", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["car", "horse", "elephant", "guard", "general", "guard", "elephant", "horse", "car"],
        ]
        self.height = len(self.raw_data)
        self.width = len(self.raw_data[0])
        for y in range(0, int(self.height/2)):
            self.raw_data[y] = [one.upper() for one in self.raw_data[y]]
        for y in range(self.height+int(self.height/2), self.height):
            self.raw_data[y] = [one.lower() for one in self.raw_data[y]]

        self.pointer = [7, 4] #[y, x]
        self.choose_pointer = None

    def _get_symbol_matrix(self):
        data = self.raw_data[:4] + [["-------"]*9] + self.raw_data[4:]
        return data

    def _get_information_about_a_point(self, pointer=None):
        if pointer == None:
            pointer = self.pointer
        point = self.raw_data[pointer[0]][pointer[1]].strip("-><- ")
        information = {
            "type": ".",
            "name": ".",
            "raw": "."
        }
        if point == ".":
            # empty slot
            return information

        if point[0].isupper():
            information["type"] = "black"
        else:
            information["type"] = "red"

        information["raw"] = point
        information["name"] = point.lower()

        return information

    def get_status(self):
        data = []
        for row in self.raw_data:
            a_row = []
            for one in row:
                a_row.append(one.strip("-><-"))
            data.append(a_row)
        return data

    def _clear_all_specail_symbols(self):
        data = []
        for row in self.raw_data:
            a_row = []
            for one in row:
                a_row.append(one.strip("-><-"))
            data.append(a_row)
        self.raw_data = data

    def _move_to_pointer(self, y, x):
        if 0 <= y < self.height and 0 <= x < self.width:
            self.pointer = [y, x]
            pointer = self.pointer
            y, x = pointer
            old_point_information = self._get_information_about_a_point([y, x])

            self. _clear_all_specail_symbols()

            if self.choose_pointer == None:
                self.raw_data[y][x] = "->" + old_point_information["raw"] + "<-"
            else:
                self.raw_data[y][x] = "-->" + old_point_information["raw"] + "<--"

    def do_an_action(self, action):
        """
        action: [pointer_from, pointer_to]
        """
        pass

    def is_win(self):
        pass

    def _clear_screen(self):
        print("\n" * 100)
        terminal.run_command("clear")

    def _display(self):
        self._clear_screen()
        result = self.render()
        print(result)

    def _focus_or_unfocus_on_current_pointer(self):
        y, x = self.pointer
        old_point_information = self._get_information_about_a_point([y, x])

        self. _clear_all_specail_symbols()

        if self.choose_pointer == None:
            self.raw_data[y][x] = "-->" + old_point_information["raw"] + "<--"
        else:
            self.raw_data[y][x] = "->" + old_point_information["raw"] + "<-"

    def _attack(self, from_pointer, to_pointer):
        def take_that_pointer(from_pointer, to_pointer):
            self.raw_data[to_pointer[0]][to_pointer[1]] = self.raw_data[from_pointer[0]][from_pointer[1]]
            self.raw_data[from_pointer[0]][from_pointer[1]] = "."
            self.pointer = to_pointer
            self._focus_or_unfocus_on_current_pointer()

        from_point_information = self._get_information_about_a_point(from_pointer)
        to_point_information = self._get_information_about_a_point(to_pointer)

        if from_point_information["type"] == to_point_information["type"]:
            # same type point, do nothing
            return
        elif from_point_information["type"] != ".":
            # attck if move allowed
            if from_point_information["name"] == "soldier":
                if from_point_information["type"] == "red":
                    if from_pointer[0] > 3:
                        if from_pointer[1] != to_pointer[1]:
                            # not moving forward
                            return
                        else:
                            # only move forward is allowd
                            if from_pointer[0] - to_pointer[0] != 1:
                                # not moving forward for one slot
                                return
                            else:
                                # do it
                                take_that_pointer(from_pointer, to_pointer)
                    else:
                        # move forward, left, right is allowd
                        if (from_pointer[0] - to_pointer[0] == 1) and (abs(from_pointer[1] - to_pointer[1]) == 0):
                            # move forward
                            take_that_pointer(from_pointer, to_pointer)
                        elif (from_pointer[0] - to_pointer[0] == 0) and (abs(from_pointer[1] - to_pointer[1]) == 1):
                            # move left or right
                            take_that_pointer(from_pointer, to_pointer)
                elif from_point_information["type"] == "black":
                    if from_pointer[0] <= 3:
                        if from_pointer[1] != to_pointer[1]:
                            # not moving forward
                            return
                        else:
                            # only move forward is allowd
                            if to_pointer[0] - from_pointer[0] != 1:
                                # not moving forward for one slot
                                return
                            else:
                                # do it
                                take_that_pointer(from_pointer, to_pointer)
                    else:
                        # move forward, left, right is allowd
                        if (to_pointer[0] - from_pointer[0] == 1) and (abs(from_pointer[1] - to_pointer[1]) == 0):
                            # move forward
                            take_that_pointer(from_pointer, to_pointer)
                        elif (to_pointer[0] - from_pointer[0] == 0) and (abs(from_pointer[1] - to_pointer[1]) == 1):
                            # move left or right
                            take_that_pointer(from_pointer, to_pointer)
            elif from_point_information["name"] == "car":
                if (abs(from_pointer[0] - to_pointer[0]) != 0) and (abs(from_pointer[1] - to_pointer[1]) == 0):
                    # horizontal move
                    if (from_pointer[0] - to_pointer[0]) > 0:
                        # go up
                        direction = -1
                    else:
                        # go down
                        direction = 1
                    if direction == -1:
                        # check if up direction has any other chess point, if so, move is not allowd
                        for i in range(to_pointer[0]+1, from_pointer[0]):
                            a_point_information = self._get_information_about_a_point([i, to_pointer[1]])
                            if a_point_information["type"] != ".":
                                return
                    else:
                        # check if up direction has any other chess point, if so, move is not allowd
                        for i in range(from_pointer[0]+1, to_pointer[0]):
                            a_point_information = self._get_information_about_a_point([i, to_pointer[1]])
                            if a_point_information["type"] != ".":
                                return
                    take_that_pointer(from_pointer, to_pointer)
                elif (abs(from_pointer[0] - to_pointer[0]) == 0) and (abs(from_pointer[1] - to_pointer[1]) != 0):
                    # vertical move
                    if (from_pointer[1] - to_pointer[1]) > 0:
                        # go left
                        direction = -1
                    else:
                        # go right
                        direction = 1
                    if direction == -1:
                        # check if left direction has any other chess point, if so, move is not allowd
                        for i in range(to_pointer[1]+1, from_pointer[1]):
                            a_point_information = self._get_information_about_a_point([to_pointer[0], i])
                            if a_point_information["type"] != ".":
                                return
                    else:
                        # check if right direction has any other chess point, if so, move is not allowd
                        for i in range(from_pointer[1]+1, to_pointer[1]):
                            a_point_information = self._get_information_about_a_point([to_pointer[0], i])
                            if a_point_information["type"] != ".":
                                return
                    take_that_pointer(from_pointer, to_pointer)

    def _handle_choose_action(self):
        empty_slot = False

        current_pointer_info = self._get_information_about_a_point(self.pointer)
        if current_pointer_info["type"] == ".":
            empty_slot = True

        #if empty_slot == False:
        self._focus_or_unfocus_on_current_pointer()

        if self.choose_pointer == None and empty_slot == False:
            self.choose_pointer = self.pointer
        elif self.choose_pointer != None:
            self._attack(self.choose_pointer, self.pointer)
            self.choose_pointer = None

    def play(self):
        self._move_to_pointer(self.pointer[0], self.pointer[1])
        self._display()
        print("\n\n")
        print("1.Use w,s,a,d to move")
        print("2.Use enter,space to choose")
        print("3.soldier can only move one slot forward each time, and if it across the line, it can move left or right one slot each time; car can only go stright, up, down, left, or right; ")
        print("x.Use q to quit")
        while True:
            char = advanced_terminal_interface.get_char_input_in_blocking_way()
            ok = False
            if char in ["q", chr(27)]:
                exit()
            elif char in ["w", "s", "a", "d"]:
                ok = True
                old_y, old_x = self.pointer
                if char == "w":
                    self._move_to_pointer(old_y-1, old_x)
                elif char == "s":
                    self._move_to_pointer(old_y+1, old_x)
                elif char == "a":
                    self._move_to_pointer(old_y, old_x-1)
                elif char == "d":
                    self._move_to_pointer(old_y, old_x+1)
            elif char in [" ", chr(13)]:
                ok = True
                self._handle_choose_action()
            if ok == True:
                self._display()

    def _get_chess_matrix_container(self):
        def chess_click():
            print("clicked")

        symbols = self._get_symbol_matrix()
        one_row_height = 1/len(symbols)
        one_point_width = 1/len(symbols[0])
        rows = []
        for y, row in enumerate(symbols):
            column_list = []
            for x, symbol in enumerate(row):
                column_list.append(Container(width=one_point_width, text=symbol, on_click_function=chess_click))

            one_row = Container(
                height=one_row_height,
                width=1.0,
                columns=True,
                children=column_list
            )

            rows.append(one_row)

        root_container = Container(
            height=1.0,
            width=1.0,
            rows=True,
            children=rows
        )

        root_container.parent_height=self.window_height
        root_container.parent_width=self.window_width

        return root_container

    def render(self):
        gui_container = self._get_chess_matrix_container()
        text_2d_array = gui_container.render_as_text()
        text = ""
        for row in text_2d_array:
            row_text = "".join(row)
            text += row_text + "\n"
        return text


if __name__ == "__main__":
    chinese_chess = Chinese_Chess()
    chinese_chess.play()
