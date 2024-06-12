from auto_everything.string_ import String
string = String()

a = "how are you"
b = "how aue you"
c = "nice try"
#print("high", string.get_similarity_score_of_two_sentence_by_substring(a,b))
#print("low", string.get_similarity_score_of_two_sentence_by_substring(a,c))
print("high", string.compare_two_sentences(a,b))
print("low", string.compare_two_sentences(b,c))


input("\n\nMore test?")
a = string.get_simple_hash("hi you")
b = string.get_simple_hash("Hi yoo")
c = string.get_simple_hash("fuck it")
d = string.get_simple_hash("oo")
print(a)
print(b)
print(c)
print(d)
print("high", string.get_similarity_score_of_two_sentence_by_position_match(a,b))
print("low", string.get_similarity_score_of_two_sentence_by_position_match(a,c))
print("low", string.get_similarity_score_of_two_sentence_by_position_match(b,c))
print("low", string.get_similarity_score_of_two_sentence_by_position_match(c,d))


