#ifndef yingshaoxo_dynamic_c
#define yingshaoxo_dynamic_c

#include "./yingshaoxo_c_dict.h"
#include <stdio.h>
#include <stdlib.h>

/* this can not support those micro_controller that have less than 20kb memory. consider only use 'yingshaoxo_c_pins.h' to do remote control. */

/*
design logic: use local variable first, such as 'unsigned char string[32];'
*/
unsigned char yingshaoxo_dynamic_c_global_variable_dict[69] = { '\0' };

/*
level 0: never get changed, especially the function name and arguments and return type
*/
#include "./yingshaoxo_c_dict.h"

void yingshaoxo_dynamic_c_create_variable(unsigned char *variable_dict, unsigned char *variable_name, unsigned char *initial_value) {
    unsigned int variable_name_length = _yingshaoxo_dict_get_string_length(variable_name);
    unsigned char new_name[variable_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "v_", variable_name);
    yingshaoxo_dict_set_key_and_value(variable_dict, new_name, initial_value);
}

unsigned char *yingshaoxo_dynamic_c_get_variable_value(unsigned char *variable_dict, unsigned char *variable_name) {
    unsigned int variable_name_length = _yingshaoxo_dict_get_string_length(variable_name);
    unsigned char new_name[variable_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "v_", variable_name);

    int start_index;
    int end_index;
    int value_length;
    yingshaoxo_dict_get_value_by_key_2(variable_dict, new_name, &start_index, &end_index, &value_length);
    value_length += 2;
    unsigned char *default_return_value = malloc(value_length);
    yingshaoxo_dict_get_value_by_key(variable_dict, new_name, default_return_value);

    if (_yingshaoxo_dict_is_string_equal(default_return_value, "") == 1) {
        _yingshaoxo_dict_string_memory_copy(default_return_value, "None");
    }

    return default_return_value;
}

void yingshaoxo_dynamic_c_create_function(unsigned char *variable_dict, unsigned char *function_name, unsigned char *arguments, unsigned char *function_code) {
    unsigned int function_name_length = _yingshaoxo_dict_get_string_length(function_name);
    unsigned char new_name[function_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "f_", function_name);

    unsigned int arguments_length = _yingshaoxo_dict_get_string_length(arguments);
    unsigned int function_code_length = _yingshaoxo_dict_get_string_length(function_code);
    unsigned char new_value[arguments_length+function_code_length+3];
    _yingshaoxo_dict_add_string(new_value, arguments, ";\n");
    _yingshaoxo_dict_add_string(new_value, new_value, function_code);

    yingshaoxo_dict_set_key_and_value(variable_dict, new_name, new_value);
}

void yingshaoxo_dynamic_c_remove_variable(unsigned char *variable_dict, unsigned char *variable_name) {
    unsigned int variable_name_length = _yingshaoxo_dict_get_string_length(variable_name);
    unsigned char new_name[variable_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "v_", variable_name);
    yingshaoxo_dict_delete_a_key(variable_dict, new_name);
    _yingshaoxo_dict_add_string(new_name, "f_", variable_name);
    yingshaoxo_dict_delete_a_key(variable_dict, new_name);
}

void _yingshaoxo_dynamic_c_float_to_string(float a_number, unsigned char *a_string) {
    /* to baidu deepseek r1 ai: '-1.82' or '8.22' or '876' can be the input. do not use stdio.h or stdlib.h or string.h. a_string have most 30 length, you can end with '\0'. just use the 'unsigned char *a_string' with pure c89 syntax. */

    if (a_number == 0.0f) {
        a_string[0] = '0';
        a_string[1] = '\0';
        return;
    }
    /* Temporary pointer for output position */
    unsigned char *p = a_string;
    int is_negative = 0;
    float abs_value = a_number;
    /* Process negative numbers */
    if (a_number < 0) {
        is_negative = 1;
        abs_value = -a_number;
        *p++ = '-';
    }
    /* Extract integer and fractional parts */
    unsigned int integer_part = (unsigned int)abs_value;
    float fractional = abs_value - (float)integer_part;
    /* Buffer for integer digits (max 12 digits for 4-byte float) */
    unsigned char int_buf[12];
    unsigned char *int_ptr = int_buf;
    int int_len = 0;
    /* Convert integer part to string (reverse order) */
    if (integer_part == 0) {
        *int_ptr++ = '0';
        int_len++;
    } else {
        while (integer_part > 0) {
            *int_ptr++ = '0' + (integer_part % 10);
            integer_part /= 10;
            int_len++;
        }
    }
    /* Reverse integer digits into output */
    unsigned char *rev_ptr = int_ptr - 1;
    int i = 0;
    for (i; i < int_len; i++) {
        *p++ = *rev_ptr--;
    }
    /* Process fractional part if exists */
    if (fractional > 1e-6f) {
        *p++ = '.';  /* Add decimal point */
        /* Convert fractional part (max 6 digits) */
        fractional += 0.5e-6f;  /* Rounding adjustment */
        int i = 0;
        for (i; i < 3; i++) {
            fractional *= 10.0f;
            int digit = (int)fractional;
            *p++ = '0' + digit;
            fractional -= (float)digit;
            if (fractional < 1e-6f) break;  /* Stop when remainder is negligible */
        }
    }
    /* Null-terminate the string */
    *p = '\0';
}

float _yingshaoxo_dynamic_c_string_to_float(unsigned char *a_string) {
    /* to baidu deepseek r1 ai: '-1.82' or '8.22' or '876' can be the input. do not use stdio.h or stdlib.h or string.h, just use the 'unsigned char *a_string' with pure c89 syntax. */

    /* Use temporary pointer to preserve original index */
    unsigned char *p = a_string;
    float sign = 1.0f;
    float integer_part = 0.0f;
    float fractional_part = 0.0f;
    float fractional_divisor = 10.0f;
    int has_decimal_point = 0;
    /* Skip leading spaces with temporary pointer */
    while (*p == ' ') p++;
    /* Handle sign using temp pointer */
    if (*p == '-') {
        sign = -1.0f;
        p++;
    } else if (*p == '+') {
        p++;
    }
    /* Process integer part */
    while (*p >= '0' && *p <= '9') {
        integer_part = integer_part * 10.0f + (float)(*p - '0');
        p++;
    }
    /* Check decimal point */
    if (*p == '.') {
        has_decimal_point = 1;
        p++;
    }
    /* Process fractional part */
    while (*p >= '0' && *p <= '9') {
        fractional_part += (float)(*p - '0') / fractional_divisor;
        fractional_divisor *= 10.0f;
        p++;
    }
    /* Combine results (original a_string remains unchanged) */
    return sign * (integer_part + fractional_part);
}

/*
level 1: could get changed
*/
unsigned int _yingshaoxo_dynamic_c_is_it_a_string(unsigned char *code) {
    if (code[0] == '\0') {
        return 0;
    }
    if (code[0] == '\'') {
        return 1;
    }
    if (code[0] == '"') {
        return 1;
    }
    if (code[0] == '`') {
        return 1;
    }
    return 0;
}

int _yingshaoxo_dynamic_c_parsing_string(unsigned char *code) {
    if (code[0] == '\0') {
        return -1;
    }
    unsigned char it_is_string = '\0';
    if (code[0] == '\'') {
        it_is_string = '\'';
    }
    if (code[0] == '"') {
        it_is_string = '"';
    }
    if (code[0] == '`') {
        it_is_string = '`';
    }
    unsigned int string_end_index = 0;
    if (it_is_string != '\0') {
        /* a const string */
        unsigned char next_punctuation[2] = { it_is_string, '\0' };
        string_end_index = _yingshaoxo_dict_find_sub_string(&code[1], next_punctuation) + 1 + 1;
        return string_end_index;
    } else {
        /* something else */
        return -1;
    }
}

void _yingshaoxo_dynamic_c_remove_string_quote(unsigned char *a_string) {
    if ((a_string[0] == '`') || (a_string[0] == '\'') || (a_string[0] == '"')) {
        _yingshaoxo_dict_string_memory_copy(a_string, &a_string[1]);
        a_string[_yingshaoxo_dict_get_string_length(a_string)-1] = '\0';
    }
}

void _yingshaoxo_dynamic_c_add_string_quote(unsigned char *a_string_that_has_2_more_space) {
    unsigned char temp_string[_yingshaoxo_dict_get_string_length(a_string_that_has_2_more_space) + 3];
    _yingshaoxo_dict_add_string(temp_string, "'", a_string_that_has_2_more_space);
    _yingshaoxo_dict_add_string(temp_string, temp_string, "'");
    _yingshaoxo_dict_string_memory_copy(a_string_that_has_2_more_space, temp_string);
}

unsigned int _yingshaoxo_dynamic_c_is_it_a_list(unsigned char *code) {
    if (code[0] == '[') {
        return 1;
    }
    return 0;
}

unsigned int _yingshaoxo_dynamic_c_is_it_a_dict(unsigned char *code) {
    if (code[0] == '{') {
        return 1;
    }
    return 0;
}

unsigned int _yingshaoxo_dynamic_c_is_it_a_tuple(unsigned char *code) {
    if (code[0] == '(') {
        return 1;
    }
    return 0;
}

unsigned int _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(unsigned char *code, unsigned char start_symbol, unsigned char end_symbol) {
    unsigned int start_counting = 0;
    unsigned int end_counting = 0;
    unsigned int index = 0;
    while (1) {
        if (code[index] == '\0') {
            break;
        }
        if (code[index] == start_symbol) {
            start_counting += 1;
        }
        if (code[index] == end_symbol) {
            end_counting += 1;
        }
        if ((end_counting != 0) && (start_counting == end_counting)) {
            break;
        }
        index += 1;
    }
    return index;
}

unsigned char _yingshaoxo_dynamic_c_operator_characters[10] = { '+', '-', '/', '*', '>', '<', '=', ' ', ';' };
unsigned int _yingshaoxo_dynamic_c_get_variable_end_index(unsigned char *the_code) {
    if (the_code[0] == '\0') {
        return 0;
    }
    int index = 0;
    int temp_index = 0;
    while (1) {
        if (the_code[index] == '\0') {
            break;
        }

        unsigned char *code = &the_code[index];
        if (_yingshaoxo_dynamic_c_is_it_a_string(code)) {
            /*a string*/
            temp_index = _yingshaoxo_dynamic_c_parsing_string(code);
            if (temp_index == -1) {
                temp_index = 0;
            }
        } else if (_yingshaoxo_dynamic_c_is_it_a_list(code)) {
            /*a list*/
            temp_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '[', ']');
        } else if (_yingshaoxo_dynamic_c_is_it_a_dict(code)) {
            /*a dict*/
            temp_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
        } else if (_yingshaoxo_dynamic_c_is_it_a_tuple(code)) {
            /*a tuple*/
            temp_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '(', ')');
        } else {
            /*variable name*/
            temp_index = 0;
        }
        index += temp_index;

        unsigned int i = 0;
        while (i <= 9) {
            if (the_code[index] == _yingshaoxo_dynamic_c_operator_characters[i]) {
                return index;
            }
            i += 1;
        }
        index += 1;
    }
    return index;
}

unsigned int _yingshaoxo_dynamic_c_is_it_a_number(unsigned char *code) {
    if (code[0] == '\0') {
        return 0;
    }
    if ((code[0] >= '0') && (code[0] <= '9')) {
        return 1;
    }
    if ((code[0] == '-') && (code[1] >= '0') && (code[1] <= '9')) {
        return 1;
    }
    return 0;
}

unsigned int _yingshaoxo_dynamic_c_is_it_a_function_call(unsigned char *code) {
    if (_yingshaoxo_dict_find_sub_string(code, "(") != -1) {
        if (_yingshaoxo_dict_find_sub_string(code, ")") != -1) {
            if (_yingshaoxo_dynamic_c_is_it_a_string(code) == 0) {
                return 1;
            }
        }
    }
    return 0;
}

void _yingshaoxo_dynamic_c_replace_list_quote(unsigned char *a_string) {
    if (a_string[0] == '[') {
        a_string[0] = ',';
        a_string[_yingshaoxo_dict_get_string_length(a_string)-1] = ',';
    }
}

void _yingshaoxo_dynamic_c_recover_list_quote(unsigned char *a_string) {
    if (a_string[0] == ',') {
        a_string[0] = '[';
        a_string[_yingshaoxo_dict_get_string_length(a_string)-1] = ']';
    }
}

unsigned int _yingshaoxo_dynamic_c_is_it_assignment(unsigned char *code) {
    unsigned int the_equal_symbol_index = _yingshaoxo_dict_find_sub_string(code, "=");
    if (the_equal_symbol_index != -1) {
        if ((the_equal_symbol_index-1) >= 0) {
            if (code[the_equal_symbol_index-1] == '+') {
                return 2;
            } else if (code[the_equal_symbol_index-1] == '-') {
                return 2;
            } else if (code[the_equal_symbol_index-1] == '*') {
                return 2;
            } else if (code[the_equal_symbol_index-1] == '/') {
                return 2;
            } else {
                return 1;
            }
        }
    }
    return 0;
}

unsigned int _yingshaoxo_dynamic_c_is_it_list_or_dict_element_access(unsigned char *code) {
    if (_yingshaoxo_dict_find_sub_string(code, "[") != -1) {
        if (_yingshaoxo_dict_find_sub_string(code, "]") != -1) {
            if (_yingshaoxo_dynamic_c_is_it_a_string(code) == 0) {
                return 1;
            }
        }
    }
    return 0;
}

/*
level 2: change quickly
*/
/*pre_defined name*/
unsigned char *yingshaoxo_dynamic_c_evaluate(unsigned char *variable_dict, unsigned char *code);
unsigned char *_yingshaoxo_dynamic_c_evaluate_3_instance(unsigned char *variable_dict, unsigned char *code);
unsigned char *yingshaoxo_dynamic_c_c_runner(unsigned char *variable_dict, unsigned char *code_string);

/*others*/
unsigned char *_yingshaoxo_dynamic_c_call_class_function(unsigned char *variable_dict, unsigned char *class_instance_name, unsigned char *function_name, unsigned char *arguments) {
    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';
    
    unsigned char *real_value_of_the_instance = yingshaoxo_dynamic_c_evaluate(variable_dict, class_instance_name);
    unsigned int real_value_length = _yingshaoxo_dict_get_string_length(real_value_of_the_instance);
    
    if (_yingshaoxo_dynamic_c_is_it_a_string(real_value_of_the_instance)) {
        /* handle string functions */
        if (_yingshaoxo_dict_is_string_equal(function_name, "strip") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(real_value_of_the_instance);
            _yingshaoxo_dict_string_strip(real_value_of_the_instance);
            _yingshaoxo_dynamic_c_add_string_quote(real_value_of_the_instance);
            free(default_return_value);
            default_return_value = real_value_of_the_instance;
        } else if (_yingshaoxo_dict_is_string_equal(function_name, "split") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(real_value_of_the_instance);
            _yingshaoxo_dynamic_c_remove_string_quote(arguments);
            if (_yingshaoxo_dict_find_sub_string(real_value_of_the_instance, arguments) == -1) {
                unsigned char *final_result = malloc(real_value_length+4);
                _yingshaoxo_dict_string_memory_copy(final_result, real_value_of_the_instance);
                _yingshaoxo_dynamic_c_add_string_quote(final_result);
                _yingshaoxo_dynamic_c_add_string_quote(final_result);
                final_result[0] = '[';
                final_result[_yingshaoxo_dict_get_string_length(final_result)-1] = ']';
                free(default_return_value);
                default_return_value = final_result;
            } else {
                unsigned char *final_result = malloc(real_value_length*3 + 3);
                unsigned char *temp_variable_1 = malloc(real_value_length*3 + 3);
                int value_length = _yingshaoxo_dict_get_string_length(real_value_of_the_instance);
                int arguments_length = _yingshaoxo_dict_get_string_length(arguments);
                _yingshaoxo_dict_add_string(final_result, "[", "");
                int index = 0;
                while (1) {
                    int found_index = _yingshaoxo_dict_find_sub_string(&real_value_of_the_instance[index], arguments);
                    if (found_index == -1) {
                        _yingshaoxo_dict_get_sub_string(real_value_of_the_instance, index, value_length, temp_variable_1);
                        _yingshaoxo_dynamic_c_add_string_quote(temp_variable_1);
                        _yingshaoxo_dict_add_string(final_result, final_result, temp_variable_1);
                        _yingshaoxo_dict_add_string(final_result, final_result, ",");
                        break;
                    }
                    _yingshaoxo_dict_get_sub_string(real_value_of_the_instance, index, index+found_index, temp_variable_1);
                    _yingshaoxo_dynamic_c_add_string_quote(temp_variable_1);
                    _yingshaoxo_dict_add_string(final_result, final_result, temp_variable_1);
                    _yingshaoxo_dict_add_string(final_result, final_result, ",");
                    index += found_index + arguments_length;
                }
                final_result[_yingshaoxo_dict_get_string_length(final_result)-1] = ']';
                free(default_return_value);
                default_return_value = final_result;
            }
        }
    } else if (_yingshaoxo_dynamic_c_is_it_a_list(real_value_of_the_instance)) {
        /* handle list functions */
        unsigned int arguments_length = _yingshaoxo_dict_get_string_length(arguments);
        if (_yingshaoxo_dict_is_string_equal(function_name, "append") == 1) {
            unsigned char final_result[real_value_length + arguments_length + 2];
            unsigned char temp_variable_1[real_value_length + arguments_length + 2];
            unsigned char temp_variable_2[real_value_length + arguments_length + 2];
            if ((real_value_of_the_instance[0] == '[') && (real_value_of_the_instance[1] == ']')) {
                /* empty list */
                _yingshaoxo_dict_add_string(final_result, "[", arguments);
                _yingshaoxo_dict_add_string(final_result, final_result, "]");
            } else {
                /* has element list */
                real_value_of_the_instance[real_value_length-1] = '\0';
                _yingshaoxo_dict_add_string(final_result, real_value_of_the_instance, ",");
                _yingshaoxo_dict_add_string(final_result, final_result, arguments);
                _yingshaoxo_dict_add_string(final_result, final_result, "]");
            }
            yingshaoxo_dynamic_c_create_variable(variable_dict, class_instance_name, final_result);
            free(real_value_of_the_instance);
        }
    }

    return default_return_value;
}

unsigned char *yingshaoxo_dynamic_c_call_function(unsigned char *variable_dict, unsigned char *function_name, unsigned char *arguments) {
    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';
    
    if (_yingshaoxo_dict_is_string_equal(function_name, "print") == 1) {
        unsigned char *real_value = yingshaoxo_dynamic_c_evaluate(variable_dict, arguments);
        printf("%s\n", real_value);
        free(real_value);
        return default_return_value;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "free") == 1) {
        yingshaoxo_dynamic_c_remove_variable(variable_dict, arguments);
        return default_return_value;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "len") == 1) {
        unsigned int the_string_length = _yingshaoxo_dict_get_string_length(arguments);
        if ((the_string_length-2) >= 0) {
            the_string_length -= 2;
        }
        free(default_return_value);
        default_return_value = malloc(10);
        _yingshaoxo_dynamic_c_float_to_string(the_string_length, default_return_value);
        return default_return_value;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "str") == 1) {
        free(default_return_value);
        unsigned char *real_value = yingshaoxo_dynamic_c_evaluate(variable_dict, arguments);
        unsigned int the_string_length = _yingshaoxo_dict_get_string_length(real_value);
        if (_yingshaoxo_dynamic_c_is_it_a_string(real_value) == 1) {
            return real_value;
        } else {
            unsigned char *new_value = malloc(the_string_length + 3);
            _yingshaoxo_dict_string_memory_copy(new_value, real_value);
            free(real_value);
            _yingshaoxo_dynamic_c_add_string_quote(new_value);
            return new_value;
        }
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "not") == 1) {
        free(default_return_value);
        unsigned char *real_value = yingshaoxo_dynamic_c_evaluate(variable_dict, arguments);
        if (_yingshaoxo_dict_is_string_equal(real_value, "0") == 1) {
            _yingshaoxo_dict_string_memory_copy(real_value, "1");
        } else {
            _yingshaoxo_dict_string_memory_copy(real_value, "0");
        }
        return real_value;
    }

    unsigned int function_name_length = _yingshaoxo_dict_get_string_length(function_name);
    unsigned char new_name[function_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "f_", function_name);

    int start_index;
    int end_index;
    int value_length;
    yingshaoxo_dict_get_value_by_key_2(variable_dict, new_name, &start_index, &end_index, &value_length);
    unsigned char code_block[value_length];
    yingshaoxo_dict_get_value_by_key(variable_dict, new_name, code_block);

    unsigned char *result_value = yingshaoxo_dynamic_c_c_runner(variable_dict, code_block);
    free(default_return_value);
    return result_value;
}

unsigned char *_yingshaoxo_dynamic_c_parse_and_call_function(unsigned char *variable_dict, unsigned char *code) {
    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';

    unsigned int function_argument_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int function_argument_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '(', ')');


    unsigned char function_name[function_argument_start_index+1];
    unsigned char arguments[(function_argument_end_index-function_argument_start_index)+1];
    _yingshaoxo_dict_get_sub_string(code, 0, function_argument_start_index, function_name);
    _yingshaoxo_dict_string_strip(function_name);
    _yingshaoxo_dict_get_sub_string(code, function_argument_start_index+1, function_argument_end_index, arguments);
    _yingshaoxo_dict_string_strip(arguments);

    unsigned char *real_arguments = yingshaoxo_dynamic_c_evaluate(variable_dict, arguments);

    if (_yingshaoxo_dict_find_sub_string(function_name, ".") != -1) {
        /*dot property function access*/
        unsigned int class_instance_name_end_index = _yingshaoxo_dict_find_sub_string(code, ".");
        unsigned char class_instance_name[class_instance_name_end_index+1];
        _yingshaoxo_dict_get_sub_string(code, 0, class_instance_name_end_index, class_instance_name);
        _yingshaoxo_dict_get_sub_string(code, class_instance_name_end_index+1, function_argument_start_index, function_name);
        free(default_return_value);
        default_return_value = _yingshaoxo_dynamic_c_call_class_function(variable_dict, class_instance_name, function_name, real_arguments);
    } else {
        /*normal function access*/
        free(default_return_value);
        default_return_value = yingshaoxo_dynamic_c_call_function(variable_dict, function_name, real_arguments);
    }

    free(real_arguments);
    return default_return_value;
}

unsigned char *_yingshaoxo_dynamic_c_parse_and_get_list_or_dict_element(unsigned char *variable_dict, unsigned char *code) {
    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';

    unsigned int element_index_start_index = _yingshaoxo_dict_find_sub_string(code, "[");
    unsigned int element_index_end_index = _yingshaoxo_dict_find_sub_string(code, "]");

    unsigned char variable_name[element_index_start_index+1];
    unsigned char index_string[(element_index_end_index-element_index_start_index)+1];
    _yingshaoxo_dict_get_sub_string(code, 0, element_index_start_index, variable_name);
    _yingshaoxo_dict_string_strip(variable_name);
    _yingshaoxo_dict_get_sub_string(code, element_index_start_index+1, element_index_end_index, index_string);
    _yingshaoxo_dict_string_strip(index_string);
    unsigned char *real_variable_value = yingshaoxo_dynamic_c_evaluate(variable_dict, variable_name);
    unsigned int real_variable_value_length = _yingshaoxo_dict_get_string_length(real_variable_value);

    if (_yingshaoxo_dynamic_c_is_it_a_list(real_variable_value)) {
        /*a_list*/
        /*maybe we can simply replace ',' and ':' to some unused ascii code*/
        /*or simply remix yingshaoxo_dict.h, so we can reuse it by change splitor*/
        if (_yingshaoxo_dict_find_sub_string(index_string, ":") == -1) {
            /* list single element access */
            int the_index = (int)_yingshaoxo_dynamic_c_string_to_float(index_string);

            _yingshaoxo_dynamic_c_replace_list_quote(real_variable_value);
            int last_found_index = 0;
            int temp_index = 0;
            int all_index = 0;
            int index = 0;
            while (1) {
                temp_index = _yingshaoxo_dict_find_sub_string(&real_variable_value[all_index], ",");
                if (temp_index == -1) {
                    break;
                }
                all_index += temp_index+1;
                if (index == (the_index+1)) {
                    all_index -= 1;
                    break;
                }
                last_found_index = all_index - 1;
                index += 1;
            }
            if (all_index != -1) {
                unsigned char *real_data = malloc(real_variable_value_length+1);
                _yingshaoxo_dict_get_sub_string(real_variable_value, last_found_index+1, all_index, real_data);
                free(default_return_value);
                default_return_value = real_data;
            }
        } else {
            /* list slice access */
            print(index_string);
        }
    } else if (_yingshaoxo_dynamic_c_is_it_a_dict(real_variable_value)) {
        /*a_dict*/
        unsigned char starting_key[real_variable_value_length+2];
        _yingshaoxo_dict_add_string(starting_key, index_string, ":");
        int starting_key_length = _yingshaoxo_dict_get_string_length(starting_key);
        int temp_index = _yingshaoxo_dict_find_sub_string(real_variable_value, starting_key);
        if (temp_index != -1) {
            int end_index = _yingshaoxo_dict_find_sub_string(&real_variable_value[temp_index+starting_key_length], ",");
            if (end_index == -1) {
                end_index = _yingshaoxo_dict_find_sub_string(&real_variable_value[temp_index+starting_key_length], "}");
            }
            if (end_index != -1) {
                unsigned char *real_data = malloc(real_variable_value_length+1);
                _yingshaoxo_dict_get_sub_string(&real_variable_value[temp_index+starting_key_length], 0, end_index, real_data);
                free(default_return_value);
                default_return_value = real_data;
            }
        }
    }

    free(real_variable_value);
    return default_return_value;
}

unsigned char *_yingshaoxo_dynamic_c_parse_and_set_list_or_dict_element(unsigned char *variable_dict, unsigned char *code, unsigned char *new_value) {
    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';

    unsigned int element_index_start_index = _yingshaoxo_dict_find_sub_string(code, "[");
    unsigned int element_index_end_index = _yingshaoxo_dict_find_sub_string(code, "]");

    unsigned char variable_name[element_index_start_index+1];
    unsigned char index_string[(element_index_end_index-element_index_start_index)+1];
    _yingshaoxo_dict_get_sub_string(code, 0, element_index_start_index, variable_name);
    _yingshaoxo_dict_string_strip(variable_name);
    _yingshaoxo_dict_get_sub_string(code, element_index_start_index+1, element_index_end_index, index_string);
    _yingshaoxo_dict_string_strip(index_string);

    unsigned char *real_variable_value = yingshaoxo_dynamic_c_evaluate(variable_dict, variable_name);
    unsigned int real_variable_value_length = _yingshaoxo_dict_get_string_length(real_variable_value);

    unsigned int new_value_length = _yingshaoxo_dict_get_string_length(new_value);
    unsigned char *final_data = malloc(real_variable_value_length+1+new_value_length);
    unsigned char *temp_data_1 = malloc(real_variable_value_length+1+new_value_length);
    unsigned char *temp_data_2 = malloc(real_variable_value_length+1+new_value_length);
    if (_yingshaoxo_dynamic_c_is_it_a_list(real_variable_value)) {
        /*a_list*/
        /*maybe we can simply replace ',' and ':' to some unused ascii code*/
        /*or simply remix yingshaoxo_dict.h, so we can reuse it by change splitor*/
        int the_index = (int)_yingshaoxo_dynamic_c_string_to_float(index_string);

        _yingshaoxo_dynamic_c_replace_list_quote(real_variable_value);
        int last_found_index = 0;
        int temp_index = 0;
        int all_index = 0;
        int index = 0;
        while (1) {
            temp_index = _yingshaoxo_dict_find_sub_string(&real_variable_value[all_index], ",");
            if (temp_index == -1) {
                break;
            }
            all_index += temp_index+1;
            if (index == (the_index+1)) {
                all_index -= 1;
                break;
            }
            last_found_index = all_index - 1;
            index += 1;
        }
        if (all_index != -1) {
            _yingshaoxo_dict_get_sub_string(real_variable_value, 0, last_found_index+1, temp_data_1);
            unsigned int string_end_index = _yingshaoxo_dict_get_string_length(real_variable_value);
            _yingshaoxo_dict_get_sub_string(real_variable_value, all_index, string_end_index, temp_data_2);
            _yingshaoxo_dict_add_string(final_data, temp_data_1, new_value);
            _yingshaoxo_dict_add_string(final_data, final_data, temp_data_2);
            _yingshaoxo_dynamic_c_recover_list_quote(final_data);
            yingshaoxo_dynamic_c_create_variable(variable_dict, variable_name, final_data);
        }
    } else if (_yingshaoxo_dynamic_c_is_it_a_dict(real_variable_value)) {
        /*a_dict*/
        unsigned char starting_key[real_variable_value_length+2];
        _yingshaoxo_dict_add_string(starting_key, index_string, ":");
        int starting_key_length = _yingshaoxo_dict_get_string_length(starting_key);
        int temp_index = _yingshaoxo_dict_find_sub_string(real_variable_value, starting_key);
        if (temp_index != -1) {
            int end_index = _yingshaoxo_dict_find_sub_string(&real_variable_value[temp_index+starting_key_length], ",");
            if (end_index == -1) {
                end_index = _yingshaoxo_dict_find_sub_string(&real_variable_value[temp_index+starting_key_length], "}");
            }
            if (end_index != -1) {
                _yingshaoxo_dict_get_sub_string(real_variable_value, 0, temp_index+starting_key_length, temp_data_1);
                unsigned int string_end_index = _yingshaoxo_dict_get_string_length(&real_variable_value[temp_index+starting_key_length]);
                _yingshaoxo_dict_get_sub_string(&real_variable_value[temp_index+starting_key_length], end_index, string_end_index, temp_data_2);
                _yingshaoxo_dict_add_string(final_data, temp_data_1, new_value);
                _yingshaoxo_dict_add_string(final_data, final_data, temp_data_2);
                yingshaoxo_dynamic_c_create_variable(variable_dict, variable_name, final_data);
            }
        }
    }

    free(real_variable_value);
    return default_return_value;
}

/*
// a = [1,2,3]
// a[0]
// aa = " ok  "
// aa.strip()
// b = {'a': 2}
// b['a']
// b['a'] = 3
// len(`hi`)
// a_list = "a b c".split(" ")
//
// a_list[:1]
// a = 1 + 1
// c = a[0] + b['a']
// d = 'hello' 
// d[2]
// a += 1
*/

unsigned char *yingshaoxo_dynamic_c_evaluate(unsigned char *variable_dict, unsigned char *code) {
    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';

    unsigned int code_length = _yingshaoxo_dict_get_string_length(code);
    unsigned int first_instance_end_index = _yingshaoxo_dynamic_c_get_variable_end_index(code);

    if (first_instance_end_index == code_length) {
        /*one instance*/
        free(default_return_value);
        unsigned char *temp_variable = malloc(code_length+2);
        if ((first_instance_end_index >= 4) && (code[0] == 'N') && (code[3] == 'e')) {
            /*None*/
            _yingshaoxo_dict_string_memory_copy(temp_variable, code);
            return temp_variable;
        } else if (_yingshaoxo_dynamic_c_is_it_a_number(code)) {
            /*pure number*/
            _yingshaoxo_dict_string_memory_copy(temp_variable, code);
            return temp_variable;
        } else if (_yingshaoxo_dynamic_c_is_it_a_string(code)) {
            /*pure string*/
            _yingshaoxo_dict_string_memory_copy(temp_variable, code);
            return temp_variable;
        } else if (_yingshaoxo_dynamic_c_is_it_a_list(code)) {
            /*pure list*/
            _yingshaoxo_dict_string_memory_copy(temp_variable, code);
            return temp_variable;
        } else if (_yingshaoxo_dynamic_c_is_it_a_dict(code)) {
            /*pure dict*/
            _yingshaoxo_dict_string_memory_copy(temp_variable, code);
            return temp_variable;
        } else if (_yingshaoxo_dynamic_c_is_it_a_function_call(code)) {
            /*function call*/
            free(temp_variable);
            return _yingshaoxo_dynamic_c_parse_and_call_function(variable_dict, code);
        } else if (_yingshaoxo_dynamic_c_is_it_list_or_dict_element_access(code)) {
            /*list or dict element access*/
            free(temp_variable);
            return _yingshaoxo_dynamic_c_parse_and_get_list_or_dict_element(variable_dict, code);
        } else {
            /*a variable*/
            free(temp_variable);
            unsigned char *real_value = yingshaoxo_dynamic_c_get_variable_value(variable_dict, code);
            return real_value;
        }
    } else {
        /*
        // multiple instances
        // has operators like +,-,*,/
        */
        return _yingshaoxo_dynamic_c_evaluate_3_instance(variable_dict, code);
    }
    return default_return_value;
}

unsigned char *_yingshaoxo_dynamic_c_evaluate_3_instance(unsigned char *variable_dict, unsigned char *code) {
    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';

    if (code[0] == '\0') {
        return default_return_value;
    }

    unsigned int code_length = _yingshaoxo_dict_get_string_length(code);
    unsigned int index = 0;

    unsigned int first_instance_end_index = _yingshaoxo_dynamic_c_get_variable_end_index(code);
    unsigned char original_variable_1_name[first_instance_end_index+2];
    _yingshaoxo_dict_get_sub_string(code, 0, first_instance_end_index, original_variable_1_name);
    _yingshaoxo_dict_string_strip(original_variable_1_name);

    unsigned char *temp_variable_1 = yingshaoxo_dynamic_c_evaluate(variable_dict, original_variable_1_name);
    index += first_instance_end_index;

    /* skip space */
    while (1) {
        if (code[index] != ' ') {
            break;
        }
        index += 1;
    }

    unsigned char operator[3] = "==";
    if (_yingshaoxo_dict_string_starts_with(&code[index], "==") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "==");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "!=") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "!=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], ">=") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, ">=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "<=") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "<=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "+=") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "+=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "-=") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "-=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], ">") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, ">");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "<") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "<");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "+") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "+");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "-") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "-");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "*") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "*");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "/") == 1) {
        _yingshaoxo_dict_string_memory_copy(operator, "/");
        index += 1;
    } else {
        free(default_return_value);
        return temp_variable_1;
    }

    /* skip space */
    while (1) {
        if (code[index] != ' ') {
            break;
        }
        index += 1;
    }

    unsigned int second_instance_end_index = _yingshaoxo_dynamic_c_get_variable_end_index(&code[index]);
    unsigned char original_variable_2_name[second_instance_end_index+2];
    _yingshaoxo_dict_get_sub_string(&code[index], 0, second_instance_end_index, original_variable_2_name);
    _yingshaoxo_dict_string_strip(original_variable_2_name);

    unsigned char *temp_variable_2 = yingshaoxo_dynamic_c_evaluate(variable_dict, original_variable_2_name);
    index += second_instance_end_index;

    free(default_return_value);
    unsigned int possible_max_length = _yingshaoxo_dict_get_string_length(temp_variable_1) + _yingshaoxo_dict_get_string_length(temp_variable_2) + 4;
    unsigned char *return_value = malloc(possible_max_length);

    /* handle operations */
    if ((_yingshaoxo_dynamic_c_is_it_a_string(temp_variable_1)==1) && ((_yingshaoxo_dynamic_c_is_it_a_string(temp_variable_2)==1))) {
        /* handle string operations */
        if (_yingshaoxo_dict_is_string_equal(operator, "+") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_2);

            _yingshaoxo_dict_add_string(return_value, temp_variable_1, temp_variable_2);
            _yingshaoxo_dynamic_c_add_string_quote(return_value);
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "==") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_2);
            if (_yingshaoxo_dict_is_string_equal(temp_variable_1, temp_variable_2) == 1) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "!=") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_2);
            if (_yingshaoxo_dict_is_string_equal(temp_variable_1, temp_variable_2) != 1) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return return_value;
        }
        return_value[0] = '\0';
        return return_value;
    }

    if ((_yingshaoxo_dynamic_c_is_it_a_number(temp_variable_1)==1) && ((_yingshaoxo_dynamic_c_is_it_a_number(temp_variable_2)==1))) {
        /* handle number operations */
        if (_yingshaoxo_dict_is_string_equal(operator, "==") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) == _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "!=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) != _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, ">=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) >= _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "<=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) <= _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "<") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) < _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, ">") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) > _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "+=") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) + _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            yingshaoxo_dynamic_c_create_variable(variable_dict, original_variable_1_name, return_value);
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "-=") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) - _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            yingshaoxo_dynamic_c_create_variable(variable_dict, original_variable_1_name, return_value);
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "+") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) + _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "-") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) - _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "*") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) * _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            return return_value;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "/") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) / _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            return return_value;
        }
        return_value[0] = '\0';
        return return_value;
    }

    if (_yingshaoxo_dict_is_string_equal(operator, "==") == 1) {
        if (_yingshaoxo_dict_is_string_equal(temp_variable_1, temp_variable_2) == 1) {
            _yingshaoxo_dict_string_memory_copy(return_value, "1");
        } else {
            _yingshaoxo_dict_string_memory_copy(return_value, "0");
        }
        return return_value;
    }
    if (_yingshaoxo_dict_is_string_equal(operator, "!=") == 1) {
        if (_yingshaoxo_dict_is_string_equal(temp_variable_1, temp_variable_2) == 1) {
            _yingshaoxo_dict_string_memory_copy(return_value, "0");
        } else {
            _yingshaoxo_dict_string_memory_copy(return_value, "1");
        }
        return return_value;
    }

    return_value[0] = '\0';
    return return_value;
}

unsigned char *_yingshaoxo_dynamic_c_run_one_line_code(unsigned char *variable_dict, unsigned char *code) {
    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';

    unsigned int code_length = _yingshaoxo_dict_get_string_length(code);

    if (_yingshaoxo_dynamic_c_is_it_assignment(code) == 1) {
        /*assignment*/
        unsigned int the_equal_symbol_index = _yingshaoxo_dict_find_sub_string(code, "=");

        unsigned char variable_name[the_equal_symbol_index+2];
        unsigned char variable_value[(code_length-the_equal_symbol_index)+2];

        _yingshaoxo_dict_get_sub_string(code, 0, the_equal_symbol_index, variable_name);
        _yingshaoxo_dict_string_strip(variable_name);

        _yingshaoxo_dict_get_sub_string(code, the_equal_symbol_index+1, code_length, variable_value);
        _yingshaoxo_dict_string_strip(variable_value);

        unsigned char *real_variable_value = yingshaoxo_dynamic_c_evaluate(variable_dict, variable_value);

        if (_yingshaoxo_dynamic_c_is_it_list_or_dict_element_access(variable_name) == 0) {
            yingshaoxo_dynamic_c_create_variable(variable_dict, variable_name, real_variable_value);
        } else {
            _yingshaoxo_dynamic_c_parse_and_set_list_or_dict_element(variable_dict, variable_name, real_variable_value);
        }

        free(real_variable_value);
    } else {
        /*not assignment*/
        /*the evaluate_3_instance will handle '+=' or '-='*/
        free(default_return_value);
        _yingshaoxo_dict_string_strip(code);
        return yingshaoxo_dynamic_c_evaluate(variable_dict, code);
    }

    return default_return_value;
}

unsigned int _yingshaoxo_dynamic_c_handle_function_define(unsigned char *variable_dict, unsigned char *code) {
    unsigned int code_length = _yingshaoxo_dict_get_string_length(code);

    unsigned int arguments_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int function_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int function_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');

    unsigned char function_name[arguments_start_index + 2];
    _yingshaoxo_dict_get_sub_string(code, 0, arguments_start_index, function_name);
    unsigned char code_block[function_block_end_index + 4];
    _yingshaoxo_dict_get_sub_string(code, function_block_start_index+1, function_block_end_index, code_block);

    yingshaoxo_dynamic_c_create_function(variable_dict, function_name, "", code_block);
    return function_block_end_index;
}

unsigned char *_yingshaoxo_dynamic_c_handle_if_code_block(unsigned char *variable_dict, unsigned char *code) {
    unsigned int if_code_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int if_code_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
    unsigned int equation_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int equation_end_index = _yingshaoxo_dict_find_sub_string(code, ")");

    unsigned char equation[(equation_end_index - equation_start_index) + 2];
    _yingshaoxo_dict_get_sub_string(code, equation_start_index+1, equation_end_index, equation);
    unsigned char *equation_result = yingshaoxo_dynamic_c_evaluate(variable_dict, equation);
    if (_yingshaoxo_dict_is_string_equal(equation_result, "1") == 1) {
        free(equation_result);
        unsigned char if_code_block[if_code_block_end_index + 4];
        _yingshaoxo_dict_get_sub_string(code, if_code_block_start_index+1, if_code_block_end_index, if_code_block);
        return yingshaoxo_dynamic_c_c_runner(variable_dict, if_code_block);
    }

    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';
    return default_return_value;
}

unsigned char *_yingshaoxo_dynamic_c_handle_while_code_block(unsigned char *variable_dict, unsigned char *code) {
    unsigned int while_code_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int while_code_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
    unsigned int equation_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int equation_end_index = _yingshaoxo_dict_find_sub_string(code, ")");
    unsigned char equation[(equation_end_index - equation_start_index) + 2];
    _yingshaoxo_dict_get_sub_string(code, equation_start_index+1, equation_end_index, equation);

    unsigned char *equation_result = yingshaoxo_dynamic_c_evaluate(variable_dict, equation);

    unsigned char while_code_block[while_code_block_end_index + 4];
    _yingshaoxo_dict_get_sub_string(code, while_code_block_start_index+1, while_code_block_end_index, while_code_block);

    unsigned char *return_value;
    while (_yingshaoxo_dict_is_string_equal(equation_result, "1") == 1) {
        free(equation_result);
        return_value = yingshaoxo_dynamic_c_c_runner(variable_dict, while_code_block);
        if (return_value[0] == '\0') {
            free(return_value);
        } else if (_yingshaoxo_dict_is_string_equal(return_value, "continue") == 1) {
            free(return_value);
        } else {
            /* break, exit, or any function return value*/
            return return_value;
        }
        equation_result = yingshaoxo_dynamic_c_evaluate(variable_dict, equation);
    }

    unsigned char *default_return_value = malloc(1);
    default_return_value[0] = '\0';
    return default_return_value;
}

unsigned char *yingshaoxo_dynamic_c_c_runner(unsigned char *variable_dict, unsigned char *code_string) {
    unsigned char *default_return_value = malloc(1);
    unsigned int index = 0;
    while (1) {
        free(default_return_value);
        default_return_value = malloc(18);
        default_return_value[0] = '\0';

        if (code_string[index] == '\0') {
            return default_return_value;
        }

        unsigned char *code = &code_string[index];
        unsigned int move_to_right_index = 0;
        if ((code[0] == ' ') || (code[0] == '\n')) {
            move_to_right_index = 1;
        } else {
            if (_yingshaoxo_dict_string_starts_with(code, "function ")) {
                move_to_right_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}') + 1;
                _yingshaoxo_dynamic_c_handle_function_define(variable_dict, &code[9]) + 9 + 1;
            } else if (_yingshaoxo_dict_string_starts_with(code, "if ")) {
                move_to_right_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}') + 1;
                free(default_return_value);
                default_return_value = _yingshaoxo_dynamic_c_handle_if_code_block(variable_dict, code);
            } else if (_yingshaoxo_dict_string_starts_with(code, "while ")) {
                move_to_right_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}') + 1;
                free(default_return_value);
                default_return_value = _yingshaoxo_dynamic_c_handle_while_code_block(variable_dict, code);
                if (_yingshaoxo_dict_string_starts_with(default_return_value, "break")) {
                    default_return_value[0] = '\0';
                }
            } else if (_yingshaoxo_dict_string_starts_with(code, "return ")) {
                int temp_end_index = _yingshaoxo_dict_find_sub_string(&code[7], ";");
                move_to_right_index += temp_end_index + 1;
                unsigned char temp_one_line[temp_end_index+2];
                 _yingshaoxo_dict_get_sub_string(&code[7], 0, temp_end_index, temp_one_line);
                free(default_return_value);
                default_return_value = yingshaoxo_dynamic_c_evaluate(variable_dict, temp_one_line);
            } else if (_yingshaoxo_dict_string_starts_with(code, "try ")) {
            } else if (_yingshaoxo_dict_string_starts_with(code, "import ")) {
            } else if (_yingshaoxo_dict_string_starts_with(code, "//")) {
                move_to_right_index += _yingshaoxo_dict_find_sub_string(code, ";") + 1;
            } else if (_yingshaoxo_dict_string_starts_with(code, "#")) {
                move_to_right_index += _yingshaoxo_dict_find_sub_string(code, ";") + 1;
            } else if (_yingshaoxo_dict_string_starts_with(code, "/*")) {
                move_to_right_index += _yingshaoxo_dict_find_sub_string(code, "*/") + 2;
            } else if (_yingshaoxo_dict_string_starts_with(code, "break;")) {
                _yingshaoxo_dict_string_memory_copy(default_return_value, "break");
                move_to_right_index += _yingshaoxo_dict_find_sub_string(code, ";") + 1;
            } else if (_yingshaoxo_dict_string_starts_with(code, "continue;")) {
                _yingshaoxo_dict_string_memory_copy(default_return_value, "continue");
                move_to_right_index += _yingshaoxo_dict_find_sub_string(code, ";") + 1;
            } else if (_yingshaoxo_dict_string_starts_with(code, "exit();")) {
                _yingshaoxo_dict_string_memory_copy(default_return_value, "exit");
                move_to_right_index += _yingshaoxo_dict_find_sub_string(code, ";") + 1;
            } else {
                unsigned int the_end_for_a_line =  _yingshaoxo_dict_find_sub_string(code, ";");
                unsigned char a_line[the_end_for_a_line+1];
                _yingshaoxo_dict_get_sub_string(code, 0, the_end_for_a_line, a_line);
                _yingshaoxo_dict_string_strip(a_line);
                unsigned char * temp_return_value = _yingshaoxo_dynamic_c_run_one_line_code(variable_dict, a_line);
                free(temp_return_value);
                move_to_right_index += the_end_for_a_line;
            }
        }

        if (move_to_right_index <= 0) {
            move_to_right_index = 1;
        }
        index += move_to_right_index;
        if (default_return_value[0] != '\0') {
            return default_return_value;
        }
    }
    return default_return_value;
}

#endif



/*
#include <stdio.h>
#include <stdlib.h>
void print(unsigned char *a_string) {
    printf("%s\n", a_string);
}

void print_number(int a_number) {
    char text[16];
    sprintf(text, "%d", a_number);
    print(text);
}

#include "./yingshaoxo_dynamic_c.h"
#include "./yingshaoxo_c_pins.h"

int main() {
    unsigned char *test_code = "\
a = [567,2,1,0];\
print(a);\
a_2 = `22`;\
print(a_2);\
print(a[0]);\
b = '1  ha ';\
c = b.strip();\
print(c);\
print(len(c));\
b = {'x':2,'y':'dd'};\
print(b['y']);\
b['x'] = 'it is x';\
print(b['x']);\
a[0] = 'shit';\
print(a[0]);\
a[0] = 99;\
b['x'] = 1;\
a.append(a[0]);\
print(a);\
d = 'hi you all';\
print(d.split(' '));\
c = a[0] + b['x'];\
print(c);\
print('good' + ' for you.');\
function hi_you() {\
    print('yeah');\
    while (1) {\
        if (1) {\
            return 988;\
        }\
        print('shit');\
    }\
    return 223;\
}\
if (1 == 1) {\
    d = hi_you();\
    print(d);\
}\
i = 0;\
while (i < 5) {\
    print(i);\
    if (i == 2) {\
        break;\
    }\
    i += 1;\
}\
print(str(113));\
";

    unsigned char a_python_global_variable_dict[1024*2];
    unsigned char *return_value_or_control_command = yingshaoxo_dynamic_c_c_runner(a_python_global_variable_dict, test_code);
    printf("%s\n", return_value_or_control_command);
    printf("%s\n", a_python_global_variable_dict);
}
*/
