print("\n\n\n1. test basic variable assignement")
parent_variable = "parent"
print(parent_variable)


print("\n\n\n2. test function call")
def a_function_1():
    a_child_variable = "whatever"
    print(parent_variable)
    print(a_child_variable)

a_function_1()


print("\n\n\n3. test not found variable")
print(a_child_variable)


print("\n\n\n4. test complex function call with arguments")
def a_function_2(temp_2, temp3):
    temp_1 = " you say"
    a_child_variable2 = "whatever" + temp_1
    print(a_child_variable2)
    print(temp_2)
    print(temp3)
a_function_2("nice", temp3="yeah")
print("is" + " right")


print("\n\n\n5. test simple dict and list")
a_dict = {"a": 3}
print(a_dict)

a_list = ["god", "yingshaoxo"]
print(a_list)


print("\n\n\n6. test simple math operations")
print(2 + 3)


print("\n\n\n7. test built in function")
a_type = type(2)
print(a_type)


print("\n\n\n8. test return in function")
def a_function_3(number_1, number_2):
    return number_1 + number_2

result1 = a_function_3(number_1=6, number_2=7)
print(result1)


print("\n\n\n9. test multiple line string variable assignment")
long_text = """
hi you,
    dear.
"""
print(long_text)


print("\n\n\n10. test equal operator")
a2 = 1
b2 = 1
print(a2 == b2)


print("\n\n\n11. test if code block")
if a2 == b2:
    print("a2 and b2 is equal")


print("\n\n\n12. test while loop with break and continue support")
while a2 < (3 + 4):
    print(a2)
    a2 = a2 + 1
    if a2 == (6 - 2):
        break
    continue
    print("will not print after continue")


print("\n\n\n13. test class")
class A_Class():
    def __init__(self):
        print("class instance creating...")
        self.pre_defined_variable = "variable created in class creation"

    def hi(self):
        temp = self.pre_defined_variable
        print(temp)
        print("yingshaoxo:")

    def hi2(self, words):
        print(words)
        return "you"

    def hi3(self):
        self.a_variable = 222
        local_variable = 666

    def hi4(self):
        a_test2 = self.a_variable
        a_test2 = a_test2 + 1
        print(a_test2)
        print(local_variable)

a_class = A_Class()
a_class.hi()
result = a_class.hi2(words="hi")
print(result)

a_class.hi3()
result2 = a_class.a_variable
print(result2)

a_class.hi4()


print("\n\n\n14. test list variable access and assignment")
print("Let's test the list")
a_list = [1, 2, 3]
print(a_list[2])
a_list[0] = 999
print(a_list[0])


print("\n\n\n15. test dict variable access and assignment")
print("Let's test the dict")
a_dict = {"a": "ying", "b": "shao,xo"}
print(a_dict["a"])
print(a_dict["b"])
a_dict["a"] = "ok"
print(a_dict)
print(a_dict["a"])
a_dict["c"] = "cc"
print(a_dict["c"])
print(a_dict.get("c"))


print("\n\n\n16. test list append and length check")
a_list = []
a_list.append("hi")
a_list.append(666)
print(a_list)
print(len(a_list))


print("\n\n\n17. test string split")
a_string = "abc edf aaa   "
a_string = a_string.strip()
a_split_list = a_string.split(" ")
print(a_split_list)


print("\n\n\n18. test string startswith")
true_or_not = a_string.startswith("abc")
print(true_or_not)


print("\n\n\n19. test eval")
print(eval("(1 + 1) * 3"))


print("\n\n\n20. test a in b")
print("a" in "ab")
print("a" in "b")


print("\n\n\n21. test not")
print(not ('a' in 'b'))


print("\n\n\n22. test complex dict and list")
a_complex_dict = {
    "username": {
        "language": ["en", "cn"]
    },
    "a_list": [1, 2, 3, None],
    "a_value": 666
}
print(a_complex_dict)

a_complex_list = [
    {"bb": "baby", "fun_list": ["fun", 2333]},
    "god_boy",
    6666
]
print(a_complex_list)


print("\n\n\n23. test deep return in a function")
def a_return_function():
    while True:
        if 1 == 1:
            print("get into a_return_function")
            return None
    print("error happened in return_function")
a_return_function()


print("\n\n\n24. test try and except")
try:
    a_value = a_function_3(1, 2)
    print(a_value)
    hiasdfkaljs()
except Exception as e:
    print("what error?")
    print(e)


print("\n\n\n25. test str and int")
print(str(123))
print(int("66"))


print("\n\n\n26. test assert")
try:
    assert 1 == 2, "no"
except Exception as e:
    print(e)
