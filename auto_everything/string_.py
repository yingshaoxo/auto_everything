from __future__ import annotations

import string as built_in_string_module
from difflib import SequenceMatcher


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

    def compare_two_sentences(self, sentence1: str, sentence2: str) -> float:
        """
        return similarity, from `0.0` to `1.0`, 1 means equal, 0 means no relate.

        Parameters
        ----------
        sentence1: string

        sentence2: string
        """
        ratio = SequenceMatcher(None, sentence1, sentence2).ratio()
        return ratio

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

    def get_all_sub_string(self, text: str) -> list[str]:
        all_substring = []
        for index in range(len(text)):
            for index2 in range(len(text[index:])):
                sub_string = text[index:index+index2+1]
                all_substring.append(sub_string)
        return all_substring

    def get_string_match_rating_level(self, input_text: str, text: str, lower_case: bool = True) -> float:
        """
        The higher, the more likely two string are equal
        """
        if lower_case == True:
            input_text = input_text.lower()
            text = text.lower()

        counting = 0
        negative_counting = 0
        for index in range(len(input_text)):
            for index2 in range(len(input_text[index:])):
                sub_string = input_text[index:index+index2+1]
                length = index2+1
                if sub_string in text:
                    counting += length
                else:
                    negative_counting += length
                #print(sub_string, length)

        return counting/(negative_counting+counting)

    def get_fuzz_match_text_from_text_list(self, input_text: str, text_list: list[str], target_score: float | None = None, quick_mode: bool = False) -> tuple[str, str, str]:
        """
        It returns [previous_text, matched_text, next_text]
        """
        if quick_mode == True:
            keywords = input_text.split()
            new_keywords = []
            for keyword in keywords:
                new_keywords += keyword.split(" ")
            keywords = [one.strip() for one in new_keywords if one.strip() != ""]

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

        all_sub_string = self.get_all_sub_string(input_text)

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


if __name__ == "__main__":
    string_ = String()
    print(string_.get_fuzz_match_text_from_text_list("d", ["dd", "c", "ab", "k"], quick_mode=True))
