from auto_everything.string_ import String
string_ = String()

text = "shit shit what happend \n" * 100
original_length = len(text)
compressed_text = string_.compress_text_by_using_yingshaoxo_method(text, ["shit shit what happend"])
new_length = len(compressed_text)
print("old length:", original_length)
print("new length:", new_length)
print("ratio:", (original_length - new_length)/original_length)
print("reduced to:", 1 - ((original_length - new_length)/original_length))
print("OK:", string_.uncompress_text_by_using_yingshaoxo_method(compressed_text) == text)
