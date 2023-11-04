from auto_everything.ml import ML
from auto_everything.disk import Disk
ml = ML()
disk = Disk()

text_generator =  ml.Yingshaoxo_Text_Generator()

text = text_generator.get_source_text_data_by_using_yingshaoxo_method(input_txt_folder_path="../../auto_everything", type_limiter=[".py"])
global_string_dict = text_generator.get_global_string_dict_by_using_yingshaoxo_method(source_text_data=text, levels=10)

while True:
    input_text = input("What you want to say?")
    result = text_generator.get_next_x_chars_by_using_yingshaoxo_method(input_text, x=30, global_string_dict=global_string_dict)
    print(result)
