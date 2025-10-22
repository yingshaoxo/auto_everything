from auto_everything.string_ import String
string = String()

source_text = """
My mother is XiaoDeng. haha

The tree is located in our brain. Do you believe it?

God is God.

My name is yingshaoxo.
"""

print(string.hard_core_string_pattern_search(source_text, "xxx mother is xxx."))
#My mother is XiaoDeng.

print(string.hard_core_string_pattern_search(source_text, "The xxx is located in xxx."))
#The tree is located in our brain.

print(string.hard_core_string_pattern_search(source_text, "xxx is xxx."))
#['My mother is XiaoDeng.', 'The tree is located in our brain.', 'God is God.']


print("\n\nGive us a introduction:")
guide_template = """
My name is xxx.
My mother is xxx.
I think:
    xxx is located in xxx. xxx it?
""".strip()
for one in guide_template.split("\n"):
    if "xxx" in one:
        one = one.strip()
        print(string.hard_core_string_pattern_search(source_text, one, unknown_max_length=30)[0])
    else:
        print(one)
