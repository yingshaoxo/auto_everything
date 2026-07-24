#terminal_arguments, input_char_=input_char, print_char_=print_char, input_=input, print_=print, real_print_=real_print, display_=display, run_command_=run_shell_command

import os
if terminal_arguments == "":
    print_("show contents of a file.")
else:
    with open(terminal_arguments, "r") as f:
        print_(f.read(5012))
