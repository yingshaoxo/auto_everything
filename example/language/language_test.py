from auto_everything.language import Language
from auto_everything.ml import Yingshaoxo_Text_Generator
from pprint import pprint

language = Language()

text="""
I am ok, how are you? my dear.
niha-

你好阿，小朋友。m,m,masd.
"""

print(Yingshaoxo_Text_Generator.get_random_text_deriation_from_source_text(source_text=text))
print(Yingshaoxo_Text_Generator(input_txt_folder_path=".", use_machine_learning=True).get_similarity_of_two_sentences("aaa", "aab"))