from auto_everything.language import Language
from auto_everything.ml import Yingshaoxo_Text_Generator
from pprint import pprint

language = Language()

text="""
I'm yingshaoxo.

你好阿，小朋友。
"""

print(Yingshaoxo_Text_Generator.get_random_text_deriation_from_source_text(source_text=text, random_remove_some_characters=False, random_add_some_characters=False))