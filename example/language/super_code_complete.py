input_text = '''
# created by yingshaoxo
Algorithem:

[
    I love you,
    I like you,
    I hate you,
]

data:
    next_word:
        [I] -> love
        [I] -> like
        [I] -> hate

        [I,love] -> you
        [I,like] -> you
        [I,hate] -> you

        [I,love,you] -> .
        [I,like,you] -> .
        [I,hate,you] -> .

> As you can see, the original data is small, but after this 'to dict process', it got bigger. why we want to do this? because we want to get as much as data as possible from original data, so the text generation will go on and on infinately.... It is just like what human do when they are in thinking, the new data always pollute the base data to generate new ideas. we keep thinking or talking in our mind.

> It seems like you just need a best data, that data is in our mind. If you could save the thinking text in your brain, you can use that data as source, to let new machine to keep generate new text based on the old thinking text, which will make a copy of you. (Think like you)

> If you can't read mind, you can talk to yourself without end, write it down as pure text, doing this for 1 week, everyday 8 hours, then you can collect enough data.

> The good part about this tech is: it will do brain copy in the exact way, 1 to 1, no other dirty data. The bad part is, it can not do self upgrade unless it has permission to change its old data, I mean, it should have "thinking to action" bindings, so that it can modify the old text it generated. All in all, if you have less data you can't make a self_upgraded_able thinking machine.

> Above is just minimum example of 'self inner brain thinking text data'.

> But if you just want to create digital person, this method will only copy yourself. You have to be a teacher, and teach your students. So that they could have sex gender. Just simplifying yourself to child level, then teach them from basics.
'''

# created by twitter grok3
import random
import json
import os

def _language_splitor(text):
    language_list = []
    index = 0
    while True:
        temp_string = ""
        if (index >= len(text)):
            break
        char = text[index]
        while ord(char) < 128:
            # english
            char = text[index]
            temp_string += char
            index += 1
            if (index >= len(text)):
                break
        if (temp_string.strip() != ""):
            temp_string = temp_string[:-1]
            index -= 1
            language_list.append({
                "language": "en",
                "text": temp_string
            })

        temp_string = ""
        if (index >= len(text)):
            break
        char = text[index]
        while not ord(char) < 128:
            # chinese 
            char = text[index]
            temp_string += char
            index += 1
            if (index >= len(text)):
                break
        if (temp_string.strip() != ""):
            temp_string = temp_string[:-1]
            index -= 1
            for one in temp_string:
                language_list.append({
                    "language": "cn",
                    "text": one
                })

        if (index+1 >= len(text)):
            break

    if len(language_list) > 0:
        language_list[-1]["text"] += text[-1]

    new_list = []
    for index, one in enumerate(language_list):
        new_text = language_list[index]["text"].strip()
        if len(new_text) > 0:
            if one['language'] == 'cn':
                for one in new_text:
                    new_list.append({
                        "language": "cn",
                        "text": one
                    })
            else:
                new_list.append({
                    'language': one['language'],
                    'text': new_text
                })

    return new_list

def my_split_function(text):
    tokens = []
    current_word = ""
    for char in text:
        if char == '\n':
            if current_word:
                tokens.append(current_word)
                current_word = ""
            tokens.append('\n')
        elif char.isspace():
            if current_word:
                tokens.append(current_word)
                current_word = ""
        else:
            current_word += char
    if current_word:
        tokens.append(current_word)

    old_tokens = tokens
    new_list = []
    for one in tokens:
        if one == "\n":
            new_list.append(one)
        else:
            temp_list = _language_splitor(one)
            temp_list = [nice["text"] for nice in temp_list]
            new_list += temp_list

    return new_list

def build_word_sequences(text, max_seq_len=11):
    """Build dictionary mapping word sequences (1 to max_seq_len) to set of next words, preserving newlines."""
    # Tokenize text, preserving newlines as '\n'
    tokens = my_split_function(text)

    word_dict = {}
    for seq_len in range(1, min(max_seq_len + 1, len(tokens))):
        for i in range(len(tokens) - seq_len):
            seq = tuple(tokens[i:i + seq_len])
            next_token = tokens[i + seq_len]
            if seq not in word_dict:
                word_dict[seq] = set()
            word_dict[seq].add(next_token)
    return word_dict

def save_dict_to_json(word_dict, filename="dict_data.json"):
    """Save dictionary to JSON file, converting tuples to strings and sets to lists."""
    json_dict = {str(k): list(v) for k, v in word_dict.items()}
    with open(filename, 'w') as f:
        json.dump(json_dict, f)
    print(f"Saved dictionary to {filename}")

def load_dict_from_json(filename="dict_data.json"):
    """Load dictionary from JSON file, converting string keys to tuples and lists to sets."""
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        json_dict = json.load(f)
    word_dict = {tuple(eval(k)): set(v) for k, v in json_dict.items()}
    return word_dict

def generate_next_word(word_dict, history, max_seq_len):
    """Predict next word based on history, trying longest sequence first."""
    for seq_len in range(min(len(history), max_seq_len), 0, -1):
        seq = tuple(history[-seq_len:])
        if seq in word_dict:
            return random.choice(list(word_dict[seq]))
    all_words = [word for seq in word_dict.keys() for word in seq]
    return random.choice(all_words) if all_words else '.'

global_word_dict = {}
def load_data(txt_file_path):
    global global_word_dict, Max_Sequenc_Length

    input_text = ""
    with open(txt_file_path, "r") as f:
        input_text = f.read()

    print("Building dictionary from input text...")
    global_word_dict = build_word_sequences(input_text, max_seq_len=Max_Sequenc_Length)

def get_next_text_block(input_text):
    global global_word_dict, Max_Sequenc_Length

    input_text = input_text.strip()
    tokens = my_split_function(input_text + ' ')

    response = ""
    for i in range(1024):
        next_token = generate_next_word(global_word_dict, tokens, max_seq_len=Max_Sequenc_Length)
        tokens.append(next_token)
        if next_token == '\n':
            response += '\n'
        else:
            response += next_token + (' ' if all(ord(c) < 128 for c in next_token) else '')
    response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0].strip()

    return response

# The bigger, the accurate, but takes more disk space
Max_Sequenc_Length = 11

def main():
    try:
        with open("all_yingshaoxo_data_2023_11_13.txt", "r") as f:
            input_text = f.read()
    except Exception as e:
        pass

    # Load or build dictionary
    dict_file = "dict_data.json"
    word_dict = load_dict_from_json(dict_file)
    if word_dict is None:
        print("Building dictionary from input text...")
        word_dict = build_word_sequences(input_text, max_seq_len=Max_Sequenc_Length)
        save_dict_to_json(word_dict, dict_file)
    else:
        print(f"Loaded dictionary from {dict_file}")

    # Chatbot interface
    print("\nWelcome to the AI Chatbot! Type 'quit' to exit.")
    history = []
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            print("AI: Goodbye!")
            break
        if user_input:
            # Split user input into tokens, preserving newlines
            tokens = my_split_function(user_input + ' ')
            history.extend(tokens)
            # Generate 128 next tokens
            print("AI: ", end="")
            response = ""
            for i in range(1024):
                next_token = generate_next_word(word_dict, history, max_seq_len=Max_Sequenc_Length)
                if next_token == '\n':
                    response += '\n'
                else:
                    response += next_token + (' ' if all(ord(c) < 128 for c in next_token) else '')
                history.append(next_token)
                if len(history) > Max_Sequenc_Length:
                    history = history[-Max_Sequenc_Length:]
            response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0].strip()
            print(response)

if __name__ == "__main__":
    main()

    #load_data("all_yingshaoxo_data_2023_11_13.txt")
    #while True:
    #    input_text = input("What you want to say?")
    #    print(get_next_text_block(input_text))
    #    print("\n\n-----------\n\n")
