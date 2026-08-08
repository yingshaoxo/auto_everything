#terminal_arguments, input_char_(), print_char_(), input_(), print_(), real_print_(), run_command_(), clear_screen_()

import os
if terminal_arguments == "":
    print_("show contents of a file.")
else:
    with open(terminal_arguments, "r") as f:
        print_(f.read(5012))
