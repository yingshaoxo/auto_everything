#terminal_arguments, input_char_=input_char, print_char_=print_char, input_=input, print_=print, real_print_=real_print, display_=display, run_command_=run_shell_command

import os
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

def insert_bytes_large_file(filepath, byte_index, new_data, chunk_size=1024):
    # this function made by gemini
    global path
    import os
    insert_len = len(new_data)
    file_size = path.getsize(filepath)
    
    if byte_index > file_size:
        byte_index = file_size

    with open(filepath, "r+b") as f:
        f.seek(file_size + insert_len - 1)
        f.write(b'\0')

        current_pos = file_size
        
        while current_pos > byte_index:
            read_size = min(chunk_size, current_pos - byte_index)
            read_at = current_pos - read_size
            f.seek(read_at)
            buffer = f.read(read_size)
            f.seek(read_at + insert_len)
            f.write(buffer)
            current_pos -= read_size
            
        f.seek(byte_index)
        f.write(new_data)

def delete_bytes_in_large_file(filepath, byte_index, delete_length, chunk_size=1024):
    # this function made by gemini
    global path
    import os
    file_size = path.getsize(filepath)
    temp_filepath = filepath + ".tmp"
    with open(filepath, "rb") as f_old:
        with open(temp_filepath, "wb") as f_new:
            current = 0
            while current < byte_index:
                to_read = min(chunk_size, byte_index - current)
                f_new.write(f_old.read(to_read))
                current += to_read
            f_old.seek(byte_index + delete_length)
            while True:
                chunk = f_old.read(chunk_size)
                if not chunk:
                    break
                f_new.write(chunk)
    os.remove(filepath)
    os.rename(temp_filepath, filepath)

def find_next_word_splited_by_space(text_bytes, horizontal_index):
    index = text_bytes.find(b" ", horizontal_index)
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
        if text_bytes[index] == (b" ")[0]:
            return index + 1

def find_bytes_in_large_file(filepath, bytes_data, start_index=0):
    temp_index = start_index
    with open(filepath, "rb") as f:
        f.seek(start_index)
        while True:
            temp_line = f.readline()
            if temp_line == None:
                break
            if temp_line == b"":
                break
            found = temp_line.find(bytes_data)
            if found != -1:
                return temp_index + found
            temp_index += len(temp_line)
    return -1

def is_ascii(text):
    if ord(text[0]) < 0x7F:
        return True
    return False


if edit_type == "help":
    help_text = """
welcome to use yingshaoxo vim editor.

edit a file: 'vim *.txt' or 'vim *.py'
edit a folder: 'vim .' or 'vim ./applications'
"""
    real_print_("\n" + help_text.strip() + "\n")
elif edit_type == "folder":
    #print_("you want to edit a folder")
    return_value = run_command_("ls " + terminal_arguments)
    print_(return_value + '\n\n' + 'edit a file by: "vim *.txt" or "vim *.py"')


line_index_list = []
def edit_file_process():
    global line_index_list, display_, real_print_, input_char_, delete_bytes_in_large_file, insert_bytes_large_file, find_next_word_splited_by_space, find_previous_word_splited_by_space, terminal_arguments, find_bytes_in_large_file, is_ascii
    def load_the_mother_fucker():
        global line_index_list, print_char_
        line_index_list = []
        bytes_index = 0
        with open(terminal_arguments, "rb") as f:
            while True:
                start = bytes_index
                current_line = f.readline()
                if current_line == None:
                    break
                if current_line == b"":
                    break
                bytes_index += len(current_line)
                end = bytes_index
                line_index_list.append(str(start) + "," + str(end))
        if len(line_index_list) == 0:
            line_index_list = ["0,0"]
    load_the_mother_fucker()

    last_horizontal_position = 0
    horizontal_position = 0
    vertical_position = 0
    in_insert_mode = False
    inserted_text = ""
    bytes_index = 0
    while True:
        with open(terminal_arguments, "rb") as f:
            temp_string = line_index_list[vertical_position]
            line_start_bytes_index, line_end_bytes_index = temp_string.split(",")
            line_start_bytes_index, line_end_bytes_index = int(line_start_bytes_index), int(line_end_bytes_index)
            line_length = line_end_bytes_index - line_start_bytes_index
            f.seek(line_start_bytes_index)
            current_line = f.readline()
            current_line_text = current_line.decode("utf-8", "ignore")

        if in_insert_mode == False:
            if horizontal_position >= line_length - 1:
                horizontal_position = line_length - 1
            else:
                horizontal_position = last_horizontal_position
            if (len(current_line_text) > 0) and (not is_ascii(current_line_text.strip()[0])):
                # is chinese
                current_line_for_display = current_line_text[:-1] + "(change this line will create error)" + current_line_text[-1]
            else:
                # is english
                current_line_for_display = current_line[0:horizontal_position] + b"~" + current_line[horizontal_position+1:]
            display_.clear()
            real_print_(current_line_for_display)

        bytes_index = line_start_bytes_index + horizontal_position
        if bytes_index < 0:
            bytes_index = 0

        if in_insert_mode == True:
            display_.clear()
            real_print_("inserted_text:" + inserted_text)
            while True:
                input_char = input_char_()
                if input_char == '$' or (len(input_char) == 1 and (ord(input_char) == 27)) or input_char.lower() == "esc":
                    # quit insert mode
                    in_insert_mode = False
                    print(terminal_arguments, bytes_index, inserted_text.encode("utf-8"))
                    insert_bytes_large_file(filepath=terminal_arguments, byte_index=bytes_index, new_data=inserted_text.encode("utf-8"))
                    inserted_text = ""
                    load_the_mother_fucker()
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
                #display_.clear()
                #if len(input_char) == 1:
                #    real_print_(str(ord(input_char)) + ", ")
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
                last_horizontal_position = horizontal_position
            if input_char == "l":
                horizontal_position += 1
                if horizontal_position >= len(current_line):
                    horizontal_position -= 1
                last_horizontal_position = horizontal_position
            if input_char == "j":
                vertical_position += 1
                if vertical_position >= len(line_index_list):
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
                delete_bytes_in_large_file(terminal_arguments, bytes_index, 1)
                load_the_mother_fucker()
            if input_char == "d":
                # delete a line
                temp_input_char = input_char_()
                if temp_input_char == "d":
                    delete_bytes_in_large_file(terminal_arguments, line_start_bytes_index, line_length, chunk_size=1024)
                    load_the_mother_fucker()
                    if vertical_position >= len(line_index_list):
                        vertical_position -= 1
            if input_char == "G":
                # go to file end
                vertical_position = len(line_index_list) - 1
                load_the_mother_fucker()
            if input_char == "w":
                # go to next word
                index = find_next_word_splited_by_space(current_line, last_horizontal_position)
                if index != -1:
                    last_horizontal_position = index
            if input_char == "b":
                # go to previous word
                index = find_previous_word_splited_by_space(current_line, last_horizontal_position)
                if index != -1:
                    last_horizontal_position = index
            if input_char == "/":
                # find a string
                search_string = ""
                display_.clear()
                real_print_("search_text:")
                while True:
                    input_char = input_char_()
                    if input_char == '$' or input_char == "\r" or input_char == "\n" or (len(input_char) == 1 and ord(input_char) == 27):
                        # end, do the serach
                        found = find_bytes_in_large_file(terminal_arguments, search_string.encode("utf-8"), start_index=line_end_bytes_index)
                        if found != -1:
                            for temp_index, temp_string in enumerate(line_index_list):
                                temp_line_start_bytes_index, temp_line_end_bytes_index = temp_string.split(",")
                                temp_line_start_bytes_index, temp_line_end_bytes_index = int(temp_line_start_bytes_index), int(temp_line_end_bytes_index)
                                if temp_line_start_bytes_index <= found <= temp_line_end_bytes_index:
                                    vertical_position = temp_index
                                    with open(terminal_arguments, "rb") as f:
                                        temp_string = line_index_list[vertical_position]
                                        line_start_bytes_index, line_end_bytes_index = temp_string.split(",")
                                        line_start_bytes_index, line_end_bytes_index = int(line_start_bytes_index), int(line_end_bytes_index)
                                        f.seek(line_start_bytes_index)
                                        current_line = f.readline()
                                    last_horizontal_position = current_line.find(search_string.encode("utf-8"))
                                    if last_horizontal_position == -1:
                                        last_horizontal_position = 0
                                    horizontal_position = last_horizontal_position
                                    break
                        break
                    search_string += input_char
                    if input_char == "\b":
                        search_string = search_string[:-2]
                    if len(input_char) == 1:
                        if ord(input_char) == 127:
                            search_string = search_string[:-2]
                    display_.clear()
                    real_print_("search_text:" + search_string)
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

if edit_type == "file":
    #print_("you want to edit a file")
    edit_file_process()
elif edit_type == "create_new_file":
    #print_("you want to create a file")
    with open(terminal_arguments, "wb") as f:
        f.write(b"")
    edit_file_process()
