import sys
import random

from auto_everything.string_ import String
string = String()
from auto_everything.disk import Disk
disk = Disk()

if len(sys.argv[1:]) > 0:
    folder_path = sys.argv[1]
else:
    folder_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Ebooks/Chinese/chinese_sex_novels"
    # some novel has bad line ending, may need to fix

source_text = ""
files = disk.get_files(folder_path, type_limiter=[".txt", ".md"])
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        temp_text = f.read()
    source_text += temp_text + "\n\n"

source_text_list = [one.strip() for one in source_text.split("\n") if one.strip() != ""]

sample_numbers = 1000000

the_index = 0
while True:
    print("\n\n\n------------\n\n\n")
    input_text = input("What you want to search? ").strip()
    if input_text == "n":
        next_lines = "\n".join(source_text_list[the_index:the_index+10])
        print(next_lines)
        the_index = the_index + 10
        continue

    sampled_list = random.sample(source_text_list, sample_numbers) if len(source_text_list) >= sample_numbers else random.choices(source_text_list, k=sample_numbers)

    result_text = string.search_text_in_text_list_by_using_long_sub_sentence_and_only_return_one_text(input_text, sampled_list)
    next_lines = ""
    for index, one in enumerate(source_text_list):
        if one == result_text:
            next_lines = "\n".join(source_text_list[index+1:index+10])
            the_index = index + 10

    #try:
    #    print(input_text + result_text.split(input_text[-3:])[-1] + next_lines)
    #except Exception as e:
    #    print(result_text + next_lines)

    print(result_text + next_lines)
