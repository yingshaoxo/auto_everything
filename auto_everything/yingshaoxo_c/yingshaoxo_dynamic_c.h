#ifndef yingshaoxo_dynamic_c
#define yingshaoxo_dynamic_c

#include "./yingshaoxo_c_dict.h"
#include <stdio.h>
#include <stdlib.h>

/* this can not support those micro_controller that have less than 20kb memory. consider only use 'yingshaoxo_c_pins.h' to do remote control. */

/*
unsigned char yingshaoxo_dynamic_c_global_variable_dict[500] = { '\0' };
unsigned int _yingshaoxo_dynamic_c_temp_varaible_length = 100;
*/
unsigned char yingshaoxo_dynamic_c_global_variable_dict[1024 * 20] = { '\0' };
unsigned int _yingshaoxo_dynamic_c_temp_varaible_length = 1024*2;
void yingshaoxo_super_c_c_runner(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value);

void new_print(unsigned char *a_string) {
    /* in micro_controller, print it directly to screen */
    printf("%s\n", a_string);
}

void yingshaoxo_dynamic_c_create_variable(unsigned char *variable_dict, unsigned char *variable_name, unsigned char *initial_value) {
    unsigned int variable_name_length = _yingshaoxo_dict_get_string_length(variable_name);
    unsigned char new_name[variable_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "v_", variable_name);
    yingshaoxo_dict_set_key_and_value(variable_dict, new_name, initial_value);
}

void yingshaoxo_dynamic_c_remove_variable(unsigned char *variable_dict, unsigned char *variable_name) {
    unsigned int variable_name_length = _yingshaoxo_dict_get_string_length(variable_name);
    unsigned char new_name[variable_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "v_", variable_name);
    yingshaoxo_dict_delete_a_key(variable_dict, new_name);
    _yingshaoxo_dict_add_string(new_name, "f_", variable_name);
    yingshaoxo_dict_delete_a_key(variable_dict, new_name);
}

void yingshaoxo_dynamic_c_give_variable_a_new_value(unsigned char *variable_dict, unsigned char *variable_name, unsigned char *new_value) {
    unsigned int variable_name_length = _yingshaoxo_dict_get_string_length(variable_name);
    unsigned char new_name[variable_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "v_", variable_name);
    yingshaoxo_dynamic_c_create_variable(variable_dict, new_name, new_value);
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

unsigned int _yingshaoxo_dynamic_c_get_variable_end_index(unsigned char *code) {
    unsigned char operator_characters[10] = { '+', '-', '/', '*', '>', '<', '=', ' ', ')', ';' };
    unsigned int index = 0;
    unsigned int i = 0;
    while (1) {
        if (code[index] == '\0') {
            break;
        }
        i = 0;
        while (i <= 9) {
            if (code[index] == operator_characters[i]) {
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
        for (i; i < 6; i++) {
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

unsigned char _yingshaoxo_dynamic_c_evaluate_one_instance(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value) {
    if (code[0] == '\0') {
        return_value[0] = '\0';
        return 0;
    }
    int string_end_index = _yingshaoxo_dynamic_c_parsing_string(code);
    unsigned int is_number = _yingshaoxo_dynamic_c_is_it_a_number(code);
    if (string_end_index != -1) {
        /* a const string */
        _yingshaoxo_dict_get_sub_string(code, 0, string_end_index, return_value);
        return string_end_index;
    } else if (is_number == 1) {
        /* a const number */
        string_end_index = _yingshaoxo_dynamic_c_get_variable_end_index(&code[1]);
        _yingshaoxo_dict_get_sub_string(code, 0, string_end_index+1, return_value);
        return string_end_index+1;
    } else {
        /* a variable */
        string_end_index = _yingshaoxo_dynamic_c_get_variable_end_index(code);
        _yingshaoxo_dict_get_sub_string(code, 0, string_end_index, return_value);
        yingshaoxo_dynamic_c_get_variable_value(variable_dict, return_value, return_value);
        return string_end_index;
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
    _yingshaoxo_dict_add_string(temp_string, "`", a_string_that_has_2_more_space);
    _yingshaoxo_dict_add_string(temp_string, temp_string, "`");
    _yingshaoxo_dict_string_memory_copy(a_string_that_has_2_more_space, temp_string);
}

void _yingshaoxo_dynamic_c_evaluate_3_instance(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value) {
    if (code[0] == '\0') {
        return_value[0] = '\0';
        return;
    }

    unsigned int index = 0;

    unsigned char temp_variable_1[_yingshaoxo_dynamic_c_temp_varaible_length];
    index += _yingshaoxo_dynamic_c_evaluate_one_instance(variable_dict, code, temp_variable_1);
    unsigned char original_variable_1_name[index+1];
    _yingshaoxo_dict_get_sub_string(code, 0, index, original_variable_1_name);
    _yingshaoxo_dict_string_strip(original_variable_1_name);

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
        _yingshaoxo_dict_string_memory_copy(return_value, temp_variable_1);
        return;
    }

    /* skip space */
    while (1) {
        if (code[index] != ' ') {
            break;
        }
        index += 1;
    }

    unsigned char temp_variable_2[_yingshaoxo_dynamic_c_temp_varaible_length];
    index += _yingshaoxo_dynamic_c_evaluate_one_instance(variable_dict, &code[index], temp_variable_2);

    /*
    printf("v1:%s\n", temp_variable_1);
    printf("operator:%s\n", operator);
    printf("v2:%s\n", temp_variable_2);
    */

    /* handle operations */
    if ((_yingshaoxo_dynamic_c_is_it_a_string(temp_variable_1)==1) && ((_yingshaoxo_dynamic_c_is_it_a_string(temp_variable_2)==1))) {
        /* handle string operations */
        if (_yingshaoxo_dict_is_string_equal(operator, "+") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_2);

            _yingshaoxo_dict_add_string(return_value, temp_variable_1, temp_variable_2);
            _yingshaoxo_dynamic_c_add_string_quote(return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "==") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_2);
            if (_yingshaoxo_dict_is_string_equal(temp_variable_1, temp_variable_2) == 1) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "!=") == 1) {
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_1);
            _yingshaoxo_dynamic_c_remove_string_quote(temp_variable_2);
            if (_yingshaoxo_dict_is_string_equal(temp_variable_1, temp_variable_2) != 1) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return;
        }
        return_value[0] = '\0';
        return;
    }

    if ((_yingshaoxo_dynamic_c_is_it_a_number(temp_variable_1)==1) && ((_yingshaoxo_dynamic_c_is_it_a_number(temp_variable_2)==1))) {
        /* handle number operations */
        if (_yingshaoxo_dict_is_string_equal(operator, "==") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) == _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "!=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) != _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, ">=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) >= _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "<=") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) <= _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "<") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) < _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, ">") == 1) {
            if (_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) > _yingshaoxo_dynamic_c_string_to_float(temp_variable_2)) {
                _yingshaoxo_dict_string_memory_copy(return_value, "1");
            } else {
                _yingshaoxo_dict_string_memory_copy(return_value, "0");
            }
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "+=") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) + _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            yingshaoxo_dynamic_c_create_variable(variable_dict, original_variable_1_name, return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "-=") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) - _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            yingshaoxo_dynamic_c_create_variable(variable_dict, original_variable_1_name, return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "+") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) + _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "-") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) - _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "*") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) * _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "/") == 1) {
            _yingshaoxo_dynamic_c_float_to_string(_yingshaoxo_dynamic_c_string_to_float(temp_variable_1) / _yingshaoxo_dynamic_c_string_to_float(temp_variable_2), return_value);
            return;
        }
        return_value[0] = '\0';
        return;
    }


    if ((_yingshaoxo_dynamic_c_is_it_a_string(temp_variable_1)==1) && ((_yingshaoxo_dynamic_c_is_it_a_number(temp_variable_2)==1))) {
        if (_yingshaoxo_dict_is_string_equal(operator, "==") == 1) {
            _yingshaoxo_dict_string_memory_copy(return_value, "0");
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "!=") == 1) {
            _yingshaoxo_dict_string_memory_copy(return_value, "1");
            return;
        }
    }
    if ((_yingshaoxo_dynamic_c_is_it_a_string(temp_variable_2)==1) && ((_yingshaoxo_dynamic_c_is_it_a_number(temp_variable_1)==1))) {
        if (_yingshaoxo_dict_is_string_equal(operator, "==") == 1) {
            _yingshaoxo_dict_string_memory_copy(return_value, "0");
            return;
        }
        if (_yingshaoxo_dict_is_string_equal(operator, "!=") == 1) {
            _yingshaoxo_dict_string_memory_copy(return_value, "1");
            return;
        }
    }

    return_value[0] = '\0';
    return;
}

void yingshaoxo_dynamic_c_evaluate(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value);

void yingshaoxo_dynamic_c_call_function(unsigned char *variable_dict, unsigned char *function_name, unsigned char *arguments, unsigned char *return_value) {
    if (_yingshaoxo_dict_is_string_equal(function_name, "print") == 1) {
        yingshaoxo_dynamic_c_evaluate(variable_dict, arguments, return_value);
        printf("%s\n", return_value);
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "print_raw") == 1) {
        yingshaoxo_dynamic_c_evaluate(variable_dict, arguments, return_value);
        printf("%s", return_value);
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "not") == 1) {
        yingshaoxo_dynamic_c_evaluate(variable_dict, arguments, return_value);
        if (_yingshaoxo_dict_is_string_equal(return_value, "0") == 1) {
            _yingshaoxo_dict_string_memory_copy(return_value, "1");
        } else {
            _yingshaoxo_dict_string_memory_copy(return_value, "0");
        }
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "str") == 1) {
        yingshaoxo_dynamic_c_evaluate(variable_dict, arguments, return_value);
        _yingshaoxo_dynamic_c_add_string_quote(return_value);
        return;
    }
    if (_yingshaoxo_dict_is_string_equal(function_name, "free") == 1) {
        yingshaoxo_dynamic_c_remove_variable(variable_dict, arguments);
        return;
    }

    unsigned int function_name_length = _yingshaoxo_dict_get_string_length(function_name);
    unsigned char new_name[function_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "f_", function_name);
    unsigned char code_block[_yingshaoxo_dynamic_c_temp_varaible_length*2];
    yingshaoxo_dict_get_value_by_key(variable_dict, new_name, code_block);
    yingshaoxo_super_c_c_runner(variable_dict, code_block, return_value);
}

void yingshaoxo_dynamic_c_create_function(unsigned char *variable_dict, unsigned char *function_name, unsigned char *arguments, unsigned char *function_code) {
    unsigned int function_name_length = _yingshaoxo_dict_get_string_length(function_name);
    unsigned char new_name[function_name_length+2];
    _yingshaoxo_dict_add_string(new_name, "f_", function_name);
    yingshaoxo_dict_set_key_and_value(variable_dict, new_name, function_code);
}

unsigned int _yingshaoxo_dynamic_c_parse_and_call_function(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value) {
    unsigned int function_argument_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int function_argument_end_index = _yingshaoxo_dict_find_sub_string(code, ")");

    if ((function_argument_start_index != -1) && (function_argument_end_index != -1) && (function_argument_start_index < function_argument_end_index)) {
        unsigned char function_name[function_argument_start_index+1];
        unsigned char arguments[(function_argument_end_index-function_argument_start_index)+1];
        _yingshaoxo_dict_get_sub_string(code, 0, function_argument_start_index, function_name);
        _yingshaoxo_dict_string_strip(function_name);
        _yingshaoxo_dict_get_sub_string(code, function_argument_start_index+1, function_argument_end_index, arguments);
        _yingshaoxo_dict_string_strip(arguments);
        yingshaoxo_dynamic_c_call_function(variable_dict, function_name, arguments, return_value);
        return 1;
    }
    return 0;
}

void yingshaoxo_dynamic_c_evaluate(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value) {
    if (code[0] == '\0') {
        return_value[0] = '\0';
        return;
    }

    unsigned int it_is_function_and_get_called = _yingshaoxo_dynamic_c_parse_and_call_function(variable_dict, code, return_value);
    if (it_is_function_and_get_called == 1) {
        return;
    }

    _yingshaoxo_dynamic_c_evaluate_3_instance(variable_dict, code, return_value);
}

void _yingshaoxo_dynamic_c_run_one_line_code(unsigned char *variable_dict, unsigned char *code) {
    unsigned int line_end_index = _yingshaoxo_dict_get_string_length(code);
    unsigned int equal_mark_index = _yingshaoxo_dict_find_sub_string(code, "=");
    unsigned int function_argument_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int function_argument_end_index = _yingshaoxo_dict_find_sub_string(code, ")");
    unsigned int list_or_dict_assignment_start_index = _yingshaoxo_dict_find_sub_string(code, "[");
    unsigned int space_index = _yingshaoxo_dict_find_sub_string(code, " ");
    unsigned int plus_equal_index = _yingshaoxo_dict_find_sub_string(code, "+=");
    unsigned int minus_equal_index = _yingshaoxo_dict_find_sub_string(code, "-=");

    if (((plus_equal_index != -1) || (minus_equal_index != -1))) {
        /* such as: index -= 1*/
        unsigned char real_value[_yingshaoxo_dynamic_c_temp_varaible_length];
        yingshaoxo_dynamic_c_evaluate(variable_dict, code, real_value);
        return;
    }

    if (equal_mark_index != -1) {
        /*
            has '=' and end with ';'
        */
        unsigned char variable_name[equal_mark_index+1];
        _yingshaoxo_dict_get_sub_string(code, 0, equal_mark_index, variable_name);
        _yingshaoxo_dict_string_strip(variable_name);
        unsigned char variable_value[(line_end_index-equal_mark_index)+1];
        _yingshaoxo_dict_get_sub_string(code, equal_mark_index+1, line_end_index, variable_value);
        _yingshaoxo_dict_string_strip(variable_value);
        unsigned char real_value[_yingshaoxo_dynamic_c_temp_varaible_length];
        yingshaoxo_dynamic_c_evaluate(variable_dict, variable_value, real_value);
        yingshaoxo_dynamic_c_create_variable(variable_dict, variable_name, real_value);
        return;
    }

    if ((function_argument_start_index != -1) && (function_argument_end_index != -1) && (function_argument_start_index < function_argument_end_index)) {
        /*
            has '(' and ')', and end with ';'
        */
        unsigned char return_value[_yingshaoxo_dynamic_c_temp_varaible_length];
        _yingshaoxo_dynamic_c_parse_and_call_function(variable_dict, code, return_value);
        return;
    }
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

unsigned int _yingshaoxo_dynamic_c_handle_if_code_block(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value) {
    unsigned int if_code_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int if_code_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
    unsigned int equation_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int equation_end_index = _yingshaoxo_dict_find_sub_string(code, ")");
    unsigned char equation[_yingshaoxo_dynamic_c_temp_varaible_length];
    unsigned char equation_result[_yingshaoxo_dynamic_c_temp_varaible_length];
    _yingshaoxo_dict_get_sub_string(code, equation_start_index+1, equation_end_index, equation);
    yingshaoxo_dynamic_c_evaluate(variable_dict, equation, equation_result);
    if (_yingshaoxo_dict_is_string_equal(equation_result, "1") == 1) {
        unsigned char if_code_block[_yingshaoxo_dynamic_c_temp_varaible_length];
        _yingshaoxo_dict_get_sub_string(code, if_code_block_start_index+1, if_code_block_end_index, if_code_block);
        yingshaoxo_super_c_c_runner(variable_dict, if_code_block, return_value);
    }
    return if_code_block_end_index;
}

unsigned int _yingshaoxo_dynamic_c_handle_while_code_block(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value) {
    unsigned int while_code_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int while_code_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
    unsigned int equation_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned int equation_end_index = _yingshaoxo_dict_find_sub_string(code, ")");
    unsigned char equation[_yingshaoxo_dynamic_c_temp_varaible_length];
    unsigned char equation_result[_yingshaoxo_dynamic_c_temp_varaible_length];
    _yingshaoxo_dict_get_sub_string(code, equation_start_index+1, equation_end_index, equation);
    yingshaoxo_dynamic_c_evaluate(variable_dict, equation, equation_result);

    unsigned char while_code_block[_yingshaoxo_dynamic_c_temp_varaible_length];
    _yingshaoxo_dict_get_sub_string(code, while_code_block_start_index+1, while_code_block_end_index, while_code_block);

    while (_yingshaoxo_dict_is_string_equal(equation_result, "1") == 1) {
        yingshaoxo_super_c_c_runner(variable_dict, while_code_block, return_value);
        if (_yingshaoxo_dict_is_string_equal(return_value, "break") == 1) {
            break;
        }
        if (_yingshaoxo_dict_is_string_equal(return_value, "exit") == 1) {
            break;
        }
        if (_yingshaoxo_dict_is_string_equal(return_value, "continue") == 1) {
            _yingshaoxo_dict_string_memory_copy(return_value, "");
        }
        yingshaoxo_dynamic_c_evaluate(variable_dict, equation, equation_result);
    }

    if (_yingshaoxo_dict_is_string_equal(return_value, "exit") == 1) {
    } else {
        _yingshaoxo_dict_string_memory_copy(return_value, "");
    }

    return while_code_block_end_index;
}

unsigned int _yingshaoxo_dynamic_c_handle_function_define(unsigned char *variable_dict, unsigned char *code) {
    unsigned int function_block_start_index = _yingshaoxo_dict_find_sub_string(code, "{");
    unsigned int function_block_end_index = _yingshaoxo_dynamic_c_get_balanced_end_symbol_index(code, '{', '}');
    unsigned int arguments_start_index = _yingshaoxo_dict_find_sub_string(code, "(");
    unsigned char function_name[_yingshaoxo_dynamic_c_temp_varaible_length];
    _yingshaoxo_dict_get_sub_string(code, 0, arguments_start_index, function_name);
    unsigned char code_block[_yingshaoxo_dynamic_c_temp_varaible_length*2];
    _yingshaoxo_dict_get_sub_string(code, function_block_start_index+1, function_block_end_index, code_block);
    yingshaoxo_dynamic_c_create_function(variable_dict, function_name, "", code_block);
    return function_block_end_index;
}

unsigned int _yingshaoxo_dynamic_c_try_to_recognize_main_keyword_and_run(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value) {
    if ((code[0] == ' ') || (code[0] == '\n')) {
        return 1;
    }

    if (_yingshaoxo_dict_string_starts_with(code, "function ")) {
        return _yingshaoxo_dynamic_c_handle_function_define(variable_dict, &code[9]) + 9 + 1;
    } else if (_yingshaoxo_dict_string_starts_with(code, "if ")) {
        return _yingshaoxo_dynamic_c_handle_if_code_block(variable_dict, code, return_value) + 1;
    } else if (_yingshaoxo_dict_string_starts_with(code, "while ")) {
        return _yingshaoxo_dynamic_c_handle_while_code_block(variable_dict, code, return_value) + 1;
    } else if (_yingshaoxo_dict_string_starts_with(code, "return ")) {
    } else if (_yingshaoxo_dict_string_starts_with(code, "try ")) {
    } else if (_yingshaoxo_dict_string_starts_with(code, "import ")) {
    } else if (_yingshaoxo_dict_string_starts_with(code, "//")) {
        return _yingshaoxo_dict_find_sub_string(code, ";") + 1;
    } else if (_yingshaoxo_dict_string_starts_with(code, "#")) {
        return _yingshaoxo_dict_find_sub_string(code, ";") + 1;
    } else if (_yingshaoxo_dict_string_starts_with(code, "break;")) {
        _yingshaoxo_dict_string_memory_copy(return_value, "break");
        return _yingshaoxo_dict_find_sub_string(code, ";") + 1;
    } else if (_yingshaoxo_dict_string_starts_with(code, "continue;")) {
        _yingshaoxo_dict_string_memory_copy(return_value, "continue");
        return _yingshaoxo_dict_find_sub_string(code, ";") + 1;
    } else if (_yingshaoxo_dict_string_starts_with(code, "exit();")) {
        _yingshaoxo_dict_string_memory_copy(return_value, "exit");
        return _yingshaoxo_dict_find_sub_string(code, ";") + 1;
    } else {
        unsigned int the_end_for_a_line =  _yingshaoxo_dict_find_sub_string(code, ";") + 1;
        /*printf("the end for a line:%d\n", the_end_for_a_line);*/
        unsigned char a_line[the_end_for_a_line+1];
        _yingshaoxo_dict_get_sub_string(code, 0, the_end_for_a_line, a_line);
        _yingshaoxo_dynamic_c_run_one_line_code(variable_dict, a_line);
        return the_end_for_a_line;
    }

    return 1;
} 

void yingshaoxo_super_c_c_runner(unsigned char *variable_dict, unsigned char *code, unsigned char *return_value) {
    unsigned int index = 0;
    unsigned int temp_index = 0;
    while (1) {
        if (code[index] == '\0') {
            return;
        }

        temp_index = _yingshaoxo_dynamic_c_try_to_recognize_main_keyword_and_run(variable_dict, &code[index], return_value);
        if (temp_index <= 0) {
            temp_index = 1;
        }
        index += temp_index;
        if (_yingshaoxo_dict_is_string_equal(return_value, "break") == 1) {
            return;
        } 
        if (_yingshaoxo_dict_is_string_equal(return_value, "continue") == 1) {
            return;
        } 
        if (_yingshaoxo_dict_is_string_equal(return_value, "exit") == 1) {
            /* you can let the python threading stop by setting the return_value to be 'exit' from outside. */
            return;
        } 
    }
    return;
}

#endif
