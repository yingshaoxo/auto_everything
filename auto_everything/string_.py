from __future__ import annotations
from typing import Any

import string as built_in_string_module
from difflib import SequenceMatcher
import re

jieba = None

from auto_everything.disk import Disk
disk = Disk()


class String:
    def __init__(self):
        pass

    def capitalize_the_first_character_of_a_string(self, text: str) -> str:
        if len(text) == 0:
            return text
        return text[0].capitalize() + text[1:]

    def remove_all_special_characters_from_a_string(self,
        text: str,
        allow_numbers: bool = True,
        allow_ascii_lowercase_characters: bool = True,
        allow_ascii_uppercase_characters: bool = True,
        allow_whitespace: bool = False,
        allow_punctuation: bool = False,
        white_list_characters: str = ''
    ) -> str:
        new_text = ""
        for char in text:
            added = False

            if allow_numbers:
                if char in built_in_string_module.digits:
                    new_text += char
                    added = True
            if allow_ascii_lowercase_characters:
                if char in built_in_string_module.ascii_lowercase:
                    new_text += char
                    added = True
            if allow_ascii_uppercase_characters:
                if char in built_in_string_module.ascii_uppercase:
                    new_text += char
                    added = True
            if allow_whitespace:
                if char in built_in_string_module.whitespace:
                    new_text += char
                    added = True
            if allow_punctuation:
                if char in built_in_string_module.punctuation:
                    new_text += char
                    added = True

            if added == False:
                if char in white_list_characters:
                    new_text += char
                    added = True

        return new_text

    def compare_two_sentences(self, sentence1: str, sentence2: str, using_yingshaoxo_method: bool = True) -> float:
        """
        return similarity, from `0.0` to `1.0`, 1 means equal, 0 means no relate.

        Parameters
        ----------
        sentence1: string

        sentence2: string
        """
        if using_yingshaoxo_method == True:
            return self.get_string_match_rating_level(input_text = sentence1, text = sentence2)
        else:
            ratio = SequenceMatcher(None, sentence1, sentence2).ratio()
            return ratio

    def get_fuzz_hash(self, text: str, level: int = 128, seperator="_") -> str:
        """
        Compress long text into 128 char long text, so that you could use it to compare similarity.
        It works better with get_similarity_score_of_two_sentence_by_position_match(hash1, hash2)
        """
        hash_code = disk.get_hash_of_a_file_by_using_yingshaoxo_method("", bytes_data=text.encode("utf-8"), level=level, length=1, seperator=seperator, with_size=False)
        return hash_code

    def get_similarity_score_of_two_sentence_by_position_match(self, sentence1: str, sentence2: str) -> float:
        """
        It returns a float in range of [0, 1], 1 means equal.
        This is a extreamly quick method.
        """
        sentence1_length = len(sentence1)
        sentence2_length = len(sentence2)
        counting = 0
        min_length = min(sentence1_length, sentence2_length)
        for index in range(min_length):
            char = sentence1[index]
            another_sentence_char = sentence2[index]
            if char == another_sentence_char:
                counting += 1
        return counting / min_length

    def get_changed_part_of_a_text(self, before_text: str, after_text: str, no_change_position_placeholder: str=" ") -> str:
        length = len(before_text)
        after_text = after_text[:length]
        result = ""
        for index in range(length):
            char = before_text[index]
            another_sentence_char = after_text[index]
            if char == another_sentence_char:
                result += no_change_position_placeholder
            else:
                result += another_sentence_char
        return result

    def is_keywords_in_text(self, keywords: list[str], text: str, lower_case: bool = True) -> bool:
        if lower_case == False:
            for key in keywords:
                if key not in text:
                    return False
            return True
        else:
            text = text.lower()
            for key in keywords:
                if key.lower() not in text:
                    return False
            return True

    def get_all_sub_string(self, text: str, get_less: bool = False) -> list[str]:
        if get_less == False:
            all_substring = []
            for index in range(len(text)):
                for index2 in range(len(text[index:])):
                    sub_string = text[index:index+index2+1]
                    all_substring.append(sub_string)
            return all_substring
        else:
            all_substring = set()
            lines = text.split("\n")
            for line in lines:
                words = line.split(" ")
                words_length = len(words)
                for index in range(words_length):
                    for index2 in range(words_length - index):
                        sub_string_list = words[index:index+index2+1]
                        the_sub_string = " ".join(sub_string_list).strip()
                        if the_sub_string != "":
                            all_substring.add(the_sub_string)
            return list(all_substring)

    def get_string_match_rating_level(self, input_text: str, text: str, lower_case: bool = True) -> float:
        """
        The higher, the more likely two string are equal

        Made by yingshaoxo
        """
        if lower_case == True:
            input_text = input_text.lower()
            text = text.lower()

        counting = 0
        negative_counting = 0
        sub_string_set = set()
        for index in range(len(input_text)):
            for index2 in range(len(input_text[index:])):
                sub_string = input_text[index:index+index2+1]

                if sub_string not in sub_string_set:
                    sub_string_set.add(sub_string)
                else:
                    continue

                length = index2+1
                if sub_string in text:
                    counting += length
                else:
                    negative_counting += length
                #print(sub_string, length)

        return counting/(negative_counting+counting)

    def get_fuzz_match_text_from_text_list(self, input_text: str, text_list: list[str], target_score: float | None = None, quick_mode: bool = False, input_sub_string_list: list[str] | None = None) -> tuple[str, str, str]:
        """
        It returns [previous_text, matched_text, next_text]
        """
        if quick_mode == True:
            keywords = input_text.split()
            new_keywords = []
            for keyword in keywords:
                new_keywords += keyword.split(" ")
            keywords = [one.strip() for one in new_keywords if one.strip() != ""]
            keywords = list(set(keywords))

            for index, value in enumerate(text_list):
                if self.is_keywords_in_text(keywords, text=value) == True:
                    previous_text = ""
                    if index > 0:
                        previous_text = text_list[index-1]
                    next_text = ""
                    if index < len(text_list) - 1:
                        next_text = text_list[index+1]
                    return previous_text, value, next_text

            return "", "", ""

        if input_sub_string_list == None:
            all_sub_string = list(set(self.get_all_sub_string(input_text)))
        else:
            all_sub_string = input_sub_string_list

        top_score = 0
        top_index = 0
        for index, value in enumerate(text_list):
            positive_counting = 0
            negative_counting = 0
            for sub_string in all_sub_string:
                if sub_string in value:
                    positive_counting += len(sub_string)
                else:
                    negative_counting += len(sub_string)
            score = positive_counting / (positive_counting + negative_counting)
            if target_score != None:
                if score >= target_score:
                    previous_text = ""
                    if index > 0:
                        previous_text = text_list[index-1]
                    next_text = ""
                    if index < len(text_list) - 1:
                        next_text = text_list[index+1]
                    return previous_text, value, next_text
            else:
                if score > top_score:
                    top_score = score
                    top_index = index

        previous_text = ""
        if top_index > 0:
            previous_text = text_list[top_index-1]
        next_text = ""
        if top_index < len(text_list) - 1:
            next_text = text_list[top_index+1]
        return previous_text, text_list[top_index], next_text

    def search_text_in_text_list(self, input_text: str, text_list: list[str], page_size: int = 10, page_number: int = 0, block_keyword_list: list[str] = []) -> list[str]:
        """
        It returns all matched text as a list
        """
        keywords = input_text.split()
        new_keywords = []
        for keyword in keywords:
            new_keywords += keyword.split(" ")
        keywords = [one.strip() for one in new_keywords if one.strip() != ""]
        keywords = list(set(keywords))

        if len(keywords) == 0:
            return []

        result_list = []
        for index, value in enumerate(text_list):
            if self.is_keywords_in_text(keywords, text=value) == True:
                if len(block_keyword_list) != 0 and self.is_keywords_in_text(block_keyword_list, text=value) == True:
                    continue
                result_list.append(value)

        start_index = page_number*page_size
        end_index = start_index + page_size
        return result_list[start_index:end_index]

    def get_common_text_in_text_list(self, text_list: list[str], frequency: int = 7, keywords_mode: bool = False) -> dict[str, dict[str, Any]]:
        """
        It will return a dict, where common part string is key, index list is value
        """
        global jieba
        if jieba == None:
            import jieba as jieba_
            jieba = jieba_

        final_dict = {}
        for current_index, current_text in enumerate(text_list):
            if keywords_mode == True:
                # it is for general natual language process
                all_sub_string_list = list(set(current_text.split()))

                new_list = []
                for one in all_sub_string_list:
                    if not one.isascii():
                        # for chinese
                        temp_list = [one.replace("。", "").replace("，", "").replace("？", "") for one in list(jieba.cut(one))]
                        temp_list = [one for one in temp_list if one.strip() != ""]
                        new_list += temp_list
                    else:
                        element = one.replace(".", "").replace(",", "").replace("?", "").strip()
                        if element != "":
                            new_list.append(element)
                all_sub_string_list = new_list

                all_sub_string_list = [one.strip() for one in all_sub_string_list]
                all_sub_string_list = list(set(all_sub_string_list))
            else:
                # accurate mode
                all_sub_string_list = list(set(self.get_all_sub_string(current_text)))

            for sub_string in all_sub_string_list:
                if sub_string in final_dict.keys():
                    continue
                counting = 0
                index_list = []
                for index, text in enumerate(text_list):
                    if index == current_index:
                        continue
                    if sub_string in text:
                        counting += 1
                        index_list.append(index)
                counting += 1
                if counting >= frequency:
                    final_dict.update({sub_string: {"counting": counting, "index_list": index_list}})
        return final_dict

    def get_meaning_group_dict_in_text_list(self, text_list: list[str], get_less: bool = True, level: int = 2, cut_half: bool = False, accurate_frequency: bool = False, code_parse_mode: bool = False) -> dict[str, int]:
        """
        text_list = ["How are you A.", "How are you B."]
        It returns ["How are you"]
        """
        def get_common_beginning(a_list: list[str]) -> str:
            length_list = [len(one) for one in a_list]
            common_part = ""
            for index in range(min(length_list)):
                the_char = a_list[0][index]
                if all([one[index]==the_char for one in a_list]):
                    common_part += the_char
                else:
                    break
            return common_part

        def get_common_endding(a_list: list[str]) -> str:
            a_list = [one[::-1] for one in a_list]
            return get_common_beginning(a_list)[::-1]

        if code_parse_mode == False:
            from auto_everything.ml import ML
            ml = ML()
            preprocessor = ml.Yingshaoxo_Text_Preprocessor()

            new_text_list = []
            for one in text_list:
                new_text_list += preprocessor.string_split_to_pure_sub_sentence_segment_list(one)
            text_list = new_text_list

        global_dict = {}
        window_size = 2
        i = 0
        while True:
            i += 1
            the_end = True
            for index in range(len(text_list)):
                if index < window_size:
                    continue
                sub_input_list = text_list[index-window_size:index]

                result_list = []
                key1 = get_common_beginning(sub_input_list)
                key2 = get_common_endding(sub_input_list)
                if key1.strip() != "":
                    result_list.append(key1)
                    the_end = False
                if key2.strip() != "":
                    result_list.append(key2)
                    the_end = False

                if get_less == False:
                    # get center text
                    if key1.strip() != "":
                        result_list += [one[len(key1):] for one in sub_input_list]
                    if key2.strip() != "":
                        result_list += [one[:-len(key2)] for one in sub_input_list]

                for key in result_list:
                    if key not in global_dict.keys():
                        global_dict[key] = 1
                        #print(result)
                    else:
                        global_dict[key] += 1

            if the_end == True:
                # no more common data to seperate
                break

            if get_less == False:
                # only in get_more mode, the level has meaning, it could do more parsing there
                if i >= level:
                    break
            else:
                break

            text_list = list(global_dict.keys())
            text_list.sort()

        # recount frequency
        if accurate_frequency == True:
            all_text = "".join(text_list)
            for key in global_dict.keys():
                global_dict[key] = all_text.count(key)

        # cut in half
        if cut_half == True:
            items = list(global_dict.items())
            items.sort(key=lambda x: (x[1], len(x[0])), reverse=True)
            items = items[:len(items)//2]
            global_dict = dict(items)

        return global_dict


if __name__ == "__main__":
    string_ = String()
    #print(string_.get_fuzz_match_text_from_text_list("d", ["dd", "c", "ab", "k"], quick_mode=True))
    #print(string_.search_text_in_text_list("d", ["dd", "c", "ab", "k"], block_keyword_list=["a"]))
    print(string_.get_all_sub_string("""
        fuck you, anny.
        because you are so honny.
    """, get_less=True))
