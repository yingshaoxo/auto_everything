from typing import Any

from auto_everything.disk import Disk, Store
from auto_everything.ml import ML
from auto_everything.string_ import String
ml = ML()
disk = Disk()
string_ = String()


the_text_list = [
    "Are you stupid?",
    "You are stupid!"
]

input_text_list = []
output_text_list = []
for index, one in enumerate(the_text_list):
    if index + 1 > len(the_text_list) - 1:
        break
    input_text_list.append(one)
    output_text_list.append(the_text_list[index + 1])

text_generator = ml.Yingshaoxo_Text_Generator()
the_regex_dict = text_generator.get_text_to_text_hard_coding_transforming_dict(input_text_list=input_text_list, output_text_list=output_text_list)


input_text = "Are you smart?"
output_text = text_generator.text_to_text_hard_coding_transforming(input_text, the_regex_dict)
print("\n\n----------\n\n")
print(output_text)
print("\n\n----------\n\n")
