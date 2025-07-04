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

while True:
    print("\n\n\n------------\n\n\n")
    input_text = input("What you want to search? ")

    sampled_list = random.sample(source_text_list, sample_numbers) if len(source_text_list) >= sample_numbers else random.choices(source_text_list, k=sample_numbers)

    result_text = string.search_text_in_text_list_by_using_long_sub_sentence_and_only_return_one_text(input_text, sampled_list)

    print(result_text)
