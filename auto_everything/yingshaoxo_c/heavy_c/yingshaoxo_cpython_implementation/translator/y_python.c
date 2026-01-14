/*
I have created a python_based python_interpreter, it works fine. (since now I can have a full control on python syntax, so I do not care about new python syntax anymore, all code will pass to my python interpreter, then the actual python interpreter. So even if I use python3.2/2.7, I can still run python4.0 or later code without problems...)

So the need for rewrite a c_based python is not that important. We will continue to work on this in the future.
*/


#include "../y_python.h"
#include "../y_python_linux.h"

// Global dictionary
Type_Ypython_Dict *global_variable_dict = NULL;

typedef struct Type_Ypython_Element_Instance Type_Ypython_Element_Instance;
struct Type_Ypython_Element_Instance {
    // none, string, bool, int, float, list, dict, function(a_string_of_code_block), class, class_instance(propertys:dict{...variable_dict, ...functions.dict})
    Type_Ypython_String *_type;
    Type_Ypython_String *_name; // variable name, function name, class name
    Type_Ypython_General *_value; // in c, it is Ypython_General()
    Type_Ypython_Dict *_information_dict; // in c, it is Ypython_General()
};

Type_Ypython_Element_Instance *Ypython_Element_Instance() {
    Type_Ypython_Element_Instance *new_element_instance;
    new_element_instance = (Type_Ypython_Element_Instance *)malloc(sizeof(Type_Ypython_Element_Instance));

    new_element_instance->_type = Ypython_String("");
    new_element_instance->_name = Ypython_String("");
    new_element_instance->_value = Ypython_General();
    new_element_instance->_information_dict = Ypython_Dict();
    
    return new_element_instance;
}

bool is_digital(Type_Ypython_String *a_string) {
    Type_Ypython_String *new_string = a_string->function_strip(a_string, Ypython_String("   \n1234567890."));
    if (new_string->function_is_equal(new_string, Ypython_String(""))) {
        return true;
    } else {
        return false;
    }
}

void convert_escape_chars(char *str) {
    // copied from baidu ai
    char *p = str;
    while ((p = strstr(p, "\\n")) != NULL) {
        *p = '\n';
        memmove(p+1, p+2, strlen(p+2)+1);
    }
}

char *_get_indent_char_string(char *a_string) {
    // copied from baidu ai
    if (!a_string) {
        return strdup("");
    }
    
    char *start = a_string;
    while (*start) {
        if (*start != ' ' && *start != '\t') {
            break;
        }
        start++;
    }
    
    size_t indent_len = start - a_string;
    char *indent = malloc(indent_len + 1);
    if (!indent) {
        return strdup("");
    }
    
    strncpy(indent, a_string, indent_len);
    indent[indent_len] = '\0';
    return indent;
}

Type_Ypython_String *get_indent_string(Type_Ypython_String *a_string) {
    //indent_number = base_line->length - base_line->function_strip(base_line, Ypython_String(" "))->length;
    char *indent = _get_indent_char_string(a_string->value);
    Type_Ypython_String *the_indent = Ypython_String(indent);
    return the_indent;
}

Type_Ypython_String *get_code_block(Type_Ypython_List *lines_list, long long *line_index) {
    Type_Ypython_String *code_block = Ypython_String("");
    long long temp_index = *line_index + 1;
    long long indent_number = 0;
    if (temp_index < lines_list->length) {
        Type_Ypython_String *base_line = lines_list->function_get(lines_list, temp_index)->string_;
        indent_number = get_indent_string(base_line)->length;
        while (temp_index < lines_list->length) {
            Type_Ypython_String *temp_line = lines_list->function_get(lines_list, temp_index)->string_;
            long long new_indent_number = get_indent_string(temp_line)->length;
            Type_Ypython_String *pure_temp_line = temp_line->function_strip(temp_line, Ypython_String(" \n"));
            if ((!pure_temp_line->function_is_equal(pure_temp_line, Ypython_String(""))) && (new_indent_number < indent_number)) {
                break;
            }
            code_block = code_block->function_add(code_block, temp_line);
            code_block = code_block->function_add(code_block, Ypython_String("\n"));
            temp_index++;
        }
    }
    *line_index = temp_index - 1;
    return code_block;
}

// pre_define the process function
Type_Ypython_Element_Instance *process(Type_Ypython_String *text_code, Type_Ypython_Dict *variable_dict);

Type_Ypython_Element_Instance *handle_function_call(Type_Ypython_String *a_line, Type_Ypython_Dict *variable_dict) {
    Type_Ypython_List *part_list = ypython_string_type_function_split(a_line, Ypython_String("("));
    Type_Ypython_String *function_name = Ypython_String(part_list->function_get(part_list, 0)->string_->value);
    Type_Ypython_General *an_general_value = variable_dict->function_get(variable_dict, function_name);
    if (an_general_value != NULL && !an_general_value->is_none && an_general_value->anything_ != NULL) {
        
        Type_Ypython_General *function_body_general = (((Type_Ypython_Element_Instance*)(an_general_value->anything_))->_value);
        Type_Ypython_Dict *new_dict = Ypython_Dict();
        new_dict = _Ypython_dict_inheritance(variable_dict, new_dict);
        Type_Ypython_Element_Instance *the_return_element = process(function_body_general->string_, new_dict);
        return the_return_element;
    } else {
        Type_Ypython_String *error_message = Ypython_String(_ypython_string_format("Error: function '%s' can't get found in current variable content dict.", function_name->value));
        Type_Ypython_Element_Instance *result_element = Ypython_Element_Instance();
        result_element->_type = Ypython_String("error");
        result_element->_value->string_ = error_message;
        return result_element;
    }

    // return none by default
    Type_Ypython_Element_Instance *result_element = Ypython_Element_Instance();
    result_element->_type = Ypython_String("none");
    Type_Ypython_General *result_value = Ypython_General();
    result_value->is_none = true;
    result_element->_value = result_value;
    return result_element;
}

Type_Ypython_Element_Instance *convert_string_value_to_c_value(Type_Ypython_String *string_value, Type_Ypython_Dict *variable_dict) {
    // todo: you should rewrite this function by using char to char stream parsing technology, for example, when you meet [, you get all other char one by one until ]. You just have to make sure their are balanced, [], {}, (), "", ''.
    string_value = string_value->function_strip(string_value, Ypython_String(" "));

    Type_Ypython_Element_Instance *result_element = Ypython_Element_Instance();
    Type_Ypython_General *result_value = Ypython_General();

    if (string_value->function_is_equal(string_value, Ypython_String("None"))) {
        // none
        result_element->_type = Ypython_String("none");
        result_value->is_none = true;
    } else if (string_value->function_is_equal(string_value, Ypython_String("True"))) {
        // true
        result_element->_type = Ypython_String("bool");
        result_value->bool_ = Ypython_Bool(true);
    } else if (string_value->function_is_equal(string_value, Ypython_String("False"))) {
        // false
        result_element->_type = Ypython_String("bool");
        result_value->bool_ = Ypython_Bool(false);
    } else if (((string_value->function_startswith(string_value, Ypython_String("\""))) && (string_value->function_endswith(string_value, Ypython_String("\"")))) && (!string_value->function_is_substring(string_value, Ypython_String("\" + \"")))) {
        // string
        // debug: there may has many bugs, because anything can be found in a string, which causes bugs, for example '"a" == "b"' will be treated as a sting, which is wrong
        result_element->_type = Ypython_String("string");

        Type_Ypython_String *pure_value = string_value->function_substring(string_value, 1, string_value->length-1);
        result_value->string_ = pure_value;
        convert_escape_chars(result_value->string_->value);
    } else if (is_digital(string_value)) {
        if (string_value->function_is_substring(string_value, Ypython_String("."))) {
            // float
            result_element->_type = Ypython_String("float");
            result_value->float_ = Ypython_Float(_ypython_string_to_float(string_value->value));
        } else {
            // int
            result_element->_type = Ypython_String("int");
            result_value->int_ = Ypython_Int(_ypython_string_to_int(string_value->value));
        }
    } else if (string_value->length == 0) {
        // has no value
        result_element->_type = Ypython_String("ignore");
    } else if ((string_value->function_startswith(string_value, Ypython_String("["))) && (string_value->function_endswith(string_value, Ypython_String("]")))) {
        // list
        result_element->_type = Ypython_String("list");
        result_value->list_ = Ypython_List();
    } else if ((string_value->function_startswith(string_value, Ypython_String("{"))) && (string_value->function_endswith(string_value, Ypython_String("}")))) {
        // dict
        result_element->_type = Ypython_String("dict");
        result_value->dict_ = Ypython_Dict();
    } else if (string_value->function_is_substring(string_value, Ypython_String(" == "))) {
        // handle == case, should return a bool value
        result_element->_type = Ypython_String("bool");

        Type_Ypython_List *temp_list = ypython_string_type_function_split(string_value, Ypython_String(" == "));
        Type_Ypython_General *part_a = temp_list->function_get(temp_list, 0);
        Type_Ypython_General *part_b = temp_list->function_get(temp_list, 1);

        Type_Ypython_Element_Instance *element_a = convert_string_value_to_c_value(part_a->string_, variable_dict);
        Type_Ypython_Element_Instance *element_b = convert_string_value_to_c_value(part_b->string_, variable_dict);

        if (element_a->_value->function_is_equal(element_a->_value, element_b->_value)) {
            result_value->bool_ = Ypython_Bool(true);
        } else {
            result_value->bool_ = Ypython_Bool(false);
        }
    } else if (string_value->function_is_substring(string_value, Ypython_String(" != "))) {
        result_element->_type = Ypython_String("bool");

        Type_Ypython_List *temp_list = ypython_string_type_function_split(string_value, Ypython_String(" != "));
        Type_Ypython_General *part_a = temp_list->function_get(temp_list, 0);
        Type_Ypython_General *part_b = temp_list->function_get(temp_list, 1);

        Type_Ypython_Element_Instance *element_a = convert_string_value_to_c_value(part_a->string_, variable_dict);
        Type_Ypython_Element_Instance *element_b = convert_string_value_to_c_value(part_b->string_, variable_dict);

        if (!element_a->_value->function_is_equal(element_a->_value, element_b->_value)) {
            result_value->bool_ = Ypython_Bool(true);
        } else {
            result_value->bool_ = Ypython_Bool(false);
        }
    } else if (string_value->function_is_substring(string_value, Ypython_String(" + "))) {
        Type_Ypython_List *temp_list = ypython_string_type_function_split(string_value, Ypython_String(" + "));
        Type_Ypython_General *part_a = temp_list->function_get(temp_list, 0);
        Type_Ypython_General *part_b = temp_list->function_get(temp_list, 1);

        Type_Ypython_Element_Instance *element_a = convert_string_value_to_c_value(part_a->string_, variable_dict);
        Type_Ypython_Element_Instance *element_b = convert_string_value_to_c_value(part_b->string_, variable_dict);

        if (element_a->_type->function_is_equal(element_a->_type, Ypython_String("string"))) {
            result_element->_type = Ypython_String("string");
            result_value = ypython_create_a_general_variable(element_a->_value->string_->function_add(element_a->_value->string_, element_b->_value->string_));
        } else if (element_a->_type->function_is_equal(element_a->_type, Ypython_String("float"))) {
            result_element->_type = Ypython_String("float");
            result_value = ypython_create_a_general_variable(element_a->_value->float_->function_add(element_a->_value->float_, element_b->_value->float_));
        } else {
            result_element->_type = Ypython_String("int");
            result_value = ypython_create_a_general_variable(element_a->_value->int_->function_add(element_a->_value->int_, element_b->_value->int_));
        }
    } else if ((string_value->function_endswith(string_value, Ypython_String(")"))) && (!string_value->function_startswith(string_value, Ypython_String("(")))) {
        // it is a function call, we should let process() function to handle it
        return handle_function_call(string_value, variable_dict);
    } else {
        // error, it is not a valid python literal value, maybe it is a variable name
        Type_Ypython_General *an_general_value = variable_dict->function_get(variable_dict, string_value);
        if (an_general_value != NULL && !an_general_value->is_none && an_general_value->anything_ != NULL) {
            // it is a variable
            Type_Ypython_Element_Instance *an_element = (Type_Ypython_Element_Instance*)(an_general_value->anything_);
            result_value = an_element->_value;
        } else {
            // it is not a valid python literal value
            result_element->_type = Ypython_String("error");
            char *error_message = _ypython_string_format("Error: %s is not a valid python value.", string_value->value);
            result_value->string_ = Ypython_String(error_message);
        }
    }

    result_element->_value = result_value;
    return result_element;
}

Type_Ypython_Element_Instance *evaluate_code(Type_Ypython_String *string_value, Type_Ypython_Dict *variable_dict) {
    // it will handle any calculation in a line and that line should not contain = symbol
    // it is similar to eval() in python
    return convert_string_value_to_c_value(string_value, variable_dict);
}

Type_Ypython_Element_Instance *process(Type_Ypython_String *text_code, Type_Ypython_Dict *variable_dict) {
    Type_Ypython_List *lines_list = ypython_string_type_function_split(text_code, Ypython_String("\n"));
    long long line_index = 0;
    while (line_index < lines_list->length) {
        Type_Ypython_General *temp = lines_list->function_get(lines_list, line_index);
        if (!temp->is_none) {
            Type_Ypython_String *original_line = Ypython_String(temp->string_->value);
            Type_Ypython_String *a_line = Ypython_String(original_line->value);
            a_line = a_line->function_strip(a_line, Ypython_String("    \n"));

            if (a_line->function_startswith(a_line, Ypython_String("#"))) {
                // do nothing
            } else if (a_line->function_is_substring(a_line, Ypython_String(" = "))) {
                Type_Ypython_List *part_list = ypython_string_type_function_split(a_line, Ypython_String(" = "));
                Type_Ypython_General *variable_name = part_list->function_get(part_list, 0);
                Type_Ypython_General *variable_value = part_list->function_get(part_list, 1);
                
                // Set the value in the dictionary
                Type_Ypython_Element_Instance *an_element = evaluate_code(variable_value->string_, variable_dict);

                Type_Ypython_General *a_general_variable_that_can_hold_anything = Ypython_General();
                a_general_variable_that_can_hold_anything->anything_ = an_element;
                
                variable_dict->function_set(variable_dict, variable_name->string_, a_general_variable_that_can_hold_anything);
            } else if ((a_line->function_startswith(a_line, Ypython_String("print("))) && (a_line->function_endswith(a_line, Ypython_String(")")))) {
                Type_Ypython_String *variable_name = a_line->function_substring(a_line, 6, a_line->length-1);
                
                Type_Ypython_Element_Instance *the_value = evaluate_code(variable_name, variable_dict);
                if (!the_value->_type->function_is_equal(the_value->_type, Ypython_String("error"))) {
                    // normal literal value
                    ypython_print(the_value->_value);
                } else {
                    // variable not found
                    the_value->_value->string_ = Ypython_String(_ypython_string_format("Error: '%s' can't get found in current variable content dict.", variable_name->value));
                    //ypython_print(the_value->_value);
                    return the_value;
                }
            } else if (a_line->function_is_substring(a_line, Ypython_String("def "))) {
                // Handle function definition
                Type_Ypython_List *part_list = ypython_string_type_function_split(a_line, Ypython_String("def "));
                Type_Ypython_String *temp_string = part_list->function_get(part_list, 1)->string_;
                part_list = ypython_string_type_function_split(temp_string, Ypython_String("("));
                Type_Ypython_String *function_name = Ypython_String(part_list->function_get(part_list, 0)->string_->value);
                // Collect function body
                Type_Ypython_String *function_body = Ypython_String("");
                function_body = get_code_block(lines_list, &line_index);
                
                // Store function definition
                Type_Ypython_General *function_body_general = Ypython_General();
                function_body_general -> string_ = function_body;

                Type_Ypython_Element_Instance *an_element = Ypython_Element_Instance();
                an_element->_type = Ypython_String("function");
                an_element->_name = Ypython_String(function_name->value);
                an_element->_value = function_body_general;

                // save function arguments
                Type_Ypython_General *function_arguments_line = ypython_create_a_general_variable(a_line);
                an_element->_information_dict->function_set(an_element->_information_dict, Ypython_String("function_arguments_line"), function_arguments_line);

                variable_dict->function_set(variable_dict, function_name, ypython_create_a_general_variable(an_element));
            } else if ((a_line->function_endswith(a_line, Ypython_String(")"))) && (!a_line->function_startswith(a_line, Ypython_String("(")))) {
                // Handle function call
                Type_Ypython_Element_Instance *the_return_element = handle_function_call(a_line, variable_dict);
                if ((the_return_element != NULL) && (the_return_element->_type->function_is_equal(the_return_element->_type, Ypython_String("error")))) {
                    return the_return_element;
                }
            } else if (a_line->function_startswith(a_line, Ypython_String("try:"))) {
                // Handle try and except logic
                Type_Ypython_String *try_code_block = get_code_block(lines_list, &line_index);

                Type_Ypython_String *next_line = lines_list->function_get(lines_list, line_index + 1)->string_;
                next_line = next_line->function_strip(next_line, Ypython_String("    \n"));
                Type_Ypython_String *except_code_block = NULL;
                if (next_line->function_startswith(next_line, Ypython_String("except "))) {
                    line_index = line_index + 1;
                    except_code_block = get_code_block(lines_list, &line_index);
                }

                Type_Ypython_Element_Instance *the_return_value = process(try_code_block, variable_dict);
                if (the_return_value->_type->function_is_equal(the_return_value->_type, Ypython_String("error"))) {
                    //ypython_print(the_return_value->_value);
                    Type_Ypython_Element_Instance *the_return_value_2 = process(except_code_block, variable_dict);
                    if (the_return_value_2 != NULL) {
                        if (the_return_value_2->_type->function_is_equal(the_return_value_2->_type, Ypython_String("error"))) {
                            return the_return_value_2;
                        }
                    }
                }
            } else if (a_line->function_startswith(a_line, Ypython_String("if "))) {
                // Handle if code block
                Type_Ypython_String *if_line = Ypython_String(a_line->value);
                Type_Ypython_String *if_code_block = get_code_block(lines_list, &line_index);

                Type_Ypython_String *verifying = if_line->function_substring(if_line, 3, if_line->length-1);
                Type_Ypython_Element_Instance *verifying_element = evaluate_code(verifying, variable_dict);
                if (verifying_element->_type->function_is_equal(verifying_element->_type, Ypython_String("bool"))) {
                    if (verifying_element->_value->bool_->value == true) {
                        Type_Ypython_Element_Instance *the_return_value = process(if_code_block, variable_dict);
                        if (the_return_value->_type->function_is_equal(the_return_value->_type, Ypython_String("error"))) {
                            return the_return_value;
                        }
                        if (the_return_value->_type->function_is_equal(the_return_value->_type, Ypython_String("break"))) {
                            return the_return_value;
                        }
                    }
                }
            } else if (a_line->function_startswith(a_line, Ypython_String("while "))) {
                // Handle if code block
                Type_Ypython_String *while_line = Ypython_String(a_line->value);
                Type_Ypython_String *while_code_block = get_code_block(lines_list, &line_index);

                Type_Ypython_String *verifying = while_line->function_substring(while_line, 6, while_line->length-1);
                Type_Ypython_Element_Instance *verifying_element = evaluate_code(verifying, variable_dict);
                if (verifying_element->_type->function_is_equal(verifying_element->_type, Ypython_String("bool"))) {
                    while (verifying_element->_value->bool_->value == true) {
                        Type_Ypython_Element_Instance *the_return_value = process(while_code_block, variable_dict);
                        if (the_return_value->_type->function_is_equal(the_return_value->_type, Ypython_String("error"))) {
                            return the_return_value;
                        }
                        if (the_return_value->_type->function_is_equal(the_return_value->_type, Ypython_String("break"))) {
                            break;
                        }
                        verifying_element = evaluate_code(verifying, variable_dict);
                        if (!verifying_element->_type->function_is_equal(verifying_element->_type, Ypython_String("bool"))) {
                            // if the while check is not bool value, break the loop
                            break;
                        }
                    }
                }
            } else if (a_line->function_startswith(a_line, Ypython_String("return "))) {
                Type_Ypython_String *the_return_variable_name = a_line->function_substring(a_line, 7, a_line->length);

                Type_Ypython_Element_Instance *the_return_element = evaluate_code(the_return_variable_name, variable_dict);
                return the_return_element;
            } else if (a_line->function_is_equal(a_line, Ypython_String("break"))) {
                Type_Ypython_Element_Instance *result_element = Ypython_Element_Instance();
                result_element->_type = Ypython_String("break");
                return result_element;
            }

            line_index = line_index + 1;
        }
    }

    // return none by default
    Type_Ypython_Element_Instance *result_element = Ypython_Element_Instance();
    result_element->_type = Ypython_String("none");
    Type_Ypython_General *result_value = Ypython_General();
    result_value->is_none = true;
    result_element->_value = result_value;
    return result_element;
}

int main(int argument_number, char **argument_list) {
    // Initialize global dictionaries
    global_variable_dict = Ypython_Dict();
    Type_Ypython_List *built_in_functions = Ypython_List();
    built_in_functions->function_append(built_in_functions, ypython_create_a_general_variable(Ypython_String("type")));
    global_variable_dict->function_set(global_variable_dict, Ypython_String("__built_in_s__"), ypython_create_a_general_variable(built_in_functions));

    if (argument_number <= 1) {
        // work as an realtime intepreter console
        Type_Ypython_String *line = Ypython_String("");
        _ypython_print_formated_string(">> ");

        while (true) {
            char character;
            //_ypython_scan_formated_string("%c", &character);
            character = getc(stdin);

            if (character != '\n') {
                //printf("%c", character);
                char *character_string = malloc(sizeof(char) * 2);
                character_string[0] = character;
                character_string[1] = '\0';

                Type_Ypython_String *new_character = Ypython_String(character_string);
                line = line->function_add(line, new_character);
            } else {
                char *one_line_input = line -> value;

                char *one_line_command = malloc(sizeof(char) * 100);
                _ypython_string_format(one_line_command, "python3 -c 'print(%s)'", one_line_input);
                char *result = ypython_run_command(one_line_command);
                _ypython_print_formated_string(">> %s", result);

                line = Ypython_String("");
            }
        }
    } else {
        // parse a python file, and execute functions
        Type_Ypython_String *file_path = Ypython_String(argument_list[1]);

        if ((!ypython_disk_exists(file_path->value)) || (ypython_disk_is_folder(file_path->value))) {
            ypython_print(file_path);
            ypython_print(Ypython_String("Make sure your python file exists!"));
            exit(1);
        }

        FILE *a_file = _ypython_file_open(file_path->value, "r");
        if (a_file != NULL) {
            Type_Ypython_String *file_content = Ypython_String("");
            while (true) {
                if (_ypython_return_end_of_file_indicator_for_a_STREAM(a_file) == 1) {
                    break;
                };

                char character = _ypython_file_get_character(a_file);
                if ((character < 0) || (character >= 255)) {
                    // ignore non_ascii character
                    continue;
                }
                
                char *character_string = malloc(sizeof(char) * 2);
                character_string[0] = character;
                character_string[1] = '\0';
                Type_Ypython_String *new_character = Ypython_String(character_string);
                file_content = file_content->function_add(file_content, new_character);
            }

            Type_Ypython_Element_Instance *the_return_value = process(file_content, global_variable_dict);
            if (the_return_value != NULL) {
                if (the_return_value->_type->function_is_equal(the_return_value->_type, Ypython_String("error"))) {
                    ypython_print(the_return_value->_value);
                }
            }
        }
        _ypython_file_close(a_file);
    }

    return 0;
}
