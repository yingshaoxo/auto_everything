# yingshaoxo_python

Here, I just want to talk about how to make a python based on any programming language.


## Easy Programming Language (易语言)
Easy Programming Language is a language similar to original VB language in windows system. It is chinese based, but you can use English to do the programming if you like.


### Handle basic variables
Source code: variable hi = "xx";

The Core of Python or any other dynamic programming language is you can create and manipulate variables in real time. 

How can you do the same thing with a compiler? You use flexable data structures, for example, dict or list.

Because we know, we can add or delete an element from dict or list in real time without redefine them again.

So we can do this: According to json data type, we make 5 list, each contains variable type of boolean, number, string, null, object, array(list). But to make it simple, we create boolean, number, string 3 data_type_lists first.

Whenever you create a new variable, for example, a string, you add that string to string list, when you do that, you'll get an index, the index is the second ID of that string variable. The full ID of that string should be 'variable_name + data_type_list_index + index'.

It seems like you have to have a dict to save those variables information. For example, the key would be the variable_name, the value would be the "data_type_list_index + index". The 'data_type_list' could be a string, for example, if it is 'boolean', you will look for the boolean list to get the real value of that variable.

So far, you basically have a way to do modification for a variable in real time. It seems to be very complexed to make a simple functionality with a compilling programming language, because you can do this kind of thing in python by using a simple dict where the key is variable name, the value is the real value.

This design will not work in some strict 1984 programming language, because they does not allow you to define infinite length list by default. And they also do not allow you to create new variable in real time.


### Handle operations between basic variables
Since you can modify basic variable types, you can also handle operations like "+", "-" symbols, for example, number or string addition, subtraction.


### Handle More complexed data structure: list, dictionary
In c programming language, we can easyly create a new list in anywhere by using malloc(memory allocation): int* arr = (int*)malloc(n * sizeof(int));

But in easy programming language, you can't do it without using c extension. If you force to implement it, you'll find later you are doing programming in C, not easy programming language.

As for dict, we could use two linked list to mimic a dict data structure, but that would have low performence. We should use hash_map to create a dict type. But I don't know the details of hash map algorithm, maybe you should check python dict implementation in C, maybe you could understand it. The hash_dict speed is 10000 times quicker than pure double_linked_list_based_dict.

As for the list or dict variable information saving, we save memory pointer than the real data.


### Make variable a general type
In python, when you define a variable, you don't really tell the python the type of that variable, you won't specify it clearly about if is a bool or integer or string. The python simply knows it by doing a check on the value string format.

Python uses a general variable format:

```
class General_Variable:
    is_none = False
    is_boolean = False
    is_number = False
    is_string = False
    is_list = False
    is_dict = False
    is_function = False
    is_class = False
    name = xxx
    value = xxx
    more_information = {}
```

Python do different operations with the variable according to the variable type.


### Handle functions
Source code: function do_it_or_sleep(option) {};

Let's talk about function. For function, it should have two parts, one is function name, another is arguments.

function name is just variable name, you can use it later, you can call it later.

the arguments or paramaters, it is just a list of different variable, or multiple variables.

Then those arguments variable get into a function, the first thing you do is do a copy for those variables from global name space into local inner function space. Then inside of that function, you do variable operations line by line until the function end.

Then you might ask, what is the function information, how can I save it to computer so that later we could call that function?

It is simple, you simply save all function text as value, where the key is function name.

Later, if we call that function, we parse the arguments, copy arguments variable into function variable, we do a merge about variables. Then we do operations based on function text line by line.

Sometimes we may meet 'for loop' or 'while loop' in function text, in that case, we will simplely repeat some operations according to those code we meet.

One thing to notice is: you have to make sure you do the memory garbage freeing for those variables that was created inside of that function after the function ends. Only the return variable will be saved by doing a copy after function ends.


### Handle class
Source code: 
```
Class Dog():
    def __init__(self):
        self.name = "god"
    def run(self):
        pass
```

As for class, it is nothing but a dict object, it has some inside class variables, or propertys. You can access them by using 'className.variable_name'.

And inside of their propertys or variables, some of those property is function. You can also call those functions that inside of that class.

Normally, functions or peopertys inside of a class should get defined when you initilize a class, in python, it is "__init__" function.

Now, create a new dict, where key is class name, value is a pointer to a dict. By doing so, you can create many class.

In fact, according to my observation in tiny cpython, I see they use a lot of pointer as value, so that they could easyly give a variable a new value by simply give it a pointer.


### Make sure your programming language has try and catch design
Source code:
```
try {
    pass
} catch (error) {
    print(error)
}

```

The try and catch design will make sure any error can get captured, so that we can handle unexpected conditions. Without it, your programming language will be danger language.

To achive it, there has two ways, one is manually precheck conditions before we run, for example, 4 divide 0, if we know the later part is zero, we will raise an error before we run it.

Another way is to relay on lower_system API, for example, in c, they use 'setjmp' and 'longjmp' to do that. But use it carefully, you will often found you can't find the same two functions across different archtecture computer. If in old c99 standard you meet this problem, you can simply give up on other more modern programming language. Because they are not stable across decades years.


### Make it simple to understand
Use underline symbol to seperate words in variable name or function name, for example: "this_is_a_variable"

Use UpperCase variable to indicate it is a class, for example: "Dog_Class"

Use more type indicator for function arguments, for example: "function sleep(sleep_time_in_second_in_float_format, sleep_time_in_millisecond_in_int_format=None)"


### Handle ralative path file import
Source code: "import './module_folder/math.py' as math"

We do this simply because we do not trust dependencies that needs outside network downloading.


### Static compilling to binary excutable file
So that you can make a application store by your own to freely distribute your applications to users.

Maybe you can also sell your own computer hardware online to make sure your programming language could last forever freely.


## Natural Language (English or any other human language)

You never think you can create a programming language without using computer, right? You just have to implement a translator.

For example, if you want to let a person to drink water. The code is "drink water now". But after the translation, it becomes "Hi, how are you? I think you should drink some water, it is good for your body health.".

If the instruction is working, that person should drink water, but if it does not work, you have to try to translate the source code to some other sentence, for example: "I just poisoned you, I won't tell you if you drink that water, the poison would be gone".
