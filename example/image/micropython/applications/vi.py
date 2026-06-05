import os_path as path

terminal_arguments = terminal_arguments.strip("'")
terminal_arguments = terminal_arguments.strip('"')

edit_type = "blank"
if terminal_arguments == "":
    edit_type = "help"
elif terminal_arguments == "." or terminal_arguments == "./":
    edit_type = "folder"

if path.isfile(terminal_arguments):
    edit_type = "file"
if path.isdir(terminal_arguments):
    edit_type = "folder"

if edit_type == "blank":
    if "." in terminal_arguments:
        edit_type = "create_new_file"

def get_file_max_line_number(file_path):
    index = 0
    with open(file_path, "r") as input_file:
        while True:
            current_line = input_file.readline()
            if current_line == None:
                break
            if current_line == "":
                break
            index += 1
    return index

def read_a_line_in_file(file_path, line_index):
    index = 0
    with open(file_path, "r") as input_file:
        while True:
            current_line = input_file.readline()
            if current_line == None:
                break
            if current_line == "":
                break
            if index == line_index:
                return current_line
            index += 1
    return None

def modify_a_line_in_file(file_path, line_index, new_content, delete=False, add=False):
    import os
    temp_path = file_path + ".tmp"
    index = 0
    modified = False
    with open(file_path, "r") as input_file:
        with open(temp_path, "w") as output_file:
            while True:
                current_line = input_file.readline()
                if current_line == None:
                    break
                if current_line == "":
                    break
                if index == line_index:
                    if add == True:
                        output_file.write(current_line)
                        output_file.write(new_content)
                        modified = True
                    else:
                        if delete == False:
                            output_file.write(new_content)
                            modified = True
                else:
                    output_file.write(current_line)
                index += 1
    #os.replace(temp_path, file_path)
    os.remove(file_path)
    os.rename(temp_path, file_path)

    if delete == False:
        if modified == False:
            with open(file_path, "a") as output_file:
                output_file.write(new_content)

def find_next_word_splited_by_space(text_bytes, horizontal_index):
    index = text_bytes.find(" ", horizontal_index)
    if index != -1:
        index += 1
    return index

def find_previous_word_splited_by_space(text_bytes, horizontal_index):
    index = horizontal_index
    index -= 1
    while True:
        index -= 1
        if index <= 0:
            index = 0
            return index
        if text_bytes[index] == (" ")[0]:
            return index + 1

def search_string_in_file_and_get_line_index(file_path, search_string, start_index=0):
    index = 0
    with open(file_path, "r") as input_file:
        while True:
            current_line = input_file.readline()
            if current_line == None:
                break
            if current_line == "":
                break
            if index > start_index:
                if search_string in current_line:
                    return index
            index += 1
    return 0

if edit_type == "help":
    help_text = """
welcome to use yingshaoxo vi editor.

edit a file: 'vi *.txt' or 'vi *.py'
edit a folder: 'vi .' or 'vi ./applications'
"""
    real_print_("\n" + help_text.strip() + "\n")
elif edit_type == "folder":
    #print_("you want to edit a folder")
    return_value = run_command_("ls " + terminal_arguments)
    print_(return_value + '\n\n' + 'edit a file by: "vi *.txt" or "vi *.py"')

def edit_file_process():
    global display_, real_print_, input_char_, print_char_, terminal_arguments, read_a_line_in_file, modify_a_line_in_file, find_next_word_splited_by_space, find_previous_word_splited_by_space, get_file_max_line_number, search_string_in_file_and_get_line_index

    def read_following_input_until_enter():
        some_input = ""
        while True:
            input_char = input_char_()
            if input_char == '$' or (len(input_char) == 1 and (ord(input_char) == 27)) or input_char.lower() == "esc" or input_char == '\r' or input_char == '\n':
                # quit
                break
            if len(input_char) == 1:
                if ord(input_char) == 9 or ord(input_char) == '\t':
                    # tab
                    input_char = "    "
            some_input += input_char
            for one in input_char:
                print_char_(one)
            if input_char == "\b":
                some_input = inserted_text[:-2]
            if len(input_char) == 1:
                if ord(input_char) == 127:
                    some_input = some_input[:-2]
        return some_input

    horizontal_position = 0
    vertical_position = 0
    in_insert_mode = False
    inserted_text = ""
    while True:
        current_line = read_a_line_in_file(terminal_arguments, vertical_position)
        if current_line == None:
            current_line = "\n"
        line_length = len(current_line)

        if in_insert_mode == False:
            current_line_for_display = current_line[0:horizontal_position] + "~" + current_line[horizontal_position+1:]
            display_.clear()
            real_print_(current_line_for_display)

        if horizontal_position < 0:
            horizontal_position = 0

        if in_insert_mode == True:
            display_.clear()
            real_print_("inserted_text:" + inserted_text)
            while True:
                input_char = input_char_()
                if input_char == '$' or (len(input_char) == 1 and (ord(input_char) == 27)) or input_char.lower() == "esc":
                    # quit insert mode
                    in_insert_mode = False
                    current_line = current_line[:horizontal_position] + inserted_text + current_line[horizontal_position:]
                    modify_a_line_in_file(terminal_arguments, vertical_position, current_line)
                    inserted_text = ""
                    # maybe refresh in here
                    break
                if input_char == "\r":
                    input_char = "\n"
                if len(input_char) == 1:
                    if ord(input_char) == 9 or ord(input_char) == '\t':
                        # tab
                        input_char = "    "
                inserted_text += input_char
                for one in input_char:
                    print_char_(one)
                if input_char == "\b":
                    inserted_text = inserted_text[:-2]
                if len(input_char) == 1:
                    if ord(input_char) == 127:
                        inserted_text = inserted_text[:-2]
            continue
            
        if in_insert_mode == False:
            input_char = input_char_()
            if input_char == '$' or (len(input_char) == 1 and (ord(input_char) == 27)) or input_char.lower() == "esc":
                # quit vim
                break

            if input_char == "h":
                horizontal_position -= 1
                if horizontal_position < 0:
                    horizontal_position = 0
            if input_char == "l":
                horizontal_position += 1
                if horizontal_position >= len(current_line):
                    horizontal_position -= 1
            if input_char == "j":
                vertical_position += 1
                if vertical_position >= get_file_max_line_number(terminal_arguments):
                    vertical_position -= 1
            if input_char == "k":
                vertical_position -= 1
                if vertical_position <= 0:
                    vertical_position = 0

            if input_char == "i":
                # into insert mode
                in_insert_mode = True
                continue
            if input_char == "a":
                # into insert mode and add char after current char
                horizontal_position += 1
                in_insert_mode = True
                continue
            if input_char == "A":
                # into insert mode and add char after end of line
                horizontal_position = len(current_line) - 1
                in_insert_mode = True
                continue
            if input_char == "esc":
                # back to direction mode
                in_insert_mode = False
            if input_char == "o":
                # into insert mode at next line
                horizontal_position = len(current_line) - 1
                inserted_text = "\n"
                in_insert_mode = True
            if input_char == "x":
                # delete a char
                current_line = current_line[:horizontal_position] + current_line[horizontal_position+1:]
                modify_a_line_in_file(terminal_arguments, vertical_position, current_line)
            if input_char == "d":
                # delete a line
                temp_input_char = input_char_()
                if temp_input_char == "d":
                    modify_a_line_in_file(terminal_arguments, vertical_position, current_line, delete=True)
                    if vertical_position >= get_file_max_line_number(terminal_arguments):
                        vertical_position -= 1
            if input_char == "G":
                # go to file end
                vertical_position = get_file_max_line_number(terminal_arguments) - 1
            if input_char == "w":
                # go to next word
                index = find_next_word_splited_by_space(current_line, horizontal_position)
                if index != -1:
                    horizontal_position = index
            if input_char == "b":
                # go to previous word
                index = find_previous_word_splited_by_space(current_line, horizontal_position)
                if index != -1:
                    horizontal_position = index
            if input_char == "/":
                # find a string
                display_.clear()
                real_print_("search_text:")
                search_string = read_following_input_until_enter()
                vertical_position = search_string_in_file_and_get_line_index(terminal_arguments, search_string, start_index=vertical_position)
            if input_char == "Z":
                # quit and saving
                temp_input_char = input_char_()
                if temp_input_char == "Z":
                    break
            if input_char == ":":
                temp_input_char = input_char_()
                if temp_input_char == "w":
                    # save
                    break
                if temp_input_char in "0123456789":
                    # line jump
                    a_number = temp_input_char + read_following_input_until_enter()
                    vertical_position = int(a_number)


if edit_type == "file":
    #print_("you want to edit a file")
    edit_file_process()
elif edit_type == "create_new_file":
    #print_("you want to create a file")
    with open(terminal_arguments, "wb") as f:
        f.write(b"")
    edit_file_process()
