import os

from auto_everything.disk import Disk, Store
from auto_everything.ml import ML
from auto_everything.string_ import String
ml = ML()
disk = Disk()
string_ = String()

offline_question_and_answer_bot_dataset_path = "/home/yingshaoxo/CS/ML/18.fake_ai_asistant/input_txt_files"
if disk.exists(offline_question_and_answer_bot_dataset_path):
    text_generator = ml.Yingshaoxo_Text_Generator()

    new_text = text_generator.get_source_text_data_by_using_yingshaoxo_method(offline_question_and_answer_bot_dataset_path, type_limiter=[".txt", ".md"])
    the_text_list = [one.strip() for one in new_text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n") if one.strip() != ""]

    new_text_list = []
    for one in the_text_list:
        new_text_list += one.split("\n#")
    the_text_list = new_text_list
else:
    print(f"Folder is not exists: {offline_question_and_answer_bot_dataset_path}")
    exit()

while True:
    input_text = input("What you want to say? ")
    os.system("clear")

    print("\n\n__________\n\n".join(string_.search_text_in_text_list(input_text, the_text_list, page_size=3)))
    print("\n\n__________\n\n")


"""
We could make a intelligence tree application:

For example, when user search an operation system, like alpine, we immediately suggest user 'docker' or 'virtualbox' or any hardware that could install all kinds of system.

And when user search for 'statically compile', we immediately suggest user 'musl' or 'alpine'.

I think this is another kind of intelligence representation compared to long sequence text data.



Intelligence tree or relative keyword tree or node graph could be used as hidden states for supper AI.

All you need to do is extract keywords from text list to get keywords_to_text_dict.

Then when user input something, you split it into keywords, search keywords tree to get more keywords.

Then use keywords_to_text dict to get natural text as response.



#search #data #ai #yingshaoxo
"""
