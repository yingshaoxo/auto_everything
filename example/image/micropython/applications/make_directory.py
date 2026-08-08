#terminal_arguments, input_char_(), print_char_(), input_(), print_(), real_print_(), run_command_(), clear_screen_()

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
