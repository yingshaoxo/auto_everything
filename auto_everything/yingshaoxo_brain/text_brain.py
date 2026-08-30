# forget about the punctuation to get real talking stability.

import os
from auto_everything.terminal import Terminal
terminal = Terminal()
from auto_everything.string_ import String
string_ = String()

intelligent_source = "./yingshaoxo_language.txt"
magic_splitor = "__**__**__yingshaoxo_is_the_top_one__**__**__"
note_path = "./temporary_memory.txt"
hidden_conscious_dict = {
    "language_type": "english",
    "input_text": "",
    "input_word_list": [],
    "index": 0,
    "end_index": 0,
}
memory_dict = {
    "task_list": [],
    "result": "",
}

def speak(a_string):
    #terminal.run_command("espeak '" + a_string + "'")
    terminal.run_command("echo '{}' | festival --tts".format(a_string))

def print1(a_string):
    print(a_string)

def print2(a_string):
    print1(a_string)
    speak(a_string)

def input1(a_string):
    return input(a_string)

def input2(a_string):
    speak(a_string)
    return input1(a_string)

def is_pure_abc(a_char):
    if a_char in "abcdefghijklmnopqrstuvwxyz":
        return True
    return False

def split_sentence_into_words_list(a_string):
    a_string = a_string.lower()
    a_string = a_string.replace("。", ".").replace("？", "?").replace("！", "!").replace("，", ",")

    word_list = []
    temp_word = ""
    for a_char in a_string:
        if is_pure_abc(a_char):
            temp_word += a_char
        else:
            if temp_word != "":
                word_list.append(temp_word)
            temp_word = ""
            word_list.append(a_char)
    if temp_word != "":
        word_list.append(temp_word)
    return word_list

def switch_you_and_me(a_string):
    return string_.switch_you_and_me(a_string)

def add(key, value):
    memory_dict[key] = value

def get(key):
    result = memory_dict.get(key)
    if result == None:
        return ""
    return result

def next_string():
    return "".join(hidden_conscious_dict["input_word_list"][hidden_conscious_dict["index"]+1:])

def previous_string(until=""):
    return "".join(hidden_conscious_dict["input_word_list"][:hidden_conscious_dict["index"]])

def previous_string_is(a_string):
    word_list = split_sentence_into_words_list(a_string)
    length = len(word_list)
    current_index = hidden_conscious_dict["index"]
    previous_word_list = hidden_conscious_dict["input_word_list"][current_index-length:current_index]
    #print1(previous_word_list, word_list)
    if previous_word_list == word_list:
        return True
    else:
        return False

def next_string_is(a_string):
    word_list = split_sentence_into_words_list(a_string)
    length = len(word_list)
    current_index = hidden_conscious_dict["index"]
    next_word_list = hidden_conscious_dict["input_word_list"][current_index+1:current_index+1+length]
    if next_word_list == word_list:
        return True
    else:
        return False

def next_word():
    current_index = hidden_conscious_dict["index"]
    if (current_index+1) >= hidden_conscious_dict["end_index"]:
        return ""
    word = hidden_conscious_dict["input_word_list"][current_index+1]
    if word == " ":
        if (current_index+2) >= hidden_conscious_dict["end_index"]:
            return ""
        word = hidden_conscious_dict["input_word_list"][current_index+2]
    return word

def previous_word():
    current_index = hidden_conscious_dict["index"]
    if (current_index-1) < 0:
        return ""
    word = hidden_conscious_dict["input_word_list"][current_index-1]
    if word == " ":
        if (current_index-2) < 0:
            return ""
        word = hidden_conscious_dict["input_word_list"][current_index-2]
    return word

def string_after(source_string, a_string):
    index = source_string.find(a_string)
    if index == -1:
        return source_string
    else:
        return source_string[index+len(a_string):]

def jump_to(target_word):
    index = hidden_conscious_dict["index"] + 1
    word_list = hidden_conscious_dict["input_word_list"]
    end_index = hidden_conscious_dict["end_index"]
    while True:
        if index >= end_index:
            break
        a_word = word_list[index]
        if a_word == target_word:
            hidden_conscious_dict["index"] = index - 1
            return
        index += 1
    hidden_conscious_dict["index"] = end_index + 1

def skip_text(a_string):
    word_list = split_sentence_into_words_list(a_string)
    end_index = hidden_conscious_dict["end_index"]
    index = hidden_conscious_dict["index"] + 1
    new_index = index + len(word_list)
    if new_index <= end_index:
        hidden_conscious_dict["index"] = new_index

def go_to_line_end(end_symbol_list=[".", "\n", "?", "!"]):
    #1.what is line end? .。\n
    #2.what is the target text? hidden_conscious_dict.get(input_text)
    index = hidden_conscious_dict["index"] + 1
    word_list = hidden_conscious_dict["input_word_list"]
    end_index = hidden_conscious_dict["end_index"]
    while True:
        if index >= end_index:
            break
        a_word = word_list[index]
        if a_word in end_symbol_list:
            if a_word == ".":
                if index + 1 < end_index:
                    next_word = word_list[index+1]
                    if next_word in "01234567890":
                        # this dot is a number
                        continue
            hidden_conscious_dict["index"] = index
            return
        index += 1
    hidden_conscious_dict["index"] = end_index + 1

def api_play_a_file(path):
    os.system("xdg-open " + path)

def api_save_diary(a_string):
    a_string = a_string.strip()
    if a_string != "":
        with open(note_path, "a") as f:
            f.write(a_string + "\n\n" + magic_splitor + "\n\n")

def api_delete_one_record_in_diary(a_string):
    a_string = a_string.strip()
    if a_string != "":
        one_record = api_search_diary(a_string, raw=True)
        if one_record != "you tell me":
            with open(note_path, "r") as f:
                all_data = f.read()
            all_data = all_data.replace("\n"+one_record+"\n", "")
            with open(note_path, "w") as f:
                f.write(all_data)

def api_search_diary(a_string, raw=False):
    #print1("search word:" + a_string)
    try:
        with open(note_path, "r") as f:
            f.readline()
    except Exception as e:
        return "you tell me"
    result_text = ""
    words_list = a_string.replace("?","").strip().split(" ")
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
                if a_line == magic_splitor + "\n":
                    continue
                matched = 0
                for word in words_list:
                    if word in a_line:
                        matched += 1
                if (matched / length) >= 0.7:
                    result_text = a_line.strip()
                    if raw == False:
                        result_text = switch_you_and_me(result_text)
                    got = True
                    break
        if got == False:
            result_text = "you tell me"
    else:
        result_text = "you tell me"
    return result_text

def sentence_pattern_match(pattens, input_text):
    data_list = []
    for rule in pattens:
        data_list += list(set(string_.hard_core_string_pattern_search(input_text, rule)))
    return data_list

def get_useful_part_of_text(input_text, strict=True):
    input_text = input_text.lower()
    patterns = [
        "xxx is xxx.",
        "xxx are xxx.",
        "xxx so xxx.",
        "xxx makes xxx.",
        "xxx can make xxx.",
        "xxx can help xxx.",
        "xxx can be xxx.",
        "xxx not only xxx but also xxx.",
        "xxx depends on xxx.",
        "xxx have xxx to xxx",
        "xxx has xxx to xxx",
        "xxx can be used for xxx.",
        "xxx can be get from xxx.",
        "xxx is composed by xxx.",
        "you can make xxx by xxx.",
        "the alternative of xxx is xxx.",
        "i think xxx can xxx.",
        "xxx already xxx.",
        "xxx needs xxx.",
        "xxx have xxx.",

        "xxx is because xxx.",
        "xxx that is why xxx.",
        "the reason of xxx is xxx.",
        "the deep reason of xxx is xxx.",
        "the good part of xxx is xxx.",
        "the bad part of xxx is xxx.",

        "to xxx, you xxx.",
        "if you want xxx, you have to xxx",
        "xxx requires xxx steps xxx",
        "the xxx step for xxx is xxx.",
        "to success in xxx you have to xxx",

        "xxx from xxx.",
        "xxx the more xxx the more xxx.",
        "xxx to do xxx.",
        "xxx love to xxx.",
        "xxx will be xxx.",
        "xxx means xxx.",

        "xxx是xxx",
        "xxx因为xxx",
        "xxx所以xxx",
        "xxx应该xxx",
        "xxx想xxx",
        "xxx已经xxx",
        "因为xxx所以xxx",
        "如果xxx就会xxx",
        "如果xxx就能xxx",
        "如果xxx就可以xxx",
        "如果xxx就应该xxx",
        "xxx为了xxx",
        "xxx不仅xxx还能xxx",
        "xxx可以xxx",
        "xxx能够xxx",
        "xxx能帮xxx",
        "xxx能做xxx",
        "xxx能干xxx",
        "xxx能得xxx",
        "xxx能取xxx",
        "xxx可能xxx",
        "xxx需要xxx",
        "xxx就像xxx",
        "xxx确保xxx",
        "xxx帮助xxx",
        "xxx基于xxx",
        "xxx类似于xxx",
        "我xxx想到xxx",
        "我xxx发现xxx",
        "看起来xxx",
        "xxx意思是xxx",
        "xxx想出了xxx",
        "xxx发明了xxx",
        "xxx创造了xxx",
        "xxx得到了xxx",
        "xxx的方法是xxx",
        "xxx的算法是xxx",
        "xxx的途径是xxx",
        "xxx的好处是xxx",
        "xxx的坏处是xxx",
        "要想xxx，你xxx",
        "没有xxx你就xxx",
        "xxx制作方法xxx",
        "理论上xxx",
        "实际上xxx",
        "xxx个秘密xxx",
    ]
    if strict == False:
        patterns += [
            "my xxx.",
            "you xxx.",
            "xxx have xxx",
            "我xxx",
            "你xxx",
            "xxx有xxx",
        ]
    result_list = sentence_pattern_match(patterns, input_text)
    result_list = [one for one in result_list if not one.endswith("?")]
    result_list = [one for one in result_list if not one.endswith("？")]
    result_list = [one for one in result_list if not one.endswith(":")]
    result_list = [one for one in result_list if not one.endswith("：")]
    new_list = []
    for one in result_list:
        one = one.strip()
        if one not in new_list:
            new_list.append(one)
    result_list = new_list
    return " ".join(result_list)

def single_word_analyze_and_operation():
    current_word = hidden_conscious_dict["input_word_list"][hidden_conscious_dict["index"]]
    if current_word == " ":
        return
    a_part = ""
    #print1(current_word)
    with open(intelligent_source, "r") as f:
        while True:
            sentence = f.readline()
            if sentence == None:
                break
            if sentence == "":
                break
            if sentence == "___\n":
                a_part = a_part.strip()
                head_line = a_part.split("\n")[0]
                if head_line == "\\n":
                    head_line = "\n"
                if head_line == current_word:
                    #print1(a_part)
                    code = "\n".join(a_part.split("\n")[1:])
                    try:
                        exec(code)
                    except Exception as e:
                        print1(e)
                    break
                a_part = ""
            else:
                a_part += sentence

def run(a_string, id="yingshaoxo"):
    word_list = split_sentence_into_words_list(a_string)

    hidden_conscious_dict["input_text"] = a_string
    hidden_conscious_dict["input_word_list"] = word_list

    hidden_conscious_dict["index"] = 0
    hidden_conscious_dict["end_index"] = len(word_list)
    while True:
        if hidden_conscious_dict["index"] >= hidden_conscious_dict["end_index"]:
            break
        single_word_analyze_and_operation()
        hidden_conscious_dict["index"] += 1

if __name__ == "__main__":
    while True:
        input_string = input1("___\n\nwhat you want to say? ").strip()
        print()
        output_string = run(input_string)
