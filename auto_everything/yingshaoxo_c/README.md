# yingshaoxo dynamic c

what if you could run c just like python?

we do not need c++ if we have a c list and dict structure. (in other words, c1989 or c1999 is enough.)

> in c, i think there only has bytes_string(unsigned char*) and int two data type.

## core function

run_c_code(code)

## what is inside the "code"?

all arguments, they are (json) string.

### version1
```
a_variable = 'hi';
print(a_variable);
// "hi" will also work, `hi` will also work;
// if a variable is not defined, it returns ""

function do_it(a, b) {
    return a+b;
}

another_variable = do_it(1,2);
print(another_variable);
free(another_variable);

if (2 < 3) {
    print('ok');
}
while (1) {
    break;
    #continue;
    //worked;
}

not(0); // return 1
str(1); // reutrn `1`

variable_3 = string_format('%s-%s', 'year', 'month');
print(variable_3);

a_string = input("what you want to say:");

//dict will pass pointer to function
a_dict = {'hi': 'you'};
print(a_dict['hi']);

//list will pass pointer to function
a_list = [1,2,3];
print(a_list[0]);

try {
    8/0;
} failed {
    print(error);
}

//actually we do not care the file name end_symbol
import "./tools.c_c" as tools;
tools.hi();

// allow char modification in string by string[2] = 'c';
// allow get ascii code of char: ascii_code('a'); //97
// allow get hex code of char: hex_code('a'); //0x61
// allow get binary code of char: binary_code('a'); //01100001
// and back to char functions

// support micro_controller, but i think for arduino nano, it should use a mini single line version of python(dynamic_c)
set_pin_type(pin_name, 0, 0); //0 as input, 1 as output. 1 as pull-up, 0 as none, -1 as pull-down

set_pin_value(pin_name, 1);
set_pin_value(pin_name, 0);
get_pin_value(pin_name);

set_pin_analog_value(pin_name, value);
float value = get_pin_analog_value(pin_name);

// support linux shell
result = run_command("./yingshaoxo_dynamic_c.run hi.c_c", 10); //timeout is 10 second
run("./yingshaoxo_dynamic_c.run hi.c_c", 60*5); //timeout is 5 second
```

### version2 (actullay is the built-in function in version1)

```
create_variable(variable_name, initial_value); //5,"string",True
remove_variable(variable_name); //5,"string",True
give_variable_a_new_value(variable_name, new_value);
get_variable_value(variable_name);


evaluate("1 + 1"); // this should return string "2"
evaluate(`"1" + "1"`); // this should return string `"11"`


create_function(function_name, argument_1, argument_2, argument_3, function_body_code); // this will create a c function

whatever = call_function(function_name, argument_1, argument_2, argument_3); // this will call a function, and return something


if(equation, code_block); // this will run the code_block if equation is true

while(equation, code_block); // this will run the code_block if equation is true. in side code_block, there might have 'break' or 'continue', but 'return' is the simplest one.


//unsigned char *temp_variable = malloc(sizeof(unsigned char)*4);
//free(temp_variable);
create_variable("temp_variable", evaluate("malloc(sizeof(char)*4)"));
call_function("free", "temp_variable");


// define("hi", "hello"); // the define here actually try to use 'hi' to replace every 'hello' it meets. but since it adds complexcity, we drop this feature.

// include("stdlib.h") or include("./whatever.c"); // this will try to add a module or code file in this line. but it adds complexcity, we drop it. we only remain char level function. a char is a 'unsigned char', we can treat it as a byte (a int between 0 and 255)

// we support relative file importing, for example, "./another_file_that_in_the_same_level_of_main_c.h"
whatever = import("./hi.c_c")


// a comment starts with '#' is also right

create_variable("code", `
    int a_number = 98;
    a_number = a_number + 1;
    printf("\n%d.\n", a_number);
`);
run_raw_c_code(code); // this function can run any raw_c_code, but it is hard to implement, it is optional, should in "additional_run_raw_c_code_module.h".
```

don't forget to add 2 more function to it: memcpy and sprintf.
```
unsigned char *pointer_of_a_string;

//allocate memory.
pointer_of_a_string = malloc( (size_t)100 );

const char *temp_string = "dynamic string.";
memcpy(pointer_of_a_string, temp_string, strlen(temp_string));

char final_string[120];
sprintf(final_string, "you will see a string created in runtime: '%s' \n\
sizeof: %d \n\
string length: %d \n\n\
", pointer_of_a_string, sizeof(temp_string), strlen(temp_string));

printf(final_string);
free(pointer_of_a_string);
free(final_string);
```

in micro_controller, there also has functions like:
```
set_pin_value(pin_name, 1);
set_pin_value(pin_name, 0);

set_pin_analog_value(pin_name, value);
float value = get_pin_analog_value(pin_name);
```

in raw c mode, these method for variable define is also OK:
```
//char a_char = '.';
//char *a_variable = "hi";
//unsigned char haha_variable2[3] = "hi";
//unsigned char a_variable[4] = { 0x00, 'o', 'k', '\0' };
//unsigned char a_variable[2][3] = { {'1', '2', '3'}, {'4', '5', '6'} };
```

## core tech

pure string based dict and list.

```
unsigned char global_variable_dict[1024*5] = { '\0' }; 
unsigned char global_function_dict[1024*15] = { '\0' };
// if we want to put function and variable into the same dict, we better add v before every variable for variable, add f before every function for function.

void *global_pointer_list[1024] = { NULL }; //we need to maintain a pointer list for all variables. but I also think it is not ok, because I can't save the memory pointer into storage after power off.

// the dict structure is: splitor1 + key + splitor2 + value
// splitor1=".#new_line#."; splitor2="|#colon#|";
```

## keys

* we use global polution for speed. child function and parent function share same variable space. if they want to be different, let them use a unique name. (python 'global' keyword is bad, I often forget about add a global variable in function. but in c micro_controller or e_easy_language, it is comfortable to use global variable, a way that let you feel you are god.)
* people mind are a state variable machine, the memory is in continus update, so as long as the software is running, the global dict can get updated by all code. c code assume you will not use others bad people code, so every function has equal rights.
* "没有全局变量的代码，就像是一个官僚体系，发展太久，底层function就失去了对自身命运的掌控权。无法见到掌权的人，无法参与国家事务。变成了没有灵魂的机器。另外，因为代码写太多，导致后期无法修改，因为改function参数的工作量太大，并且增加通信成本。但如果有全局变量，我可以直接对着总统吼一句我的想法，然后问题就解决了。"
