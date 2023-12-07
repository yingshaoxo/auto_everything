from auto_everything.ml import ML
from auto_everything.disk import Disk
from auto_everything.terminal import Terminal
ml = ML()
disk = Disk()
terminal = Terminal()


#offline_question_and_answer_bot_dataset_path = "~/.yppm/offline_yingshaoxo_bot/dataset_txt_files"
offline_question_and_answer_bot_dataset_path = "/home/yingshaoxo/CS/ML/18.fake_ai_asistant/input_txt_files"
offline_question_and_answer_bot_dataset_path = disk._expand_user(offline_question_and_answer_bot_dataset_path)
text_generator = ml.Yingshaoxo_Text_Generator(
    input_txt_folder_path=offline_question_and_answer_bot_dataset_path,
    use_machine_learning=False
)
text_data_source = text_generator.text_source_data

def decode_response(text: str, chat_context: str):
    splits = text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n")
    if (len(splits) > 1):
        response = splits[1].strip()
    elif (len(splits) == 1):
        response = splits[0].strip()
    else:
        response = ""
    new_code = f"""
chat_context = '''{chat_context}'''

{response}
"""
    final_response = terminal.run_python_code(code=new_code)
    if final_response.strip() == "":
        final_response = response
    final_response = "\n".join([one for one in final_response.split("\n") if not one.strip().startswith("__**")])
    return final_response


print("\n\n")
all_input_text = ""

while True:
    input_text = input("What you want to say? \n")

    all_input_text += input_text + "\n"
    real_input = all_input_text[-800:].strip()

    #response = text_generator.search_and_get_following_text_in_a_exact_way(input_text=real_input, quick_mode=True)
    previous_text, response = text_generator.next_fuzz_sentence_generation(text_source_data=text_data_source, input_text=real_input, how_long_the_text_you_want_to_get=800, compare_times=10, also_return_previous_text=True)
    response = decode_response(text=response, chat_context=all_input_text)

    print("\n\n---------\n\n")
    response = text_generator.fuzz_text_to_text_transforming(input_text=input_text, example_input_text=previous_text, example_output_text=response, levels=3)
    print(response)
    print("\n\n---------\n\n")



#######
# If you want to have a less accurate one, you use the following version
#######


"""
from auto_everything.ml import ML
from auto_everything.disk import Disk
from auto_everything.terminal import Terminal
ml = ML()
disk = Disk()
terminal = Terminal()

text_generator =  ml.Yingshaoxo_Text_Generator()

text = text_generator.get_source_text_data_by_using_yingshaoxo_method(input_txt_folder_path="/home/yingshaoxo/CS/ML/18.fake_ai_asistant/input_txt_files")
text = text.replace("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n", "\n\n\n") # You have to replace this seperator with your own dataset seperator
global_string_dict = text_generator.get_global_string_dict_by_using_yingshaoxo_method(source_text_data=text, levels=50)

while True:
    input_text = input("What you want to say? ")
    result = text_generator.get_next_x_chars_by_using_yingshaoxo_method(input_text, x=128, global_string_dict=global_string_dict)
    splits = result.split("\n\n\n")
    if len(splits) > 1:
        print(splits[1])
    else:
        print(splits[0])
"""
