# guide for phone

1.the phone itself is actually a python terminal, you can use it as calculator. it supports '2**8\n' or 'a=2\n' kind of operations.
2.there has input method choose, you can press * button to do the switch, * is number 10 button. # is number 12 button.

```
"1abc()#", "2def[]@", "3g\bhi{}",
"4jkl<>", "5mno\n+-", "6pqr*/=",
"7stu'\"`", "8vwx:;", "9yz&|\\",
           #0_,.?!
```

## english input

when you press a button, you have to press a number again to do the input.

press the number 0 for 2 times, it will input space.

press the number 3 for 2 times, it will delete a chracter.

press the number 5 for 2 times, it will hit the enter button. normally it will execute current line of code.

in this mode, if you press 0, it will do a reset. if you press #, it will complete a command. for example, for 'li', if you press #, it will become 'list'.

## chinese input

if you press '5 and 3' 2 button sequently, then hit the # button, you can see "你", because 'n and i'(ni) was inside the button '5 and 3'. then you can press a number button to choose. if current page do not have the chinese you want, you can press the # button again to get next page of chinese.

press button 0, or button 11, will do a reset when input chinese.

if you input nothing, directly hit # button, you can input ",.?", 3 is still a delete button in this case.

## some functions

```
clear

add <note>
get <note>

list <folder_path>
cat <file_path>
remove <file_path>

make_directory <folder path>
vi <file_path>

memory #check current memory
search <yingshaoxo note>
```

## none input mode

for this mode, it still has input, but is for advanced user, for those who want to use 'vi' to edit text file.

after 'vi s.txt' command:

```
if a_number == 2:
    # up
    temp_input_char = "k"
elif a_number == 8:
    # down
    temp_input_char = "j"
elif a_number == 4:
    # left
    temp_input_char = "h"
elif a_number == 6:
    # right
    temp_input_char = "l"
elif a_number == 5:
    # insert a char
    temp_input_char = "a"
elif a_number == 9:
    # insert a line
    temp_input_char = "o"
elif a_number == 3:
    # delete
    temp_input_char = "x"
elif a_number == 7:
    # press twice, delete a line
    temp_input_char = "d"
elif a_number == 1:
    # esc and save
    temp_input_char = "$"
elif a_number == 11:
    # find
    temp_input_char = "/"
```


## for more functions

you can make your own functions, all functions are actually python files in side the ./applications folder.

for example, you can make a dictionary application by make a new file under ./application folder:

dictionary.py
```
#terminal_arguments, input_=input, print_=print

app_parent_folder = "./applications/dictionary"
note_path = app_parent_folder+"/最强双行词库.txt"

words_list = terminal_arguments.replace("?","").strip().split(" ")
result = ""
if len(words_list) > 0:
    word = words_list[0].strip()
    if ord(word[0]) <= 0x7F:
        is_en = True
        word = word + "\n"
    else:
        is_en = False
    last_line = ""
    got = False
    with open(note_path, "r") as f:
        while True:
            a_line = f.readline()
            if a_line == "":
                break
            if a_line == None:
                break
            if a_line == "___":
                continue
            if is_en:
                if word == a_line:
                    got = True
                    temp_result = a_line.strip() + " == " + f.readline().strip() + "\n"
                    if temp_result not in result:
                        result += temp_result
                        break
            else:
                if word in a_line:
                    got = True
                    temp_result = last_line.strip() + " == " + a_line.strip() + "\n"
                    if temp_result not in result:
                        result += temp_result
            last_line = a_line
    if got == True:
        print_(result)
    else:
        print_("error: not found")
else:
    print_("error: not found")
```
