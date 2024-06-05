from auto_everything.string_ import String
string_ = String()

with open("/home/yingshaoxo/Downloads/hero2_white_and_black.png.txt") as f:
    text = f.read()
original_length = len(text)

compressed_text = string_.compress_text_by_using_yingshaoxo_method(text, set(text.split()))
new_length = len(compressed_text)
print("old length:", original_length)
print("new length:", new_length)
print("ratio:", (original_length - new_length)/original_length)
print("reduced to:", 1 - ((original_length - new_length)/original_length))
print("OK:", string_.uncompress_text_by_using_yingshaoxo_method(compressed_text) == text)

print(compressed_text[:1000])
