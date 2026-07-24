#terminal_arguments, input_char_=input_char, print_char_=print_char, input_=input, print_=print, real_print_=real_print, display_=display, run_command_=run_shell_command

import os
if terminal_arguments == "" or terminal_arguments == "./" or terminal_arguments == "/":
    print_("remove a file or folder.")
else:
    the_target_file_path = terminal_arguments

    def exists(path):
        try:
            os.stat(path)
            return True
        except Exception as e:
            return False

    def file_exists(path):
        try:
            f = open(path, "r")
            f.close()
            return True
        except Exception as e:
            return False

    def dir_exists(path):
        try:
            if os.stat(path)[0] & 0x4000:
                return True
            else:
                return False
        except Exception as e:
            return False

    def recursive_delete(target_file_path):
        global exists
        if not exists(target_file_path):
            return

        if file_exists(target_file_path):
            os.remove(target_file_path)
        elif dir_exists(target_file_path):
            sub_list = os.listdir(target_file_path)
            for a_path in sub_list:
                recursive_delete(target_file_path + "/" + a_path)
            os.rmdir(target_file_path)

    recursive_delete(the_target_file_path)
