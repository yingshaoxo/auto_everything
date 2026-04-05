_yingshaoxo_dict_splitor_1 = b".#new_line#."
_yingshaoxo_dict_splitor_2 = b"|#colon#|"

if "str" in str(type(b"")):
    _is_python2 = True
    _is_python3 = False
else:
    _is_python2 = False
    _is_python3 = True

def _string_strat_with(string, start_string):
    return string.startswith(start_string)

def _string_find_sub_string_index(string, sub_string, start_index=0):
    return string.find(sub_string, start_index)

def _string_split_into_list(string, splitor):
    return string.split(splitor)

def _string_strip(string, chars=b" \n"):
    return string.strip(b" ").strip(chars)

def _string_get_char(string, index):
    one = string[index]
    if _is_python3 == True:
        one = chr(one).encode("utf-8")
    return one

def _string_get_sub_string(string, start_index, end_index):
    return string[start_index: end_index]

def _string_is_ascii(string):
    ascii_string = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=`~!@#$%^&*()_+  []\\{}|;':\",./<>? \n"
    for one in string:
        if _is_python3 == True:
            one = one.encode("utf-8")
        if one not in ascii_string:
            return False
    return True

def _dict_to_yingshaoxo_dict(a_dict):
    temp_text_bytes = b""
    for key, value in a_dict.items():
        temp_text_bytes += bytes(key) + _yingshaoxo_dict_splitor_2 + bytes(value) + _yingshaoxo_dict_splitor_1
    return temp_text_bytes

def _yingshaoxo_dict_to_dict(a_bytes_string):
    temp_dict = {}
    for one in a_bytes_string.split(_yingshaoxo_dict_splitor_1):
        if _yingshaoxo_dict_splitor_2 in one:
            key, value = one.split(_yingshaoxo_dict_splitor_2)
            temp_dict[key] = value
    return temp_dict

def _set_function(variable_dict, function_name, function_arguments_string, function_content_string):
    # we will save the data into disk file in the future
    temp_dict = {}
    temp_dict[b"function_name"] = function_name
    temp_dict[b"function_pre_defined_arguments_string"] = function_arguments_string
    temp_dict[b"function_content_string"] = function_content_string
    if b"___function_dict" not in variable_dict:
        variable_dict[b"___function_dict"] = {}
    variable_dict[b"___function_dict"][function_name] = temp_dict

def _get_function(variable_dict, function_name):
    function_dict = variable_dict.get(b"___function_dict")
    if function_dict == None:
        return None
    temp_data = function_dict.get(function_name)
    if temp_data == None:
        return None
    return temp_data

def _is_function_exists(variable_dict, function_name):
    function_dict = variable_dict.get(b"___function_dict")
    if function_dict == None:
        return False
    temp_data = function_dict.get(function_name)
    if temp_data == None:
        return False
    return True

def _set_variable(variable_dict, variable_name, variable_value):
    temp_dict = {}
    temp_dict[b"variable_name"] = variable_name
    temp_dict[b"variable_value"] = variable_value
    if b"___variable_dict" not in variable_dict:
        variable_dict[b"___variable_dict"] = {}
    variable_dict[b"___variable_dict"][variable_name] = temp_dict

def _get_variable(variable_dict, variable_name):
    a_dict = variable_dict.get(b"___variable_dict")
    if a_dict == None:
        return None
    temp_data = a_dict.get(variable_name)
    if temp_data == None:
        return None
    return temp_data

def _is_variable_exists(variable_dict, variable_name):
    a_dict = variable_dict.get(b"___variable_dict")
    if a_dict == None:
        return False
    temp_data = a_dict.get(variable_name)
    if temp_data == None:
        return False
    return True

def _is_a_char_equal(bytes_text, index, char):
    if _is_python2 == False:
        char = ord(char)
    if bytes_text[index] == char:
        return True
    return False

def _get_end_index_of_paired_punctuation(text, start_punctuation, end_punctuation):
    if start_punctuation not in text:
        return -1
    if end_punctuation not in text:
        return -1
    if _is_python2 == False:
        start_punctuation = ord(start_punctuation)
        end_punctuation = ord(end_punctuation)
    start_counting = 0
    end_counting = 0
    index = 0
    while True:
        character = text[index]
        # in python3, you get number, in python2, you get char
        if character == start_punctuation:
            start_counting += 1
        if character == end_punctuation:
            end_counting += 1
        if start_counting > 0:
            if start_counting == end_counting:
                return index
        index += 1
        if index >= len(text):
            break
    return -1

def _is_it_a_string(code):
    if _is_a_char_equal(code, 0, b"'"):
        if _is_a_char_equal(code, len(code)-1, b"'"):
            return True
    if _is_a_char_equal(code, 0, b"\""):
        if _is_a_char_equal(code, len(code)-1, b"\""):
            return True
    return False

def _is_it_a_number(code):
    if code.isdigit():
        return True
    return False

def _operator_add(a, b):
    if _is_python2 == True:
        if type(a) == str and type(b) == str:
            if _is_it_a_string(a) and _is_it_a_string(b):
                return b'"' + a[1:-1] + b[1:-1] + b'"'
        return a+b
    if _is_python3 == True:
        if type(a) == bytes and type(b) == bytes:
            if _is_it_a_string(a) and _is_it_a_string(b):
                return b'"' + a[1:-1] + b[1:-1] + b'"'
        return a+b
    return a+b

def _is_assignment(code):
    if _string_find_sub_string_index(code, b"=") != -1:
        return True
    return False

def _is_operator_assignment(code):
    if _string_find_sub_string_index(code, b"+=") != -1:
        return True
    if _string_find_sub_string_index(code, b"-=") != -1:
        return True
    if _string_find_sub_string_index(code, b"*=") != -1:
        return True
    if _string_find_sub_string_index(code, b"/=") != -1:
        return True
    return False

def _do_variable_assignment(variable_dict, code):
    code = _string_strip(code, b";")
    the_index = _string_find_sub_string_index(code, b"=")
    if the_index != -1:
        key = code[:the_index]
        key = _string_strip(key)
        value = code[the_index+1:]
        value = _string_strip(value)
        value = _evaluate(variable_dict, value)
        _set_variable(variable_dict, variable_name=key, variable_value=value)
        #print(key, value)

def _do_operator_assignment(variable_dict, code):
    code = _string_strip(code, b";")
    the_index = _string_find_sub_string_index(code, b"+=")
    if the_index != -1:
        key = code[:the_index]
        key = _string_strip(key)
        value = code[the_index+2:]
        value = _string_strip(value)
        value = _evaluate(variable_dict, value)
        new_key = _evaluate(variable_dict, key)
        new_key = _operator_add(new_key, value)
        _set_variable(variable_dict, variable_name=key, variable_value=new_key)
        return
    the_index = _string_find_sub_string_index(code, b"-=")
    if the_index != -1:
        key = code[:the_index]
        key = _string_strip(key)
        value = code[the_index+2:]
        value = _string_strip(value)
        value = _evaluate(variable_dict, value)
        new_key = _evaluate(variable_dict, key)
        new_key = new_key - value
        _set_variable(variable_dict, variable_name=key, variable_value=new_key)
        return
    the_index = _string_find_sub_string_index(code, b"*=")
    if the_index != -1:
        key = code[:the_index]
        key = _string_strip(key)
        value = code[the_index+2:]
        value = _string_strip(value)
        value = _evaluate(variable_dict, value)
        new_key = _evaluate(variable_dict, key)
        new_key = new_key * value
        _set_variable(variable_dict, variable_name=key, variable_value=new_key)
        return
    the_index = _string_find_sub_string_index(code, b"/=")
    if the_index != -1:
        key = code[:the_index]
        key = _string_strip(key)
        value = code[the_index+2:]
        value = _string_strip(value)
        value = _evaluate(variable_dict, value)
        new_key = _evaluate(variable_dict, key)
        new_key = new_key / value
        _set_variable(variable_dict, variable_name=key, variable_value=new_key)
        return

def _parse_function_define_code(code):
    code = _string_strip(code, b";")
    code = code[len(b"define "):]
    start_index_of_argument_string = _string_find_sub_string_index(code, b"(")
    if start_index_of_argument_string == -1:
        return None
    function_name = code[0:start_index_of_argument_string]
    end_index_of_argument_string = _string_find_sub_string_index(code, b")")
    if end_index_of_argument_string == -1:
        return None
    function_arguments_string = code[start_index_of_argument_string+1: end_index_of_argument_string]
    start_index_of_content_string = _string_find_sub_string_index(code, b"{")
    if start_index_of_content_string == -1:
        return None
    end_index_of_content_string = _get_end_index_of_paired_punctuation(text=code, start_punctuation=b"{", end_punctuation=b"}")
    if end_index_of_content_string == -1:
        return None
    function_content_string = code[start_index_of_content_string+1: end_index_of_content_string]
    #print(function_name, "<->", function_arguments_string, "<->", function_content_string.replace(b"\n", "\\n"))
    return {
        b"function_name": function_name,
        b"function_arguments_string": function_arguments_string,
        b"function_content_string": function_content_string,
    }

def _is_it_a_function_call(code):
    code = _string_strip(code, b";")
    first = _string_find_sub_string_index(code, b"(")
    second = _string_find_sub_string_index(code, b")")
    if first == -1:
        return False
    if first < second:
        if _string_get_char(code, len(code)-1) == b")":
            return True
    return False

def _evaluate(variable_dict, code):
    code = _string_strip(code, b";")

    double_equal_mark = _string_find_sub_string_index(code, b"==")
    if double_equal_mark != -1:
        a, b = code.split(b"==")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        if a == b:
            return True
        else:
            return False
    a_mark = _string_find_sub_string_index(code, b">")
    if a_mark != -1:
        a, b = code.split(b">")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        if a > b:
            return True
        else:
            return False
    a_mark = _string_find_sub_string_index(code, b"<")
    if a_mark != -1:
        a, b = code.split(b"<")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        if a < b:
            return True
        else:
            return False
    a_mark = _string_find_sub_string_index(code, b">=")
    if a_mark != -1:
        a, b = code.split(b">=")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        if a >= b:
            return True
        else:
            return False
    a_mark = _string_find_sub_string_index(code, b"<=")
    if a_mark != -1:
        a, b = code.split(b"<=")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        if a <= b:
            return True
        else:
            return False

    a_mark = _string_find_sub_string_index(code, b"+")
    if a_mark != -1:
        a, b = code.split(b"+")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        return _operator_add(a, b)
    a_mark = _string_find_sub_string_index(code, b"-")
    if a_mark != -1:
        a, b = code.split(b"-")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        return a - b
    a_mark = _string_find_sub_string_index(code, b"*")
    if a_mark != -1:
        a, b = code.split(b"*")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        return a * b
    a_mark = _string_find_sub_string_index(code, b"/")
    if a_mark != -1:
        a, b = code.split(b"/")
        a = _evaluate(variable_dict, a)
        b = _evaluate(variable_dict, b)
        return a / b

    if _is_variable_exists(variable_dict=variable_dict, variable_name=code):
        real_value = _get_variable(variable_dict=variable_dict, variable_name=code)
        return real_value[b"variable_value"]

    if _is_it_a_string(code):
        return code

    if _is_it_a_number(code):
        return float(code)

    return None

def _parse_a_function_call(code):
    code = _string_strip(code, b";")
    index = _string_find_sub_string_index(code, b"(")
    if index == -1:
        return None
    function_name = code[0:index]
    function_real_arguments_string = code[index+1:-1]
    return {
        b"function_name": function_name,
        b"function_real_arguments_string": function_real_arguments_string,
    }

def _parse_if_code_block(code):
    argument_start_index = _string_find_sub_string_index(code, b"(")
    if argument_start_index == -1:
        return None
    argument_end_index = _get_end_index_of_paired_punctuation(text=code, start_punctuation=b"(", end_punctuation=b")")
    if argument_end_index == -1:
        return None
    equation = code[argument_start_index+1:argument_end_index]
    content_start_index = _string_find_sub_string_index(code, b"{")
    if content_start_index == -1:
        return None
    content_end_index = _get_end_index_of_paired_punctuation(text=code, start_punctuation=b"{", end_punctuation=b"}")
    if content_end_index == -1:
        return None
    content = code[content_start_index+1:content_end_index]
    return {
        b"equation": equation,
        b"content": content,
    }

def _handle_if_code_block(variable_dict, equation, content):
    equation_value = _evaluate(variable_dict, equation)
    if equation_value:
        run_yingshaoxo_ai_parser_and_executor(variable_dict=variable_dict, code=content)

def _handle_while_code_block(variable_dict, equation, content):
    while True:
        equation_value = _evaluate(variable_dict, equation)
        if equation_value:
            run_yingshaoxo_ai_parser_and_executor(variable_dict=variable_dict, code=content)
        else:
            break

def _call_a_function(variable_dict, function_name, function_real_arguments_string):
    "we will pass keywords dict based arguments for function execution"
    if function_name == b"print":
        print(_evaluate(variable_dict=variable_dict, code=function_real_arguments_string))
        return None

    if function_name == b"run_python":
        function_real_arguments_string = _string_strip(function_real_arguments_string, b"'")
        function_real_arguments_string = _string_strip(function_real_arguments_string, b'"')
        exec(function_real_arguments_string, variable_dict) # should have a format of run_python(input_dict, code);
        return None

    if function_name == b"eval_python":
        function_real_arguments_string = _string_strip(function_real_arguments_string, b"'")
        function_real_arguments_string = _string_strip(function_real_arguments_string, b'"')
        return eval(function_real_arguments_string)

    if _is_function_exists(variable_dict=variable_dict, function_name=function_name):
        function_info = _get_function(variable_dict=variable_dict, function_name=function_name)
        function_info[b"function_real_arguments_string"] = function_real_arguments_string
        """
        function_info[b"function_name"]
        function_info[b"function_pre_defined_arguments_string"]
        function_info[b"function_content_string"]
        function_info[b"function_real_arguments_string"]
        """
        _set_variable(variable_dict, b"___function_info", function_info)

        # remember parent variables
        parent_key_dict = {}
        for key in variable_dict.keys():
            parent_key_dict[key] = 1

        run_yingshaoxo_ai_parser_and_executor(variable_dict=variable_dict, code=function_info[b"function_content_string"])

        # delete sub_function generated garbage variables
        for key in list(variable_dict.keys()):
            if key not in parent_key_dict:
                del variable_dict[key]

def _run_one_piece_of_code(variable_dict, code_type, code):
    if code_type == "define function":
        #print(code.replace(b"\n", "\\n"))
        function_info_dict = _parse_function_define_code(code)
        if function_info_dict == None:
            return
        _set_function(variable_dict=variable_dict, function_name=function_info_dict[b"function_name"], function_arguments_string=function_info_dict[b"function_arguments_string"], function_content_string=function_info_dict[b"function_content_string"])
    if code_type == "comment":
        #print(code.replace(b"\n", "\\n"))
        pass
    if code_type == "if":
        #print(code.replace(b"\n", "\\n"))
        code_block_info_dict = _parse_if_code_block(code)
        if code_block_info_dict == None:
            return
        _handle_if_code_block(variable_dict=variable_dict, equation=code_block_info_dict[b"equation"], content=code_block_info_dict[b"content"])
    if code_type == "while loop":
        #print(code.replace(b"\n", "\\n"))
        code_block_info_dict = _parse_if_code_block(code)
        if code_block_info_dict == None:
            return
        _handle_while_code_block(variable_dict=variable_dict, equation=code_block_info_dict[b"equation"], content=code_block_info_dict[b"content"])
    if code_type == "define variable":
        #print(code.replace(b"\n", "\\n"))
        _do_variable_assignment(variable_dict=variable_dict, code=code)
        pass
    if code_type == "operator assignment":
        #print(code.replace(b"\n", "\\n"))
        _do_operator_assignment(variable_dict=variable_dict, code=code)
        pass
    if code_type == "equation":
        #print(code.replace(b"\n", "\\n"))
        pass
    if code_type == "function call":
        #print(code.replace(b"\n", b"\\n"))
        function_info_dict = _parse_a_function_call(code)
        if function_info_dict == None:
            return
        _call_a_function(variable_dict=variable_dict, function_name=function_info_dict[b"function_name"], function_real_arguments_string=function_info_dict[b"function_real_arguments_string"])
    if code_type == "one line code":
        #print(code.replace(b"\n", b"\\n"))
        if _is_operator_assignment(code):
            _run_one_piece_of_code(variable_dict=variable_dict, code_type="operator assignment", code=code)
            return
        if _is_assignment(code):
            _run_one_piece_of_code(variable_dict=variable_dict, code_type="define variable", code=code)
            return
        if _is_it_a_function_call(code):
            _run_one_piece_of_code(variable_dict=variable_dict, code_type="function call", code=code)
            return
        pass

def run_yingshaoxo_ai_parser_and_executor(variable_dict, code):
    "loop text by character, skip space and newline, when meet 'define' or 'xx=xx' or 'xx();', do something, the ';' is the line end, run code line by line"
    "in this function we handle before keyword, such as define or #, in another function, we handle a whole sentence, such as ;"
    index = 0
    while True:
        character = code[index]

        # jump space
        current_code = code[index:]
        if _string_strat_with(current_code, b" "):
            index += 1
            if index >= len(code):
                break
            continue

        # jump new line
        current_code = code[index:]
        if _string_strat_with(current_code, b"\n"):
            index += 1
            if index >= len(code):
                break
            continue

        # define function
        if _string_strat_with(current_code, b"define "):
            end_index = _get_end_index_of_paired_punctuation(text=current_code, start_punctuation=b"{", end_punctuation=b"}")
            if end_index != -1:
                define_code = current_code[0: end_index+1]
                _run_one_piece_of_code(variable_dict=variable_dict, code_type="define function", code=define_code)
                index += end_index + 1
                continue

        # define if
        if _string_strat_with(current_code, b"if "):
            end_index = _get_end_index_of_paired_punctuation(text=current_code, start_punctuation=b"{", end_punctuation=b"}")
            if end_index != -1:
                define_code = current_code[0: end_index+1]
                _run_one_piece_of_code(variable_dict=variable_dict, code_type="if", code=define_code)
                index += end_index + 1
                continue

        # define while
        if _string_strat_with(current_code, b"while "):
            end_index = _get_end_index_of_paired_punctuation(text=current_code, start_punctuation=b"{", end_punctuation=b"}")
            if end_index != -1:
                define_code = current_code[0: end_index+1]
                _run_one_piece_of_code(variable_dict=variable_dict, code_type="while loop", code=define_code)
                index += end_index + 1
                continue

        # comment
        if _string_strat_with(current_code, b"//") or _string_strat_with(current_code, b"#"):
            end_index = _string_find_sub_string_index(current_code, b"\n")
            if end_index != -1:
                comments = current_code[0: end_index]
                _run_one_piece_of_code(variable_dict=variable_dict, code_type="comment", code=comments)
                index += end_index
                continue
            end_index = _string_find_sub_string_index(current_code, b";") + 1
            if end_index != -1:
                comments = current_code[0: end_index]
                _run_one_piece_of_code(variable_dict=variable_dict, code_type="comment", code=comments)
                index += end_index
                continue
        if _string_strat_with(current_code, b'/*'):
            end_index = _string_find_sub_string_index(current_code, b"*/", 2) + 2
            if end_index != -1:
                comments = current_code[0: end_index]
                _run_one_piece_of_code(variable_dict=variable_dict, code_type="comment", code=comments)
                index += end_index
                continue
        if _string_strat_with(current_code, b"'''"):
            end_index = _string_find_sub_string_index(current_code, b"'''", 3) + 3
            if end_index != -1:
                comments = current_code[0: end_index]
                _run_one_piece_of_code(variable_dict=variable_dict, code_type="comment", code=comments)
                index += end_index
                continue
        if _string_strat_with(current_code, b'"""'):
            end_index = _string_find_sub_string_index(current_code, b'"""', 3) + 3
            if end_index != -1:
                comments = current_code[0: end_index]
                _run_one_piece_of_code(variable_dict=variable_dict, code_type="comment", code=comments)
                index += end_index
                continue

        # one line code
        end_index = _string_find_sub_string_index(current_code, b'\n')
        if end_index == -1:
            end_index = _string_find_sub_string_index(current_code, b';') + 1
        if end_index != -1:
            one_line_code = current_code[0: end_index]
            _run_one_piece_of_code(variable_dict=variable_dict, code_type="one line code", code=one_line_code)
            index += end_index

        index += 1
        if index >= len(code):
            break

def run_yingshaoxo_ai_parser_and_executor_for_file(variable_dict, file_path):
    "this function will not load the whole file into memory, but directly from disk, line by line"
    pass

with open("./demo.ai_v3.txt", "rb") as f:
    source_code = f.read()

run_yingshaoxo_ai_parser_and_executor(variable_dict={}, code=b'''
//"it is a good show";
#;
"""fuck"""
/*shit*/

"fuck" = 'make love';
'shit' = 'output something useless';
"no"

// print(_variable_dict);
# should let __variable_dict = variable_dict in user level

"fuck" = "do making love";
print("fuck");
run_python("print(1+1)");


define "do it"("do what") {
    print("no, you do it");
};
"do it"();

if (exists == None) {
    print("i should define a thing");
}

i = 1;
i = i + 1;
i += 5;
print(i);

print("loop test");
while (i < 10) {
    print(i);
    i = i + 1;
}

"love" = "chinese ai";
print("love");
"love" += "!!!";
print("love");

if ("love" == "chinese ai!!!") {
    print("oh, chinese ai is good!");
}

define "who is yingshaoxo?"() {
    return "you name it";
};

'''+source_code)
