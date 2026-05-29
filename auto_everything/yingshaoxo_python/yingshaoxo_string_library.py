# use pinyin

"""
def to_lower(type, string):
    # "ABcd" -> "abcd"
    return string.lower()

def to_simpler(type, string):
    #i, me -> i
    #my, mine -> my
    #am, is, are, were -> is
    string = string.replace(" me ", " i ")
    string = string.replace(" mine ", " my ")
    string = string.replace(" am ", " is ")
    string = string.replace(" are ", " is ")
    string = string.replace(" were ", " is ")
    return string

def get_stright_sentence_from_question(type, string):
    # "what is your name?" -> "your name"
    string = string.replace("?", "")
    index = string.find("what is")
    if index != -1:
        return string[index+8:]
    return string

def from_other_view_to_my_view(type, string):
    # "your name" -> "my name"
    if string.startswith("your "):
        return "my" + string[4:]
    if " your " in string:
        return string.replace(" your ", " my ")

if __name__ == "__main__":
    print(to_lower("", "ABCd"))
    print(get_stright_sentence_from_question("", "what is your name?"))
    print(from_other_view_to_my_view("", "the time you born"))
"""
