/*
unsigned char global_variable_dict[1024*10] = { '\0' };

int main() {
    printf("%s\n", global_variable_dict);

    yingshaoxo_dict_set_key_and_value(global_variable_dict, "hi", "you");

    if (yingshaoxo_dict_has_key(global_variable_dict, "hi") == 0) {
        printf("no hi\n");
    } else {
        printf("has hi\n");
    }

    unsigned char a_value[10];
    yingshaoxo_dict_get_value_by_key(global_variable_dict, "hi", a_value);
    printf("%s\n", a_value);

    printf("maybe in one day, you could let the dict_string be an id_string, instead of using pure string, you use real data storage or sqlite.\n";
}
*/

#ifndef yingshaoxo_c_dict
#define yingshaoxo_c_dict

/*
unsigned char *yingshaoxo_dict_global_splitor1 = ".#new_line#.";
unsigned char *yingshaoxo_dict_global_splitor2 = "|#colon#|";
*/
unsigned char yingshaoxo_dict_global_splitor1[] = { '|', ',', ',', ',', ',', '|', '\0' };
unsigned char yingshaoxo_dict_global_splitor2[] = { '|', '>', '>', '>', '>', '|', '\0' };

void _yingshaoxo_dict_string_memory_copy(unsigned char *source_data, unsigned char *new_data) {
    /*
        source_data must be defined by 'unsigned char source_data[200]="hi";'
        'unsigned char *source_data="hi";' won't work for unknown reason
        'unsigned char *source_data=malloc(200);' works fine
    */
    unsigned int index = 0;
    while (1) {
        if (new_data[index] == '\0') {
            break;
        }
        source_data[index] = new_data[index];
        index += 1;
    }
    source_data[index] = '\0';
    return;
}

void yingshaoxo_dict_redefine_splitor(unsigned char *the_splitor1, unsigned char *the_splitor2) {
    _yingshaoxo_dict_string_memory_copy(yingshaoxo_dict_global_splitor1, the_splitor1);
    _yingshaoxo_dict_string_memory_copy(yingshaoxo_dict_global_splitor2, the_splitor2);
}

unsigned int _yingshaoxo_dict_get_string_length(unsigned char *a_string) {
    unsigned int index = 0;
    while (1) {
        if (a_string[index] == '\0') {
            break;
        }
        index += 1;
    }
    return index;
}

void _yingshaoxo_dict_add_string(unsigned char *final_string, unsigned char *left_string, unsigned char *right_string) {
    unsigned int index1 = 0;
    unsigned int index2 = 0;
    while (1) {
        if (left_string[index1] == '\0') {
            break;
        }
        final_string[index1] = left_string[index1];
        index1 += 1;
    }
    while (1) {
        if (right_string[index2] == '\0') {
            final_string[index1] = '\0';
            break;
        }
        final_string[index1] = right_string[index2];
        index2 += 1;
        index1 += 1;
    }
    final_string[index1] = '\0';
}

unsigned int _yingshaoxo_dict_find_sub_string_complex(unsigned char *parent_string, unsigned char *child_string, unsigned int start_index) {
    /*
        if not found, we return -1
        otherwise, return the_start_index_of_the_sub_string
        similar to 'read_until(source, end_string)'
    */
    if (start_index >= _yingshaoxo_dict_get_string_length(parent_string)) {
        return -1;
    }
    unsigned int index = start_index;
    unsigned int child_index = 0;
    unsigned char temp_char = '\0';
    while (1) {
        if (parent_string[index] == '\0') {
            break;
        }
        child_index = 0;
        while (1) {
            if (child_string[child_index] == '\0') {
                return index;
                break;
            }
            temp_char = parent_string[index+child_index];
            if (temp_char != child_string[child_index]) {
                break;
            }
            if (temp_char == '\0') {
                break;
            }
            child_index += 1;
        }
        index += 1;
    }
    return -1;
}

unsigned int _yingshaoxo_dict_find_sub_string(unsigned char *parent_string, unsigned char *child_string) {
    /*
        if not found, we return -1
        otherwise, return the_start_index_of_the_sub_string
    */
    return _yingshaoxo_dict_find_sub_string_complex(parent_string, child_string, 0);
}

int _yingshaoxo_dict_get_sub_string(unsigned char *a_string, unsigned int start_index, unsigned int end_index, unsigned char *sub_string) {
    /*
        if no error, we return 1
        otherwise, return 0
    */
    int return_value = 0;
    unsigned int index = 0;
    unsigned int second_index = 0;
    while (1) {
        if (a_string[index] == '\0') {
            break;
        }
        if ((start_index <= index) && (end_index > index)) {
            sub_string[second_index] = a_string[index];
            second_index += 1;
            return_value = 1;
        }
        index += 1;
    }
    sub_string[second_index] = '\0';
    return return_value;
}

int _yingshaoxo_dict_string_starts_with(unsigned char *a_string, unsigned char *start_string) {
    unsigned int index = 0;
    while (1) {
        if (start_string[index] == '\0') {
            break;
        }
        if (start_string[index] != a_string[index]) {
            return 0;
        }
        if (a_string[index] == '\0') {
            break;
        }
        index += 1;
    }
    return 1;
}

void _yingshaoxo_dict_string_strip(unsigned char *a_string) {
    if (a_string[0] == '\0') {
        return;
    }
    unsigned int real_index = -1;
    unsigned int index = 0;
    while (1) {
        if (a_string[index] == '\0') {
            break;
        }
        if (real_index == -1) {
            if ((a_string[index] != ' ') && (a_string[index] != '\n')) {
                real_index = 0;
                a_string[real_index] = a_string[index];
                real_index += 1;
            }
        } else {
            a_string[real_index] = a_string[index];
            real_index += 1;
        }
        index += 1;
    }
    a_string[real_index] = '\0';

    while (1) {
        real_index -= 1;
        if (real_index < 0) {
            break;
        }
        if ((a_string[real_index] == ' ') || (a_string[real_index] == '\n')) {
        } else {
            break;
        }
    }
    if ((real_index+1) >= 0) {
        a_string[(real_index+1)] = '\0';
    } else {
        a_string[0] = '\0';
    }
}

unsigned int _yingshaoxo_dict_is_string_equal(unsigned char *string_1, unsigned char *string_2) {
    unsigned int index = 0;
    while (1) {
        if (string_1[index] != string_2[index]) {
            return 0;
        }
        if (string_1[index] == '\0') {
            break;
        }
        if (string_2[index] == '\0') {
            break;
        }
        index += 1;
    }
    return 1;
}

int yingshaoxo_dict_has_key(unsigned char *dict_string, unsigned char *key) {
    /*
        if "splitor1 + key + splitor2" in dict_string, we return 1
        otherwise, return 0

        # the general sub_string finding algorithm is slow. they should only loop the parent string for once.
    */
    if (_yingshaoxo_dict_get_string_length(key) == 0) {
        return 0;
    }

    unsigned char temp_string[_yingshaoxo_dict_get_string_length(key) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor1) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor2) + 1];
    _yingshaoxo_dict_add_string(temp_string, yingshaoxo_dict_global_splitor1, key);
    _yingshaoxo_dict_add_string(temp_string, temp_string, yingshaoxo_dict_global_splitor2);

    if (_yingshaoxo_dict_find_sub_string(dict_string, temp_string) != -1) {
        return 1;
    }
    return 0;
}

void yingshaoxo_dict_set_key_and_value(unsigned char *dict_string, unsigned char *key, unsigned char *value) {
    /*
        splitor1 + key + splitor2 + value

        # the default string adding algorithm is slow. they copy the previous string again than appending to its tail.
    */
    if (_yingshaoxo_dict_get_string_length(key) == 0) {
        return;
    }
    if (_yingshaoxo_dict_get_string_length(value) == 0) {
        return;
    }

    unsigned char temp_string[_yingshaoxo_dict_get_string_length(key) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor1) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor2) + 1];
    _yingshaoxo_dict_add_string(temp_string, yingshaoxo_dict_global_splitor1, key);
    _yingshaoxo_dict_add_string(temp_string, temp_string, yingshaoxo_dict_global_splitor2);

    unsigned int start_index_of_temp_string = _yingshaoxo_dict_find_sub_string(dict_string, temp_string);
    if (start_index_of_temp_string == -1) {
        _yingshaoxo_dict_add_string(dict_string, dict_string, yingshaoxo_dict_global_splitor1);
        _yingshaoxo_dict_add_string(dict_string, dict_string, key);
        _yingshaoxo_dict_add_string(dict_string, dict_string, yingshaoxo_dict_global_splitor2);
        _yingshaoxo_dict_add_string(dict_string, dict_string, value);
        return;
    } else {
        unsigned int end_index_of_temp_string = start_index_of_temp_string + _yingshaoxo_dict_get_string_length(temp_string);
        int result = _yingshaoxo_dict_find_sub_string_complex(dict_string, yingshaoxo_dict_global_splitor1, end_index_of_temp_string);
        if (result == -1) {
            unsigned char end_string[_yingshaoxo_dict_get_string_length(key) + _yingshaoxo_dict_get_string_length(value) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor1) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor2) + 1];

            _yingshaoxo_dict_add_string(end_string, yingshaoxo_dict_global_splitor1, key);
            _yingshaoxo_dict_add_string(end_string, end_string, yingshaoxo_dict_global_splitor2);
            _yingshaoxo_dict_add_string(end_string, end_string, value);
            _yingshaoxo_dict_string_memory_copy(&dict_string[start_index_of_temp_string], end_string);
            return;
        } else {
            _yingshaoxo_dict_string_memory_copy(&dict_string[start_index_of_temp_string], &dict_string[result]);
            unsigned char end_string[_yingshaoxo_dict_get_string_length(key) + _yingshaoxo_dict_get_string_length(value) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor1) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor2) + 1];

            _yingshaoxo_dict_add_string(end_string, yingshaoxo_dict_global_splitor1, key);
            _yingshaoxo_dict_add_string(end_string, end_string, yingshaoxo_dict_global_splitor2);
            _yingshaoxo_dict_add_string(end_string, end_string, value);

            _yingshaoxo_dict_add_string(dict_string, dict_string, end_string);
            return;
        }
    }
}

int yingshaoxo_dict_get_value_by_key(unsigned char *dict_string, unsigned char *key, unsigned char *value) {
    /*
        if not found, we return 0
        otherwise, return 1
    */
    if (_yingshaoxo_dict_get_string_length(key) == 0) {
        value[0] = '\0';
        return 0;
    }

    unsigned char temp_string[_yingshaoxo_dict_get_string_length(key) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor1) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor2) + 1];
    _yingshaoxo_dict_add_string(temp_string, yingshaoxo_dict_global_splitor1, key);
    _yingshaoxo_dict_add_string(temp_string, temp_string, yingshaoxo_dict_global_splitor2);

    unsigned int start_index_of_temp_string = _yingshaoxo_dict_find_sub_string(dict_string, temp_string);
    if (start_index_of_temp_string == -1) {
        value[0] = '\0';
        return 0;
    }

    unsigned int end_index_of_temp_string = start_index_of_temp_string + _yingshaoxo_dict_get_string_length(temp_string);
    int result = _yingshaoxo_dict_find_sub_string_complex(dict_string, yingshaoxo_dict_global_splitor1, end_index_of_temp_string);
    if (result == -1) {
         _yingshaoxo_dict_get_sub_string(dict_string, end_index_of_temp_string, _yingshaoxo_dict_get_string_length(dict_string), value);
        return 1;
    } else {
         _yingshaoxo_dict_get_sub_string(dict_string, end_index_of_temp_string, result, value);
        return 1;
    }
}

int yingshaoxo_dict_get_value_by_key_2(unsigned char *dict_string, unsigned char *key, int *start_index, int *end_index, int *value_length) {
    /*
        if not found, we return 0
        otherwise, return 1
    */
    *start_index = 0;
    *end_index = 0;
    *value_length = 0;

    if (_yingshaoxo_dict_get_string_length(key) == 0) {
        return 0;
    }

    unsigned char temp_string[_yingshaoxo_dict_get_string_length(key) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor1) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor2) + 1];
    _yingshaoxo_dict_add_string(temp_string, yingshaoxo_dict_global_splitor1, key);
    _yingshaoxo_dict_add_string(temp_string, temp_string, yingshaoxo_dict_global_splitor2);

    unsigned int start_index_of_temp_string = _yingshaoxo_dict_find_sub_string(dict_string, temp_string);
    if (start_index_of_temp_string == -1) {
        return 0;
    }

    unsigned int end_index_of_temp_string = start_index_of_temp_string + _yingshaoxo_dict_get_string_length(temp_string);
    int result = _yingshaoxo_dict_find_sub_string_complex(dict_string, yingshaoxo_dict_global_splitor1, end_index_of_temp_string);
    if (result == -1) {
        *start_index = end_index_of_temp_string;
        *end_index = _yingshaoxo_dict_get_string_length(dict_string);
        *value_length = *end_index - *start_index;
        return 1;
    } else {
        *start_index = end_index_of_temp_string;
        *end_index = result;
        *value_length = *end_index - *start_index;
        return 1;
    }
}

void yingshaoxo_dict_delete_a_key(unsigned char *dict_string, unsigned char *key) {
    if (_yingshaoxo_dict_get_string_length(key) == 0) {
        return;
    }

    unsigned char temp_string[_yingshaoxo_dict_get_string_length(key) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor1) + _yingshaoxo_dict_get_string_length(yingshaoxo_dict_global_splitor2) + 1];
    _yingshaoxo_dict_add_string(temp_string, yingshaoxo_dict_global_splitor1, key);
    _yingshaoxo_dict_add_string(temp_string, temp_string, yingshaoxo_dict_global_splitor2);

    unsigned int start_index_of_temp_string = _yingshaoxo_dict_find_sub_string(dict_string, temp_string);
    if (start_index_of_temp_string == -1) {
        return;
    } else {
        unsigned int end_index_of_temp_string = start_index_of_temp_string + _yingshaoxo_dict_get_string_length(temp_string);
        int result = _yingshaoxo_dict_find_sub_string_complex(dict_string, yingshaoxo_dict_global_splitor1, end_index_of_temp_string);
        if (result == -1) {
            dict_string[start_index_of_temp_string] = '\0';
            return;
        } else {
            _yingshaoxo_dict_string_memory_copy(&dict_string[start_index_of_temp_string], &dict_string[result]);
            return;
        }
    }
}

/*
void yingshaoxo_dict_get_all_keys(unsigned char *dict_string, unsigned char *key_list_string) {
    each key splited by 0x03, the whole string end with '\0';
}

void yingshaoxo_dict_get_all_values(unsigned char *dict_string, unsigned char *value_list_string) {
    each value splited by 0x03, the whole string end with '\0'
}
*/

#endif
