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
\
print(`string add:`);\n\
a_variable = `hi`;\n\
print(a_variable);\n\
//a way to comment;\n\
#a way to comment;\n\
print(a_variable + `_hello`);\
print(`number divide:`);\n\
ok = 0.2;\
print(1.3 / ok);\n\
is_it_true = 'hi' == 'hi';\n\
print('this is bool:');\n\
print(is_it_true);\n\
is_it_true = not(is_it_true);\n\
print(is_it_true);\n\
print(`it is number:`);\n\
no = 5;\
no += 5;\
print(no);\
no -= 1;\
print(no);\
print(`handle if:`);\n\
if (2 == 2) {\n;\
    if (2 < 3) {\n;\
        print(2333);\n\
    }\n;\
}\n;\
print(`if done.`);\n\
print(`handle while:`);\n\
index = 0; {\n;\
while (index < 3) {\n;\
    print(index);\n\
    index += 1;\
}\n;\
print(`_`);\n\
while (index > 0) {\n;\
    print(index);\n\
    index -= 1;\
    if (index == 1) {\
        break;\
    }\
}\n;\
print(`while done.`);\n\
if (not_exists == None) {\
    print('not exists works');\
}\
\
\
print(`handle function define:`);\n\
function hi() {\
    print('    no shit, it is working!');\
    print('    like nobody else!');\
}\
hi();\
free(hi);\
print(`function define done`);\n\
#a way to comment;\n\
exit();\
";

    unsigned char a_python_global_variable_dict[1024*2];
    unsigned char *return_value_or_control_command = yingshaoxo_dynamic_c_c_runner(a_python_global_variable_dict, test_code);
    printf("%s\n", return_value_or_control_command);
    printf("%s\n", a_python_global_variable_dict);
}
