from __future__ import annotations
from typing import Any

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
        import string as built_in_string_module

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

    def _get_core_info_of_string(self, text):
        a_dict = dict()
        sequence_list = []
        for char in text:
            if char in a_dict:
                a_dict[char] += 1
            else:
                a_dict[char] = 1
                sequence_list.append(char)
        max_counting = -1
        for counting in a_dict.values():
            if counting > max_counting:
                max_counting = counting
        for key in a_dict.keys():
            a_dict[key] = int(a_dict[key]/max_counting*99)
        return sequence_list, a_dict

    def compare_two_sentences(self, sentence1: str, sentence2: str, using_yingshaoxo_method: bool = True) -> float:
        """
        return similarity, from `0.0` to `1.0`, 1 means equal, 0 means no relate.

        Parameters
        ----------
        sentence1: string

        sentence2: string
        """
        if using_yingshaoxo_method == True:
            #return self.get_string_match_rating_level(input_text = sentence1, text = sentence2)

            similarity0 = self.get_similarity_score_of_two_sentence_by_position_match(sentence1, sentence2)
            similarity1 = self.get_similarity_score_of_two_sentence_by_position_match(self.get_simple_hash(sentence1), self.get_simple_hash(sentence2))

            sequence_list_1, a_dict_1 = self._get_core_info_of_string(sentence1)
            sequence_list_2, a_dict_2 = self._get_core_info_of_string(sentence2)
            similarity2 = self.get_similarity_score_of_two_sentence_by_position_match("".join(sequence_list_1), "".join(sequence_list_2))

            char_set_1 = set(sequence_list_1)
            char_set_2 = set(sequence_list_2)
            common_char_set = char_set_1 & char_set_2
            similarity3 = len(common_char_set) / ((len(sequence_list_1) + len(sequence_list_2))/2)

            all_counting = 0
            counting_difference = 0
            for char in common_char_set:
                counting1 = a_dict_1[char]
                counting2 = a_dict_2[char]
                counting_difference += abs(counting1 - counting2)
                all_counting += a_dict_1[char] + a_dict_2[char]
            if all_counting == 0:
                similarity4 = 0
            else:
                similarity4 = (all_counting-counting_difference) / all_counting

            return similarity0 * 0.1 + similarity1 * 0.1 + similarity2 * 0.2 + similarity3 * 0.2 + similarity4 * 0.4
        else:
            from difflib import SequenceMatcher
            ratio = SequenceMatcher(None, sentence1, sentence2).ratio()
            return ratio

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

    def get_similarity_score_of_two_sentence_by_substring(self, sentence1, sentence2, end=False):
        """
        It returns a float in range of [0, 1], 1 means equal.
        This is also a extreamly quick method.
        """
        sentence1_length = len(sentence1)
        all_counting = 0
        match_counting = 0
        length = sentence1_length
        while length > 0:
            index = 0
            while True:
                if index > sentence1_length:
                    break
                sub_string = sentence1[index: index + length]
                if len(sub_string) == 0:
                    break
                if sub_string in sentence2:
                    match_counting += 1
                all_counting += 1
                index += length
            length = int(length / 2)
        result = match_counting / all_counting

        if end == False:
            result = (result + self.get_similarity_score_of_two_sentence_by_substring(sentence2, sentence1, end=True)) / 2
        return result

    def get_string_match_rating_level(self, input_text: str, text: str, lower_case: bool = True) -> float:
        """
        The higher, the more likely two string are equal
        We assume input_text length less than text, normally input_text is a search text

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

    def get_fuzz_hash(self, text: str, level: int = 128, seperator="_") -> str:
        """
        Compress long text into 128 char long text, so that you could use it to compare similarity.
        It works better with get_similarity_score_of_two_sentence_by_position_match(hash1, hash2)
        """
        hash_code = disk.get_hash_of_a_file_by_using_yingshaoxo_method("", bytes_data=text.encode("utf-8"), level=level, length=1, seperator=seperator, with_size=False)
        return hash_code

    def get_simple_hash(self, text, level=32, seperator="_"):
        """
        Can only used to identify the uniqueness of a file, in other words, get a shorter id of that file
        Don't use this function to do comparation.
        """
        hash_code = disk.get_simple_hash_of_a_file_by_using_yingshaoxo_method("", bytes_data=text.encode("utf-8"), level=level, seperator=seperator, with_size=False)
        return hash_code

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

    def get_common_string_list_in_text(self, text, get_less: bool = True, only_return_longest: bool = False) -> list[str]:
        all_sub_string_list = list(set(self.get_all_sub_string(text, get_less=get_less)))
        repeated_text_list = []
        for one in all_sub_string_list:
            check_index = text.find(one)
            if check_index != -1:
                if text.find(one, check_index + len(one)) != -1:
                    repeated_text_list.append(one)

        if only_return_longest:
            kill_list = []
            for index1, one1 in enumerate(repeated_text_list):
                for index2, one2 in enumerate(repeated_text_list):
                    if index1 != index2:
                        if one2 in one1:
                            kill_list.append(one2)

            final_list = []
            for one in repeated_text_list:
                if one not in kill_list:
                    final_list.append(one)

            return final_list
        else:
            return repeated_text_list

    def get_repeated_string_in_text_by_using_sub_window(self, text, window_length=4) -> dict[str, int]:
        text_length = len(text)

        cache_dict = dict()
        the_dict = dict()
        index = 0
        increasing_index = 0
        while True:
            sub_string = text[index: index+window_length]
            if sub_string != "":
                if sub_string not in cache_dict:
                    cache_dict[sub_string] = 1
                else:
                    cache_dict[sub_string] += 1
                    if cache_dict[sub_string] == 2:
                        the_dict[sub_string] = increasing_index
                        increasing_index += 1
                    index += window_length - 1
            index += 1
            if index >= text_length:
                break

        new_dict = {}
        for key in the_dict.keys():
            new_dict[key] = cache_dict[key]

        return new_dict

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

    def get_common_text_in_text_list(self, text_list: list[str], frequency: int = 7, keywords_mode: bool = False, get_less: bool = True) -> dict[str, dict[str, Any]]:
        """
        It will return a dict, where common part string is key, index list is value
        """
        final_dict = {}
        for current_index, current_text in enumerate(text_list):
            if keywords_mode == True:
                # it is for general natual language process
                all_sub_string_list = list(set(current_text.split()))

                chinese_stuff = ""
                new_list = []
                for one in all_sub_string_list:
                    if not one.isascii():
                        # for chinese
                        some_string = one.replace("。", "").replace("，", "").replace("？", "").strip()
                        if some_string != "":
                            chinese_stuff += some_string + " "
                    else:
                        element = one.replace(".", "").replace(",", "").replace("?", "").strip()
                        if element != "":
                            new_list.append(element)
                all_sub_string_list = new_list

                all_sub_string_list += self.get_common_string_list_in_text(chinese_stuff, get_less=True)

                all_sub_string_list = [one.strip() for one in all_sub_string_list]
                all_sub_string_list = list(set(all_sub_string_list))
            else:
                # accurate mode
                all_sub_string_list = list(set(self.get_all_sub_string(current_text, get_less=True)))

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

    def get_meaning_group_dict_in_text_list(self, text_list: list[str], get_less: bool = True, level: int = 2, code_parse_mode: bool = False) -> dict[str, int]:
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
            new_text_list = []
            for one in text_list:
                new_text_list += one.split("\n")
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
        all_text = "".join(text_list)
        for key in global_dict.keys():
            global_dict[key] = all_text.count(key)

        if "" in global_dict.keys():
            del global_dict[""]

        return global_dict

    def compress_text_by_using_yingshaoxo_method(self, text, common_part_list=[]) -> str:
        """
        Example: (the real output is a more compact string)

        Input:
            ("How are you? yingshaoxo.", common_part_list=["How are you", "yingshaoxo."])

        Returns:
            {"dict": {"1": "How are you", "-1": " ", "2": "yingshaoxo."}, "data_list": [1, -1, 2]}
        """
        """
        The method is simple,
            the first line contains a dict of {key, index}, for example, {ab:2, c:1}.
            the second line is pure text of index sequence, seperated by '_', for example "2_1_2", the real information is "abcab"
        The common string finding logic is: divide and conquer. We first split the big file into 7 parts. To see if it got two part equal, then we go on split smaller part into another 7 parts, to see if there has any common parts or not. If there has common part, we add it to index dict. We do this until cover all content, make it pure number index. Then we do a reverse sort, let small index represent big file part, big index represent small file part. the sort logic should be [length_bigger, frequency_more_appearence]

        Another way to find common stuff is to use the sub_string and count, when you find a string that apears twice, you make a index. After the first loop, you get a pure index list. Then you do the process to the pure index again to further compress. you stop until you can't find duplicate text. The key for this method is to use a small text to do the compression first, for example, 1 to 3 character permutation in set(all_text), so you would get sub_string quicker.

        Another way is to just use sub_string, but whenever you got a new substring, you replace it in old text to empty string. And you do this process to new index list until you find no repeat.
        """
        """
        Or return dict{1: "how are you", 2: " "} list[1,2,[1,0,3],2,[1,8,3]] to represent "how are you how you"
        The element format in list is [sub_sentence_id, start_index, length]
        The dict could get loaded in real time, the whole output data could use be a list, it contains either string or index
        """
        """
        Or you simply encode word or meaning group by split text using space
        """
        """
        todo: speed up encoding speed by using dict than loop list
        """
        def get_common_keyword_dict(text):
            all_substring = self.get_common_string_list_in_text(text, get_less=True, only_return_longest=True)
            the_dict = {}
            for one in all_substring:
                one = one.strip()
                if one not in the_dict.keys():
                    the_dict[one] = text.count(one)
            return the_dict

        frequency_dict = {}
        if common_part_list == None or common_part_list == []:
            frequency_dict = get_common_keyword_dict(text)
            for key, value in list(frequency_dict.items()):
                if len(key)-11 < 0:# or value < 10: # if use index will increase the size, we do nothing
                    del frequency_dict[key]
            common_part_list = list(frequency_dict.keys())
        else:
            if type(common_part_list) == dict:
                frequency_dict = common_part_list
            else:
                for one in common_part_list:
                    frequency_dict[one] = text.count(one)

        common_part_list = [one for one in common_part_list if one != ""]
        common_part_list.sort(key=lambda item: (frequency_dict[item], len(item)), reverse=True) # string from longest to shortest
        common_part_list_backup = common_part_list.copy()
        common_dict = {value: index+1 for index, value in enumerate(common_part_list)}
        result_list = []
        index = 0
        text_length = len(text)
        temp_text = ""
        while True:
            matched = False
            for part_index, part in enumerate(common_part_list.copy()):
                part_length = len(part)
                if text[index: index+part_length] == part:
                    if temp_text != "":
                        result_list.append(temp_text)
                        temp_text = ""

                    result_list.append(common_dict[part])
                    #print(index, part, part_length)
                    matched = True
                    index += part_length-1

                    # do deletion for those key that does not exists in following text any more
                    frequency_dict[part] -= 1
                    if frequency_dict[part] == 0:
                        del frequency_dict[part]
                        del common_part_list[part_index]

                    break
            if matched == False:
                single_char = text[index]
                temp_text += single_char
                #raise Exception(f"single char '{single_char}' not found in common_dict, which should not happen.")
                #result_list.append(single_char)

            index += 1
            if index >= text_length:
                break

        if temp_text != "":
            result_list.append(temp_text)

        special_char_1 = chr(1)
        special_char_2 = chr(2)

        new_dict_text = special_char_1.join([one.replace(special_char_1, "#") for one in common_part_list_backup])
        new_data_list = []
        for one in result_list:
            if type(one) == str:
                # pure text
                text_part = one.replace(special_char_1, "#")
                if len(new_data_list) > 0:
                    if new_data_list[-1].startswith(special_char_2):
                        new_data_list[-1] += text_part
                    else:
                        new_data_list.append(special_char_2 + text_part)
                else:
                    new_data_list.append(special_char_2 + text_part)
            else:
                # index
                new_data_list.append(str(one))

        return new_dict_text + "_____777_____yingshaoxo_____777_____" + special_char_1.join(new_data_list)

    def uncompress_text_by_using_yingshaoxo_method(self, text) -> str:
        """
        Example: (the real input is a more compact string)

        Input:
            {"dict": {"1": "How are you", "-1": " ", "2": "yingshaoxo."}, "data_list": [1, -1, 2]}

        Returns:
            "How are you? yingshaoxo."
        """
        special_char_1 = chr(1)
        special_char_2 = chr(2)

        dict_string, data_list_string = text.split("_____777_____yingshaoxo_____777_____")

        dict_ = {str(index+1):one for index, one in enumerate(dict_string.split(special_char_1))}
        data_list = data_list_string.split(special_char_1)

        result = ""
        for one in data_list:
            if one.startswith(special_char_2):
                result += one[1:]
            else:
                result += dict_[one]

        return result


if __name__ == "__main__":
    string_ = String()
