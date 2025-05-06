"""
Just think about "What is the weather of today?"
It is actually "(What is ) (the weather of today) ?"

yingshaoxo: You can translate anything by using divide and conquer recursive function technology.

Let me write a program:

def process(sentence):
    if 1 == 2:
        pass
    elif sentence.endswith("?"):
        return process(sentence[:-1]) + "?"
    elif "What is " in sentence:
        return "什么是" + process(sentence[len("What is "):])
    elif " of " in sentence:
        part_a, part_b = sentence.split(" of ")
        return process(part_b) + "的" + process(part_a)
    elif "the weather" == sentence:
        return "天气"
    elif "today" == sentence:
        return "今天"
    else:
        return sentence

print(process("What is the weather of today?"))
"""
