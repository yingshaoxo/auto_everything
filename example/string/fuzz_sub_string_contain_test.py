from auto_everything.string_ import String
string = String()


source_text = "Morning, hi you."
print(string.check_if_string_is_inside_string(source_text, list("Hxi you.")))
print(string.check_if_string_is_inside_string(source_text, list("xx night.")))


print(string.check_if_string_is_inside_string("你知道你智力的起源吗？", list("你知道你智力从哪儿来的吗？"), 0.4))
# True

print(string.check_if_string_is_inside_string("你知道你智力的起源吗？", list("你知道你鞋子从哪儿来的吗？"), 0.4))
# False

print(string.check_if_string_is_inside_string("你知道你鞋子从哪儿来的吗？", list("你知道你智力从哪儿来的吗？"), 0.4))
# True

print(string.check_if_string_is_inside_string("你知道你鞋子从哪儿来的吗？", list("你知道你智力从哪儿来的吗？"), wrong_limit_ratio=0.2))
# False
