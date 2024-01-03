from auto_everything.string_ import String
string_ = String()

input_text_1 = "What the fuck? What the hell?"
print(string_.get_common_string_list_in_text(input_text_1, only_return_longest=True))
print(string_.get_repeated_string_in_text_by_using_sub_window(input_text_1, window_length=4))

input_text_2 = "What the shit? What the hell?"
print("similarity_1: ", string_.get_similarity_score_of_two_sentence_by_position_match(input_text_1, input_text_2))
print("similarity_2: ", string_.get_string_match_rating_level(input_text_1, input_text_2))

print("hash1", string_.get_fuzz_hash(input_text_1, level=4))
print("hash2", string_.get_fuzz_hash(input_text_2, level=4))
