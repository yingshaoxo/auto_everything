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
