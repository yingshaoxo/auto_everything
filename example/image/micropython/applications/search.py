#terminal_arguments, input_=input, print_=print

note_path = "./all_yingshaoxo_data_2023_11_13.txt"
try:
    with open(note_path, "r") as f:
        f.readline()
except Exception as e:
    note_path = "./applications/note/note.txt"
search_string = terminal_arguments.lower()

replace_list = ["？", "?", "what ", "why ", "how to ", "how ", "为什么", "什么", "你知道", "吗", "怎么", "如何"]
for one in replace_list:
    search_string = search_string.replace(one,"")

en = False
if " " in search_string:
    words_list = search_string.strip().split(" ")
    en = True
else:
    words_list = list(search_string.strip())
    en = False

def check_if_string_is_inside_string(source_string, sub_word_list, wrong_limit_ratio=0.1, near_distance=15):
    wrong_limit = int(len(sub_word_list) * wrong_limit_ratio)
    not_found_counting = 0
    all_found = 0
    last_index = 0
    found_index = -1
    for word in sub_word_list:
        all_found += 1
        found_index = source_string.find(word)
        if found_index == -1:
            not_found_counting += 1
        else:
            if near_distance != None:
                if abs(found_index - last_index) > near_distance:
                    not_found_counting += 1
                else:
                    last_index = found_index
            else:
                last_index = found_index
        if not_found_counting > wrong_limit:
            return False
    if all_found == 0:
        return False
    if (not_found_counting/all_found) > wrong_limit_ratio:
        return False
    return True

length = len(words_list)
if length > 0:
    got = False
    with open(note_path, "r") as f:
        while True:
            a_line = f.readline()
            if not a_line:
                break
            if a_line.startswith("__**__**__"):
                continue
            a_line = a_line.lower()
            matched = 0
            for word in words_list:
                if word in a_line:
                    matched += 1
            if (matched / length) >= 0.7:
                if en == False:
                    a_check = check_if_string_is_inside_string(a_line, words_list, wrong_limit_ratio=0.1)
                else:
                    if matched == length:
                        a_check = True
                    else:
                        a_check = check_if_string_is_inside_string(a_line, words_list, wrong_limit_ratio=0.4, near_distance=30)
                if a_check == False:
                    if search_string in a_line:
                        a_check = True
                if a_check:
                    print_(a_line.strip())
                    temp_text = ""
                    for i in range(15):
                        some_line = f.readline()
                        if not some_line:
                            break
                        temp_text += some_line
                    if "__**__**__" in temp_text:
                        print_(temp_text.split("__**__**__")[0].strip())
                    else:
                        print_(temp_text.split("___")[0].strip())
                    got = True
                    break
    if got == False:
        print_("error: not found")
else:
    print_("error: not found")
               
