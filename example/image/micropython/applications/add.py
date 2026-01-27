#terminal_arguments, input_=input, print_=print

app_parent_folder = "./applications/note"
note_path = app_parent_folder+"/note.txt"
magic_splitor = "\n\n"

try:
    import os
    os.mkdir(app_parent_folder)
    del os
except Exception as e:
    pass
try:
    with open(note_path, "r") as f:
        f.read(1)
except Exception as e:
    pass

with open(note_path, "a") as f:
    f.write(terminal_arguments + magic_splitor)

print_("saved: " + terminal_arguments)
