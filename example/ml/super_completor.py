from auto_everything.ml import Yingshaoxo_Text_Completor

def read_text_files_recursively(root_dir, recursively=True, type_limiter=[".txt", ".md"]):
    import os
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

if __name__ == "__main__":
    source_text = read_text_files_recursively("./", type_limiter=[".txt", ".py"], recursively=False)
    yingshaoxo_text_completor = Yingshaoxo_Text_Completor()

    #lines = yingshaoxo_text_completor.get_source_text_lines(source_text)
    #lines = source_text.split("__**__**__yingshaoxo_is_the_top_one__**__**__")

    while True:
        input_text = input("What you want to say: ")
        response = yingshaoxo_text_completor.get_next_text_by_pure_text(source_text, input_text, how_many_character_you_want=200, level=64)
        if response:
            response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0]
            print("Computer: " + response)
            print("\n\n")
