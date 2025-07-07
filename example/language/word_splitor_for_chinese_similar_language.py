# yingshaoxo: this is a project that aim to replace jieba word spliting by manually split word

chinese_sentences = [
    "yingshaoxo 是上帝",
    "上帝是万能的",
    "万能的通常是最弱的",
    "最弱的通常死得快",
    "所以上帝一定不存在于你们的世界",
    "在你的世界，你得靠你自己了",
    "愿主与你同在",
    "愿原力与你同在",
]

# maybe you should find a way to load the word_list from disk storage
word_list = list()
for chinese_sentence in chinese_sentences:
    while True:
        if len(chinese_sentence) == 0:
            break

        while True:
            found = False
            for word in word_list:
                if chinese_sentence.startswith(word):
                    found = True
                    chinese_sentence = chinese_sentence[len(word):]
                    break
            if found == False:
                break

        print(chinese_sentence)
        response = input("What is the word start in head(the space can be in head):")
        new_word_length = len(response)
        new_word = chinese_sentence[:new_word_length]
        print("new_word:", new_word)
        print("sentence_left:", chinese_sentence[new_word_length:])
        print(word_list + [new_word])

        response = input("\nLooks OK?(y/n)").strip()
        if "n" in response:
            continue
        else:
            word_list.append(new_word)
            word_list.sort(key=lambda item: -len(item))
            # maybe you should find a way to save the word_list
            chinese_sentence = chinese_sentence[new_word_length:]
            continue
