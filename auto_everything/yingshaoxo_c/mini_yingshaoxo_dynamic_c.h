/* tested in arduino nano v3 (no wifi version, 2k memory, 30kb flash) */ 

// as i tested, the arduino has bugs on inner_function variable creation, so better set all variable as global variable. and this also cause the program can't do multiple_layer function call. so in while loop can't have another while loop.

#ifndef mini_yingshaoxo_dynamic_c
#define mini_yingshaoxo_dynamic_c

/*
void print(unsigned char *a_string) {
    printf("%s\n", a_string);
    //print_string(0, 2, "                ");
    //print_string(0, 2, a_string);
    //set_LCD_pin_to_low();
    //delay(1000);
}

void print_number(int a_number) {
    //char text[16];
    //sprintf(text, "%d", a_number);
    //print_string(0, 2, "                ");
    //print_string(0, 2, text);
    //set_LCD_pin_to_low();
    //delay(1000);
}
*/

unsigned char yingshaoxo_dynamic_c_global_variable_dict[250] = { '\0' };
#define _yingshaoxo_dynamic_c_temp_string_length 20

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

void yingshaoxo_dynamic_c_get_variable_value(unsigned char *variable_dict, unsigned char *variable_name, unsigned char *variable_value) {
    unsigned int variable_name_length = _yingshaoxo_dict_get_string_length(variable_name);
    unsigned char new_name[variable_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "v_", variable_name);
    yingshaoxo_dict_get_value_by_key(variable_dict, new_name, variable_value);
    if (_yingshaoxo_dict_is_string_equal(variable_value, "") == 1) {
        _yingshaoxo_dict_string_memory_copy(variable_value, "``");
    }
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

    /* Handle special case for zero */
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
void _yingshaoxo_dynamic_c_remove_string_quote(unsigned char *a_string) {
    if ((a_string[0] == '`') || (a_string[0] == '\'') || (a_string[0] == '"')) {
        _yingshaoxo_dict_string_memory_copy(a_string, &a_string[1]);
        a_string[_yingshaoxo_dict_get_string_length(a_string)-1] = '\0';
    }
}

void _yingshaoxo_dynamic_c_add_string_quote(unsigned char *a_string_that_has_2_more_space) {
    unsigned char temp_string[_yingshaoxo_dict_get_string_length(a_string_that_has_2_more_space) + 3];
    _yingshaoxo_dict_add_string(temp_string, "`", a_string_that_has_2_more_space);
    _yingshaoxo_dict_add_string(temp_string, temp_string, "`");
    _yingshaoxo_dict_string_memory_copy(a_string_that_has_2_more_space, temp_string);
}

unsigned char _yingshaoxo_dynamic_c_operator_characters[10] = { '+', '-', '/', '*', '>', '<', '=', ' ', ')', ';' };
unsigned int _yingshaoxo_dynamic_c_get_variable_end_index(unsigned char *code) {
    unsigned int index = 0;
    unsigned int i = 0;
    while (1) {
        if (code[index] == '\0') {
            break;
        }
        i = 0;
        while (i <= 9) {
            if (code[index] == _yingshaoxo_dynamic_c_operator_characters[i]) {
                return index;
            }
            i += 1;
        }
        index += 1;
    }
    return index;
}

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

/*
level 2: change quickly
*/
// pre_defined arguments and functions
unsigned char yingshaoxo_dynamic_c_c_runner_result[_yingshaoxo_dynamic_c_temp_string_length*2];
unsigned char *yingshaoxo_dynamic_c_c_runner(unsigned char *variable_dict, unsigned char *code);

unsigned char _yingshaoxo_dynamic_c_evaluate_one_instance_return_value[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_evaluate_one_instance(unsigned char *variable_dict, unsigned char *code);

unsigned char _yingshaoxo_dynamic_c_function_return_value[_yingshaoxo_dynamic_c_temp_string_length];

void yingshaoxo_dynamic_c_call_function(unsigned char *variable_dict, unsigned char *function_name, unsigned char *arguments);

// others
unsigned char _yingshaoxo_dynamic_c_handle_function_define_function_name[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_handle_function_define_arguments[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_handle_function_define_code_block[_yingshaoxo_dynamic_c_temp_string_length*3];
unsigned int _yingshaoxo_dynamic_c_handle_function_define(unsigned char *variable_dict, unsigned char *code) {
    unsigned int function_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int function_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
    unsigned int arguments_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int arguments_end_index = _yingshaoxo_dict_find_sub_string(code, ")");
    _yingshaoxo_dict_get_sub_string(code, 0, arguments_start_index, _yingshaoxo_dynamic_c_handle_function_define_function_name);
    _yingshaoxo_dict_get_sub_string(code, arguments_start_index+1, arguments_end_index, _yingshaoxo_dynamic_c_handle_function_define_code_block);
    _yingshaoxo_dict_get_sub_string(code, function_block_start_index+1, function_block_end_index, _yingshaoxo_dynamic_c_handle_function_define_code_block);
    yingshaoxo_dynamic_c_create_function(variable_dict, _yingshaoxo_dynamic_c_handle_function_define_function_name, _yingshaoxo_dynamic_c_handle_function_define_arguments, _yingshaoxo_dynamic_c_handle_function_define_code_block);
    return function_block_end_index;
}

unsigned char _yingshaoxo_dynamic_c_parse_function_calling_function_name[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_parse_function_calling_function_arguments[_yingshaoxo_dynamic_c_temp_string_length];
int _yingshaoxo_dynamic_c_parse_function_calling(unsigned char *variable_dict, unsigned char *code) {
    int function_name_end_index = _yingshaoxo_dict_find_sub_string(code, "(");
    _yingshaoxo_dict_get_sub_string(code, 0, function_name_end_index, _yingshaoxo_dynamic_c_parse_function_calling_function_name);
    _yingshaoxo_dict_string_strip(_yingshaoxo_dynamic_c_parse_function_calling_function_name);
    int function_arguments_end_index = _yingshaoxo_dict_find_sub_string(code, ")");
    _yingshaoxo_dict_get_sub_string(code, function_name_end_index+1, function_arguments_end_index, _yingshaoxo_dynamic_c_parse_function_calling_function_arguments);
    _yingshaoxo_dict_string_strip(_yingshaoxo_dynamic_c_parse_function_calling_function_arguments);
    _yingshaoxo_dynamic_c_evaluate_one_instance(variable_dict, _yingshaoxo_dynamic_c_parse_function_calling_function_arguments);
    _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_parse_function_calling_function_arguments, _yingshaoxo_dynamic_c_evaluate_one_instance_return_value);
    return function_arguments_end_index;
}

unsigned char _yingshaoxo_dynamic_c_evaluate_one_instance(unsigned char *variable_dict, unsigned char *code) {
    // save result into _yingshaoxo_dynamic_c_evaluate_one_instance_return_value
    // has to add a check for function calling
    if (code[0] == '\0') {
        _yingshaoxo_dynamic_c_evaluate_one_instance_return_value[0] = '\0';
        return 0;
    }
    int string_end_index = _yingshaoxo_dynamic_c_parsing_string(code);
    unsigned int is_number = _yingshaoxo_dynamic_c_is_it_a_number(code);
    unsigned int is_function_call = _yingshaoxo_dynamic_c_is_it_a_function_call(code);
    if (string_end_index != -1) {
        /* a const string */
        _yingshaoxo_dict_get_sub_string(code, 0, string_end_index, _yingshaoxo_dynamic_c_evaluate_one_instance_return_value);
        return string_end_index;
    } else if (is_number == 1) {
        /* a const number */
        string_end_index = _yingshaoxo_dynamic_c_get_variable_end_index(&code[1]);
        _yingshaoxo_dict_get_sub_string(code, 0, string_end_index+1, _yingshaoxo_dynamic_c_evaluate_one_instance_return_value);
        return string_end_index+1;
    } else if (is_function_call == 1) {
        /* a function call */
        int arguments_end_index = _yingshaoxo_dynamic_c_parse_function_calling(variable_dict, code);
        yingshaoxo_dynamic_c_call_function(variable_dict, _yingshaoxo_dynamic_c_parse_function_calling_function_name, _yingshaoxo_dynamic_c_parse_function_calling_function_arguments);
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_one_instance_return_value, _yingshaoxo_dynamic_c_function_return_value);
        return arguments_end_index+1;
    } else {
        /* a variable */
        string_end_index = _yingshaoxo_dynamic_c_get_variable_end_index(code);
        _yingshaoxo_dict_get_sub_string(code, 0, string_end_index, _yingshaoxo_dynamic_c_evaluate_one_instance_return_value);
        yingshaoxo_dynamic_c_get_variable_value(variable_dict, _yingshaoxo_dynamic_c_evaluate_one_instance_return_value, _yingshaoxo_dynamic_c_evaluate_one_instance_return_value);
        return string_end_index;
    }
}

unsigned char _yingshaoxo_dynamic_c_evaluate_3_instance_return_value[_yingshaoxo_dynamic_c_temp_string_length*2];
unsigned char _yingshaoxo_dynamic_c_evaluate_3_instance_variable_1[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_evaluate_3_instance_variable_1_name[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_evaluate_3_instance_operator[3] = { '=', '=', '\0'};
unsigned char _yingshaoxo_dynamic_c_evaluate_3_instance_variable_2[_yingshaoxo_dynamic_c_temp_string_length];
void _yingshaoxo_dynamic_c_evaluate_3_instance(unsigned char *variable_dict, unsigned char *code) {
    if (code[0] == '\0') {
        _yingshaoxo_dynamic_c_evaluate_3_instance_return_value[0] = '\0';
        return;
    }

    unsigned int index = 0;

    index += _yingshaoxo_dynamic_c_evaluate_one_instance(variable_dict, code);
    _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1, _yingshaoxo_dynamic_c_evaluate_one_instance_return_value);
    _yingshaoxo_dict_get_sub_string(code, 0, index, _yingshaoxo_dynamic_c_evaluate_3_instance_variable_1_name);
    _yingshaoxo_dict_string_strip(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1_name);

    /* skip space */
    while (1) {
        if (code[index] != ' ') {
            break;
        }
        index += 1;
    }

    if (_yingshaoxo_dict_string_starts_with(&code[index], "==") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "==");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "!=") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "!=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], ">=") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, ">=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "<=") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "<=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "+=") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "+=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "-=") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "-=");
        index += 2;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], ">") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, ">");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "<") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "<");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "+") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "+");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "-") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "-");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "*") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "*");
        index += 1;
    } else if (_yingshaoxo_dict_string_starts_with(&code[index], "/") == 1) {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "/");
        index += 1;
    } else {
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, _yingshaoxo_dynamic_c_evaluate_3_instance_variable_1);
        return;
    }

    /* skip space */
    while (1) {
        if (code[index] != ' ') {
            break;
        }
        index += 1;
    }

    index += _yingshaoxo_dynamic_c_evaluate_one_instance(variable_dict, &code[index]);
    _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2, _yingshaoxo_dynamic_c_evaluate_one_instance_return_value);

    /* handle operations */
    if ((_yingshaoxo_dynamic_c_is_it_a_string(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1)==1) && ((_yingshaoxo_dynamic_c_is_it_a_string(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)==1))) {
        /* handle string operations */
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "+") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2);

            _yingshaoxo_dict_add_string(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, _yingshaoxo_dynamic_c_evaluate_3_instance_variable_1, _yingshaoxo_dynamic_c_evaluate_3_instance_variable_2);
            _yingshaoxo_dynamic_c_add_string_quote(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "==") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2);
            if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1, _yingshaoxo_dynamic_c_evaluate_3_instance_variable_2) == 1) {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "!=") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2);
            if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1, _yingshaoxo_dynamic_c_evaluate_3_instance_variable_2) != 1) {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            }
            return;
        }
        _yingshaoxo_dynamic_c_evaluate_3_instance_return_value[0] = '\0';
        return;
    }

    if ((_yingshaoxo_dynamic_c_is_it_a_number(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1)==1) && ((_yingshaoxo_dynamic_c_is_it_a_number(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)==1))) {
        /* handle number operations */
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "==") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) == _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "!=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) != _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, ">=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) >= _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "<=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) <= _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "<") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) < _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, ">") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) > _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "+=") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) + _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2), _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            yingshaoxo_dynamic_c_create_variable(variable_dict, _yingshaoxo_dynamic_c_evaluate_3_instance_variable_1_name, _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "-=") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) - _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2), _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            yingshaoxo_dynamic_c_create_variable(variable_dict, _yingshaoxo_dynamic_c_evaluate_3_instance_variable_1_name, _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "+") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) + _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2), _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "-") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) - _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2), _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "*") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) * _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2), _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "/") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1) / _yingshaoxo_dynamic_c_string_to_float(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2), _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
            return;
        }
        _yingshaoxo_dynamic_c_evaluate_3_instance_return_value[0] = '\0';
        return;
    }


    if ((_yingshaoxo_dynamic_c_is_it_a_string(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1)==1) && ((_yingshaoxo_dynamic_c_is_it_a_number(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)==1))) {
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "==") == 1) {
            _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "!=") == 1) {
            _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            return;
        }
    }
    if ((_yingshaoxo_dynamic_c_is_it_a_string(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_2)==1) && ((_yingshaoxo_dynamic_c_is_it_a_number(_yingshaoxo_dynamic_c_evaluate_3_instance_variable_1)==1))) {
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "==") == 1) {
            _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "0");
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_evaluate_3_instance_operator, "!=") == 1) {
            _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value, "1");
            return;
        }
    }

    _yingshaoxo_dynamic_c_evaluate_3_instance_return_value[0] = '\0';
    return;
}

unsigned char _yingshaoxo_dynamic_c_evaluate_return_value[_yingshaoxo_dynamic_c_temp_string_length*2];
unsigned char *_yingshaoxo_dynamic_c_evaluate(unsigned char *variable_dict, unsigned char *code) {
    if (_yingshaoxo_dynamic_c_is_it_a_function_call(code) == 1) {
        // a function call
        int arguments_end_index = _yingshaoxo_dynamic_c_parse_function_calling(variable_dict, code);
        yingshaoxo_dynamic_c_call_function(variable_dict, _yingshaoxo_dynamic_c_parse_function_calling_function_name, _yingshaoxo_dynamic_c_parse_function_calling_function_arguments);
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_return_value, _yingshaoxo_dynamic_c_function_return_value);
        return _yingshaoxo_dynamic_c_evaluate_return_value;
    }

    if (_yingshaoxo_dynamic_c_is_it_a_list(code) == 1) {
        // a list
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_return_value, code);
        return _yingshaoxo_dynamic_c_evaluate_return_value;
    }
    if (_yingshaoxo_dynamic_c_is_it_a_list(code) == 1) {
        // a dict
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_return_value, code);
        return _yingshaoxo_dynamic_c_evaluate_return_value;
    }

    // normal variable value
    _yingshaoxo_dynamic_c_evaluate_3_instance(variable_dict, code);
    _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_evaluate_return_value, _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
    return _yingshaoxo_dynamic_c_evaluate_return_value;
}

unsigned char _yingshaoxo_dynamic_c_function_code_block[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_call_function_real_argument_value[_yingshaoxo_dynamic_c_temp_string_length];
void yingshaoxo_dynamic_c_call_function(unsigned char *variable_dict, unsigned char *function_name, unsigned char *arguments) {
    // should save return value to _yingshaoxo_dynamic_c_function_return_value
    if (_yingshaoxo_dict_is_string_equal(function_name, "print") == 1) {
        _yingshaoxo_dynamic_c_evaluate_3_instance(variable_dict, arguments);
        print(_yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "free") == 1) {
        yingshaoxo_dynamic_c_remove_variable(variable_dict, arguments);
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "len") == 1) {
        unsigned int the_string_length = _yingshaoxo_dict_get_string_length(arguments);
        if ((the_string_length-2) >= 0) {
            the_string_length -= 2;
        }
        _yingshaoxo_dynamic_c_float_to_string(the_string_length, _yingshaoxo_dynamic_c_function_return_value);
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "split") == 1) {
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "get_sub_string") == 1) {
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "find") == 1) {
        return;
    }

    unsigned int function_name_length = _yingshaoxo_dict_get_string_length(function_name);
    unsigned char new_name[function_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "f_", function_name);
    if (yingshaoxo_dict_has_key(variable_dict, new_name) == 1) {
        yingshaoxo_dict_get_value_by_key(variable_dict, new_name, _yingshaoxo_dynamic_c_function_code_block);
        yingshaoxo_dynamic_c_c_runner(variable_dict, _yingshaoxo_dynamic_c_function_code_block);
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_function_return_value, yingshaoxo_dynamic_c_c_runner_result);
        return;
    }
}

unsigned char _yingshaoxo_dynamic_c_variable_part_1[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_variable_part_2[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_variable_part_3[_yingshaoxo_dynamic_c_temp_string_length];
void _yingshaoxo_dynamic_c_process_one_line(unsigned char *variable_dict, unsigned char *code) {
    unsigned int length = _yingshaoxo_dict_get_string_length(code);

    int index = 0;
    int part_char_index = 0;
    while (1) {
        if (code[index] == '\0') {
            return;
        }

        while (code[index] == ' ') {
            index += 1;
        }
        while (code[index] == '\n') {
            index += 1;
        }

        _yingshaoxo_dynamic_c_variable_part_1[part_char_index] = code[index];
        if (part_char_index >= 49) {
            part_char_index = -1;
        }
        if ((_yingshaoxo_dynamic_c_variable_part_1[part_char_index] == '+') || ((_yingshaoxo_dynamic_c_variable_part_1[part_char_index] == '-'))) {
            if (code[index+1] == '=') {
                _yingshaoxo_dynamic_c_evaluate(variable_dict, code);
                return;
            }
        }
        if (_yingshaoxo_dynamic_c_variable_part_1[part_char_index] == '=') {
            _yingshaoxo_dynamic_c_variable_part_1[part_char_index] = '\0';
            _yingshaoxo_dict_string_strip(_yingshaoxo_dynamic_c_variable_part_1);

            _yingshaoxo_dict_get_sub_string(code, index+1, length, _yingshaoxo_dynamic_c_variable_part_2);
            _yingshaoxo_dict_string_strip(_yingshaoxo_dynamic_c_variable_part_2);

            _yingshaoxo_dynamic_c_evaluate(variable_dict, _yingshaoxo_dynamic_c_variable_part_2);
            _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_variable_part_2, _yingshaoxo_dynamic_c_evaluate_return_value);

            yingshaoxo_dynamic_c_create_variable(variable_dict, _yingshaoxo_dynamic_c_variable_part_1, _yingshaoxo_dynamic_c_variable_part_2);

            /*
            print(_yingshaoxo_dynamic_c_variable_part_1);
            print(_yingshaoxo_dynamic_c_variable_part_2);
            */

            return;
        }
        if (_yingshaoxo_dynamic_c_variable_part_1[part_char_index] == '(') {
            _yingshaoxo_dynamic_c_variable_part_1[part_char_index] = '\0';
            _yingshaoxo_dict_string_strip(_yingshaoxo_dynamic_c_variable_part_1);

            _yingshaoxo_dict_get_sub_string(code, index+1, length-1, _yingshaoxo_dynamic_c_variable_part_2);
            _yingshaoxo_dict_string_strip(_yingshaoxo_dynamic_c_variable_part_2);

            /*
            print(_yingshaoxo_dynamic_c_variable_part_1);
            print(_yingshaoxo_dynamic_c_variable_part_2);
            */
            yingshaoxo_dynamic_c_call_function(variable_dict, _yingshaoxo_dynamic_c_variable_part_1, _yingshaoxo_dynamic_c_variable_part_2);

            return;
        }

        index += 1;
        part_char_index += 1;
    }
}

unsigned char _yingshaoxo_dynamic_c_handle_if_code_block_equation[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_handle_if_code_block_equation_result[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_handle_if_code_block_the_block_code[_yingshaoxo_dynamic_c_temp_string_length*3];
unsigned int _yingshaoxo_dynamic_c_handle_if_code_block(unsigned char *variable_dict, unsigned char *code) {
    unsigned int if_code_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int if_code_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
    unsigned int equation_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int equation_end_index = _yingshaoxo_dict_find_sub_string(code, ")");
    _yingshaoxo_dict_get_sub_string(code, equation_start_index+1, equation_end_index, _yingshaoxo_dynamic_c_handle_if_code_block_equation);

    _yingshaoxo_dynamic_c_evaluate_3_instance(variable_dict, _yingshaoxo_dynamic_c_handle_if_code_block_equation);
    _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_handle_if_code_block_equation_result, _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);

    if (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_handle_if_code_block_equation_result, "1") == 1) {
        _yingshaoxo_dict_get_sub_string(code, if_code_block_start_index+1, if_code_block_end_index, _yingshaoxo_dynamic_c_handle_if_code_block_the_block_code);
        yingshaoxo_dynamic_c_c_runner(variable_dict, _yingshaoxo_dynamic_c_handle_if_code_block_the_block_code);
    }
    return if_code_block_end_index;
}

unsigned char _yingshaoxo_dynamic_c_handle_while_code_block_equation[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_handle_while_code_block_equation_result[_yingshaoxo_dynamic_c_temp_string_length];
unsigned char _yingshaoxo_dynamic_c_handle_while_code_block_the_block_code[_yingshaoxo_dynamic_c_temp_string_length*4];
unsigned int _yingshaoxo_dynamic_c_handle_while_code_block(unsigned char *variable_dict, unsigned char *code) {
    unsigned int while_code_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int while_code_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
    unsigned int equation_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int equation_end_index = _yingshaoxo_dict_find_sub_string(code, ")");
    _yingshaoxo_dict_get_sub_string(code, equation_start_index+1, equation_end_index, _yingshaoxo_dynamic_c_handle_while_code_block_equation);

    _yingshaoxo_dynamic_c_evaluate_3_instance(variable_dict, _yingshaoxo_dynamic_c_handle_while_code_block_equation);
    _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_handle_while_code_block_equation_result, _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);

    while (_yingshaoxo_dict_is_string_equal(_yingshaoxo_dynamic_c_handle_while_code_block_equation_result, "1") == 1) {
        _yingshaoxo_dict_get_sub_string(code, while_code_block_start_index+1, while_code_block_end_index, _yingshaoxo_dynamic_c_handle_while_code_block_the_block_code);

        yingshaoxo_dynamic_c_c_runner(variable_dict, _yingshaoxo_dynamic_c_handle_while_code_block_the_block_code);

        _yingshaoxo_dynamic_c_evaluate_3_instance(variable_dict, _yingshaoxo_dynamic_c_handle_while_code_block_equation);
        _yingshaoxo_dict_string_memory_copy(_yingshaoxo_dynamic_c_handle_while_code_block_equation_result, _yingshaoxo_dynamic_c_evaluate_3_instance_return_value);
    }

    return while_code_block_end_index;
}

unsigned char _yingshaoxo_dynamic_c_one_line[_yingshaoxo_dynamic_c_temp_string_length*2];
unsigned char *yingshaoxo_dynamic_c_c_runner(unsigned char *variable_dict, unsigned char *code) {
    // use 'result = xxx;' to get yingshaoxo_dynamic_c_c_runner_result
    yingshaoxo_dynamic_c_c_runner_result[0] = '\0';
    int char_index = 0;
    while (1) {
        if (code[char_index] == '\0') {
            yingshaoxo_dynamic_c_get_variable_value(variable_dict, "result", yingshaoxo_dynamic_c_c_runner_result);
            return yingshaoxo_dynamic_c_c_runner_result;
        }

        while ((code[char_index] == ' ') || (code[char_index] == '\n')) {
            char_index += 1;
        }

        if (_yingshaoxo_dict_string_starts_with(&code[char_index], "if ")) {
            char_index += _yingshaoxo_dynamic_c_handle_if_code_block(variable_dict, &code[char_index]) + 1;
            continue;
        }

        if (_yingshaoxo_dict_string_starts_with(&code[char_index], "while ")) {
            char_index += _yingshaoxo_dynamic_c_handle_while_code_block(variable_dict, &code[char_index]) + 1;
            continue;
        }

        if (_yingshaoxo_dict_string_starts_with(&code[char_index], "function ")) {
            char_index += _yingshaoxo_dynamic_c_handle_function_define(variable_dict, &code[char_index+9]) + 9 + 1;
            continue;
        }

        if (_yingshaoxo_dict_string_starts_with(&code[char_index], "//")) {
            char_index += _yingshaoxo_dict_find_sub_string(&code[char_index], ";") + 1;
            continue;
        } else if (_yingshaoxo_dict_string_starts_with(&code[char_index], "#")) {
            char_index += _yingshaoxo_dict_find_sub_string(&code[char_index], ";") + 1;
            continue;
        }

        if (_yingshaoxo_dict_string_starts_with(&code[char_index], "exit();")) {
            yingshaoxo_dynamic_c_get_variable_value(variable_dict, "result", yingshaoxo_dynamic_c_c_runner_result);
            return yingshaoxo_dynamic_c_c_runner_result;
        }

        unsigned int the_end_for_a_line = _yingshaoxo_dict_find_sub_string(&code[char_index], ";");
        if (the_end_for_a_line != -1) {
            _yingshaoxo_dict_get_sub_string(code, char_index, char_index+the_end_for_a_line, _yingshaoxo_dynamic_c_one_line);
            _yingshaoxo_dynamic_c_process_one_line(variable_dict, _yingshaoxo_dynamic_c_one_line);
            //_yingshaoxo_dict_get_sub_string(_yingshaoxo_dynamic_c_one_line, 0, 16, _yingshaoxo_dynamic_c_one_line);
            //print(_yingshaoxo_dynamic_c_one_line);
            char_index += the_end_for_a_line + 1;
            continue;
        }

        char_index += 1;
    }
} 

#endif

/*
void setup() {
    initialize_LCD();
    response_to_keypad_number(0);

    delay(200);
    clear_the_screen();

    unsigned char *test_code = "\
data=`hi`;\n\
print(data);\n\
data=1+1;\n\
print('ok_' + 'dd');\n\
if (1 == 1) {\
    print('if works');\
}\
i = 0;\
while (i < 4) {\
    print(i);\
    i += 1;\
}\
print(3*2.5);\
result = len('xoo');\
function okk() {\
    print('yeah');\
}\
print(1);\
okk();\
";
    unsigned char *result;
    result = yingshaoxo_dynamic_c_c_runner(yingshaoxo_dynamic_c_global_variable_dict, test_code);
    print(result);
}

int i = 0;
void loop() {
    if (i % 2 == 0) {
        smart_print_string(0, 0, "1");
    } else {
        smart_print_string(0, 0, "2");
    }
    i += 1;
    delay(2000);
}
*/
