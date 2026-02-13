/*
int main() {
    unsigned char *test_1 = "\
set_pin_type(21, 1, 0);\n\
set_pin_value(32, 1);\n\
get_pin_value(40);\
set_pin_analog_value(50, 1.2);\
get_pin_analog_value(66);\
";
    yingshaoxo_c_pins_set_pins(test_1);
}
*/

#ifndef yingshaoxo_c_pins
#define yingshaoxo_c_pins

#include "./yingshaoxo_c_dict.h"

void _yingshaoxo_c_pins_set_pin_type(unsigned int pin_number, unsigned int input_or_output, int defualt_up_or_none_or_down) {
    /* fill with your code */
}

void _yingshaoxo_c_pins_set_pin_value(unsigned int pin_number, unsigned int new_value) {
    /* fill with your code */
}

int _yingshaoxo_c_pins_get_pin_value(unsigned int pin_number) {
    /* fill with your code */
}

void _yingshaoxo_c_pins_set_pin_analog_value(unsigned int pin_number, float voltage) {
    /* fill with your code */
}

float _yingshaoxo_c_pins_get_pin_analog_value(unsigned int pin_number) {
    /* fill with your code */
}

void yingshaoxo_c_pins_get_pins(unsigned char *return_value) {
    /*
    return "pin,number,value;"
    
    actually the above functions will do the return job. this is just a reminder for the return format.
    */
}

float _yingshaoxo_c_pins_string_to_float(unsigned char *a_string) {
    /* to baidu deepseek r1 ai: '-1.82' or '8.22' or '876' can be the input. do not use stdio.h or stdlib.h or string.h, just use the 'unsigned char *a_string' with pure c89 syntax. */
    unsigned char *p = a_string;
    float sign = 1.0f;
    float integer_part = 0.0f;
    float fractional_part = 0.0f;
    float fractional_divisor = 10.0f;
    int has_decimal_point = 0;

    while (*p == ' ') p++;

    if (*p == '-') {
        sign = -1.0f;
        p++;
    } else if (*p == '+') {
        p++;
    }

    while (*p >= '0' && *p <= '9') {
        integer_part = integer_part * 10.0f + (float)(*p - '0');
        p++;
    }

    if (*p == '.') {
        has_decimal_point = 1;
        p++;
    }

    while (*p >= '0' && *p <= '9') {
        fractional_part += (float)(*p - '0') / fractional_divisor;
        fractional_divisor *= 10.0f;
        p++;
    }

    return sign * (integer_part + fractional_part);
}

unsigned char yingshaoxo_c_pins_temp_one_line[50];
unsigned char yingshaoxo_c_pins_temp_pin_name[10];
unsigned char yingshaoxo_c_pins_temp_pin_argument_1[10];
unsigned char yingshaoxo_c_pins_temp_pin_argument_2[10];
void _yingshaoxo_c_pins_parse_pin_name_and_arguments(unsigned char *code) {
    yingshaoxo_c_pins_temp_pin_name[0] = '\0';
    yingshaoxo_c_pins_temp_pin_argument_1[0] = '\0';
    yingshaoxo_c_pins_temp_pin_argument_2[0] = '\0';

    unsigned int should_end = 0;
    unsigned int index = 0;
    unsigned int pin_name_start = _yingshaoxo_dict_find_sub_string(&code[index], "(") + 1;
    index += pin_name_start;
    unsigned int pin_name_end = _yingshaoxo_dict_find_sub_string(&code[index], ",");
    if (pin_name_end == -1) {
        pin_name_end = _yingshaoxo_dict_find_sub_string(&code[index], ")");
        should_end = 1;
    }
    _yingshaoxo_dict_get_sub_string(&code[index], 0, pin_name_end, yingshaoxo_c_pins_temp_pin_name);
    _yingshaoxo_dict_string_strip(yingshaoxo_c_pins_temp_pin_name);
    if (should_end) {
        return;
    }

    index += pin_name_end + 1;
    unsigned int argument_1_end_index = _yingshaoxo_dict_find_sub_string(&code[index], ",");
    if (argument_1_end_index == -1) {
        argument_1_end_index = _yingshaoxo_dict_find_sub_string(&code[index], ")");
        should_end = 1;
    }
    _yingshaoxo_dict_get_sub_string(&code[index], 0, argument_1_end_index, yingshaoxo_c_pins_temp_pin_argument_1);
    _yingshaoxo_dict_string_strip(yingshaoxo_c_pins_temp_pin_argument_1);
    if (should_end) {
        return;
    }

    index += argument_1_end_index + 1;
    unsigned int argument_2_end_index = _yingshaoxo_dict_find_sub_string(&code[index], ")");
    if (argument_2_end_index != -1) {
        _yingshaoxo_dict_get_sub_string(&code[index], 0, argument_2_end_index, yingshaoxo_c_pins_temp_pin_argument_2);
        _yingshaoxo_dict_string_strip(yingshaoxo_c_pins_temp_pin_argument_2);
        return;
    }
    _yingshaoxo_dict_string_memory_copy(yingshaoxo_c_pins_temp_pin_argument_2, "");
}

void yingshaoxo_c_pins_set_pins(unsigned char *code) {
    /*
    set_pin_type(pin_name, 1); //0 as input, 1 as output
    set_pin_type(pin_name, 1, 0); //1 as pull-up, 0 as none, -1 as pull-down

    set_pin_value(pin_name, 1);
    get_pin_value(pin_name);

    set_pin_analog_value(pin_name, value);
    get_pin_analog_value(pin_name);
    */
    unsigned int i = 0;
    unsigned int temp_i = 0;
    while (1) {
        while (code[i] == ' ') {
            i += 1;
        }
        while (code[i] == '\n') {
            i += 1;
        }

        if (code[i] == '\0') {
            break;
        }

        temp_i = _yingshaoxo_dict_find_sub_string(&code[i], ";") + 1;
        _yingshaoxo_dict_get_sub_string(&code[i], 0, temp_i+1, yingshaoxo_c_pins_temp_one_line);

        if (_yingshaoxo_dict_string_starts_with(yingshaoxo_c_pins_temp_one_line, "set_pin_type(") == 1) {
            _yingshaoxo_c_pins_parse_pin_name_and_arguments(yingshaoxo_c_pins_temp_one_line);
            _yingshaoxo_c_pins_set_pin_type((int)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_name)), (int)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_argument_1)), (int)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_argument_2)));
            /*print("type set.")*/
        } else if(_yingshaoxo_dict_string_starts_with(yingshaoxo_c_pins_temp_one_line, "set_pin_value(") == 1) {
            _yingshaoxo_c_pins_parse_pin_name_and_arguments(yingshaoxo_c_pins_temp_one_line);
            _yingshaoxo_c_pins_set_pin_value((int)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_name)), (int)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_argument_1)));
            /*print("value set.")*/
        } else if(_yingshaoxo_dict_string_starts_with(yingshaoxo_c_pins_temp_one_line, "get_pin_value(") == 1) {
            _yingshaoxo_c_pins_parse_pin_name_and_arguments(yingshaoxo_c_pins_temp_one_line);
            int result = _yingshaoxo_c_pins_get_pin_value((int)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_name)));
            /*print_number(result) // if not equal to -1*/
        } else if(_yingshaoxo_dict_string_starts_with(yingshaoxo_c_pins_temp_one_line, "set_pin_analog_value(") == 1) {
            _yingshaoxo_c_pins_parse_pin_name_and_arguments(yingshaoxo_c_pins_temp_one_line);
            _yingshaoxo_c_pins_set_pin_analog_value((int)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_name)), (float)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_argument_1)));
        } else if(_yingshaoxo_dict_string_starts_with(yingshaoxo_c_pins_temp_one_line, "get_pin_analog_value(") == 1) {
            _yingshaoxo_c_pins_parse_pin_name_and_arguments(yingshaoxo_c_pins_temp_one_line);
            _yingshaoxo_c_pins_get_pin_analog_value((int)(_yingshaoxo_c_pins_string_to_float(yingshaoxo_c_pins_temp_pin_name)));
        }

        if (temp_i <= 0) {
            temp_i = 1;
        }
        i += temp_i;
    }
    /*print("done.")*/
}

#endif
