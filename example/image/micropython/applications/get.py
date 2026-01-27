#terminal_arguments, input_=input, print_=print

app_parent_folder = "./applications/note"
note_path = app_parent_folder+"/note.txt"
magic_splitor = "\n\n"

with open(note_path, "r") as f:
    text = f.read()

note_list = text.split(magic_splitor)
words_list = terminal_arguments.replace("?","").strip().split(" ")
if len(words_list) > 0:
    got = False
    for note in note_list:
        length = len(words_list)
        matched = 0
        for word in words_list:
            if word in note:
                matched += 1
        if (matched / length) >= 0.7:
            print_(note)
            got = True
            break
    if got == False:
        print_("error: not found")
else:
    print_("error: not found")
