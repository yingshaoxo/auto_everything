#terminal_arguments, input_char_=input_char, print_char_=print_char, input_=input, print_=print, real_print_=real_print, display_=display, run_command_=run_shell_command

import os
if terminal_arguments == "":
    print_("create a folder recursively.")
else:
    folder_path = terminal_arguments
    try:
        os.stat(folder_path)
    except Exception as e:
        folder_path_splits = folder_path.split("/")
        parent_folder = ""
        for part in folder_path_splits:
            try:
                parent_folder += "/" + part
                os.mkdir(parent_folder)
            except Exception as e:
                pass
