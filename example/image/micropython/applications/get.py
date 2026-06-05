#terminal_arguments, input_=input, print_=print

app_parent_folder = "./applications/note"
note_path = app_parent_folder+"/note.txt"

words_list = terminal_arguments.replace("?","").strip().split(" ")
length = len(words_list)
if length > 0:
    got = False
    with open(note_path, "r") as f:
        while True:
            a_line = f.readline()
            if a_line == "":
                break
            if a_line == None:
                break
            if a_line == "___":
                continue
            matched = 0
            for word in words_list:
                if word in a_line:
                    matched += 1
            if (matched / length) >= 0.7:
                print_(a_line.strip())
                got = True
                break
    if got == False:
        print_("error: not found")
else:
    print_("error: not found")
               
