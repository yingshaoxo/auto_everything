// A thing to mention is: **Why python is 60 times slower than c code?** Because for each variable, for example, string variable, it has more data structure than char*. And when we parse the python code, it takes time.
//
//
//
// #ifndef stdio.h
// #define stdio.h
#include <stdio.h>
// #endif
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

/*
Say hello to yingshaoxo.
*/
void hello_yingshaoxo()
{
    printf("Hello, world!\n");
}

/*
##################################################
Let's give those built-in c functions another name
##################################################
*/

// We could directly use '#define' to set a global replacement for function, but for the argurments hint, I choose not to do so.
// #define _ypython_resize_memory_block(buf,size) realloc(buf, size)

/*
Print formated string.
*/
/*
#define _ypython_print_formated_string(string_format, ...) printf(string_format, __VA_ARGS__);                \
*/
void _ypython_print_formated_string(const char* format, ...) {
    va_list arg;
    va_start(arg, format);
    vprintf(format, arg);
    va_end(arg);
    fflush(stdout);
}

/*
The sprintf() function is used to print formatted data to buffer.
*/
//#define _ypython_string_format(result_string, string_format, ...) sprintf(result_string, string_format, __VA_ARGS__);
char* _ypython_string_format(const char* fmt, ...) {
    // copied from baidu ai
    va_list args;
    va_start(args, fmt);
    
    int len = vsnprintf(NULL, 0, fmt, args);
    if (len < 0) { va_end(args); return NULL; }
    
    char* buf = malloc(len + 1);
    if (!buf) { va_end(args); return NULL; }
    
    va_end(args);
    va_start(args, fmt);
    vsnprintf(buf, len + 1, fmt, args);
    va_end(args);
    
    return buf;
}

/*
`scanf` is a function that stands for Scan Formatted String. It is used to read data from stdin (standard input stream i.e. usually keyboard) and then writes the result into the given arguments.

It accepts character, string, and numeric data from the user using standard input.
scanf also uses format specifiers like printf.
*/
#define _ypython_scan_formated_string(string_format, ...) scanf(string_format, __VA_ARGS__);                \

/*
Get the absolute value of a floating point number.
*/

double _ypython_get_float_absolute_value(double __x) {
    return fabs(__x);
}

/*
malloc() allocates the requested memory and returns a pointer to it.
 */
void *_ypython_memory_allocation_for_data(size_t size) {
    return malloc(size);
}

/*
The C library function `void *realloc(void *ptr, size_t size)` attempts to resize the memory block pointed to by `ptr` that was previously allocated with a call to `malloc` or `calloc`.
*/
void *_ypython_resize_memory_block_for_a_pointer(void *__ptr, size_t __size)
{
    return realloc(__ptr, __size);
}

/*
Get a newline-terminated string of finite length from STREAM.

This function is a possible cancellation point and therefore not
marked with __THROW.
*/
char *_ypython_get_a_newline_terminated_string_of_finite_length_from_a_STREAM(char *__restrict__ __s, int __n, FILE *__restrict__ __stream)
{
    return fgets(__s, __n, __stream);
}

/*
Return the EOF(end of file) indicator for STREAM. If the end, return 1, otherwise, 0.
*/
int _ypython_return_end_of_file_indicator_for_a_STREAM(FILE *__stream)
{
    return feof(__stream);
}

/*
The C library function `size_t strlen(const char *str)` computes the length of the string `str` up to, but not including the terminating null character.
*/
size_t _ypython_get_string_length(const char *__s)
{
    return strlen(__s);
}

/*
The popen function executes the shell command command as a subprocess.
However, instead of waiting for the command to complete, it creates a pipe to the subprocess and returns a stream that corresponds to that pipe.
*/
FILE *_ypython_execute_shell_command_as_a_subprocess_pipe_stream(const char *command, const char *mode)
{
    return popen(command, mode);
}

/*
The pclose() function closes a stream that was opened by popen(), waits for the command specified as an argument in popen() to terminate.
It returns the status of the process that was running the shell command.
*/
int _ypython_close_subprocess_pipe_stream(FILE *stream)
{
    return pclose(stream);
}

/*
The strcmp() compares two strings character by character. If the strings are equal, the function returns 0.
*/
int _ypython_string_compare(const char *str1, const char *str2)
{
    return strcmp(str1, str2);
}

/*
The C library function `char *strcat(char *dest, const char *src)` appends the string pointed to by src to the end of the string pointed to by dest.
In other words, second string will get added to the end of the first string.
*/
char *_ypython_string_adding(char *dest, const char *src) {
    return strcat(dest, src);
}

/*
The C library function `char *strstr(const char *haystack, const char *needle)` function finds the first occurrence of the substring needle in the string haystack. 
It will return null pointer if the sub_sequence is not present in haystack.
The terminating '\0' characters are not compared.
*/
const char *_ypython_find_the_first_sub_string_in_a_string(const char *a_string, const char *sub_string) {
    return strstr(a_string, sub_string);
}

/*
The fopen() method in C is used to open a file to perform various operations which include reading, writing, etc.
The function is used to return a pointer to FILE if the execution succeeds else NULL is returned. 

mode_of_operation: 
    r: read
    w: write
    a: append data to the end of file
    rb: read binary bytes stream
    wb: write binary bytes stream
*/
FILE *_ypython_file_open(const char *file_name, const char *mode_of_operation) {
    return fopen(file_name, mode_of_operation);
}

int _ypython_file_close(FILE *stream) {
    return fclose(stream);
}

int _ypython_file_get_character(FILE *pointer) {
    return fgetc(pointer);
}

int _ypython_file_put_character(int character, FILE *pointer) {
    return fputc(character, pointer);
}

int _ypython_string_to_int(char *number_string) {
    return atoi(number_string);
}

float _ypython_string_to_float(char *number_string) {
    return atof(number_string);
}


/*
##################################################
Let's use those built-in c functions to do some useful things
##################################################
*/

bool _ypython_string_is_string_equal(const char* x, const char* y)
{
    int flag = 0;
 
    // Iterate a loop till the end
    // of both the strings
    while (*x != '\0' || *y != '\0') {
        if (*x == *y) {
            x++;
            y++;
        }
 
        // If two characters are not same
        // print the difference and exit
        else if ((*x == '\0' && *y != '\0')
                 || (*x != '\0' && *y == '\0')
                 || *x != *y) {
            flag = 1;
            break;
        }
    }
 
    // If two strings are exactly same
    if (flag == 0) {
        return true;
    } else {
        return false;
    }
}

bool _ypython_string_is_sub_string(const char *a_string, const char *sub_string) {
    if (_ypython_find_the_first_sub_string_in_a_string(a_string, sub_string) != NULL) {
        return true;
    } else {
        return false;
    }
}

long long _ypython_string_count_sub_string(const char *a_string, const char *sub_string) {
    long long counting = 0;
    const char *temprary = a_string;
    temprary = _ypython_find_the_first_sub_string_in_a_string(temprary, sub_string);
    while (temprary != NULL) {
        counting++;

        temprary++;
        temprary = _ypython_find_the_first_sub_string_in_a_string(temprary, sub_string);
    }
    return counting;
}

bool _ypython_is_general_space(char c)
{
    switch (c)
    {
    case ' ':
    case '\n':
    case '\t':
    case '\f':
    case '\r':
        return true;
        break;
    default:
        return false;
        break;
    }
}

char *_ypython_string_left_strip(char *s)
{
    while (_ypython_is_general_space(*s))
    {
        s++;
    }
    return s;
}

char *_ypython_string_right_strip(char *s)
{
    char *back = s + strlen(s) - 1;
    while (_ypython_is_general_space(*back))
    {
        --back;
    }
    *(back + 1) = '\0';
    return s;
}

/*
strip \s before and after a string.
*/
const char *ypython_string_strip(char *s)
{
    return (const char *)_ypython_string_right_strip(_ypython_string_left_strip(s));
}

/*
copy char* string
*/
char *ypython_string_copy(char *source_string)
{
    size_t string_length = 0;
    while (true) {
        if (source_string[string_length] == '\0') {
            string_length += 1;
            break;
        }
        string_length += 1;
    }

    char *new_string = _ypython_memory_allocation_for_data(sizeof(char) * string_length);
    size_t index = 0;
    while (true) {
        if (index >= string_length) {
            break;
        }
        new_string[index] = source_string[index];
        index += 1;
    }

    return new_string;
}

char *_ypython_get_infinate_length_text_line(FILE *f)
{
    size_t size = 0;
    size_t len = 0;
    size_t last = 0;
    char *buf = NULL;

    do
    {
        size += BUFSIZ;                                              /* BUFSIZ is defined as "the optimal read size for this platform" */
        buf = (char *) _ypython_resize_memory_block_for_a_pointer(buf, size); /* realloc(NULL,n) is the same as malloc(n) */
        /* Actually do the read. Note that fgets puts a terminal '\0' on the
           end of the string, so we make sure we overwrite this */
        if (buf == NULL)
            return NULL;
        _ypython_get_a_newline_terminated_string_of_finite_length_from_a_STREAM(buf + last, BUFSIZ, f);
        len = _ypython_get_string_length(buf);
        last = len - 1;
    } while (!_ypython_return_end_of_file_indicator_for_a_STREAM(f) && buf[last] != '\n');

    return buf;
}

char *_ypython_get_infinate_length_text(FILE *f)
{
    size_t size = 0;
    size_t len = 0;
    size_t last = 0;
    char *buf = NULL;

    do
    {
        size += BUFSIZ;                                              /* BUFSIZ is defined as "the optimal read size for this platform" */
        buf = (char *)_ypython_resize_memory_block_for_a_pointer(buf, size); /* realloc(NULL,n) is the same as malloc(n) */
        /* Actually do the read. Note that fgets puts a terminal '\0' on the
           end of the string, so we make sure we overwrite this */
        if (buf == NULL)
            return NULL;
        _ypython_get_a_newline_terminated_string_of_finite_length_from_a_STREAM(buf + last, BUFSIZ, f);
        len = _ypython_get_string_length(buf);
        last = len - 1;

        if (buf[last] == '\n')
        {
            last = len;
        }
    } while (!_ypython_return_end_of_file_indicator_for_a_STREAM(f));

    return buf;
}

/*
Run a bash command and return the result as a string.
*/
/*
const char *ypython_run_command(const char *bash_command_line)
{
    FILE *FileOpen;
    FileOpen = _ypython_execute_shell_command_as_a_subprocess_pipe_stream(bash_command_line, "r");

    char *all_lines = _ypython_get_infinate_length_text(FileOpen);
    _ypython_close_subprocess_pipe_stream(FileOpen);

    return all_lines;
}
*/

/*
Run a bash command and wait for it to get finished, it won't return anything.
*/
/*
void ypython_run(const char *bash_command_line)
{
    FILE *FileOpen;
    FileOpen = _ypython_execute_shell_command_as_a_subprocess_pipe_stream(bash_command_line, "r");

    while (!_ypython_return_end_of_file_indicator_for_a_STREAM(FileOpen))
    {
        char *a_line = _ypython_get_infinate_length_text_line(FileOpen);
        printf("%s", a_line);
    }

    _ypython_close_subprocess_pipe_stream(FileOpen);
}
*/

/*
Python_like print function.
*/
void ypython_raw_print(void *value); //function pre_define
void ypython_print(void *text)
{
    //printf("%s\n", (char *)text);
    ypython_raw_print(text);
    printf("%s", "\n");
}
/*
void ypython_print(const char *text, ...)
{
    // this should work, but not work
    
    va_list variable_pointer;
    va_start(variable_pointer, text);

    printf("%s ", text);

    for (int i=0; i < 2; i++) {
        char* a_string = va_arg(variable_pointer, char *);
        if (a_string == NULL) {
            break;
        }
        printf("%s ", a_string);
    }

    printf("\n");

    va_end(variable_pointer);
}
*/

/*
Python_like exit function.
*/
void ypython_exit()
{
    exit(0);
}

/*
##################################################
Let's create some built-in data types that similar to python data types
For example, str, double, int, bool, dict, list and so on
##################################################
*/

/*
Forward declarations
*/
typedef struct Type_Ypython_None Type_Ypython_None;
typedef struct Type_Ypython_String Type_Ypython_String;
typedef struct Type_Ypython_Bool Type_Ypython_Bool;
typedef struct Type_Ypython_Int Type_Ypython_Int;
typedef struct Type_Ypython_Float Type_Ypython_Float;
typedef struct Type_Ypython_General Type_Ypython_General;
typedef struct _Ypython_Linked_List_Node _Ypython_Linked_List_Node;
typedef struct Type_Ypython_List Type_Ypython_List;
typedef struct Type_Ypython_Dict Type_Ypython_Dict;

Type_Ypython_None *Ypython_None();
Type_Ypython_Bool *Ypython_Bool(bool value);
Type_Ypython_String *Ypython_String(char *value);
Type_Ypython_Int *Ypython_Int(long long value);
Type_Ypython_Float *Ypython_Float(long double value);
Type_Ypython_General *Ypython_General();
Type_Ypython_List *Ypython_List();
Type_Ypython_Dict *Ypython_Dict();

Type_Ypython_General *_Ypython_copy_general_variable(Type_Ypython_General *value);

/*
None type
*/
typedef struct Type_Ypython_None Type_Ypython_None;
struct Type_Ypython_None {
    bool is_none;
    char *type;
    int value;
};

Type_Ypython_None *Ypython_None() {
    Type_Ypython_None *new_none_value;
    new_none_value = (Type_Ypython_None *)malloc(sizeof(Type_Ypython_None));

    new_none_value->is_none = true;
    new_none_value->type = (char *)"none";

    new_none_value->value = 0;

    return new_none_value;
}


/*
String type

Tip: You can use wchar to replace char* to support utf-8 characters.
*/
typedef struct Type_Ypython_String Type_Ypython_String;
struct Type_Ypython_String {
    bool is_none;
    char *type;

    char *value;
    long long length;

    Type_Ypython_String* (*function_add)(Type_Ypython_String *self, Type_Ypython_String *another_string);
    bool (*function_is_equal)(Type_Ypython_String *self, Type_Ypython_String *another_string);
    //Type_Ypython_List *(*function_split)(Type_Ypython_String *self, Type_Ypython_String *seperator_string);
    //Type_Ypython_String *(*function_join)(Type_Ypython_String *self, Type_Ypython_List *string_list, Type_Ypython_String *seperator_string);
    Type_Ypython_String *(*function_strip)(Type_Ypython_String *self, Type_Ypython_String *characters);
    bool (*function_startswith)(Type_Ypython_String *self, Type_Ypython_String *a_string);
    bool (*function_endswith)(Type_Ypython_String *self, Type_Ypython_String *a_string);
    long long (*function_length)(Type_Ypython_String *self);
    bool (*function_is_substring)(Type_Ypython_String *self, Type_Ypython_String *a_string);
    Type_Ypython_String *(*function_substring)(Type_Ypython_String *self, long long start_index, long long end_index);
};

Type_Ypython_String *Ypython_String(char *value);
Type_Ypython_String *Type_Ypython_String_add(Type_Ypython_String *self, Type_Ypython_String *another_string) {
    Type_Ypython_String *new_string_value = Ypython_String((char *)"");

    if (self->is_none || another_string->is_none) {
        new_string_value->value = (char *)"";
        new_string_value->length = strlen(new_string_value->value);
        new_string_value->is_none = true;
    } else {
        new_string_value->is_none = false;

        size_t total_length = _ypython_get_string_length(self->value) + _ypython_get_string_length(another_string->value) + 1;
        char *new_chars_value = (char *)malloc(total_length);
        snprintf(new_chars_value, total_length, "%s%s", self->value, another_string->value);

        new_string_value->value = new_chars_value;
        new_string_value->length = strlen(new_string_value->value);
    }

    return new_string_value;

    /*
    Type_Ypython_String *new_string_value = Ypython_String((char *)"");

    if (self->is_none || another_string->is_none) {
        new_string_value->value = (char *)"";
        new_string_value->length = 0;
        new_string_value->is_none = true;
        return new_string_value;
    }

    new_string_value->is_none = false;

    // Calculate total length including null terminator
    size_t self_len = strlen(self->value);
    size_t another_len = strlen(another_string->value);
    size_t total_length = self_len + another_len + 1;  // +1 for null terminator

    // Allocate memory for the new string
    char *new_chars_value = (char *)malloc(total_length);
    if (new_chars_value == NULL) {
        new_string_value->is_none = true;
        return new_string_value;
    }

    // Copy first string
    strcpy(new_chars_value, self->value);
    // Append second string
    strcat(new_chars_value, another_string->value);

    // Set the new string value
    new_string_value->value = new_chars_value;
    new_string_value->length = total_length - 1;  // -1 because we don't count null terminator

    return new_string_value;
    */
}

bool Type_Ypython_String_is_equal(Type_Ypython_String *self, Type_Ypython_String *another_string) {
    if (self->is_none && another_string->is_none) {
        return true;
    }
    else if ((!(self->is_none)) && (another_string->is_none)) {
        return false;
    }
    else if ((self->is_none) && (!(another_string->is_none))) {
        return false;
    } else {
        if (_ypython_string_is_string_equal(self->value, another_string->value)) {
            return true;
        } else {
            return false;
        }   
    }
}

/*
Type_Ypython_List *Type_Ypython_String_split(Type_Ypython_String *self, Type_Ypython_String *seperator_string) {
    Type_Ypython_List *result_list = Ypython_List();

    char *token;
    char *str = self->value;
    char *sep = seperator_string->value;

    token = strtok(str, sep);
    while(token != NULL) {
        Type_Ypython_String *new_string = Ypython_String(strdup(token));

        Type_Ypython_General *a_general_variable = Ypython_General();
        a_general_variable->string_ = new_string;

        result_list->function_append(result_list, a_general_variable);

        token = strtok(NULL, sep);
    }

    return result_list;
}
*/

/*
Type_Ypython_String *Type_Ypython_String_join(Type_Ypython_String *self, Type_Ypython_List *string_list, Type_Ypython_String *seperator_string) {
    return NULL;
}
*/

Type_Ypython_String *Type_Ypython_String_substring(Type_Ypython_String *self, long long start_index, long long end_index) {
    Type_Ypython_String *default_string = Ypython_String("");
    default_string->is_none = true;

    if (start_index > end_index) {
        return default_string;
    }

    if (self->is_none || ((start_index < 0) || (end_index > self->length))) {
        return default_string;
    }

    end_index -= 1;

    char *str = self->value;
    long long result_len = end_index - start_index + 1;
    char *result = (char *)malloc((result_len + 1) * sizeof(char));
    strncpy(result, str + start_index, result_len);
    result[result_len] = '\0';

    return Ypython_String(result);
}

bool Type_Ypython_String_is_substring(Type_Ypython_String *self, Type_Ypython_String *a_string) {
    char *str = self->value;
    char *substring = a_string->value;
    return _ypython_find_the_first_sub_string_in_a_string(str, substring) != NULL;
}

Type_Ypython_String *Type_Ypython_String_strip(Type_Ypython_String *self, Type_Ypython_String *characters) {
    long long len = strlen(self->value);
    char *str = self->value;

    long long start = 0;
    long long end = len - 1;

    if (characters != NULL) {
        char *ch = characters->value;

        while (start < len && strchr(ch, str[start]) != NULL) {
            start++;
        }

        while (end >= start && strchr(ch, str[end]) != NULL) {
            end--;
        }
    }

    return self->function_substring(self, start, end+1);
}

bool Type_Ypython_String_startswith(Type_Ypython_String *self, Type_Ypython_String *a_string) {
    char *str = self->value;
    char *prefix = a_string->value;
    int str_len = strlen(str);
    int prefix_len = strlen(prefix);

    if (str_len < prefix_len) {
        return false;
    }

    for (int i = 0; i < prefix_len; i++) {
        if (str[i] != prefix[i]) {
            return false;
        }
    }

    return true;
}

bool Type_Ypython_String_endswith(Type_Ypython_String *self, Type_Ypython_String *a_string) {
    char *str = self->value;
    char *tail = a_string->value;

    int str_length = strlen(str);
    int tail_length = strlen(tail);

    if (str_length < tail_length) {
        return false;
    }

    int another_i = str_length - 1;
    for (int i = tail_length-1; i >= 0 ; i--) {
        if (str[another_i] != tail[i]) {
            return false;
        }
        another_i = another_i - 1;
    }

    return true;
}

Type_Ypython_String *Ypython_String(char *value) {
    Type_Ypython_String *new_string_value;
    new_string_value = (Type_Ypython_String *)malloc(sizeof(Type_Ypython_String));

    new_string_value->is_none = false;
    new_string_value->type = (char *)"string";

    new_string_value->length = strlen(value);
    new_string_value->value = ypython_string_copy(value);
    //new_string_value->value = strdup(value);

    new_string_value->function_add = &Type_Ypython_String_add;
    new_string_value->function_is_equal = &Type_Ypython_String_is_equal;
    //new_string_value->function_split = &Type_Ypython_String_split; // I want to use this, but hit errors
    //new_string_value->function_join = &Type_Ypython_String_join;
    new_string_value->function_substring = &Type_Ypython_String_substring;
    new_string_value->function_is_substring = &Type_Ypython_String_is_substring;
    new_string_value->function_strip = &Type_Ypython_String_strip;
    new_string_value->function_startswith = &Type_Ypython_String_startswith;
    new_string_value->function_endswith = &Type_Ypython_String_endswith;

    return new_string_value;
}


/*
Bool type
*/
typedef struct Type_Ypython_Bool Type_Ypython_Bool;
struct Type_Ypython_Bool {
    bool is_none;
    char *type;
    bool value;
};

Type_Ypython_Bool *Ypython_Bool(bool value) {
    Type_Ypython_Bool *new_bool_value;
    new_bool_value = (Type_Ypython_Bool *)malloc(sizeof(Type_Ypython_Bool));

    new_bool_value->is_none = false;
    new_bool_value->type = (char *)"bool";

    new_bool_value->value = value;

    return new_bool_value;
}


/*
Int type
*/
typedef struct Type_Ypython_Int Type_Ypython_Int;
struct Type_Ypython_Int {
    bool is_none;
    char *type;
    long long value;

    Type_Ypython_Int *(*function_add)(Type_Ypython_Int *self, Type_Ypython_Int *another_int);
    Type_Ypython_Int *(*function_multiply)(Type_Ypython_Int *self, Type_Ypython_Int *another_int);
};

Type_Ypython_Int *Ypython_Int(long long value);

Type_Ypython_Int *Type_Ypython_Int_add(Type_Ypython_Int *self, Type_Ypython_Int *another_int) {
    Type_Ypython_Int *new_int_value = Ypython_Int(0);

    if (self->is_none || another_int->is_none) {
        new_int_value->value = 0;
        new_int_value->is_none = true;
        return new_int_value;
    } else {
        new_int_value->is_none = false;
        new_int_value->value = self->value + another_int->value;
        return new_int_value;
    }
}

Type_Ypython_Int *Type_Ypython_Int_multiply(Type_Ypython_Int *self, Type_Ypython_Int *another_int) {
    Type_Ypython_Int *new_int_value = Ypython_Int(0);

    if (self->is_none || another_int->is_none) {
        new_int_value->value = 0;
        new_int_value->is_none = true;
        return new_int_value;
    } else {
        new_int_value->is_none = false;
        new_int_value->value = self->value * another_int->value;
        return new_int_value;
    }
}

Type_Ypython_Int *Ypython_Int(long long value) {
    Type_Ypython_Int *new_int_value;
    new_int_value = (Type_Ypython_Int *)malloc(sizeof(Type_Ypython_Int));

    new_int_value->is_none = false;
    new_int_value->type = (char *)"int";

    new_int_value->value = value;

    new_int_value->function_add = &Type_Ypython_Int_add;
    new_int_value->function_multiply = &Type_Ypython_Int_multiply;

    return new_int_value;
}


/*
Float type
*/
typedef struct Type_Ypython_Float Type_Ypython_Float;
struct Type_Ypython_Float {
    bool is_none;
    char *type;
    long double value;

    Type_Ypython_Float *(*function_add)(Type_Ypython_Float *self, Type_Ypython_Float *another_float);
    Type_Ypython_Float *(*function_multiply)(Type_Ypython_Float *self, Type_Ypython_Float *another_float);
};

Type_Ypython_Float *Ypython_Float(long double value);

Type_Ypython_Float *Type_Ypython_Float_add(Type_Ypython_Float *self, Type_Ypython_Float *another_float) {
    Type_Ypython_Float *new_float_value = Ypython_Float(0.0);

    if (self->is_none || another_float->is_none) {
        new_float_value->value = 0;
        new_float_value->is_none = true;
        return new_float_value;
    } else {
        new_float_value->is_none = false;
        new_float_value->value = self->value + another_float->value;
        return new_float_value;
    }
}

Type_Ypython_Float *Type_Ypython_Float_multiply(Type_Ypython_Float *self, Type_Ypython_Float *another_float) {
    Type_Ypython_Float *new_float_value = Ypython_Float(0.0);

    if (self->is_none || another_float->is_none) {
        new_float_value->value = 0;
        new_float_value->is_none = true;
        return new_float_value;
    } else {
        new_float_value->is_none = false;
        new_float_value->value = self->value * another_float->value;
        return new_float_value;
    }
}

Type_Ypython_Float *Ypython_Float(long double value) {
    Type_Ypython_Float *new_float_value;
    new_float_value = (Type_Ypython_Float *)malloc(sizeof(Type_Ypython_Float));

    new_float_value->is_none = false;
    new_float_value->type = (char *)"float";

    new_float_value->value = value;

    new_float_value->function_add = &Type_Ypython_Float_add;
    new_float_value->function_multiply = &Type_Ypython_Float_multiply;

    return new_float_value;
}


/*
Forward declaration for: List, Dict
*/
typedef struct Type_Ypython_List Type_Ypython_List;
typedef struct Type_Ypython_Dict Type_Ypython_Dict;


/*
General type
*/
typedef struct Type_Ypython_General Type_Ypython_General;
struct Type_Ypython_General {
    bool is_none;
    char *type;

    Type_Ypython_Bool *bool_;
    Type_Ypython_Float *float_;
    Type_Ypython_Int *int_;
    Type_Ypython_String *string_;
    Type_Ypython_List *list_;
    Type_Ypython_Dict *dict_;
    void *anything_;

    bool (*function_is_equal)(Type_Ypython_General *element_1, Type_Ypython_General *element_2);
};

bool Type_Ypython_General_is_equal(Type_Ypython_General *element_1, Type_Ypython_General *element_2) {
    if (element_1->is_none && element_2->is_none) {
        return true;
    }
    else if ((!(element_1->is_none)) && (element_2->is_none)) {
        return false;
    }
    else if ((element_1->is_none) && (!(element_2->is_none))) {
        return false;
    } else {
        if ((element_1->bool_ != NULL) && (element_2->bool_ != NULL)) {
            if (element_1->bool_->is_none && element_2->bool_->is_none) {
                return true;
            } else if ((element_1->bool_->is_none) && (!element_2->bool_->is_none)) {
                return false;
            } else if ((!element_1->bool_->is_none) && (element_2->bool_->is_none)) {
                return false;
            } else if ((!element_1->bool_->is_none) && (!element_2->bool_->is_none)) {
                if (element_1->bool_->value == element_2->bool_->value) {
                    return true;
                }
            }
        }

        if ((element_1->float_ != NULL) && (element_2->float_ != NULL)) {
            if (element_1->float_->is_none && element_2->float_->is_none) {
                return true;
            } else if ((element_1->float_->is_none) && (!element_2->float_->is_none)) {
                return false;
            } else if ((!element_1->float_->is_none) && (element_2->float_->is_none)) {
                return false;
            } else if ((!element_1->float_->is_none) && (!element_2->float_->is_none)) {
                if (element_1->float_->value == element_2->float_->value) {
                    return true;
                }
            }
        }

        if ((element_1->int_ != NULL) && (element_2->int_ != NULL)) {
            if (element_1->int_->is_none && element_2->int_->is_none) {
                return true;
            } else if ((element_1->int_->is_none) && (!element_2->int_->is_none)) {
                return false;
            } else if ((!element_1->int_->is_none) && (element_2->int_->is_none)) {
                return false;
            } else if ((!element_1->int_->is_none) && (!element_2->int_->is_none)) {
                if (element_1->int_->value == element_2->int_->value) {
                    return true;
                }
            }
        }

        if ((element_1->string_ != NULL) && (element_2->string_ != NULL)) {
            if (element_1->string_->is_none && element_2->string_->is_none) {
                return true;
            } else if ((element_1->string_->is_none) && (!element_2->string_->is_none)) {
                return false;
            } else if ((!element_1->string_->is_none) && (element_2->string_->is_none)) {
                return false;
            } else if ((!element_1->string_->is_none) && (!element_2->string_->is_none)) {
                if (element_1->string_->function_is_equal(element_1->string_, element_2->string_)) {
                    return true;
                }
            }
        }
    }
    return false;
}

Type_Ypython_General *Ypython_General() {
    Type_Ypython_General *new_value;
    new_value = (Type_Ypython_General *)malloc(sizeof(Type_Ypython_General));

    new_value->is_none = false;
    new_value->type = (char *)"general";

    new_value->bool_ = NULL;
    new_value->float_ = NULL;
    new_value->int_ = NULL;
    new_value->string_ = NULL;
    new_value->list_ = NULL;
    new_value->dict_ = NULL;
    new_value->anything_ = NULL;

    new_value->function_is_equal = &Type_Ypython_General_is_equal;

    return new_value;
}


/*
List type

A good list data type has to have:
1. infinity list size increasing in real time
2. automatically garbage collection

Tip: If you know the length of that list when you creat it, you should use normal c_list. Only when you change list length later, you use linked list.
*/
/*
typedef struct _Ypython_Linked_List_Node _Ypython_Linked_List_Node;
struct _Ypython_Linked_List_Node {
    Type_Ypython_General *value;
    _Ypython_Linked_List_Node *next;
};

typedef struct Type_Ypython_List Type_Ypython_List;
struct Type_Ypython_List {
    bool is_none;
    char *type;

    _Ypython_Linked_List_Node *head;
    _Ypython_Linked_List_Node *tail;
    long long length;

    bool iteration_not_done;
    _Ypython_Linked_List_Node *_current_iterate_node;

    void (*function_append)(Type_Ypython_List *self, Type_Ypython_General *an_element);
    Type_Ypython_Int *(*function_index)(Type_Ypython_List *self, Type_Ypython_General *an_element);
    void (*function_delete)(Type_Ypython_List *self, long long index);
    void (*function_insert)(Type_Ypython_List *self, long long index, Type_Ypython_General *an_element);
    void (*function_set)(Type_Ypython_List *self, long long index, Type_Ypython_General *an_element);
    Type_Ypython_General* (*function_get)(Type_Ypython_List *self, long long index);
    Type_Ypython_List* (*function_sublist)(Type_Ypython_List *self, long long start_index, long long end_index);
    void (*function_start_iteration)(Type_Ypython_List *self);
    Type_Ypython_General* (*function_get_next_one)(Type_Ypython_List *self);
};

// Function to create a new linked list node
_Ypython_Linked_List_Node *_Ypython_create_list_Node(Type_Ypython_General *value) {
    _Ypython_Linked_List_Node *newNode = (_Ypython_Linked_List_Node *)malloc(sizeof(_Ypython_Linked_List_Node));
    newNode->value = value;
    newNode->next = NULL;
    return newNode;
}

Type_Ypython_List *Ypython_List();
void Type_Ypython_List_append(Type_Ypython_List *self, Type_Ypython_General *an_element) {
    if (self->is_none) {
        return;
    }

    _Ypython_Linked_List_Node *newNode = _Ypython_create_list_Node(an_element);

    if (self->head == NULL) {
        self->head = newNode;
        self->tail = newNode;
    } else {
        self->tail->next = newNode;
        self->tail = newNode;
    }

    self->length = self->length + 1;
    return;
}

Type_Ypython_Int *Type_Ypython_List_index(Type_Ypython_List *self, Type_Ypython_General *an_element) {
    Type_Ypython_Int *index = Ypython_Int(-1);

    if (self->is_none) {
        index->is_none = true;
        return index;
    } else {
        int i = 0;
        _Ypython_Linked_List_Node *current_node = self->head;

        if (current_node == NULL) {
            // 0 elements inside;
            index->is_none = true;
            return index;
        }

        while (current_node != NULL) {
            if (current_node->value->function_is_equal(current_node->value, an_element)) {
                index->value = i;
                return index;
            }
            current_node = current_node->next;
            i++;
        }
    }

    index->is_none = true;
    return index;
}

void Type_Ypython_List_delete(Type_Ypython_List *self, long long index) {
    if (self->is_none || ((index < 0) || (index >= self->length))) {
        return;
    }

    _Ypython_Linked_List_Node *current_node = self->head;
    _Ypython_Linked_List_Node *previous_node = NULL;

    if (index == 0) {
        // Delete the head node
        self->head = current_node->next;
        if (self->head == NULL) {
            // If the list becomes empty, update the tail as well
            self->tail = NULL;
        }
        free(current_node->value); // Free the value stored in the node
        free(current_node);        // Free the node itself
    } else {
        // Traverse the list to find the node to delete
        for (long long i = 0; i < index; i++) {
            previous_node = current_node;
            current_node = current_node->next;
        }

        // Update the links to bypass the node to delete
        previous_node->next = current_node->next;

        // Update the tail if the last node is deleted
        if (current_node->next == NULL) {
            self->tail = previous_node;
        }

        free(current_node->value); // Free the value stored in the node
        free(current_node);        // Free the node itself
    }

    self->length--; // Decrement the length of the list
}

void Type_Ypython_List_insert(Type_Ypython_List *self, long long index, Type_Ypython_General *an_element) {
    if (self->is_none || ((index < 0) || (index > self->length))) {
        return;
    }

    _Ypython_Linked_List_Node *newNode = _Ypython_create_list_Node(an_element);
    if (newNode == NULL) {
        fprintf(stderr, "Memory allocation failed in insert\n");
        exit(1);
    }

    if (index == 0) {
        // Insert at the head
        newNode->next = self->head;
        self->head = newNode;
        if (self->tail == NULL) {
            // If the list was empty, update the tail as well
            self->tail = newNode;
        }
    } else {
        // Traverse the list to find the node before the insertion point
        _Ypython_Linked_List_Node *current_node = self->head;
        for (long long i = 0; i < index - 1; i++) {
            current_node = current_node->next;
        }

        // Insert the new node
        // In here, the current_node becomes previous node
        newNode->next = current_node->next;
        current_node->next = newNode;

        // Update the tail if the new node is inserted at the end
        if (newNode->next == NULL) {
            self->tail = newNode;
        }
    }

    self->length++; // Increment the length of the list
}

void Type_Ypython_List_set(Type_Ypython_List *self, long long index, Type_Ypython_General *an_element) {
    if (self->is_none || ((index < 0) || (index >= self->length))) {
        return;
    }

    _Ypython_Linked_List_Node *current_node = self->head;
    if (current_node == NULL) {
        // 0 elements inside;
        return;
    }

    long long current_index = 0;
    while (current_node != NULL) {
        if (current_index == index) {
            // Free the old value to prevent memory leaks
            if (current_node->value != NULL) {
                free(current_node->value);
            }

            // Set the new value
            current_node->value = an_element;
            return;
        }
        current_node = current_node->next;
        current_index = current_index + 1;
    }
}

Type_Ypython_General* Type_Ypython_List_get(Type_Ypython_List *self, long long index) {
    Type_Ypython_General *default_element = Ypython_General();
    default_element->is_none = true;

    if (self->is_none || ((index < 0) || (index >= self->length))) {
        return default_element;
    }

    int i = 0;
    _Ypython_Linked_List_Node *current_node = self->head;
    _Ypython_Linked_List_Node *previous = NULL;

    if (current_node == NULL) {
        // 0 elements inside;
        return default_element;
    }
  
    while (current_node != NULL) {
        if (i == index) {
            free(default_element);
            return current_node->value;
        }
        previous = current_node;
        current_node = current_node->next;
        i++;
    }

    return default_element;
}

Type_Ypython_List* Type_Ypython_List_sublist(Type_Ypython_List *self, long long start_index, long long end_index) {
    Type_Ypython_List *default_list = Ypython_List();
    default_list->is_none = true;

    if (start_index > end_index) {
        return default_list;
    }

    if (self->is_none || ((start_index < 0) || (end_index > self->length))) {
        return default_list;
    }

    int i = 0;
    _Ypython_Linked_List_Node *current_node = self->head;
    _Ypython_Linked_List_Node *previous = NULL;

    if (current_node == NULL) {
        // 0 elements inside;
        return default_list;
    }

    default_list->is_none = false;
  
    while (current_node != NULL) {
        if ((i >= start_index) && (i < end_index)) {
            default_list->function_append(default_list, current_node->value);
        } 
        if (i >= end_index) {
            break;
        }
        previous = current_node;
        current_node = current_node->next;
        i++;
    }

    return default_list;
}

void Type_Ypython_List_start_iteration(Type_Ypython_List *self) {
    if (self->is_none) {
        return;
    }

    self->_current_iterate_node = self->head;
    self->iteration_not_done = true;

    if (self->_current_iterate_node == NULL) {
        self->iteration_not_done = false;
    }
}

Type_Ypython_General* (Type_Ypython_List_get_next_one)(Type_Ypython_List *self) {
    Type_Ypython_General *default_element = Ypython_General();
    default_element->is_none = true;

    if (self->is_none) {
        self->iteration_not_done = false;
        return default_element;
    }

    if (self->_current_iterate_node == NULL) {
        self->iteration_not_done = false;
        return default_element;
    }

    default_element = self->_current_iterate_node->value;
    self->_current_iterate_node = self->_current_iterate_node->next;
    return default_element;
}

Type_Ypython_List *Ypython_List() {
    Type_Ypython_List *new_list_value;
    new_list_value = (Type_Ypython_List *)malloc(sizeof(Type_Ypython_List));

    new_list_value->is_none = false;
    new_list_value->type = (char *)"list";

    new_list_value->head = NULL;
    new_list_value->tail = NULL;
    new_list_value->length = 0;

    new_list_value->function_append = &Type_Ypython_List_append;
    new_list_value->function_index = &Type_Ypython_List_index;
    new_list_value->function_delete = &Type_Ypython_List_delete;
    new_list_value->function_insert = &Type_Ypython_List_insert;
    new_list_value->function_set = &Type_Ypython_List_set;
    new_list_value->function_get = &Type_Ypython_List_get;
    new_list_value->function_sublist = &Type_Ypython_List_sublist;
    new_list_value->function_start_iteration = &Type_Ypython_List_start_iteration;
    new_list_value->function_get_next_one = &Type_Ypython_List_get_next_one;

    return new_list_value;
}
*/


/*
Old non_linked_list List type
//https://dev.to/bekhruzniyazov/creating-a-python-like-list-in-c-4ebg

A good list data type has to have:
1. infinity list size increasing in real time
2. automatically garbage collection

Tip: Uses a dynamic array with doubling/halving strategy for efficient access.
List structure was created by grok3 from yingshaoxo_list python implementation
*/
typedef struct Type_Ypython_List Type_Ypython_List;
struct Type_Ypython_List {
    bool is_none;
    char *type;

    Type_Ypython_General **items; // Dynamic array of pointers
    long long length;            // Number of elements
    long long memory_slots;      // Allocated slots

    void (*function_append)(Type_Ypython_List *self, Type_Ypython_General *an_element);
    Type_Ypython_Int *(*function_index)(Type_Ypython_List *self, Type_Ypython_General *an_element);
    Type_Ypython_General* (*function_get)(Type_Ypython_List *self, long long index);
    void (*function_set)(Type_Ypython_List *self, long long index, Type_Ypython_General *an_element);
    void (*function_delete)(Type_Ypython_List *self, long long index);
    void (*function_insert)(Type_Ypython_List *self, long long index, Type_Ypython_General *an_element);
    Type_Ypython_List* (*function_sublist)(Type_Ypython_List *self, long long start_index, long long end_index);
};

void Type_Ypython_List_append(Type_Ypython_List *self, Type_Ypython_General *an_element) {
    if (self->is_none) {
        return;
    }

    if (self->length >= self->memory_slots) {
        self->memory_slots *= 2;
        Type_Ypython_General **new_items = (Type_Ypython_General **)_ypython_resize_memory_block_for_a_pointer(self->items, self->memory_slots * sizeof(Type_Ypython_General *));
        if (!new_items) {
            fprintf(stderr, "Memory reallocation failed in append\n");
            exit(1);
        }
        self->items = new_items;
        for (long long i = self->length; i < self->memory_slots; i++) {
            self->items[i] = NULL;
        }
    }

    self->items[self->length] = an_element;
    self->length++;
}

Type_Ypython_Int *Type_Ypython_List_index(Type_Ypython_List *self, Type_Ypython_General *an_element) {
    Type_Ypython_Int *index = Ypython_Int(-1);
    if (self->is_none) {
        index->is_none = true;
        return index;
    }

    for (long long i = 0; i < self->length; i++) {
        if (self->items[i] && self->items[i]->function_is_equal(self->items[i], an_element)) {
            index->value = i;
            index->is_none = false;
            return index;
        }
    }

    index->is_none = true;
    return index;
}

Type_Ypython_General* Type_Ypython_List_get(Type_Ypython_List *self, long long index) {
    Type_Ypython_General *default_element = Ypython_General();
    default_element->is_none = true;

    if (self->is_none || index < 0 || index >= self->length) {
        return default_element;
    }

    free(default_element);
    return self->items[index];
}

void Type_Ypython_List_set(Type_Ypython_List *self, long long index, Type_Ypython_General *an_element) {
    if (self->is_none || index < 0 || index >= self->length) {
        return;
    }

    // Free old element
    //if (self->items[index]) {
    //    free(self->items[index]);
    //}
    self->items[index] = an_element;
}

void Type_Ypython_List_delete(Type_Ypython_List *self, long long index) {
    if (self->is_none || index < 0 || index >= self->length) {
        return;
    }

    // Free the element at index
    //if (self->items[index]) {
    //    free(self->items[index]);
    //    self->items[index] = NULL;
    //}

    // Shift elements left
    for (long long i = index; i < self->length - 1; i++) {
        self->items[i] = self->items[i + 1];
    }
    self->items[self->length - 1] = NULL;
    self->length--;

    // Shrink if underutilized
    if (self->length < self->memory_slots / 2 && self->memory_slots > 8) {
        self->memory_slots = _ypython_get_float_absolute_value(self->memory_slots / 2);
        if (self->memory_slots < 8) {
            self->memory_slots = 8;
        }
        Type_Ypython_General **new_items = (Type_Ypython_General **)_ypython_resize_memory_block_for_a_pointer(self->items, self->memory_slots * sizeof(Type_Ypython_General *));
        if (!new_items) {
            fprintf(stderr, "Memory reallocation failed in delete\n");
            exit(1);
        }
        self->items = new_items;
        for (long long i = self->length; i < self->memory_slots; i++) {
            self->items[i] = NULL;
        }
    }
}

void Type_Ypython_List_insert(Type_Ypython_List *self, long long index, Type_Ypython_General *an_element) {
    if (self->is_none || index < 0 || index > self->length) {
        return;
    }

    if (self->length >= self->memory_slots) {
        self->memory_slots *= 2;
        Type_Ypython_General **new_items = (Type_Ypython_General **)_ypython_resize_memory_block_for_a_pointer(self->items, self->memory_slots * sizeof(Type_Ypython_General *));
        if (!new_items) {
            fprintf(stderr, "Memory reallocation failed in insert\n");
            exit(1);
        }
        self->items = new_items;
        for (long long i = self->length; i < self->memory_slots; i++) {
            self->items[i] = NULL;
        }
    }

    // Shift elements right
    for (long long i = self->length; i > index; i--) {
        self->items[i] = self->items[i - 1];
    }
    self->items[index] = an_element;
    self->length++;
}

Type_Ypython_List* Type_Ypython_List_sublist(Type_Ypython_List *self, long long start_index, long long end_index) {
    Type_Ypython_List *new_list = Ypython_List();
    new_list->is_none = true;

    if (self->is_none || start_index < 0 || end_index > self->length || start_index > end_index) {
        return new_list;
    }

    new_list->is_none = false;
    for (long long i = start_index; i < end_index; i++) {
        new_list->function_append(new_list, self->items[i]); // Shallow copy
    }

    return new_list;
}

Type_Ypython_List *Ypython_List() {
    Type_Ypython_List *new_list_value = (Type_Ypython_List *)_ypython_memory_allocation_for_data(sizeof(Type_Ypython_List));
    if (!new_list_value) {
        fprintf(stderr, "Memory allocation failed for list\n");
        exit(1);
    }

    new_list_value->is_none = false;
    new_list_value->type = (char *)"list";

    new_list_value->memory_slots = 8;
    new_list_value->length = 0;
    new_list_value->items = (Type_Ypython_General **)_ypython_memory_allocation_for_data(new_list_value->memory_slots * sizeof(Type_Ypython_General *));
    if (!new_list_value->items) {
        free(new_list_value);
        fprintf(stderr, "Memory allocation failed for list items\n");
        exit(1);
    }
    for (long long i = 0; i < new_list_value->memory_slots; i++) {
        new_list_value->items[i] = NULL;
    }

    new_list_value->function_append = &Type_Ypython_List_append;
    new_list_value->function_index = &Type_Ypython_List_index;
    new_list_value->function_set = &Type_Ypython_List_set;
    new_list_value->function_get = &Type_Ypython_List_get;
    new_list_value->function_delete = &Type_Ypython_List_delete;
    new_list_value->function_insert = &Type_Ypython_List_insert;
    new_list_value->function_sublist = &Type_Ypython_List_sublist;

    return new_list_value;
}


/*
Dict type
//You can use 2 dimentional array, one to store the key, another to store the value, and two array uses same index and length.
//Key will always be Type_Ypython_String type inside Type_Ypython_General
*/
/*
 * Need to convert this dict to hash_table based dict to increase dict look up speed
 */
typedef struct Type_Ypython_Dict Type_Ypython_Dict;
struct Type_Ypython_Dict {
    bool is_none;
    char *type;

    Type_Ypython_List* keys;
    Type_Ypython_List* values;

    void (*function_set)(Type_Ypython_Dict *self, Type_Ypython_String *a_key, Type_Ypython_General *a_value);
    Type_Ypython_General *(*function_get)(Type_Ypython_Dict *self, Type_Ypython_String *a_key);
    bool (*function_has_key)(Type_Ypython_Dict *self, Type_Ypython_String *a_key);
};

void Type_Ypython_Dict_set(Type_Ypython_Dict *self, Type_Ypython_String *a_key, Type_Ypython_General *a_value) {
    if (self->is_none) {
        return;
    } 

    if (self->keys == NULL || self->values == NULL) {
        return;
    }

    Type_Ypython_General *the_key = Ypython_General();
    the_key->string_ = Ypython_String(a_key->value);

    Type_Ypython_Int *index = self->keys->function_index(self->keys, the_key);

    if (index->is_none) {
        // we don't have this key in this dict, add a new one
        self->keys->function_append(self->keys, the_key);
        self->values->function_append(self->values, a_value);
    } else {
        // we have this key in this dict, update old one
        self->values->function_set(self->values, index->value, a_value);
    }
}

Type_Ypython_General *Type_Ypython_Dict_get(Type_Ypython_Dict *self, Type_Ypython_String *a_key) {
    Type_Ypython_General *result = Ypython_General();

    if (self->is_none) {
        result->is_none = true;
        return result;
    } 

    if (self->keys == NULL || self->values == NULL) {
        result->is_none = true;
        return result;
    }

    Type_Ypython_General *the_key = Ypython_General();
    the_key->string_ = a_key;

    Type_Ypython_Int *index = self->keys->function_index(self->keys, the_key);
    if (index->is_none) {
        // we don't have this key in this dict, return none
        result->is_none = true;
        return result;
    } else {
        // we have this key in this dict, return the value
        Type_Ypython_General *a_value = self->values->function_get(self->values, index->value);
        return a_value;
    }
}

bool Type_Ypython_Dict_has_key(Type_Ypython_Dict *self, Type_Ypython_String *a_key) {
    if (self->is_none) {
        return false;
    } 

    if (self->keys == NULL || self->values == NULL) {
        return false;
    }

    Type_Ypython_General *the_key = Ypython_General();
    the_key->string_ = a_key;

    Type_Ypython_Int *index = self->keys->function_index(self->keys, the_key);

    if (index->is_none) {
        // we don't have this key in this dict, return none
        return false;
    } else {
        // we have this key in this dict, return the value
        return true;
    }
}

bool (*function_has_key)(Type_Ypython_Dict *self, Type_Ypython_String *a_key);

Type_Ypython_Dict *Ypython_Dict() {
    Type_Ypython_Dict *new_value;
    new_value = (Type_Ypython_Dict *)malloc(sizeof(Type_Ypython_Dict));

    new_value->is_none = false;
    new_value->type = (char *)"dict";

    new_value->keys = Ypython_List();
    new_value->values = Ypython_List();

    new_value->function_set = &Type_Ypython_Dict_set;
    new_value->function_get = &Type_Ypython_Dict_get;
    new_value->function_has_key = &Type_Ypython_Dict_has_key;

    return new_value;
}

// function to create a new general variable by copying old one
Type_Ypython_General *_Ypython_copy_general_variable(Type_Ypython_General *value) {
    if (value == NULL) {
        return NULL;
    }

    Type_Ypython_General *new_value = Ypython_General();
    new_value->is_none = value->is_none;
    
    if (value->string_ != NULL) {
        new_value->string_ = Ypython_String(value->string_->value);
        new_value->string_->is_none = value->string_->is_none;
        new_value->is_none = false;
    } else if (value->bool_ != NULL) {
        new_value->bool_ = Ypython_Bool(value->bool_->value);
        new_value->bool_->is_none = value->bool_->is_none;
        new_value->is_none = false;
    } else if (value->int_ != NULL) {
        new_value->int_ = Ypython_Int(value->int_->value);
        new_value->int_->is_none = value->int_->is_none;
        new_value->is_none = false;
    } else if (value->float_ != NULL) {
        new_value->float_ = Ypython_Float(value->float_->value);
        new_value->float_->is_none = value->float_->is_none;
        new_value->is_none = false;
    } else if (value->list_ != NULL) {
        // For lists, we need to create a deep copy
        new_value->list_ = Ypython_List();
        new_value->list_->is_none = value->list_->is_none;
        new_value->is_none = false;
        // Copy each element from the source list
        long long a_index = 0; 
        while (a_index < value->list_->length) {
            Type_Ypython_General *element = value->list_->function_get(value->list_, a_index);
            if (!element->is_none) {
                new_value->list_->function_append(new_value->list_, element);
            }
            a_index += 1;
        }
    } else if (value->dict_ != NULL) {
        // For dicts, we need to create a deep copy
        new_value->dict_ = Ypython_Dict();
        new_value->dict_->is_none = value->dict_->is_none;
        new_value->is_none = false;
        // Copy each key-value pair from the source dict
        long long a_index = 0;
        while (a_index < value->dict_->keys->length) {
            Type_Ypython_General *key = value->dict_->keys->function_get(value->dict_->keys, a_index);
            if (!key->is_none) {
                Type_Ypython_General *dict_value = value->dict_->function_get(value->dict_, key->string_);
                if (!dict_value->is_none) {
                    new_value->dict_->function_set(new_value->dict_, key->string_, dict_value);
                }
            }
            a_index += 1;
        }
    } else if (value->anything_ != NULL) {
        new_value->anything_ = value->anything_;
    }
    
    return new_value;
}

Type_Ypython_General *ypython_create_a_general_variable(void *value) {
    Type_Ypython_General *new_value = (Type_Ypython_General *)malloc(sizeof(Type_Ypython_General));
    if (value == NULL) {
        return NULL;
    }

    new_value->is_none = false;
    new_value->type = (char *)"general";
    new_value->bool_ = NULL;
    new_value->float_ = NULL;
    new_value->int_ = NULL;
    new_value->string_ = NULL;
    new_value->list_ = NULL;
    new_value->dict_ = NULL;
    new_value->anything_ = NULL;
    new_value->function_is_equal = &Type_Ypython_General_is_equal;

    if (strcmp(((Type_Ypython_None *)value)->type, "none") == 0) {
        new_value->is_none = true;
    } else if (strcmp(((Type_Ypython_String *)value)->type, "string") == 0) {
        Type_Ypython_String *str = (Type_Ypython_String *)value;
        new_value->string_ = Ypython_String(str->value);
    } else if (strcmp(((Type_Ypython_Bool *)value)->type, "bool") == 0) {
        Type_Ypython_Bool *bool_val = (Type_Ypython_Bool *)value;
        new_value->bool_ = Ypython_Bool(bool_val->value);
    } else if (strcmp(((Type_Ypython_Int *)value)->type, "int") == 0) {
        Type_Ypython_Int *int_val = (Type_Ypython_Int *)value;
        new_value->int_ = Ypython_Int(int_val->value);
    } else if (strcmp(((Type_Ypython_Float *)value)->type, "float") == 0) {
        Type_Ypython_Float *float_val = (Type_Ypython_Float *)value;
        new_value->float_ = Ypython_Float(float_val->value);
    } else if (strcmp(((Type_Ypython_List *)value)->type, "list") == 0) {
        Type_Ypython_List *list_val = (Type_Ypython_List *)value;
        new_value->list_ = Ypython_List();
        for (size_t i = 0; i < list_val->length; i++) {
            Type_Ypython_General *item = list_val->function_get(list_val, i);
            item = _Ypython_copy_general_variable(item);
            if (item != NULL) {
                new_value->list_->function_append(new_value->list_, item);
            }
        }
    } else if (strcmp(((Type_Ypython_Dict *)value)->type, "dict") == 0) {
        Type_Ypython_Dict *dict_val = (Type_Ypython_Dict *)value;
        new_value->dict_ = Ypython_Dict();
        for (size_t i = 0; i < dict_val->keys->length; i++) {
            Type_Ypython_String *the_key = dict_val->keys->function_get(dict_val->keys, i)->string_;
            Type_Ypython_General *the_value = dict_val->values->function_get(dict_val->values, i);
            if (the_key != NULL && the_value != NULL) {
                the_value = _Ypython_copy_general_variable(the_value);
                new_value->dict_->function_set(new_value->dict_, the_key, the_value);
            }
        }
    } else if (value != NULL) {
        new_value->anything_ = value;
    }

    return new_value;
}

// dict inheritance
// it should remain access to old dict while add new_dict data to a new dict variable. it is mainly used in function arguments passing
Type_Ypython_Dict *_Ypython_dict_inheritance(Type_Ypython_Dict *old_dict, Type_Ypython_Dict *new_dict) {
    Type_Ypython_Dict *result_dict = Ypython_Dict();

    if ((old_dict == NULL) || (new_dict == NULL)) {
        return result_dict;
    }

    long long loop_index = 0;
    while (loop_index < old_dict->keys->length) {
        Type_Ypython_String *new_key = Ypython_String(old_dict->keys->function_get(old_dict->keys, loop_index)->string_->value);
        Type_Ypython_General *new_value = old_dict->values->function_get(old_dict->values, loop_index);
        // here we are basically using the address of those values, so when you change a global variable inside a function, it will really do the change without you to specifying the 'global xx'
        result_dict->function_set(result_dict, new_key, new_value);
        loop_index += 1;
    }

    loop_index = 0;
    while (loop_index < new_dict->keys->length) {
        Type_Ypython_String *new_key = Ypython_String(new_dict->keys->function_get(new_dict->keys, loop_index)->string_->value);
        Type_Ypython_General *new_value = new_dict->values->function_get(new_dict->values, loop_index);
        result_dict->function_set(result_dict, new_key, new_value);
        loop_index += 1;
    }
    
    return result_dict;
}

// string functions
Type_Ypython_List *ypython_string_type_function_split(Type_Ypython_String *self, Type_Ypython_String *seperator_string) {
    Type_Ypython_List *result_list = Ypython_List();

    if (seperator_string == NULL) {
        // we should split the string into characters
        long long index = 0; 
        while (index < self->length) {
            char *character_string = malloc(sizeof(char) * 2);
            character_string[0] = self->value[index];
            character_string[1] = '\0';
            Type_Ypython_String *a_character_string = Ypython_String(character_string);
            Type_Ypython_General *an_element = Ypython_General();
            an_element->string_ = a_character_string; 
            result_list->function_append(result_list, an_element);

            index += 1;
        }
    } else {
        // normal split
        char *str = ypython_string_copy(self->value);
        const char *delimiter = ypython_string_copy(seperator_string->value);

        int str_len = strlen(str);
        int delim_len = strlen(delimiter);
        
        char* temp_string = _ypython_memory_allocation_for_data((sizeof(char) * str_len) + 1);
        int temp_string_index = 0;
        for (int i = 0; i < str_len; i++) {
            int match = 1;
            for (int j = 0; j < delim_len; j++) {
                if (str[i + j] != delimiter[j]) {
                    match = 0;
                    break;
                }
            }
            
            if (match) {
                temp_string[temp_string_index] = '\0';

                Type_Ypython_String *new_string = Ypython_String(temp_string);
                Type_Ypython_General *a_general_variable = Ypython_General();
                a_general_variable->string_ = new_string;
                result_list->function_append(result_list, a_general_variable);

                temp_string_index = 0;
                i += delim_len - 1;
            } else {
                temp_string[temp_string_index] = str[i];
                temp_string_index += 1;
            }
        }

        if (temp_string_index != 0) {
            temp_string[temp_string_index] = '\0';

            Type_Ypython_String *new_string = Ypython_String(temp_string);
            Type_Ypython_General *a_general_variable = Ypython_General();
            a_general_variable->string_ = new_string;
            result_list->function_append(result_list, a_general_variable);
        }
    }
    
    return result_list;
}

Type_Ypython_String *ypython_string_type_function_join(Type_Ypython_List *a_string_list, Type_Ypython_String *seperator_string) {
    Type_Ypython_String *result = Ypython_String("");

    long long last_minus_1 = a_string_list->length - 1;
    for (long long i = 0; i < a_string_list->length; i++) {
        result = result->function_add(result, a_string_list->function_get(a_string_list, i)->string_);
        if (i < last_minus_1) {
            result = result->function_add(result, seperator_string);
        }
    }

    return result;
}

/*
It should print out variable without new line unless user add '\n'
It should be able to print str, double, int, bool, dict, list, none type variable directly 
Just similar to how you print variables in python's realtime shell interpreter.

It has bug for now, it is OK, because in the future, there would have json.dumps() and json.loads(), we will simply print formated json text.
*/
void ypython_raw_print(void *value)
{
    if (value == NULL) {
        printf("NULL");
        return;
    }

    if (strcmp(((Type_Ypython_General *)value)->type, "general") == 0) {
        Type_Ypython_General *item = (Type_Ypython_General *)value;
        if (item->is_none == true) {
            ypython_raw_print(Ypython_String("None"));
        } else if (item->string_ != NULL) {
            ypython_raw_print(item->string_);
        } else if (item->bool_ != NULL) {
            ypython_raw_print(item->bool_);
        } else if (item->int_ != NULL) {
            ypython_raw_print(item->int_);
        } else if (item->float_ != NULL) {
            ypython_raw_print(item->float_);
        } else if (item->list_ != NULL) {
            ypython_raw_print(item->list_);
        } else if (item->dict_ != NULL) {
            ypython_raw_print(item->dict_);
        } else if (item->anything_ != NULL) {
            ypython_raw_print(Ypython_String("anything_"));
        }
    } else if (strcmp(((Type_Ypython_String *)value)->type, "string") == 0) {
        Type_Ypython_String *str = (Type_Ypython_String *)value;
        // Print the string directly, allowing newlines to be interpreted
        printf("%s", str->value);
    } else if (strcmp(((Type_Ypython_Bool *)value)->type, "bool") == 0) {
        Type_Ypython_Bool *bool_val = (Type_Ypython_Bool *)value;
        if (bool_val->value == true) {
            printf("True");
        } else {
            printf("False");
        }
    } else if (strcmp(((Type_Ypython_Int *)value)->type, "int") == 0) {
        Type_Ypython_Int *int_val = (Type_Ypython_Int *)value;
        printf("%lld", int_val->value);
    } else if (strcmp(((Type_Ypython_Float *)value)->type, "float") == 0) {
        Type_Ypython_Float *float_val = (Type_Ypython_Float *)value;
        printf("%Lf", float_val->value);
    } else if (strcmp(((Type_Ypython_List *)value)->type, "list") == 0) {
        Type_Ypython_List *list_val = (Type_Ypython_List *)value;
        printf("[");
        for (size_t i = 0; i < list_val->length; i++) {
            Type_Ypython_General *item = list_val->function_get(list_val, i);
            if (item != NULL) {
                if (item->string_ != NULL) {
                    ypython_raw_print(item->string_);
                } else if (item->bool_ != NULL) {
                    ypython_raw_print(item->bool_);
                } else if (item->int_ != NULL) {
                    ypython_raw_print(item->int_);
                } else if (item->float_ != NULL) {
                    ypython_raw_print(item->float_);
                } else if (item->list_ != NULL) {
                    ypython_raw_print(item->list_);
                } else if (item->dict_ != NULL) {
                    ypython_raw_print(item->dict_);
                } else if (item->anything_ != NULL) {
                    ypython_raw_print(Ypython_String("anything_"));
                }
                if (i < list_val->length - 1) {
                    printf(", ");
                }
            }
        }
        printf("]");
    } else if (strcmp(((Type_Ypython_Dict *)value)->type, "dict") == 0) {
        Type_Ypython_Dict *dict_val = (Type_Ypython_Dict *)value;
        printf("{");
        for (size_t i = 0; i < dict_val->keys->length; i++) {
            Type_Ypython_String *the_key = dict_val->keys->function_get(dict_val->keys, i)->string_;
            Type_Ypython_General *the_value = dict_val->values->function_get(dict_val->values, i);
            if (the_key != NULL && the_value != NULL) {
                ypython_raw_print(the_key);
                printf(": ");
                if (the_value->string_ != NULL) {
                    ypython_raw_print(the_value->string_);
                } else if (the_value->bool_ != NULL) {
                    ypython_raw_print(the_value->bool_);
                } else if (the_value->int_ != NULL) {
                    ypython_raw_print(the_value->int_);
                } else if (the_value->float_ != NULL) {
                    ypython_raw_print(the_value->float_);
                } else if (the_value->list_ != NULL) {
                    ypython_raw_print(the_value->list_);
                } else if (the_value->dict_ != NULL) {
                    ypython_raw_print(the_value->dict_);
                } else if (the_value->anything_ != NULL) {
                    ypython_raw_print(Ypython_String("anything_"));
                }
                if (i < dict_val->keys->length - 1) {
                    printf(", ");
                }
            }
        }
        printf("}");
    } else if (strcmp(((Type_Ypython_None *)value)->type, "none") == 0) {
        printf("None");
    } else {
    }
}

