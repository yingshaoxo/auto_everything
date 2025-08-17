input_text = '''yingshaoxo: simple code works! '''

# created by twitter grok3 with the guide of yingshaoxo
import random
import json
import os
import sqlite3

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

def generate_next_word(history, max_seq_len):
    """Predict next word based on history, trying longest sequence first."""
    for seq_len in range(min(len(history), max_seq_len), 0, -1):
        seq = tuple(history[-seq_len:])
        result = the_get_random_value(' '.join(list(seq)))
        if result != None:
            result_list = result.split('🤬')
            return random.choice(result_list)
    if len(history) > 0:
        return random.choice(list(history))
    else:
        return '.'

def read_text_files_recursively(root_dir, recursively=True, type_limiter=[".txt", ".md"]):
    if recursively == False:
        result = []
        for file in os.listdir("./"):
            ok = False
            for type in type_limiter:
                if type in file:
                    ok = True
                    break
            if ok == True:
                with open(file, "r", encoding="utf-8", errors="ignore") as f:
                    result.append(f.read())
    else:
        result = []
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(tuple(type_limiter)):
                    filepath = os.path.join(dirpath, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            result.append(f.read())
                    except UnicodeDecodeError:
                        # Fallback to system default encoding if UTF-8 fails
                        with open(filepath, 'r') as f:
                            result.append(f.read())
    return '\n\n'.join(result)

def save_dict_to_db(db_path, table_name, data_dict):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')

    for key_str, value_str in data_dict.items():
        cursor.execute(
            "INSERT OR REPLACE INTO {table_name} VALUES (?, ?)".format(table_name=table_name),
            (key_str, value_str)
        )

    conn.commit()
    conn.close()

def get_random_value(db_path, table_name, key):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT value FROM {table_name} WHERE key=? ORDER BY RANDOM() LIMIT 1".format(table_name=table_name),
            (key,)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()
    return None

def the_get_random_value(key):
    value = get_random_value(db_path, the_table_name, key)
    return value

def prepare_sql_data(txt_file_path, sql_file_path, text_data=None, max_sequence_length=None):
    global Max_Sequence_Length
    global_word_dict = {}

    if max_sequence_length != None:
        Max_Sequence_Length = max_sequence_length

    if text_data == None:
        input_text = ""
        with open(txt_file_path, "r") as f:
            input_text = f.read()
    else:
        input_text = text_data

    print("Building dictionary from input text...")
    word_dict = build_word_sequences(input_text, max_seq_len=max_sequence_length)
    word_dict = {" ".join(list(key)):'🤬'.join(list(value)) for key, value in word_dict.items()}
    save_dict_to_db(db_path, the_table_name, word_dict)

    return sql_file_path

def get_next_text_block(input_text):
    input_text = input_text.strip()
    tokens = my_split_function(input_text + ' ')

    response = ""
    for i in range(1024):
        next_token = generate_next_word(tokens, max_seq_len=Max_Sequence_Length)
        tokens.append(next_token)
        if len(tokens) > Max_Sequence_Length:
            tokens = tokens[-Max_Sequence_Length:]
        if next_token == '\n':
            response += '\n'
        else:
            response += next_token + (' ' if all(ord(c) < 128 for c in next_token) else '')
    response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0].strip()

    return response

# The bigger, the accurate, but takes more disk space
Max_Sequence_Length = 7
db_path = "./the_dict.sql"
the_table_name = "hi"

def main():
    if not os.path.exists(db_path):
        input_text = read_text_files_recursively("./", type_limiter=[".txt"], recursively=False)
        prepare_sql_data(txt_file_path="", sql_file_path=db_path, text_data=input_text, max_sequence_length=Max_Sequence_Length)

    # Chatbot interface
    print("\nWelcome to the AI Chatbot! Type 'quit' to exit.")
    history = ""
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            print("AI: Goodbye!")
            break
        if user_input:
            history += "\n" + user_input
            response = get_next_text_block(history)
            print("\nAI: ", end="")
            print(user_input+" "+response)
            print("\n\n\n")

if __name__ == "__main__":
    main()
