from auto_everything.ml import ML
from auto_everything.disk import Disk
ml = ML()
disk = Disk()

text_generator =  ml.Yingshaoxo_Text_Generator()

text = text_generator.get_source_text_data_by_using_yingshaoxo_method(input_txt_folder_path="../../auto_everything", type_limiter=[".py"])
global_string_dict = None

while True:
    input_text = input("What you want to say? ")
    #if global_string_dict == None:
    #    global_string_dict = text_generator.get_global_string_dict_by_using_yingshaoxo_method(source_text_data=text, levels=10)
    #result = text_generator.get_next_x_chars_by_using_yingshaoxo_method(input_text, x=30, global_string_dict=global_string_dict)
    result = text_generator.next_code_generation(data_source_text=text, input_text=input_text, type_limiter=[".py"], how_long_the_text_you_want_to_get=30)
    print(result)
