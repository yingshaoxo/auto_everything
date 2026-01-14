name = "Hi"
name = "yingshaoxo"
print(name)
#assert name == "yingshaoxo"

def a_function():
    new_variable = "nice"
    print(new_variable)
    print(name)
    print("\n\n")

a_function()

def a_function2():
    no_way = "haha"
    a_number = 12345
    a_float_number = 2.3
    print(no_way)
    print(a_number)
    print(a_float_number)

a_function2()

try:
    print(an_error_of_not_exists)
    print("will not print")
except Exception as e:
    print("try and except works")

if 1 == 2:
    function3()

if 2 == 2:
    print("if works for literal characters")


if name == "yingshaoxo":
    print("if works for variables")

if name == "shit":
    print("if not work for variables")

def function_4():
    tip = "the function return works fine"
    return tip

result_4 = function_4()
print(result_4)

def function_5()
    print("it get runned")
    return "100"

if function_5() == "100":
    print("function() in if expression works ok")

a_index = 0
while True:
    print(a_index)
    print("while loop works")
    a_index = a_index + 1
    if a_index == 3:
        break

print(1.2 + 2.5)
print("string " + "add string works")
