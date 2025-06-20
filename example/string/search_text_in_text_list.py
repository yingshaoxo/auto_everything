from auto_everything.string_ import String
string = String()

text_source_list = [
    "I love you",
    "You love me",
    "I really love you so much",
    "You love I",
]

while True:
    print("\n\n\n------------\n\n\n")
    input_text = input("What you want to search? ")
    result_text = string.search_text_in_text_list_by_using_long_sub_sentence_and_only_return_one_text(input_text, text_source_list)
    print(result_text)
