from auto_everything.ml import ML
from auto_everything.disk import Disk
ml = ML()
disk = Disk()

text_generator =  ml.Yingshaoxo_Text_Generator()

text = text_generator.get_source_text_data_by_using_yingshaoxo_method(input_txt_folder_path="/home/yingshaoxo/CS/ML/18.fake_ai_asistant/input_txt_files", type_limiter=[".txt"])

while True:
    #input_text = input("What you want to say? ")
    input_text = """
全员行为:

1.不听宣传不信宣传不执行指令
2.宣传新思想
新文化号召新行动



个体行为:

1. 做好准备2. 隐藏反叛思想，暗中捣乱，像穿了隐身衣一样战斗
"""
    result = text_generator.correct_sentence_by_using_yingshaoxo_regex_method(input_text=input_text, source_data_text=text, level=3)
    print(input_text)
    print("\n\n**********\n\n")
    print(result)
    break
