from typing import Any

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
    response1, response, response2 = text_generator.do_text_search(input_text, the_text_list, quick_mode=False)
    #response = response + "\n\n-------\n\n" + response2
    if response2 != "":
        if string_.compare_two_sentences(input_text, response) >= 0.5:
            response = response2
    print("\n\n----------\n\n")
    print(response)
    print("\n\n----------\n\n")
