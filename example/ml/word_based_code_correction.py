from auto_everything.ml import ML
from auto_everything.disk import Disk
ml = ML()
disk = Disk()

text_generator =  ml.Yingshaoxo_Text_Generator()

text = text_generator.get_source_text_data_by_using_yingshaoxo_method(input_txt_folder_path="../../auto_everything", type_limiter=[".py"])
global_string_word_based_corrector_dict = text_generator.get_global_string_word_based_corrector_dict_by_using_yingshaoxo_method(text, 4)

while True:
    input_text = input("What you want to say? ")
    """
    from auto_everything.what import Terminal
    """
    result = text_generator.correct_sentence_based_on_word_by_using_yingshaoxo_method(input_text, global_string_corrector_dict=global_string_word_based_corrector_dict)
    print(result)
