from typing import Any

from auto_everything.disk import Disk, Store
from auto_everything.ml import ML
from auto_everything.string_ import String
ml = ML()
disk = Disk()
string_ = String()


the_text_list = [
    "Are you the stupid one?",
    "You are the stupid one!",
    "Call me.",
    "Call us.",
    "fuck everything you say",
    "you are right about everything you say",
    #"You're the one who decided to (?P<a_0_0>.*) this job, right?": '"Why aren\'t '
    #                                                                'you going?" '
    #                                                                '"Because I '
    #                                                                "{a_0_0}n't "
    #                                                                'want to."',
]

input_text_list = []
output_text_list = []
for index, one in enumerate(the_text_list):
    if index + 1 > len(the_text_list) - 1:
        break
    input_text_list.append(one)
    output_text_list.append(the_text_list[index + 1])
print(input_text_list)
print(output_text_list)

text_transformer = ml.Yingshaoxo_Text_Transformer()
the_regex_dict = text_transformer.get_regex_expression_dict_from_input_and_output_list(input_text_list=input_text_list, output_text_list=output_text_list)
print(the_regex_dict)


input_text = "Are you the smart one?"
output_text = text_transformer.yingshaoxo_regex_expression_based_transformer(input_text, the_regex_dict)
#output_text = text_transformer.yingshaoxo_regex_expression_based_recursive_transformer(input_text, the_regex_dict)
print("\n\n----------\n\n")
print(output_text)
print("\n\n----------\n\n")
