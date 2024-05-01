from typing import Any
from pprint import pprint
import json

from auto_everything.io import IO
from auto_everything.disk import Disk, Store
from auto_everything.ml import ML
from auto_everything.string_ import String
ml = ML()
disk = Disk()
string_ = String()
io_ = IO()


text_generator = ml.Yingshaoxo_Text_Generator()
text_transformer = ml.Yingshaoxo_Text_Transformer()


the_regex_dict = {}
text = io_.read("./en_to_zh_word_dict_yingshaoxo_version.txt")
data_list = [one for one in text.split("\n\n_\n\n") if one != ""]
for one in data_list:
    key, value = one.split("\n")[:2]
    the_regex_dict[key.lower()] = value.lower()

text = io_.read("./regex_en_to_zh_dict_yingshaoxo_version.txt")
data_list = [one.strip() for one in text.split("\n_\n") if one.strip() != ""]
for one in data_list:
    key, value = one.split("\n")[:2]
    the_regex_dict[key.lower()] = value.lower()
    #print(key, value)


input_text_list = []
output_text_list = []
for key, value in the_regex_dict.items():
    input_text_list.append(key)
    output_text_list.append(value)
the_real_regex_dict = text_transformer.get_regex_expression_dict_from_input_and_output_list(input_text_list=input_text_list, output_text_list=output_text_list)


for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ',.:()\"?!*/;%#@$[]-|":
    if char not in the_regex_dict.keys():
        the_regex_dict[char] = char


while True:
    input_text = input("What you want to translate? ")
    output_text = text_transformer.pure_string_dict_based_sequence_transformer(input_text.lower(), the_regex_dict)
    #output_text = text_transformer.yingshaoxo_regex_expression_based_transformer(input_text, the_real_regex_dict)
    print("\n\n----------\n\n")
    print(output_text)
    print("\n\n----------\n\n")
