# yingshaoxo search engine

I wanted to name this folder as "yingshaoxo_google", but for some copyright reason, I used another name.

## What is in this chapter?

Well, I mainly wanted to talk about how to create a search engine. It is valueable to have this knowledge because you hardly found useable search engine that could work in your local computer.

### According to what I have learned, there has 3 types of search engine

1. Use longest_sub_sentence to match the most accurate result

2. Use {"previous_sub_sentence": "next_one_character_or_more_characters"} dictionary to force generate useable information. Some people call this method "text_generation". The value in that dict can be a list, so that for each previous_sub_sentence, it may generate next words randomly to generates new text. (It is more like uses pieces to combine a whole picture game)

3. Use code_logic to manually mimic humans thinking to help you search text from database. This is the most advanced one. And it requires 1000MB hard coding code to parse human language, and convert them into real code to do the search and text_re_organization. Sometimes you can even think it as a general AI which generates "search_code" in real time based on your search_text_input. It is very flexable.
