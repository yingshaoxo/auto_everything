# yingshaoxo: A demo python parser, definately have bugs, it is just fake code, rewrite it carefully to prevent bugs. Read the code from bottom to top will save your time.


# If you can implement the eval() function that matchs original python functionality, then this project would be 100% available for production. Then you just have to implement the 'import' functionality.

# I think there might have ways to implement try and catch method, because we know if a variable_name or function_name is defined or not before we run a line of code, and we also know if code in a function has syntax error or not. I just need to find a way to mimic the original python try and except error handling behavior. OK, I got it, we just have to create a Python_Element_Instance where its type is "Error" and give the general_value a error_string to descript that error. Then in the process_code function, if we get a error element, we print error and return immediately. And when we hit 'try code_block', we run that code block first, if we get any error element, we drop that code_block, then we run 'except code_block'.

# As for the class, actually we could use a dict to replace class. Just create a dict with some propertys and functions, then whenever you want to create a "new class", you copy that dict, and change those data in that new dict with functions defined inside of that dict. Ofcause you have to pass that dict as 'self' to those functions each time. The python class machinism is just a helper grammer to simplifying that process.

# Now, you can try to implement the 'import' stuff, but I think it is better use relative or absolute .py file path. For example: 'import "./a_lib.py" as a_lib'.


# normally in python you get this dict by using dir()
global_variable_dict = {
    "__built_in_s__": ["type", "len", "eval"]
}

process = None # later it would be a function

class Python_Element_Instance():
    def __init__(self):
        # none, string, bool, int, float, list, dict, function(a_string_of_code_block), class, class_instance(propertys:dict{...variable_dict, ...functions.dict})
        self.type = "None"
        self.name = None # variable name, function name, class name
        self.value = None # in c, it is Ypython_General()
        self.information = {}

def get_text_until_closed_symbol(code_text, start_symbol, end_symbol):
    # value = get_text_until_closed_symbol(lines[line_index:], start_symbol, end_symbol)
    result_text = ""

    start_symbol_counting = 0
    end_symbol_counting = 0

    start_the_process = False
    index = 0
    for char in code_text:
        if start_symbol == char:
            start_symbol_counting += 1
            start_the_process = True
        elif end_symbol == char:
            end_symbol_counting += 1

        if start_the_process == True:
            result_text += char

            if start_symbol_counting == end_symbol_counting:
                break

        index += 1

    return result_text, index

def expression_segment_extraction(variable_dict, a_line_of_code):
    a_line_of_code += " "
    a_list_of_string_segment = []
    a_list_of_elements = []

    index = 0
    while index < len(a_line_of_code):
        character = a_line_of_code[index]
        if character == '"':
            temp_string = character
            temp_index = index + 1
            previous_character = None
            while temp_index < len(a_line_of_code):
                temp_character = a_line_of_code[temp_index]
                if previous_character != "\\":
                    if temp_character == '"':
                        temp_string += temp_character
                        a_list_of_string_segment.append(temp_string)
                        a_element = Python_Element_Instance()
                        a_element.type = "string"
                        a_element.value = temp_string[1:-1]
                        a_list_of_elements.append(a_element)
                        break
                temp_string += temp_character
                previous_character = temp_character
                temp_index += 1
            index = temp_index
        elif character == "'":
            temp_string = character
            temp_index = index + 1
            previous_character = None
            while temp_index < len(a_line_of_code):
                temp_character = a_line_of_code[temp_index]
                if previous_character != "\\":
                    if temp_character == "'":
                        temp_string += temp_character
                        a_list_of_string_segment.append(temp_string)
                        a_element = Python_Element_Instance()
                        a_element.type = "string"
                        a_element.value = temp_string[1:-1]
                        a_list_of_elements.append(a_element)
                        break
                temp_string += temp_character
                previous_character = temp_character
                temp_index += 1
            index = temp_index
        elif character.isdigit():
            # also parse float until it meets space
            temp_string = character
            temp_index = index + 1
            while temp_index < len(a_line_of_code):
                temp_character = a_line_of_code[temp_index]
                if temp_character == " " or temp_character == ",":
                    a_list_of_string_segment.append(temp_string)
                    a_element = Python_Element_Instance()
                    if "." in temp_string:
                        a_element.type = "float"
                        a_element.value = float(temp_string)
                    else:
                        a_element.type = "int"
                        a_element.value = int(temp_string)
                    a_list_of_elements.append(a_element)

                    if temp_character == " ":
                        break
                    else:
                        # return immediately if end with ,
                        return a_list_of_string_segment, a_list_of_elements, index + 1
                temp_string += temp_character
                temp_index += 1
            index = temp_index
        elif character == " ":
            pass
        elif character == ",":
            #a_list_of_string_segment.append(character)
            #a_element = Python_Element_Instance()
            #a_element.type = "comma_separator"
            #a_element.value = character
            #a_list_of_elements.append(a_element)
            return a_list_of_string_segment, a_list_of_elements, index + 1
        elif character in ["+", "-", "*", "/", "%"]:
            a_list_of_string_segment.append(character)
            a_element = Python_Element_Instance()
            a_element.type = "operator"
            a_element.value = character
            a_list_of_elements.append(a_element)
        elif character in [">", "<", "="]:
            # also parse ">=", "<=", "==" until it meets space
            temp_string = character
            temp_index = index + 1
            while temp_index < len(a_line_of_code):
                temp_character = a_line_of_code[temp_index]
                if temp_character == " ":
                    a_list_of_string_segment.append(temp_string)
                    a_element = Python_Element_Instance()
                    a_element.type = "operator"
                    a_element.value = temp_string
                    a_list_of_elements.append(a_element)
                    break
                temp_string += temp_character
                temp_index += 1
            index = temp_index
        elif character in ['(', "[", "{"]:
            if character == "(":
                temp_string, new_index = get_text_until_closed_symbol(a_line_of_code[index:], "(", ")")
            elif character == "[":
                temp_string, new_index = get_text_until_closed_symbol(a_line_of_code[index:], "[", "]")
            elif character == "{":
                temp_string, new_index = get_text_until_closed_symbol(a_line_of_code[index:], "{", "}")
            old_index = index
            index = index + new_index
            a_list_of_string_segment.append(temp_string)
            if character == "(":
                a_element = Python_Element_Instance()
                a_element.type = "one_line_code_block"
                a_element.value = temp_string
                a_list_of_elements.append(a_element)
            elif character == "[":
                # handle list
                # in the end, the element.value should be a list of values
                # and, you should also implement the list and dict get and set function, such as "a_list = []; a_list.append(1); a_list[0] = 1; del a_list[0]" or "a_dict = {}; a_dict['2'] = 3; del a_dict['2']"

                temp_a_list = []
                pure_temp_string = temp_string[1:-1]
                while len(pure_temp_string) > 0:
                    temp_a_list_of_string_segment, temp_a_list_of_elements, temp_index = expression_segment_extraction(variable_dict, pure_temp_string)
                    temp_part_value = evaluate_expression(variable_dict, "", a_list_of_elements=temp_a_list_of_elements)
                    temp_a_list.append(temp_part_value)
                    pure_temp_string = pure_temp_string[temp_index:]

                a_element = Python_Element_Instance()
                a_element.type = "list"
                a_element.value = temp_a_list
                a_list_of_elements.append(a_element)
            elif character == "{":
                # handle dict, let's make it a simple one
                pure_temp_string = temp_string[1:-1]
                values = pure_temp_string.split(",") # there may have a bug when a list is in the dict, but we do not care
                temp_dict = {evaluate_expression(variable_dict, one.split(":")[0].strip()).value: evaluate_expression(variable_dict, one.split(":")[1].strip()) for one in values}

                a_element = Python_Element_Instance()
                a_element.type = "dict"
                a_element.value = temp_dict
                a_list_of_elements.append(a_element)
        elif character.isalpha():
            temp_string = character
            temp_index = index + 1
            previous_character = None
            while temp_index < len(a_line_of_code):
                temp_character = a_line_of_code[temp_index]
                if temp_character == '(':
                    # need to handle function call
                    arguments_string, new_index = get_text_until_closed_symbol(a_line_of_code[temp_index:], "(", ")")
                    temp_string += arguments_string
                    temp_index += new_index
                    a_list_of_string_segment.append(temp_string)
                    a_element = Python_Element_Instance()
                    a_element.type = "function_call"
                    a_element.value = temp_string
                    a_list_of_elements.append(a_element)
                    break
                elif temp_character == " " or temp_character == ",":
                    # maybe just a variable name
                    # can also be [and, or, not, True, False, None]
                    a_list_of_string_segment.append(temp_string)

                    a_element = Python_Element_Instance()
                    a_element.value = temp_string
                    if temp_string == "True":
                        a_element.type = "bool"
                        a_element.value = True
                    elif temp_string == "False":
                        a_element.type = "bool"
                        a_element.value = False
                    elif temp_string == "None":
                        a_element.type = "none"
                        a_element.value = None
                    elif temp_string in ["and", "or", "not"]:
                        a_element.type = "operator"
                    else:
                        a_element.type = "variable"
                        a_element.name = temp_string
                    a_list_of_elements.append(a_element)

                    if temp_character == " ":
                        break
                    else:
                        # return immediately if end with ,
                        return a_list_of_string_segment, a_list_of_elements, index + 1
                elif temp_character == "[":
                    # it might be a dict[] or list[] element access variable
                    key_string, new_index = get_text_until_closed_symbol(a_line_of_code[temp_index:], "[", "]")
                    list_or_dict_variable_name = temp_string

                    temp_string += key_string
                    temp_index += new_index
                    a_list_of_string_segment.append(temp_string)

                    pure_key = key_string[1:-1]
                    if pure_key.startswith('"') or pure_key.startswith("'"):
                        pure_key = pure_key[1:-1]
                    else:
                        pure_key = int(pure_key)

                    if type(pure_key) == str:
                        if pure_key in variable_dict[list_or_dict_variable_name].value:
                            the_real_value_element = variable_dict[list_or_dict_variable_name].value.get(pure_key)
                            if the_real_value_element == None:
                                return Python_Element_Instance()
                        else:
                            the_real_value_element = Python_Element_Instance()
                    else:
                        if pure_key < len(variable_dict[list_or_dict_variable_name].value):
                            the_real_value_element = variable_dict[list_or_dict_variable_name].value[pure_key]
                        else:
                            the_real_value_element = Python_Element_Instance()

                    the_real_value_element.information["list_or_dict_variable_name"] = list_or_dict_variable_name
                    the_real_value_element.information["key_string"] = pure_key

                    a_list_of_elements.append(the_real_value_element)
                    break
                temp_string += temp_character
                previous_character = temp_character
                temp_index += 1
            index = temp_index
        index += 1

    return a_list_of_string_segment, a_list_of_elements, index

def get_real_value_of_a_element(variable_dict, an_element):
    if an_element.type == "one_line_code_block" and an_element.value.startswith("(") and an_element.value.endswith(")"):
        return evaluate_expression(variable_dict, an_element.value[1:-1])

    if an_element.type == "one_line_code_block":
        result = get_python_element_instance(variable_dict, an_element.value)
        return result

    if an_element.type == "variable":
        result = get_python_element_instance(variable_dict, an_element.value)
        return result

    if an_element.type == "function_call":
        return handle_function_call(variable_dict, an_element.value)

    return an_element

def do_operation_for_two_element(operator_element, an_element_1, an_element_2):
    # basic operators: ["+", "-", "*", "/", ">", "<", "==", ">=", "<=", "and", "or"]

    new_element = Python_Element_Instance()
    if operator_element.type != "operator":
        return new_element

    new_element.type = an_element_1.type

    operator = operator_element.value
    if operator == "+":
        new_element.value = an_element_1.value + an_element_2.value
    elif operator == "-":
        new_element.value = an_element_1.value - an_element_2.value
    elif operator == "*":
        # in python, it allow you do "a sting" * 100
        new_element.value = an_element_1.value * an_element_2.value
    elif operator == "/":
        new_element.value = an_element_1.value / an_element_2.value
    elif operator == ">":
        new_element.type = "bool"
        new_element.value = an_element_1.value > an_element_2.value
    elif operator == "<":
        new_element.type = "bool"
        new_element.value = an_element_1.value < an_element_2.value
    elif operator == "==":
        new_element.type = "bool"
        new_element.value = an_element_1.value == an_element_2.value
    elif operator == ">=":
        new_element.type = "bool"
        new_element.value = an_element_1.value >= an_element_2.value
    elif operator == "<=":
        new_element.type = "bool"
        new_element.value = an_element_1.value <= an_element_2.value
    elif operator == "and":
        new_element.type = "bool"
        new_element.value = an_element_1.value and an_element_2.value
    elif operator == "or":
        new_element.type = "bool"
        new_element.value = an_element_1.value or an_element_2.value
    else:
        new_element.type == "none"

    return new_element

def evaluate_expression(variable_dict, a_line_of_code, a_list_of_elements=None):
    # parsing the code char by char from left to right. this should be a replacement for handle_one_line_operations()
    # it will not care about operation orders, use () to do things first
    global global_variable_dict

    new_dict = {}
    for key in variable_dict.keys():
        if key in global_variable_dict:
            new_dict[key] = global_variable_dict[key]
        else:
            new_dict[key] = variable_dict[key]

    if a_list_of_elements == None:
        a_list_of_string_segment, a_list_of_elements, _ = expression_segment_extraction(new_dict, a_line_of_code)

    if len(a_list_of_elements) == 0:
        a_element = Python_Element_Instance()
        return a_element
    elif len(a_list_of_elements) == 1:
        one_element = a_list_of_elements[0]
        if one_element.type == "one_line_code_block" and one_element.value.startswith("(") and one_element.value.endswith(")"):
            return evaluate_expression(variable_dict, one_element.value[1:-1])
        one_element = get_real_value_of_a_element(variable_dict, one_element)
        return one_element
    elif len(a_list_of_elements) == 2:
        one_element = a_list_of_elements[0]
        one_element = get_real_value_of_a_element(variable_dict, one_element)
        return one_element

    value_1 = a_list_of_elements[0]
    value_2 = a_list_of_elements[1]
    value_3 = a_list_of_elements[2]

    value_1 = get_real_value_of_a_element(variable_dict, value_1)
    value_3 = get_real_value_of_a_element(variable_dict, value_3)

    new_element = do_operation_for_two_element(value_2, value_1, value_3)

    left_elements = a_list_of_elements[3:]
    if len(left_elements) < 2:
        return new_element
    else:
        return evaluate_expression(variable_dict, [new_element] + left_elements)

##a_list, _, _ = expression_segment_extraction("""("2" + "2") * ('1' * (2 * 2)) + shit_99(sss, (yy, xx), [2,2])""")
##a_list, _, _ = expression_segment_extraction({}, '''[1, 2 * 3, 3]''')
##print(a_list)
#a_value = evaluate_expression({}, '{"a": 3, "b": "222"}')
#print(a_value.value["a"].value)
##for one in a_value.value:
##    print(one.value)
#exit()

def get_python_element_instance(variable_dict, a_variable_name_or_raw_value):
    # As a simplest solution, I'd like to save this function forever.
    global global_variable_dict

    if (a_variable_name_or_raw_value not in variable_dict) and (a_variable_name_or_raw_value not in global_variable_dict):
        # may detect if its a number or bool or string or ...
        a_element = Python_Element_Instance()
        if a_variable_name_or_raw_value.startswith('"') and a_variable_name_or_raw_value.endswith('"'):
            # it is a string
            a_element.type = "string"
            a_element.value = a_variable_name_or_raw_value[1:-1]
        elif a_variable_name_or_raw_value.replace(".","").isdigit():
            # it is a number
            # is_digit: use xx.strip("0123456789.") == "" could also do the job
            if "." in a_variable_name_or_raw_value:
                # it is float
                a_element.type = "float"
                a_element.value = float(a_variable_name_or_raw_value)
            else:
                # it is int
                a_element.type = "int"
                a_element.value = int(a_variable_name_or_raw_value)
        elif a_variable_name_or_raw_value == "True" or a_variable_name_or_raw_value == "False":
            # it is bool
            a_element.type = "bool"
            if a_variable_name_or_raw_value == "True":
                a_element.value = True
            else:
                a_element.value = False
        elif a_variable_name_or_raw_value.startswith('[') and a_variable_name_or_raw_value.endswith(']'):
            # it is list
            a_element.type = "list"
            values = a_variable_name_or_raw_value[1:-1].split(", ")
            values = [get_python_element_instance(variable_dict, one) for one in values]
            a_element.value = values
        elif a_variable_name_or_raw_value.startswith('{') and a_variable_name_or_raw_value.endswith('}'):
            # it is dict
            a_element.type = "dict"
            values = a_variable_name_or_raw_value[1:-1].split(", ") # there may have a bug when a list is in the dict
            values = {one.split(": ")[0].strip(): get_python_element_instance(variable_dict, one.split(":")[1].strip()) for one in values}
            a_element.value = values
        else:
            # unknow, treat it as string
            a_element.type = "string"
            a_element.value = "Error: no variable called '" + str(a_variable_name_or_raw_value) + "'"
        return a_element
    else:
        if a_variable_name_or_raw_value in variable_dict:
            return variable_dict[a_variable_name_or_raw_value]
        elif a_variable_name_or_raw_value in global_variable_dict:
            return global_variable_dict[a_variable_name_or_raw_value]

def handle_one_line_operations(variable_dict, one_line_code):
    #return eval(one_line_code)

    # sometimes I think this is a simpler parsing method, you see, if you use variable_name for operations, there would have no parsing errors, for example: a == 'xxxx'; b == 'yyyy'; a == b;
    # variable a and b will have no special chracters.
    # do operations one by one, simple and easy

    # But now it gets replaces by evaluate_expression()
    # As a simplest solution, I'd like to save this function forever.
    if " + " in one_line_code:
        parts = one_line_code.split(" + ")
        parts = [get_python_element_instance(variable_dict, one) for one in parts]
        value = parts[0].value
        for one_value in parts[1:]:
            value += one_value.value

        an_element = Python_Element_Instance()
        an_element.type = "string"
        an_element.value = value

        return an_element
    elif " - " in one_line_code:
        pass
    elif " * " in one_line_code:
        pass
    elif " / " in one_line_code:
        pass
    elif " > " in one_line_code:
        pass
    elif " >= " in one_line_code:
        pass
    elif " < " in one_line_code:
        parts = one_line_code.split(" < ")

        an_element = Python_Element_Instance()
        an_element.type = "bool"

        if len(parts) == 2:
            an_element.value = get_python_element_instance(variable_dict, parts[0]).value < get_python_element_instance(variable_dict, parts[1]).value
        else:
            an_element.value = False

        return an_element
    elif " <= " in one_line_code:
        pass
    elif " == " in one_line_code:
        parts = one_line_code.split(" == ")

        an_element = Python_Element_Instance()
        an_element.type = "bool"

        if len(parts) == 2:
            an_element.value = get_python_element_instance(variable_dict, parts[0]).value == get_python_element_instance(variable_dict, parts[1]).value
        else:
            an_element.value = False

        return an_element
    elif " != " in one_line_code:
        pass
    #elif " and " in one_line_code: # cause parsing error, need to find a way to solve this problem
    #    pass
    #elif " or " in one_line_code:
    #    pass
    else:
        return get_python_element_instance(variable_dict, one_line_code)

def handle_function_call(variable_dict, one_line_code, class_instance=None):
    global global_variable_dict
    line = one_line_code

    function_name = line.split("(")[0]
    #function_arguments = line.split("(")[1].split(")")[0].strip()
    function_arguments, _ = get_text_until_closed_symbol(line, "(", ")")
    function_arguments = function_arguments[1:-1]

    if "." in function_name:
        # might be class function call
        class_instance_name = function_name.split(".")[0]
        function_name = function_name.split(".")[1]
        if (class_instance_name in variable_dict) or (class_instance_name in global_variable_dict):
            class_instance = variable_dict.get(class_instance_name)
            if class_instance == None:
                class_instance = global_variable_dict.get(class_instance_name)
            if class_instance.type == "list":
                if function_name == "append":
                    append_value = evaluate_expression(variable_dict, function_arguments)
                    class_instance.value.append(append_value)
                    return Python_Element_Instance()
            elif class_instance.type == "dict":
                if function_name == "get":
                    get_key = evaluate_expression(variable_dict, function_arguments)
                    the_value_element = class_instance.value.get(get_key.value)
                    if the_value_element == None:
                        return Python_Element_Instance()
                    else:
                        return the_value_element
            elif class_instance.type == "string":
                if function_name == "split":
                    split_value = evaluate_expression(variable_dict, function_arguments).value
                    an_element = Python_Element_Instance()
                    an_element.type = "list"
                    a_list = class_instance.value.split(split_value)
                    for index, one in enumerate(a_list):
                        temp_value = Python_Element_Instance()
                        temp_value.type = "string"
                        temp_value.value = one
                        a_list[index] = temp_value
                    an_element.value = a_list
                    return an_element
                elif function_name == "startswith":
                    an_element = Python_Element_Instance()
                    an_element.type = "bool"
                    an_element.value = class_instance.value.startswith(evaluate_expression(variable_dict, function_arguments).value)
                    return an_element
                elif function_name == "endswith":
                    an_element = Python_Element_Instance()
                    an_element.type = "bool"
                    an_element.value = class_instance.value.endswith(evaluate_expression(variable_dict, function_arguments).value)
                    return an_element
                elif function_name == "strip":
                    an_element = Python_Element_Instance()
                    an_element.type = "string"
                    an_element.value = class_instance.value.strip()
                    return an_element
            else:
                return handle_function_call(class_instance.value["properties"], one_line_code[len(class_instance_name)+1:-1], class_instance=class_instance)
        else:
            print("Error: no class_instance called '" + class_instance_name + "'")
            return Python_Element_Instance()

    arguments_are_variable_dict = {}
    if function_arguments != "":
        for index, one in enumerate(function_arguments.split(", ")):
            if "=" in one:
                key = one.split("=")[0]
                value = one.split("=")[1]
                value = evaluate_expression(variable_dict, value)
            else:
                key = "___argument"+str(index)
                value = evaluate_expression(variable_dict, one)
            arguments_are_variable_dict[key] = value

    if (function_name in variable_dict) or (function_name in global_variable_dict):
        if function_name in variable_dict:
            an_element = variable_dict[function_name]
        elif function_name in global_variable_dict:
            an_element = global_variable_dict[function_name]
        if an_element.type == "function":
            if class_instance != None:
                # function call in class, so we drop all other property except 'self'
                local_dict_for_a_function = {"self": variable_dict["self"]}
            else:
                local_dict_for_a_function = variable_dict.copy()

            function_defined_arguments_line = an_element.value.split("\n")[0].split("(")[1].split(")")[0]
            defined_list_of_arguments = function_defined_arguments_line.split(", ")
            if class_instance != None:
                # handle the keyword 'self' in class function
                local_dict_for_a_function["self"] = class_instance
                defined_list_of_arguments = defined_list_of_arguments[1:]
            for index in range(len(defined_list_of_arguments)):
                key = defined_list_of_arguments[index]
                value = None
                if "=" in key:
                    # set pre_defined key and value to local_variable_dict first
                    key = key.split("=")[0].strip()
                    value = key.split("=")[1].strip()
                    local_dict_for_a_function.update({key: value})
                if key in arguments_are_variable_dict.keys():
                    # use new arguments from function call command
                    value = arguments_are_variable_dict.get(key)
                    local_dict_for_a_function.update({key: value})
                if key not in arguments_are_variable_dict.keys():
                    # set arguments by indexing
                    value = arguments_are_variable_dict.get("___argument"+str(index))
                    local_dict_for_a_function.update({key: value})

            real_code = "\n".join(an_element.value.split("\n")[1:])
            return process_code(local_dict_for_a_function, real_code)
        elif an_element.type == "class":
            new_element = Python_Element_Instance()
            new_element.type = "class_instance"
            new_element.value = {
                "class_name": an_element.name,
                "properties": {
                    "self": new_element
                }
            }
            process_code(new_element.value["properties"], an_element.value)
            if "__init__" in new_element.value["properties"]:
                # run the __init__ function when we create a class instance
                handle_function_call(new_element.value["properties"], "__init__(self)", class_instance=new_element)
            return new_element
    elif function_name in global_variable_dict["__built_in_s__"]:
        if function_name == "type":
            an_element = Python_Element_Instance()
            an_element.type = "string"
            an_element.value = evaluate_expression(variable_dict, function_arguments).type
            return an_element
        elif function_name == "len":
            an_element = Python_Element_Instance()
            an_element.type = "int"
            an_element.value = len(evaluate_expression(variable_dict, function_arguments).value)
            return an_element
        elif function_name == "eval":
            an_element = Python_Element_Instance()
            return evaluate_expression(variable_dict, function_arguments[1:-1])
    else:
        print("Error: no function called '" + function_name + "'")
        return Python_Element_Instance()

def general_print(an_element, end="\n"):
    if "type" in dir(an_element):
        if an_element.type == "list":
            print("[", end="")
            for index, temp_element in enumerate(an_element.value):
                general_print(temp_element, end="")
                if index != len(an_element.value)-1:
                    print(", ", end="")
            print("]", end="\n")
        elif an_element.type == "dict":
            print("{", end="")
            for temp_element_key, temp_element_value in an_element.value.items():
                print(temp_element_key, end="")
                print(": ", end="")
                general_print(temp_element_value, end="")
            print("}", end="\n")
        elif an_element.type == "string":
            print('"' + an_element.value + '"', end=end)
        else:
            print(an_element.value, end=end)
    else:
        print(an_element)

def get_code_block(lines, line_index):
    temp_index = line_index + 1
    temp_code_block = ""
    base_line = lines[temp_index]
    indents_number = len(base_line) - len(base_line.lstrip())
    while temp_index < len(lines):
        temp_line = lines[temp_index]
        new_indents_number = len(temp_line) - len(temp_line.lstrip())
        if temp_line.strip()!="" and new_indents_number < indents_number:
            break
        temp_code_block += temp_line + "\n"
        temp_index += 1
    line_index = temp_index - 1 #if the code block search stop on new code block, it should minus 1
    return temp_code_block, line_index

def process_code(variable_dict, text_code):
    # handle code, mainly just for codes inside of a function
    lines = text_code.split("\n")
    line_index = 0
    while line_index < len(lines):
        line = lines[line_index]
        if line.strip().startswith("#"):
            pass
        elif line.strip().startswith("if "):
            if_line = line

            temp_index = line_index + 1
            temp_code_block = ""
            base_line = lines[temp_index]
            indents_number = len(base_line) - len(base_line.lstrip())
            while temp_index < len(lines):
                temp_line = lines[temp_index]
                new_indents_number = len(temp_line) - len(temp_line.lstrip())
                if temp_line.strip()!="" and new_indents_number < indents_number:
                    break
                temp_code_block += temp_line + "\n"
                temp_index += 1
            line_index = temp_index - 1 #if the code block search stop on new code block, it should minus 1

            verifying = if_line.split("if ")[1].split(":")[0]
            verifying = evaluate_expression(variable_dict, verifying)

            if verifying.type == "bool":
                if verifying.value == True:
                    result_element = process_code(variable_dict, temp_code_block)
                    if result_element.type == "special_operation":
                        if result_element.value == "continue":
                            return result_element
                        elif result_element.value == "break":
                            return result_element
        elif line.strip().startswith("while "):
            while_line = line

            temp_code_block, line_index = get_code_block(lines, line_index)

            while True:
                verifying = while_line.split("while ")[1].split(":")[0]
                verifying = evaluate_expression(variable_dict, verifying)

                if verifying.type == "bool":
                    if verifying.value == True:
                        result_element = process_code(variable_dict, temp_code_block)
                        if result_element.type == "special_operation":
                            if result_element.value == "continue":
                                continue
                            elif result_element.value == "break":
                                break
                        continue
                break
        elif " = " in line:
            # we save that variable to global variable dict
            key, value = line.split(" = ")
            key, value = key.strip(), value.strip()
            if "." in key:
                # class_instance assignment
                class_instance_name = key.split(".")[0]
                class_instance_property_name = key.split(".")[1]
                if class_instance_name in variable_dict.keys():
                    class_instance = variable_dict[class_instance_name]
                    if class_instance.type == "class_instance":
                        if value.endswith(")"):
                            class_instance.value["properties"][class_instance_property_name] = handle_function_call(variable_dict, value)
                        else:
                            class_instance.value["properties"][class_instance_property_name] = evaluate_expression(variable_dict, value)

            elif "." in value and not value.endswith(")"):
                # class_instance assignment
                class_instance_name = value.split(".")[0]
                class_instance_property_name = value.split(".")[1]
                if class_instance_name in variable_dict.keys():
                    class_instance = variable_dict[class_instance_name]
                    if class_instance.type == "class_instance":
                        variable_dict[key] = class_instance.value["properties"][class_instance_property_name]
            else:
                if value.endswith(")"):
                    # it is a function call
                    an_element = handle_function_call(variable_dict, value)
                elif value.startswith('"""'):
                    # it is a raw string, """could have no leading space in next line"""
                    long_text = ""
                    temp_index = line_index + 1
                    while temp_index < len(lines):
                        temp_line = lines[temp_index]
                        long_text += temp_line + "\n"
                        if temp_line.endswith('"""'):
                            break
                        temp_index += 1
                    line_index = temp_index
                    an_element = Python_Element_Instance()
                    an_element.type = "string"
                    an_element.value = long_text[:-5]
                else:
                    # normal value
                    an_element = evaluate_expression(variable_dict, value)
                if "[" not in key:
                    an_element.name = key
                    variable_dict[key] = an_element
                else:
                    # could be a dict or list assignment
                    key_element = evaluate_expression(variable_dict, key)
                    list_or_dict_variable_name = key_element.information["list_or_dict_variable_name"]
                    key_string = key_element.information["key_string"]
                    if list_or_dict_variable_name in variable_dict:
                        variable_dict[list_or_dict_variable_name].value[key_string] = an_element
        elif "print(" in line:
            key = line.split("print(")[1][:-1]
            value_instance = evaluate_expression(variable_dict, key)
            general_print(value_instance)
        elif line.strip().startswith("def "):
            # it is a function, we should save it in somewhere
            function_name = line.split("def ")[1].split("(")[0]
            function_code = ""
            end_of_a_function_new_line_counting = 0

            function_code += lines[line_index] + "\n" #try to save the function arguments

            temp_code_block, line_index = get_code_block(lines, line_index)
            function_code += temp_code_block

            an_element = Python_Element_Instance()
            an_element.type = "function"
            an_element.name = function_name
            an_element.value = function_code
            variable_dict[function_name] = an_element
        elif (not line.startswith("def ")) and "(" in line and line.endswith(")"):
            handle_function_call(variable_dict, line)
        elif line.strip().startswith("class "):
            class_name = line.split("class ")[1].split(":")[0].split("()")[0].strip()

            temp_code_block, line_index = get_code_block(lines, line_index)

            an_element = Python_Element_Instance()
            an_element.type = "class"
            an_element.name = class_name
            an_element.value = temp_code_block
            variable_dict[class_name] = an_element
        elif line.strip().startswith("return "):
            return_variable_name = line.split("return ")[1]
            return_variable_name = evaluate_expression(variable_dict, return_variable_name)
            return return_variable_name
        elif line.strip() == "break":
            an_element = Python_Element_Instance()
            an_element.type = "special_operation"
            an_element.value = "break"
            return an_element
        elif line.strip() == "continue":
            an_element = Python_Element_Instance()
            an_element.type = "special_operation"
            an_element.value = "continue"
            return an_element

        line_index += 1

    return Python_Element_Instance()

a_py_file_text = '''
parent_variable = "parent"
print(parent_variable)

def a_function_1():
    a_child_variable = "whatever"
    print(parent_variable)
    print(a_child_variable)

a_function_1()
print(a_child_variable)

def a_function_2(temp_2, temp3):
    temp_1 = " you say"
    a_child_variable2 = "whatever" + temp_1
    print(a_child_variable2)
    print(temp_2)
    print(temp3)

a_function_2("nice", temp3="yeah")
print("is" + " right")

a_dict = {"a": 3}
print(a_dict)

a_list = ["god", "yingshaoxo"]
print(a_list)

print(2 + 3)

a_type = type(2)
print(a_type)

def a_function_3(number_1, number_2):
    return number_1 + number_2

result1 = a_function_3(number_1=6, number_2=7)
print(result1)

long_text = """
hi you,
    dear.
"""

print(long_text)


a2 = 1
b2 = 1
print(a2 == b2)
if a2 == b2:
    print("a2 and b2 is equal")

while a2 < (3 + 4):
    print(a2)
    a2 = a2 + 1
    if a2 == (6 - 2):
        break


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



print("Let's test the list")
a_list = [1, 2, 3]
print(a_list[2])
a_list[0] = 999
print(a_list[0])

print("Let's test the dict")
a_dict = {"a": "ying", "b": "shaoxo"}
print(a_dict["a"])
print(a_dict["b"])
a_dict["a"] = "ok"
print(a_dict["a"])
a_dict["c"] = "cc"
print(a_dict["c"])
print(a_dict.get("c"))

a_list = []
a_list.append("hi")
a_list.append(666)
print(a_list)
print(len(a_list))

a_string = "abc edf aaa   "
a_string = a_string.strip()
a_split_list = a_string.split(" ")
print(a_split_list)

true_or_not = a_string.startswith("abc")
print(true_or_not)

print(eval("(1 + 1) * 3"))
'''

process_code(global_variable_dict, a_py_file_text)
