from auto_everything.terminal import Terminal, Advanced_Terminal_User_Interface
terminal = Terminal()
advanced_terminal_interface = Advanced_Terminal_User_Interface()

from time import sleep


class Yingshaoxo_Terminal_Mario():
    def __init__(self):
        self.window_height = 10
        self.window_width = 20
        self.delay = 0.1

        self.reset()

    def _reset_background(self):
        self.raw_data = [['-']*self.window_width for one in range(self.window_height)]

    def reset(self):
        self._reset_background()
        self.mario_position = [6, 0]
        self.brick_position = [6, 11]
        self.render()

    def _get_hero(self):
        return [
            [" ","@"," "],
            ["/","|","\\"],
            [" ","M"," "],
        ]

    def _get_brick(self):
        return [
            ["O","O"],
            ["O","O"],
            ["O","O"],
        ]

    def _real_two_object_collision_detection(self, object_a, object_b):
        if object_a["id"] == object_b["id"]:
            return False
        object_b_4_point_list = [
            object_b["position"].copy(),
            [object_b["position"][0]+object_b["shape"][0], object_b["position"][1]],
            [object_b["position"][0], object_b["position"][1]+object_b["shape"][1]],
            [object_b["position"][0]+object_b["shape"][0], object_b["position"][1]+object_b["shape"][1]],
        ]
        min_y = object_a["position"][0]
        max_y = min_y + object_a["shape"][0]
        min_x = object_a["position"][1]
        max_x = min_x + object_a["shape"][1]
        for point in object_b_4_point_list:
            if (min_y <= point[0] < max_y) and (min_x <= point[1] < max_x):
                return True
        return False

    def _collision_detection(self):
        object_list = [
            {
                "id": "mario",
                "position": self.mario_position,
                "shape": [len(self._get_hero()), len(self._get_hero()[0])],
            },
            {
                "id": "brick",
                "position": self.brick_position,
                "shape": [len(self._get_brick()), len(self._get_brick()[0])],
            },
        ]
        for index_a, object_a in enumerate(object_list):
            for object_b in object_list[index_a:]:
                #if self._real_two_object_collision_detection(object_a, object_b) and self._real_two_object_collision_detection(object_b, object_a):
                if self._real_two_object_collision_detection(object_a, object_b):
                    return True
        return False

    def _place_2d_list_to_raw_data(self, y, x, a_2d_list):
        canvas_height = self.window_height
        canvas_width = self.window_width
        for y_index, row in enumerate(a_2d_list):
            new_y = y + y_index
            if new_y >= canvas_height:
                continue
            for x_index, char in enumerate(row):
                new_x = x + x_index
                if new_x >= canvas_width:
                    continue
                self.raw_data[new_y][new_x] = char

    def _play_animation(self, action):
        if action == "jump":
            jump_height = 4
            mario_position_list = []
            for i in range(jump_height):
                self.mario_position[0] -= 1
                mario_position_list.append(self.mario_position.copy())
            for i in range(jump_height):
                self.mario_position[0] += 1
                mario_position_list.append(self.mario_position.copy())
        elif action == "right_jump":
            jump_height = 5
            mario_position_list = []
            for i in range(jump_height):
                self.mario_position[0] -= 1
                self.mario_position[1] += i
                if self.mario_position[1] >= self.window_width-3:
                    self.mario_position[1] = self.window_width-3
                mario_position_list.append(self.mario_position.copy())
            for i in range(jump_height):
                self.mario_position[0] += 1
                mario_position_list.append(self.mario_position.copy())
        elif action == "left_jump":
            jump_height = 5
            mario_position_list = []
            for i in range(jump_height):
                self.mario_position[0] -= 1
                self.mario_position[1] -= i
                if self.mario_position[1] < 0:
                    self.mario_position[1] = 0
                mario_position_list.append(self.mario_position.copy())
            for i in range(jump_height):
                self.mario_position[0] += 1
                mario_position_list.append(self.mario_position.copy())

        last_position = self.mario_position.copy()
        for position in mario_position_list:
            self.mario_position = position
            if self._collision_detection() == True:
                self.mario_position = last_position
                break
            self.render()
            self._display()
            sleep(self.delay)
            last_position = position.copy()

    def _move_background(self):
        old_brick_position_x = self.brick_position[1]

        self.brick_position[1] -= 1
        if self.brick_position[1] < 0:
            self.brick_position[1] = self.window_width - 2

        if self._collision_detection() == True:
            self.brick_position[1] = old_brick_position_x

    def do_an_action(self, action):
        """
        action: one of [left, right, jump, right_jump, left_jump]
        """
        if action == "right":
            max_x_limitation = self.window_width - 3
            self.mario_position[1] += 1
            if self._collision_detection() == True:
                self.mario_position[1] -= 1
            if self.mario_position[1] >= max_x_limitation:
                self.mario_position[1] = max_x_limitation
            self._move_background()
        elif action == "left":
            min_x_limitation = 0
            self.mario_position[1] -= 1
            if self._collision_detection() == True:
                self.mario_position[1] += 1
            if self.mario_position[1] < min_x_limitation:
                self.mario_position[1] = min_x_limitation
        elif action == "jump":
            self._play_animation("jump")
        elif action == "right_jump":
            self._play_animation("right_jump")
        elif action == "left_jump":
            self._play_animation("left_jump")

        # falling
        if self.mario_position[0] != 6:
            while True:
                sleep(self.delay)
                self._display()
                self.mario_position[0] += 1
                if self._collision_detection() == True:
                    self.mario_position[0] -= 1
                    break
                if self.mario_position[0] == 6:
                    break

        # moving background when user go beyound 1/2 width
        while self.mario_position[1] >= (self.window_width / 2):
            self._move_background()
            self.mario_position[1] -= 1
            sleep(self.delay)
            self._display()

    def render(self):
        self._reset_background()

        self._place_2d_list_to_raw_data(self.mario_position[0], self.mario_position[1], self._get_hero())
        self._place_2d_list_to_raw_data(self.brick_position[0], self.brick_position[1], self._get_brick())

        text = ""
        for row in self.raw_data:
            text += "".join(row)
            text += "\n"
        return text

    def _clear_screen(self):
        print("\n" * 50)
        terminal.run_command("clear")

    def _display(self):
        self._clear_screen()
        result = self.render()
        print(result)

    def play(self):
        self._display()
        print("\n\n")
        print("1.Use w,s,a,d to move")
        print("2.Use j or k to jump")
        print("x.Use q to quit")
        while True:
            char = advanced_terminal_interface.get_char_input_in_blocking_way()
            if char in ["q", chr(27)]:
                exit()
            elif char in ["w", "s", "a", "d"]:
                if char == "w":
                    self.do_an_action("jump")
                elif char == "s":
                    pass
                elif char == "a":
                    self.do_an_action("left")
                elif char == "d":
                    self.do_an_action("right")
            elif char == "j":
                self.do_an_action("right_jump")
            elif char == "k":
                self.do_an_action("left_jump")
            elif char in [" ", chr(13)]:
                pass
            self._display()



if __name__ == "__main__":
    yingshaoxo_terminal_mario = Yingshaoxo_Terminal_Mario()
    yingshaoxo_terminal_mario.play()
