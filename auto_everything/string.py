from __future__ import annotations
import string as built_in_string_module


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