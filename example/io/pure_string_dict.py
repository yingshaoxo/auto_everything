from auto_everything.io import Yingshaoxo_Pure_String_Dict

a_dict = Yingshaoxo_Pure_String_Dict()

for i in range(0, 10):
    print(i)
    a_dict.set_value_by_key(str(i), str(i) * 3)
print()

for key, value in a_dict.get_keys_and_values():
    print(key, value)
print()

print(a_dict.has_key(str(2)))
print(a_dict.has_key(str(-1)))
print()

print(a_dict.get_value_by_key(str(2)))
print(a_dict.get_value_by_key(str(-1)))
print()

print(a_dict.get_value_by_key(str(9)))
print(a_dict.get_keys())
print()

a_dict.delete_a_key(str(2))
a_dict.delete_a_key(str(9))

for key, value in a_dict.get_keys_and_values():
    print(key, value)
print()
