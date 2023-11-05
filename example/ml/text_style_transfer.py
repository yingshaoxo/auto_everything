from auto_everything.ml import ML
from auto_everything.disk import Disk
from auto_everything.terminal import Terminal
ml = ML()
disk = Disk()
terminal = Terminal()

text_generator =  ml.Yingshaoxo_Text_Generator()

def correct_sentence_by_using_yingshaoxo_regex_method(input_text: str, source_data_text: str, level: int=3):
    import re

    def find_match_string_in_source_data(before_chars: str, after_chars: str):
        before_chars = re.escape(before_chars)
        after_chars = re.escape(after_chars)
        result_list = re.findall(pattern=f"{before_chars}(.){after_chars}", string=source_data_text)
        counting_dict = {}
        for one in result_list:
            if one in counting_dict.keys():
                counting_dict[one] += 1
            else:
                counting_dict[one] = 1
        items = list(counting_dict.items())
        items.sort(key=lambda item: item[1], reverse=True)
        if len(items) > 0:
            return items[0][0]
        else:
            return None

    new_text = ""
    for index, _ in enumerate(input_text):
        if index < (level-1):
            new_text += input_text[index]
            continue
        if index >= len(input_text) - level:
            new_text += input_text[index]
            continue
        before_chars = input_text[index-level: index]
        after_chars = input_text[index+1: index+1+level]
        #print(before_chars, input_text[index], after_chars)
        new_chars = find_match_string_in_source_data(before_chars, after_chars)
        if new_chars != None:
            new_text += new_chars
        else:
            new_text += input_text[index]

    return new_text


source_data_text = """
不管什么语言，什么形式，不过让人明白那道理罢了，不必纠结于表面那些东西，着重去理解、去感悟才是真的。
"""
input_text = """
不管什么语言 什么形式 不过让人明白那道理罢了 不必纠结于表面那些东西 着重去理解、去感悟才是真的。
"""

new_response = correct_sentence_by_using_yingshaoxo_regex_method(input_text, source_data_text=source_data_text, level=3)
#new_response = text_generator.correct_sentence_by_using_yingshaoxo_regex_method(input_text, source_data_text=source_data_text, level=3)

print(input_text)
print("\n**********\n", new_response, "\n************\n")
