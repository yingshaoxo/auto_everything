if terminal_arguments == "" or terminal_arguments == "./" or terminal_arguments == "/":
    print_("remove a file or folder.")
else:
    the_target_file_path = terminal_arguments
    run_command_("delete " + terminal_arguments)
