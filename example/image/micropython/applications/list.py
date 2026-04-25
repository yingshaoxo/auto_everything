#terminal_arguments, input_=input, print_=print, display_=display, run_command_=run_shell_command

if terminal_arguments == "":
    terminal_arguments = "./"
if not terminal_arguments.endswith("/"):
    terminal_arguments += "/"

import os
import os_path as path
all_files = os.listdir(terminal_arguments)
folder_list = []
file_list = []
for one in all_files:
    full_path = terminal_arguments + one
    if path.isfile(full_path):
        file_list.append(one)
    if path.isdir(full_path):
        folder_list.append(one)
print_("\n".join(folder_list + file_list))
