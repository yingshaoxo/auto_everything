from typing import Any
import random
import os
import re
import json

from auto_everything.terminal import Terminal, Terminal_User_Interface
from auto_everything.disk import Disk, Store
from auto_everything.io import IO
from auto_everything.language import Language
from auto_everything.time import Time
from auto_everything.string_ import String
disk = Disk()
io_ = IO()
language = Language()
terminal = Terminal()
terminal_user_interface = Terminal_User_Interface()
time_ = Time()
store = Store('auto_everything_ml_module')
string_ = String()


class DataProcessor():
    """
    To implement some functionality related to data
    """

    def __init__(self):
        pass

    def get_time_series_data_from_a_list(self, the_list, sequence_length):
        """
        Get sub sequences for LSTM network.

        Parameters
        ----------
        the_list:
        sequence_length: int
            how long you want the subsequence to be.

        Returns
        -------
        tuple
            return ([features], [labels])
        """
        assert len(the_list) >= sequence_length + 1, "len(the_list) should >= sequence_length + 1"
        array_1d = []
        array_2d = []
        array_target = []
        for element in the_list:
            array_1d.append(element)
            if len(array_1d) == sequence_length + 1:
                target = array_1d.pop()
                array_target.append(target)
                array_2d.append(array_1d.copy())
                array_1d.clear()
        return array_2d, array_target


#####
#Some basic functions
#####
class Yingshaoxo_Text_Preprocessor():
    def split_string_into_list_by_punctuations(self, input_text, special_punctuations = "\n ，。；！@#￥%……&*（）-——+=『【』】|、：；“‘～`《》，。？/~`!@#$%^&*()_+-={}[]|\:;\"'<,>.?/,.!?()[]{}<>;:’‘“”\"'`’‘「」『』【】〖〗《》《 》〈 〉〔 〕（ ）﹙ ﹚【 】［ ］｛ ｝〖 〗「 」『 』《 》〈 〉《》〔 〕【 】（ ）﹙﹚｛ ｝‘ ’“ ”‘ ’“ ”〞 〝— -—— ……~·•※☆★●○■□▲△▼▽⊙⊕⊖⊘⊚⊛⊜⊝◆◇◊⊿◣◢◥◤@#$%^&*+=_|\\/:;", not_include_punctuations: str = ""):
        """
        return list like: [
            { "language": "punctuation", "text": },
            { "language": "not_punctuation", "text": },
        ]
        it should be a mixed result list, the order of punctuation and not_punctuation should follow orginal text
        """
        if input_text.strip() == "":
            return []

        if not_include_punctuations != "":
            for char in not_include_punctuations:
                special_punctuations = special_punctuations.replace(char, "")

        result_list = []
        index = 0
        temp_string = ""
        last_punctuation_flag =True
        if len(input_text) > 0:
            if input_text[-1] in special_punctuations:
                last_punctuation_flag = True
            else:
                last_punctuation_flag = False
        is_punctuation = True
        while True:
            current_char = input_text[index]

            if current_char in special_punctuations:
                is_punctuation = True
            else:
                is_punctuation = False

            if last_punctuation_flag != is_punctuation:
                if last_punctuation_flag == True:
                    result_list.append({
                        "language": "punctuation",
                        "text": temp_string
                    })
                else:
                    result_list.append({
                        "language": "not_punctuation",
                        "text": temp_string
                    })
                temp_string = ""

            last_punctuation_flag = is_punctuation
            temp_string += current_char

            index += 1
            if index >= len(input_text):
                break

        if len(result_list) > 0:
            if result_list[0]["text"] == "":
                result_list = result_list[1:]
        if temp_string != "":
            is_punctuation = True
            if temp_string[-1] in special_punctuations:
                is_punctuation = True
            else:
                is_punctuation = False

            if is_punctuation == True:
                result_list.append({
                    "language": "punctuation",
                    "text": temp_string
                })
            else:
                result_list.append({
                    "language": "language",
                    "text": temp_string
                })

        return result_list

    def split_string_into_english_and_not_english_list(self, input_text):
        """
        Split a string into a list of language segments based on Chinese and English characters.

        :param input_text: The input string to split.
        :return: A list of language segments with Chinese and English text.
        """
        """
        return list like: [
            { "language": "en", "text": },
            { "language": "not_en", "text": },
        ]
        """
        if input_text.strip() == "":
            return []

        result_list = []
        index = 0
        temp_string = ""
        last_punctuation_flag = False
        if len(input_text) > 0:
            if input_text[-1].isascii():
                last_punctuation_flag = True
            else:
                last_punctuation_flag = False
        is_en = True
        while True:
            current_char = input_text[index]

            if current_char.isascii():
                is_en = True
            else:
                is_en = False

            if last_punctuation_flag != is_en:
                if last_punctuation_flag == False:
                    result_list.append({
                        "language": "not_en",
                        "text": temp_string
                    })
                else:
                    result_list.append({
                        "language": "en",
                        "text": temp_string
                    })
                temp_string = ""

            last_punctuation_flag = is_en
            temp_string += current_char

            index += 1
            if index >= len(input_text):
                break

        if len(result_list) > 0:
            if result_list[0]["text"] == "":
                result_list = result_list[1:]
        if temp_string != "":
            if temp_string[-1].isascii():
                is_en = True
            else:
                is_en = False

            if is_en == False:
                result_list.append({
                    "language": "not_en",
                    "text": temp_string
                })
            else:
                result_list.append({
                    "language": "en",
                    "text": temp_string
                })

        return result_list

    def string_split_by_using_yingshaoxo_method(self, input_text, without_punctuation: bool = False):
        """
        Split a string into language segments based on punctuations, English and not_English text.

        return list like: [
            { "language": "en", "text": },
            { "language": "not_en", "text": },
            { "language": "punctuation", "text": },
        ]
        """
        if input_text.strip() == "":
            return []

        final_list = []
        punctuation_list = self.split_string_into_list_by_punctuations(input_text)
        for one in punctuation_list:
            if one["language"] == "punctuation":
                if without_punctuation == False:
                    final_list.append({
                        "language": "punctuation",
                        "text": one["text"]
                    })
                else:
                    pass
            else:
                language_list = self.split_string_into_english_and_not_english_list(one["text"])
                final_list += language_list
        return final_list

    def string_split_to_pure_segment_list_by_using_yingshaoxo_method(self, input_text, without_punctuation: bool = False) -> list[str]:
        """
        Split a string into language segments based on punctuations, English and not_English text.

        return list like: ["how", "are", "you", "?"]
        """
        if input_text.strip() == "":
            return []

        final_list = []
        a_list = self.string_split_by_using_yingshaoxo_method(input_text, without_punctuation=without_punctuation)
        for one in a_list:
            if one["language"] == "not_en":
                final_list += list(one["text"])
            else:
                final_list += [one["text"]]
        return final_list


    def string_split_to_pure_sub_sentence_segment_list(self, input_text, without_punctuation: bool = True, without_number: bool = True, not_include_punctuations: str="' _*->#") -> list[str]:
        sentence_segment_list = self.split_string_into_list_by_punctuations(input_text, not_include_punctuations=not_include_punctuations)
        new_list = []
        for segment in sentence_segment_list:
            if segment["language"] == "punctuation":
                if without_punctuation == True:
                    continue
                else:
                    if len(new_list) == 0:
                        new_list = [segment["text"]]
                    else:
                        new_list[-1] += segment["text"]
            else:
                if without_number == True:
                    if segment["text"].isdigit():
                        continue
                    else:
                        new_list.append(segment["text"])
                else:
                    if segment["text"].isdigit():
                        new_list += list(segment["text"])
                    else:
                        new_list.append(segment["text"])
        return new_list

    def is_english_string(self, text: str) -> bool:
        return text.isascii()


class Yingshaoxo_Text_Transformer():
    """
    We will use char level operation to get unknown keywords regex from "multiple key -> one value" data pairs

    Hi AA -> Hi you.
    Hi BB -> Hi you.
    Hi CC -> Hi you.

    We need to get "Hi (.*?) -> Hi you." from above data automatically.



    Did you see AA? => I see AA.
    Did you see BB? => I see BB.

    We need to get "Did you see (?P<someone>.*?)? -> I see {someone}." from above data automatically.



    That is steven, my uncle. => I see, steven is your uncle.
    That is wind_god, my uncle. => I see, wind_god is your uncle.

    We need to get "That is (?P<name>.*?), my uncle. => I see, {name} is your uncle." from above data automatically.
    """

    """
    Or, you could think it as a very simple problem, if you got current_line of text, if some sub_string appears in the next_line of text, you can safely replace it with regex expression.

    For example: what is the age of uncle? => uncle is 18 years old.

    You can just do a search for every sub_string in the first sentence, if that substring appears 1 or more times in the second sentence, you get a general regex sentence.

    For example: what is the age of (?P<name>.*?)? => {name} is 18 years old.

    And later when you meet new input, if it full matchs any regex expression, you return following sentence with related content formated. In other words, you are returning a reactive answer than fixed answer.
    """

    """
    Source Text: Did you see AA?\nI see AA.

    Generalized Text: Did you {see} {AA}?\n I {see} {AA}.

    So next time when you meet "Did you attack that monster?", you will get "\n I attack that monster." because of "Did you {attack} {that monster}\n I {attack} {that monster}."

    #ai #idea #yingshaoxo
    """
    """
    def get_regex_expression_from_current_text_and_following_text(self, current_text: str, following_text: str, meaning_group_list: list[str] = []) -> tuple[str, str]:
        if len(meaning_group_list) == 0:
            sub_string_list = string_.get_all_sub_string(text=current_text)
        else:
            sub_string_list = meaning_group_list
        sub_string_list.sort(key=len, reverse=True)

        fake_current_text = current_text
        fake_following_text = following_text
        new_current_text = current_text
        new_following_text = following_text
        counting = 0
        for index, sub_string in enumerate(sub_string_list):
            if (sub_string in fake_current_text) and (sub_string in fake_following_text):
                fake_following_text = fake_following_text.replace(sub_string, "")
                new_current_text_list = new_current_text.split(sub_string)
                new_current_text_list = [re.escape(one)  for one in new_current_text_list]
                new_current_text = f"(.*?)".join(new_current_text_list)
                #new_current_text = new_current_text.replace(sub_string, f"(?P<y{counting}>.*?)") # You have to find a way to avoid new sub_string replace old regex expression
                new_following_text = new_following_text.replace(sub_string, "{}")
                counting += 1
                break

        return new_current_text, new_following_text
    """
    def _number_to_fake_alphabet(self, id_, number):
        return f"a_{id_}_{number}"

    def _fake_alphabet_to_number(self, string):
        return string.split("_")[1]

    def _escape_regex_expression(self, expression):
        result = ""
        index = 0
        if expression[:4] == "(?P<":
            result += expression[:4]
            index += 4
            end_index = index + 1
            for temp_index, temp_char in enumerate(expression[index+1:]):
                if expression[index+1+temp_index:].startswith(">.*)"):
                    end_index = index+1+temp_index+len(">.*)")
                    break
            result += expression[index+1: end_index]
            index = end_index
        while True:
            if index >= len(expression)-1:
                result += re.escape(expression[-1])
                break

            char = expression[index]
            next_4_chars = expression[index+1: index+1 + 4]
            if next_4_chars != "(?P<":
                result += re.escape(char)
                index += 1
            else:
                result += re.escape(char)
                end_index = index + 1
                for temp_index, temp_char in enumerate(expression[index+1:]):
                    if expression[index+1+temp_index:].startswith(">.*)"):
                        end_index = index+1+temp_index+len(">.*)")
                        break
                result += expression[index+1: end_index]
                index = end_index
        return result

    def _check_if_regex_expression_is_valid(self, expression, string, next_string) -> bool:
        #print("fuck:", expression)
        try:
            result = re.fullmatch(expression, string, flags=re.DOTALL)
            #print(expression, string, result)
            if result == None:
                return False
            else:
                # You have to find a way to drop bad match, for example, if a_1_0 and a_1_1 does not equal, it is a wrong match
                data = dict(result.groupdict())
                check_dict = {}
                for key, value in data.items():
                    real_key = self._fake_alphabet_to_number(key)
                    if real_key not in check_dict:
                        check_dict[real_key] = value
                    else:
                        if value != check_dict[real_key]:
                            return False
                    # make sure next string also starts with space or end with space
                    # todo: here has a bug
                    start_index = 0
                    value_length = len(value)
                    while True:
                        index = next_string.find(value, start_index)
                        if index == -1:
                            break
                        if (next_string[index-1] != " " and next_text[index+value_length+1] != " "):
                            if (next_string[index-1] != " ") and (index != 0):
                                if (next_string[index+value_length+1] != " ") and (index+value_length != len(next_string) - 1):
                                    return False
                        start_index = index + value_length
        except Exception as e:
            #print(e)
            return False

        # remove any regex that does not have space in before and end
        while expression.startswith("(?P<"):
            expression = expression[4:]
        while expression.endswith(">.*)"):
            expression = expression[:-4]
        expression = expression.replace("\ (?P<", "")
        expression = expression.replace(">.*)\ ", "")
        if "(?P<" in expression or ">.*)" in expression:
            return False

        return True

    def get_regex_expression_from_current_text_and_following_text(self, current_text: str, following_text: str, meaning_group_list: list[str] = []) -> tuple[str, str]:
        """
        {
            (?P<a_0_0>.*) is (?P<a_0_1>.*), (?P<a_1_0>.*) is (?P<b_1_1>.*).:
            A is A, B is B.
        """
        if len(meaning_group_list) == 0:
            sub_string_list = string_.get_all_sub_string(text=current_text, get_less=True)
        else:
            sub_string_list = [one for one in list(set(meaning_group_list)) if one.strip() != ""]
        sub_string_list.sort(key=len, reverse=True) # longer first
        #print(sub_string_list)
        if "a" in sub_string_list:
            del sub_string_list[sub_string_list.index('a')]

        fake_current_text = current_text
        fake_following_text = following_text
        new_current_text = current_text
        new_following_text = following_text
        id_ = 0
        for index, sub_string in enumerate(sub_string_list):
            if fake_current_text.strip() == "" or fake_following_text.strip() == "":
                break

            if (sub_string in fake_current_text) and (sub_string in fake_following_text):
                fake_current_text_backup = fake_current_text
                fake_following_text_backup = fake_following_text
                new_current_text_backup = new_current_text
                new_following_text_backup = new_following_text

                fake_current_text = fake_current_text.replace(sub_string, "")
                fake_following_text = fake_following_text.replace(sub_string, "")

                new_current_text_list = new_current_text.split(sub_string)
                #new_current_text_list = [re.escape(one) for one in new_current_text_list]
                new_current_text = ""
                for index, one in enumerate(new_current_text_list):
                    if index == 0:
                        new_current_text += one
                    else:
                        fake_id = self._number_to_fake_alphabet(id_, index-1)
                        new_current_text += f"(?P<{fake_id}>.*)" + one
                temp_following_text = new_following_text

                index = 0
                while True:
                    fake_id = self._number_to_fake_alphabet(id_, index)
                    new_following_text = new_following_text.replace(sub_string, f"{{{fake_id}}}", 1)
                    if temp_following_text == new_following_text:
                        break
                    temp_following_text = new_following_text
                    index += 1
                    if index > 20:
                        break

                #print(fake_current_text)
                #print(fake_following_text)
                #print(new_current_text)
                #print(new_following_text)
                #print(new_current_text)

                if self._check_if_regex_expression_is_valid(self._escape_regex_expression(new_current_text), current_text, following_text) == False:
                    fake_current_text = fake_current_text_backup
                    fake_following_text = fake_following_text_backup
                    new_current_text = new_current_text_backup
                    new_following_text = new_following_text_backup
                    continue
                else:
                    id_ += 1

        return new_current_text, new_following_text

    def get_regex_expression_version_string_dict(self, input_text: str, seporator: str = "\n", meaning_group_list: list[str] = []) -> dict[str, str]:
        final_dict = {}

        text_list = input_text.split(seporator)
        for index, text in enumerate(text_list):
            if index + 1 > len(text_list) - 1:
                break

            text = text.strip()
            next_text = text_list[index+1].strip()
            if text != "" and next_text != "":
                key, value = self.get_regex_expression_from_current_text_and_following_text(text, next_text, meaning_group_list)
                #print(key, value)
                final_dict[key] = value

        return final_dict

    def get_regex_expression_dict_from_input_and_output_list(self, input_text_list: list[str], output_text_list: list[str], meaning_group_list: list[str] = []) -> dict[str, str]:
        the_dict = {}
        for index in range(len(input_text_list)):
            source_text = input_text_list[index]
            target_text = output_text_list[index]
            key, value = self.get_regex_expression_from_current_text_and_following_text(source_text, target_text, meaning_group_list)
            the_dict[key] = value
        return the_dict

    def _get_complex_transforming_dict_for_translation(self, input_text_list: list[str], output_text_list: list[str], window_size: int = 100) -> dict[str, str]:
        if len(input_text_list) != len(output_text_list):
            raise Exception("The input_text_list should have the same length of output_text_list")

        """
        You have to get the recursive version of data manually.
        For example, analyze the input_text_list, get common words or substring.
        Then find common words or substring in output_text_list.
        Then do a loop for input common substring list, let user choose what output common sub_string is linked to that input substring, after user do 100 times of choose, it can be very accurate. (This process can be simplifyed by using all output substring to match the current input output, to limit or scale down the choice for the output substring
        """
        existing_dict = {}

        for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ',.:":
            if char not in existing_dict.keys():
                existing_dict[char] = char

        for index in range(len(input_text_list)):
            if index < window_size:
                continue
            sub_input_list = input_text_list[index-window_size:index]
            sub_output_list = output_text_list[index-window_size:index]
            input_dict = string_.get_common_text_in_text_list(sub_input_list, frequency=3, keywords_mode=True)
            output_dict = string_.get_common_text_in_text_list(sub_output_list, frequency=3, keywords_mode=True)
            for sub_string in sorted(input_dict.keys(), key=len, reverse=False):
                if sub_string in existing_dict.keys():
                    continue
                output_source_list = []
                for target_index in input_dict[sub_string]["index_list"]:
                    output_source_list.append(sub_output_list[target_index])
                for one in output_dict.keys():
                    if input_dict[sub_string] == output_dict[one]:
                        value = one
                        data_piece = {sub_string: value}
                        print(data_piece)
                        existing_dict.update(data_piece)
                        break

        for index in range(len(input_text_list)):
            source_text = input_text_list[index]
            target_text = output_text_list[index]
            key, value = self.get_regex_expression_from_current_text_and_following_text(source_text, target_text)
            existing_dict[key] = value

        return existing_dict

    def pure_string_dict_based_sequence_transformer(self, input_text: str, the_dict: dict[str, str], add_space: bool = False) -> str:
        """
        no regex is allowed in here
        """
        dict_items = list(the_dict.items())
        dict_items.sort(key=lambda item: len(item[0]), reverse=True)
        result = ""
        while True:
            did_change = False
            for key, value in dict_items:
                if input_text.startswith(key) and key != "":
                    result += value
                    if add_space == True:
                        result += " "
                    input_text = input_text[len(key):]
                    did_change = True
                    break
            if did_change == False:
                result += input_text
                return result

    def yingshaoxo_regex_expression_based_transformer(self, input_text: str, regex_expression_dict: dict[str, str]) -> str:
        """
        If you want to let it smarter or equal than google bard chat ai, you have to use recursive function
        You have to recursively replace the context (the one inside of (.*?)) to a detailed information
        For example, "How to make love?", the first template it meets is "How to (.*?)"
        The answer is probabally "If you want to make love, you have to:\nmake love"
        But it's not done yet, you have to use 'make love' as keyword, search regex_expression_dict to get a more detaild info/value
        In the end, you'll get a detaild response: "If you want to make love, you have to:\n1.ask permission from the one you want to make love with..."
        """
        for key in sorted(list(regex_expression_dict.keys()), key=len, reverse=True):
            try:
                result = re.match(key, input_text, flags=re.DOTALL)
                if result != None:
                    #print(dict(result.groupdict()))
                    # You have to find a way to drop bad match, for example, if a_1_0 and a_1_1 does not equal, it is a wrong match
                    return regex_expression_dict[key].format(**dict(result.groupdict()))
            except Exception as e:
                pass
        return ""

    '''
    def yingshaoxo_regex_expression_based_recursive_transformer(self, input_text: str, regex_expression_dict: dict[str, str]) -> str:
        """
        This is good for 1:1 transformer, for example, translation dataset, but should also doing fine in email replying dataset.
        """
        regex_keys = sorted(list(regex_expression_dict.keys()), key=len, reverse=True)
        def the_transformer(input_text: str) -> str:
            for key in regex_keys:
                result = re.search(key, input_text, flags=re.DOTALL)
                if result != None:
                    if len(result.groups()) < 1:
                        # no regex inside of that dict
                        #return regex_expression_dict[key]
                        continue

                    value = result.group(1)

                    dict_value = regex_expression_dict[key]
                    dict_value_splits = dict_value.split("{}")

                    next_level_value = the_transformer(value)
                    if next_level_value != "":
                        return next_level_value.join(dict_value_splits)
                    else:
                        return value.join(dict_value_splits)

            if input_text.strip() == "":
                return ""

            result = ""
            did_change = False
            for key in regex_keys:
                if input_text.startswith(key) and key != "":
                    result += regex_expression_dict[key]
                    input_text = input_text[len(key):]
                    did_change = True
                    break
            if did_change == False:
                # can't do anything here
                return ""
            else:
                result += the_transformer(input_text)
                return result

        return the_transformer(input_text)
    '''


class Yingshaoxo_Text_Generator():
    """
    # dict based next word generator

    ```
    One character predict next character
    two character predict next character
    ...
    One word predict next word
    Two words predict next word
    Three words predict next word
    ... words predict next word
    ```

    When you use it, use it from bottom to top, use longest sequence to predict the next word first.
    """
    """
    Extreme Lite version of chatgpt:

    Use one sentence predicts the next concept word. Then use concept word to predict next x words.

    What it is? Call wiki.
    Why? Call a wiki or Q&A site.
    How to do it? Call a Q&A website.
    How to write code? Call stackiverflow.

    > use text similarity to do the search

    #lite #chatgpt #yingshaoxo
    """
    """
    1. First you have to have a folder where has multiple txt files
    2. This class will parse those text, convert it into 30000, 3000, 300, 30, 3, 1 char length sub_context_window, we slide that window by one char each search time
    3. If we found previous x_chars matchs the input_text user asks in our database, we return the following chars from database to the user
    4. Normally, we'll add a formater to the end of pipeline to format the final result to make it looks better.

    Second method is to do it with full-match, we only return full-match following text, if it can't get the following text, we do the search again with input_text[1:]
    And we could also use a transformer to get 1000 different ways format of the input_text, then do the full_match again.

    Third method:
        利用类似于谷歌search一样的东西
        加上问答系统，你也可以制作一个ChatGPT，并且准确率特别高
        举个例子，把input_text放进谷歌搜索，将第一页所有网页的内容作为问答系统的context
        准确率将高得惊人
        https://huggingface.co/distilbert-base-cased-distilled-squad?context=My+name+is+%E8%83%A1%E8%8B%B1%E6%9D%B0&question=What+is+my+name%3F

    Wha kind of problem I have solved using traditional programming (similarity)?
    1. ChatBot
    2. Sentence translation
    3. Grammar correction
    4. Punctuation Correction Or Adding
    5. Code completion
    6. Sentence rewrite
    """
    def __init__(self, input_txt_folder_path: str = "", type_limiter: list[str] = [".txt", ".md"], use_machine_learning: bool = False, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.input_txt_folder_path = input_txt_folder_path

        if input_txt_folder_path == "":
            self.text_source_data = ""
        else:
            self.text_source_data = self.get_source_text_data_by_using_yingshaoxo_method(input_txt_folder_path=input_txt_folder_path, type_limiter=type_limiter)
            self.lower_case_text_source_data = self.text_source_data.lower()

        self.use_machine_learning = use_machine_learning
        if (use_machine_learning == True):
            # pip install sentence_transformers
            from sentence_transformers import SentenceTransformer, util
            self.sentence_transformers_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.sentence_transformers_utility = util

        self.text_preprocessor = Yingshaoxo_Text_Preprocessor()

    def get_source_text_data_by_using_yingshaoxo_method(self, input_txt_folder_path: str, type_limiter: list[str] = [".txt", ".md"]) -> str:
        text_source_data = ""
        if disk.exists(input_txt_folder_path):
            files = disk.get_files(input_txt_folder_path, recursive=True, type_limiter=type_limiter, use_gitignore_file=True)
            for file in files:
                text_source_data += io_.read(file)
            return text_source_data
        else:
            return ""

    def get_global_string_dict_by_using_yingshaoxo_method(self, source_text_data: str, levels: int = 10):
        global_string_dict = {
        }

        def get_x_level_dict(source_text: str, x: int):
            level_dict = {}
            for index, _ in enumerate(source_text):
                if index < (x-1):
                    continue
                if index == len(source_text) - x:
                    break
                current_chars = source_text[index-(x-1): index+1]
                next_char = source_text[index+1]
                if current_chars in level_dict:
                    if next_char in level_dict[current_chars]:
                        level_dict[current_chars][next_char] += 1
                    else:
                        level_dict[current_chars][next_char] = 1
                else:
                    level_dict[current_chars] = {next_char: 1}

            pure_level_dict = {}
            for key, value in level_dict.items():
                biggest_value = 0
                biggest_key = None
                for key2, value2 in value.items():
                    if value2 > biggest_value:
                        biggest_value = value2
                        biggest_key = key2
                pure_level_dict[key] = biggest_key

            return pure_level_dict

        max_level = levels
        for level in reversed(list(range(1, 1+max_level))):
            global_string_dict[level] = get_x_level_dict(source_text_data, level)

        return global_string_dict

    def get_next_x_chars_by_using_yingshaoxo_method(self, input_text: str, x: int, levels: int = 10, source_text_data: str|None = None, global_string_dict: dict|None = None) -> Any:
        """
        This will generate text based on hash map or hash dict. If you use it in memory, the speed would be super quick.

        ChatGPT4 uses levels of 8049.

        Normally you just have to set levels to 50 for small dataset.
        """
        if source_text_data == None:
            source_text_data = self.text_source_data

        if global_string_dict != None:
            pass
        else:
            global_string_dict = self.get_global_string_dict_by_using_yingshaoxo_method(source_text_data, levels)

        def predict_next_char(input_text: str):
            for level in global_string_dict.keys():
                last_chars = input_text[len(input_text)-level:]
                if last_chars in global_string_dict[level].keys():
                    return global_string_dict[level][last_chars]
            return None

        def predict_next_x_chars(input_text: str, x: int):
            complete_text = input_text
            for _ in range(x):
                result = predict_next_char(complete_text)
                if result == None:
                    break
                else:
                    complete_text += result
            return complete_text

        final_text = predict_next_x_chars(input_text=input_text, x=x)
        return final_text[len(input_text):]

    def get_global_string_corrector_dict_by_using_yingshaoxo_method(self, source_text_data: str, levels: int = 10, for_minus_character: bool = False):
        global_string_dict = {
        }

        seperator = "☺"

        def get_x_level_dict(source_text: str, x: int):
            level_dict = {}
            for index, _ in enumerate(source_text):
                if index < x:
                    continue
                #if index == len(source_text) - x:
                #    break
                if for_minus_character == True:
                    current_chars = source_text[index-x: index] + seperator + source_text[index: index+x]
                    center_char = ""
                else:
                    current_chars = source_text[index-x: index] + seperator + source_text[index+1: index+x+1]
                    center_char = source_text[index]
                if current_chars in level_dict:
                    if center_char in level_dict[current_chars]:
                        level_dict[current_chars][center_char] += 1
                    else:
                        level_dict[current_chars][center_char] = 1
                else:
                    level_dict[current_chars] = {center_char: 1}

            pure_level_dict = {}
            for key, value in level_dict.items():
                biggest_value = 0
                biggest_key = None
                for key2, value2 in value.items():
                    if value2 > biggest_value:
                        biggest_value = value2
                        biggest_key = key2
                pure_level_dict[key] = biggest_key

            return pure_level_dict

        max_level = levels
        for level in reversed(list(range(1, 1+max_level))):
            global_string_dict[level] = get_x_level_dict(source_text_data, level)
            break

        return global_string_dict

    def correct_sentence_by_using_yingshaoxo_method(self, input_text: str, levels: int = 6, source_text_data: str|None = None, global_string_corrector_dict: dict|None = None, plus_character: bool = False, minus_character: bool = False) -> any:
        """
        This will correct text based on pure text or hash map or hash dict. if you use it in memory, the speed would be super quick.
        If you can modify this function from char level to word level, the accuracy could be 100%.
        """
        if source_text_data == None:
            source_text_data = self.text_source_data

        if global_string_corrector_dict != None:
            pass
        else:
            global_string_corrector_dict = self.get_global_string_corrector_dict_by_using_yingshaoxo_method(source_text_data, levels)

        input_text = "\n"*len(global_string_corrector_dict) + input_text + "\n"*len(global_string_corrector_dict)

        seperator = "☺"
        new_text = ""
        for level in global_string_corrector_dict.keys():
            for index, _ in enumerate(input_text):
                if index < (level-1):
                    new_text += input_text[index]
                    continue
                if index >= len(input_text) - level:
                    new_text += input_text[index]
                    continue
                if plus_character == True:
                    current_chars = input_text[index-level: index] + seperator + input_text[index: index+level]
                    if current_chars in global_string_corrector_dict[level].keys():
                        new_text += global_string_corrector_dict[level][current_chars] + input_text[index]
                    else:
                        new_text += input_text[index]
                elif minus_character == True:
                    current_chars = input_text[index-level: index] + seperator + input_text[index+1: index+1+level]
                    if current_chars in global_string_corrector_dict[level].keys():
                        new_text += ""
                    else:
                        new_text += input_text[index]
                else:
                    current_chars = input_text[index-level: index] + seperator + input_text[index+1: index+1+level]
                    if current_chars in global_string_corrector_dict[level].keys():
                        new_text += global_string_corrector_dict[level][current_chars]
                    else:
                        new_text += input_text[index]
            break
        return new_text

    def correct_sentence_by_using_yingshaoxo_regex_method(self, input_text: str, source_data_text: str, level: int=3) -> str:
        import re

        def find_match_string_in_source_data(before_chars: str, after_chars: str, for_minus_character: bool = False):
            before_chars = re.escape(before_chars)
            after_chars = re.escape(after_chars)
            if for_minus_character == True:
                result_list = re.findall(pattern=f"{before_chars}{after_chars}", string=source_data_text)
            else:
                result_list = re.findall(pattern=f"{before_chars}(.){after_chars}", string=source_data_text, flags=re.DOTALL)
            counting_dict = {}
            for one in result_list:
                if one in counting_dict.keys():
                    counting_dict[one] += 1
                else:
                    counting_dict[one] = 1
            items = list(counting_dict.items())
            items.sort(key=lambda item: item[1], reverse=True)
            if len(items) > 0:
                return items[0][0]
            else:
                return None

        def do_the_process(input_text: str, plus_character: bool = False, minus_character: bool = False) -> str:
            new_text = ""
            for index, _ in enumerate(input_text):
                if index < (level-1):
                    new_text += input_text[index]
                    continue
                if index >= len(input_text) - level:
                    new_text += input_text[index]
                    continue

                if plus_character == True:
                    before_chars = input_text[index-level: index]
                    after_chars = input_text[index: index+level]
                    new_chars = find_match_string_in_source_data(before_chars, after_chars)
                    if new_chars != None:
                        new_text += new_chars + input_text[index]
                    else:
                        new_text += input_text[index]
                elif minus_character == True:
                    before_chars = input_text[index-level: index]
                    after_chars = input_text[index+1: index+1+level]
                    new_chars = find_match_string_in_source_data(before_chars, after_chars, for_minus_character=True)
                    if new_chars != None:
                        new_text += ""
                    else:
                        new_text += input_text[index]
                else:
                    before_chars = input_text[index-level: index]
                    after_chars = input_text[index+1: index+1+level]
                    new_chars = find_match_string_in_source_data(before_chars, after_chars)
                    if new_chars != None:
                        new_text += new_chars
                    else:
                        new_text += input_text[index]
            return new_text

        # minus acb to ab
        input_text = do_the_process(input_text, minus_character=True)

        # correct a*c to abc
        input_text = do_the_process(input_text)

        # plus ac to abc
        input_text = do_the_process(input_text, plus_character=True)

        return input_text

    def sort_sub_sentence_in_text(self, input_text: str, source_text: str) -> list[str]:
        """
        If you have input_text "Thank you. I'm fine."
        If you have source_text "I'm fine. Thank you."
        You will get ["I'm fine", "Thank you."]
        """
        sub_sentence_sort_list =  self.text_preprocessor.string_split_to_pure_sub_sentence_segment_list(source_text, without_punctuation=True)
        input_text_sub_sentence_list = self.text_preprocessor.string_split_to_pure_sub_sentence_segment_list(input_text, without_punctuation=True)

        def _sort_by_source_order_unknown(input_list, source_order_list):
            """Sorts the input_list by the source_order_list order, and keep unknown elements in input_list order untouched."""

            # Create a dictionary mapping each element in source_order_list to its index.
            element_to_index = {element: i for i, element in enumerate(source_order_list)}

            # Create a list of known elements and a list of unknown elements.
            known_elements = []
            unknown_elements = []
            for element in input_list:
                if element in element_to_index:
                    known_elements.append(element)
                else:
                    unknown_elements.append(element)

            # Sort the known elements using the dictionary as a key.
            sorted_known_elements = sorted(known_elements, key=lambda element: element_to_index[element])

            # Combine the sorted known elements and the unknown elements.
            sorted_list = sorted_known_elements + unknown_elements
            return sorted_list

        input_text_sub_sentence_list = _sort_by_source_order_unknown(input_text_sub_sentence_list, sub_sentence_sort_list)

        return input_text_sub_sentence_list

    def get_global_string_word_based_corrector_dict_by_using_yingshaoxo_method(self, source_text_data: str, levels: int = 10):
        global_string_dict = {}

        seperator = "☺"

        def get_x_level_dict(source_text: str, x: int):
            level_dict = {}
            tokens = self.text_preprocessor.string_split_to_pure_segment_list_by_using_yingshaoxo_method(source_text)
            for index in range(len(tokens)):
                if index < x:
                    continue
                #if index == len(tokens) - x:
                #    break
                current_words = ''.join(tokens[index-x: index]) + seperator + ''.join(tokens[index+1: index+x+1])
                center_word = tokens[index]
                if current_words in level_dict:
                    if center_word in level_dict[current_words]:
                        level_dict[current_words][center_word] += 1
                    else:
                        level_dict[current_words][center_word] = 1
                else:
                    level_dict[current_words] = {center_word: 1}

            pure_level_dict = {}
            for key, value in level_dict.items():
                biggest_value = 0
                biggest_key = None
                for key2, value2 in value.items():
                    if value2 > biggest_value:
                        biggest_value = value2
                        biggest_key = key2
                pure_level_dict[key] = biggest_key

            return pure_level_dict

        max_level = levels
        for level in reversed(list(range(1, 1+max_level))):
            global_string_dict[level] = get_x_level_dict(source_text_data, level)
            break

        return global_string_dict

    def correct_sentence_based_on_word_by_using_yingshaoxo_method(self, input_text: str, levels: int = 10, source_text_data: str|None = None, global_string_corrector_dict: dict|None = None) -> any:
        if source_text_data == None:
            source_text_data = ""

        if global_string_corrector_dict != None:
            pass
        else:
            global_string_corrector_dict = self.get_global_string_word_based_corrector_dict_by_using_yingshaoxo_method(source_text_data, levels)

        input_text = "\n" * len(global_string_corrector_dict) + input_text + "\n" * len(global_string_corrector_dict)

        seperator = "☺"
        new_text = ""
        for level in global_string_corrector_dict.keys():
            tokens = self.text_preprocessor.string_split_to_pure_segment_list_by_using_yingshaoxo_method(input_text)
            for index in range(len(tokens)):
                if index < level or index >= len(tokens) - level:
                    new_text += tokens[index]
                    continue
                current_words = ''.join(tokens[index - level: index]) + seperator + ''.join(tokens[index + 1 : index + 1 + level])
                if current_words in global_string_corrector_dict[level].keys():
                    new_text += global_string_corrector_dict[level][current_words]
                else:
                    new_text += tokens[index]
            break
        return new_text

    @staticmethod
    def get_random_text_deriation_from_source_text(source_text: str, random_remove_some_characters: bool = False, random_add_some_characters: bool = False, random_char_source_text: str = "") -> str:
        source_text_lines = source_text.split("\n")
        random.shuffle(source_text_lines)
        new_lines = []
        for line in source_text_lines:
            segments_list = language.seperate_text_to_segments(text=line, ignore_space=False)
            segments_list = [one["text"] for one in segments_list]
            random.shuffle(segments_list)
            new_line = "".join(segments_list)
            new_lines.append(new_line)
        final_random_text = "\n".join(new_lines)

        random_length = int(len(source_text) * 0.2)
        if random_remove_some_characters:
            for i in range(random_length):
                random_index = random.randint(0, len(final_random_text)-1)
                final_random_text = final_random_text[:random_index] + final_random_text[random_index + 1:]
        if random_add_some_characters:
            for i in range(random_length):
                random_index = random.randint(0, len(final_random_text)-1)
                if (random_char_source_text == ""):
                    random_char_source_text = source_text
                final_random_text = final_random_text[:random_index] + random.choice(random_char_source_text) + final_random_text[random_index:]

        return final_random_text

    def get_similarity_of_two_sentences(self, sentence_1: str, sentence_2: str, use_both_machine_learning_and_traditional_method: bool = False) -> float:
        if use_both_machine_learning_and_traditional_method == True:
            sentence_embedding_list = self.sentence_transformers_model.encode(sentences=[sentence_1, sentence_2], convert_to_tensor=True)
            similarity = self.sentence_transformers_utility.cos_sim(sentence_embedding_list[0], sentence_embedding_list[1])
            similarity1 = float(similarity.cpu().numpy()[0][0])
            similarity2 = language.compare_two_sentences(sentence_1, sentence_2)
            return (similarity1 + similarity2) / 2
        else:
            if self.use_machine_learning == True:
                sentence_embedding_list = self.sentence_transformers_model.encode(sentences=[sentence_1, sentence_2], convert_to_tensor=True)
                similarity = self.sentence_transformers_utility.cos_sim(sentence_embedding_list[0], sentence_embedding_list[1])
                return float(similarity.cpu().numpy()[0][0])
            else:
                return language.compare_two_sentences(sentence_1, sentence_2)

    def _count_how_many_sub_string_in_previous_context(self, start_index: int, input_text: str, how_long_the_text_you_want_to_get: int = 1024):
        input_text = input_text.lower()

        all_substring_list = []
        for index, _ in enumerate(input_text):
            for index2, _ in enumerate(input_text[index:]):
                index2 = index + index2 + 1
                sub_string = input_text[index: index2]
                all_substring_list.append(sub_string)
        all_substring_list.sort(key=len, reverse=True)
        all_substring_list = all_substring_list[:len(all_substring_list)//2]

        new_source_text = self.lower_case_text_source_data[start_index-how_long_the_text_you_want_to_get: start_index]
        counting = 0
        for index, sub_string in enumerate(all_substring_list):
            if sub_string in new_source_text:
                counting += len(sub_string)
        return counting

    def search_and_get_following_text(self, input_text: str, quick_mode: bool = True, use_fuzz_search: bool = True, how_long_the_text_you_want_to_get: int = 1024) -> tuple[str, str]:
        """
        It will return you the context and following text as a format of tuple[context, following_text]
        """
        if (input_text.strip() == ""):
            return "", ""

        input_text = input_text.lower()

        found_dict = {}
        search_start_index = 0
        while True:
            found = self.lower_case_text_source_data.find(input_text, search_start_index)
            if found == -1:
                # didn't found
                break
            else:
                start = found
                end = found + len(input_text)
                found_dict[found] = {
                    "start": start,
                    "end": end,
                    "following": self.text_source_data[end: end + how_long_the_text_you_want_to_get]
                }
                search_start_index = start + 1

                #if quick_mode == True:
                #    break

        if len(found_dict.keys()) > 0:
            random_key = random.choice(list(found_dict.keys()))
            return self.text_source_data[found_dict[random_key]["end"]-how_long_the_text_you_want_to_get:found_dict[random_key]["end"]+how_long_the_text_you_want_to_get], found_dict[random_key]["following"]
        else:
            if use_fuzz_search == False:
                return self.search_and_get_following_text(input_text = input_text[len(input_text)//2+1:], quick_mode = True, use_fuzz_search = True, how_long_the_text_you_want_to_get = how_long_the_text_you_want_to_get)
            else:
                if (self.debug_mode):
                    print("Using fuzz searching...")

                all_substring_list = []
                for index, _ in enumerate(input_text):
                    for index2, _ in enumerate(input_text[index:]):
                        index2 = index + index2 + 1
                        sub_string = input_text[index: index2]
                        all_substring_list.append(sub_string)
                all_substring_list.sort(key=len, reverse=True)
                all_substring_list = all_substring_list[:len(all_substring_list)//2]

                # what I did here is simply try to search keywords(sub_strings) in previous text, the more matchs, that part of text if more likely the one we are looking for.
                # It can get improved by using some word_spliting library, and even more, you can add same_meaning_words library to it to make sure it always finds out the right data.
                possibility_list = []
                for sub_string in all_substring_list:
                    search_start_index = 0
                    highest_counting = 0
                    highest_counting_info_dict = None
                    while True:
                        found = self.lower_case_text_source_data.find(sub_string, search_start_index)
                        if found == -1:
                            # didn't found
                            break
                        else:
                            start = found
                            end = found + len(input_text)
                            info_dict = {
                                "start": start,
                                "end": end,
                                "following": self.text_source_data[end: end + how_long_the_text_you_want_to_get],
                                "relative_counting": 0
                            }
                            search_start_index = start + 1

                            relative_counting = self._count_how_many_sub_string_in_previous_context(start_index=end, input_text=sub_string, how_long_the_text_you_want_to_get=how_long_the_text_you_want_to_get)
                            if relative_counting > highest_counting:
                                highest_counting = relative_counting
                                info_dict["relative_counting"] = relative_counting
                                highest_counting_info_dict = info_dict.copy()

                                if quick_mode == True:
                                    break

                    if highest_counting_info_dict != None:
                        possibility_list.append(highest_counting_info_dict.copy())

                if len(possibility_list) > 0:
                    possibility_list.sort(key=lambda item: item["relative_counting"], reverse=True)
                    return self.text_source_data[possibility_list[0]['end']-how_long_the_text_you_want_to_get:possibility_list[0]['end']+how_long_the_text_you_want_to_get], possibility_list[0]["following"]
                else:
                    return self.search_and_get_following_text(input_text = input_text[len(input_text)//2+1:], quick_mode = quick_mode, use_fuzz_search = use_fuzz_search, how_long_the_text_you_want_to_get = how_long_the_text_you_want_to_get)

    def search_and_get_following_text_in_a_exact_way(self, input_text: str, quick_mode: bool = False, use_fuzz_search: bool = True, extremly_accrate_mode: bool = False, how_long_the_text_you_want_to_get: int = 1024, also_want_the_current_line: bool = False) -> str:
        context, following_text = self.search_and_get_following_text(input_text=input_text, quick_mode=quick_mode, use_fuzz_search=use_fuzz_search, how_long_the_text_you_want_to_get=how_long_the_text_you_want_to_get)
        if (context.strip() == ""):
            return "..."

        context_splits = language.seperate_text_to_segments(context)
        input_text_splits = language.seperate_text_to_segments(input_text)
        # context_splits = context.split("\n") 
        # input_text_splits = [one for one in input_text.split("\n") if one.strip() != ""]

        last_input_sentence = ""
        for one_input in reversed(input_text_splits):
            if one_input["is_punctuation_or_space"] == False:
                last_input_sentence = one_input["text"]
                if (self.debug_mode):
                    print(f"last_input_sentence: {last_input_sentence}")
                break

        similarity_list = []
        for index, one_target in enumerate(context_splits):
            if one_target ["is_punctuation_or_space"] == False:
                one_sentence = one_target["text"]
                if (self.use_machine_learning):
                    similarity = self.get_similarity_of_two_sentences(one_sentence, last_input_sentence)
                else:
                    similarity = language.compare_two_sentences(one_sentence, last_input_sentence)
                similarity_list.append({
                    "similarity": similarity,
                    "start_index": index
                })
        similarity_list.sort(key=lambda item: item["similarity"], reverse=True)
        the_seperator_index = similarity_list[0]["start_index"]

        if extremly_accrate_mode == True:
            for index, one_target in enumerate(context_splits):
                if one_target ["is_punctuation_or_space"] == False:
                    one_sentence = one_target["text"]
                    if one_sentence.lower() == last_input_sentence.lower():
                        the_seperator_index = index
                        break

        if (also_want_the_current_line == False):
            for index, one in enumerate(context_splits[the_seperator_index:]):
                if one["is_punctuation_or_space"] == False:
                    the_seperator_index += index
                    break
        else:
            the_seperator_index -= 1

        return "".join([one["text"] for one in context_splits[the_seperator_index:]])

    @staticmethod
    def next_code_generation(input_text: str, type_limiter: list[str] = [".txt", ".py", ".md"], how_long_the_text_you_want_to_get: int = 1024, quck_mode: bool = True, data_source_text: str | None = None, data_source_folder_path: str | None = None, only_return_source_text: bool = False) -> str:
        """
        1. take the previous text as input
        2. take sub_string of the input_text, from right to left, from long to short.
        3. search the database source text, if that sub_string matchs, add len(sub_string) to variable {one_following_char: count + len(sub_string)}
        4. take the biggest counting char as the next char

        method1: previous_text[-i:], search from i == 0 to i == len(previous_text), until it founds nothing, then go back, choose a random one
        method2: previous_text[i:], search from i == 0 to i == len(previous_text), for each time, i=i*2, until it found something, return that
        """
        text_source_data = ""
        should_update_datasource = False

        if data_source_text == None:
            if data_source_txt_file_path == None:
                return ""

            datestamp_string = store.get('last_code_generation_database_update_time', None)
            if (datestamp_string == None):
                should_update_datasource = True
            else:
                old_time = time_.get_datetime_object_from_timestamp(int(datestamp_string))
                new_time = time_.get_datetime_object_from_timestamp(time_.get_current_timestamp_in_10_digits_format())
                if (new_time - old_time).days > 3: #update the database for every 3 days
                    should_update_datasource = True

            data_source_txt_file_path = terminal.fix_path("~/.auto_everything/ml/code_completion_data_source.txt")
            disk.create_a_folder(disk.get_directory_path(data_source_txt_file_path))
            if (not disk.exists(data_source_txt_file_path)):
                io_.write(file_path=data_source_txt_file_path, content="")

            if should_update_datasource == True:
                files = disk.get_files(folder=terminal.fix_path(data_source_folder_path), type_limiter=type_limiter)
                io_.write(file_path=data_source_txt_file_path, content="")
                for file in files:
                    io_.append(file_path=data_source_txt_file_path, content=io_.read(file) + "\n\n\n\n")
                store.set('last_code_generation_database_update_time', str(time_.get_current_timestamp_in_10_digits_format()))
            else:
                text_source_data = io_.read(data_source_txt_file_path)

            if only_return_source_text == True:
                return text_source_data
        else:
            text_source_data = data_source_text

        def real_next_code_generation(input_text: str, how_long_the_text_you_want_to_get: int = 1024):
            if (input_text.strip() == ""):
                return ""

            found_start_index = text_source_data.find(input_text)
            if found_start_index == -1:
                # didn't found
                if quck_mode == True:
                    input_text = input_text[len(input_text)//2+1:]
                else:
                    input_text = input_text[1:]
                return real_next_code_generation(input_text=input_text, how_long_the_text_you_want_to_get=how_long_the_text_you_want_to_get)
            else:
                start = found_start_index
                end = found_start_index + len(input_text)
                following = text_source_data[end: end + how_long_the_text_you_want_to_get]
                following = following.rstrip()
                return following

        return real_next_code_generation(input_text=input_text, how_long_the_text_you_want_to_get=how_long_the_text_you_want_to_get)

    def next_fuzz_sentence_generation(self, input_text: str, how_long_the_text_you_want_to_get: int = 1024, text_source_data: str | None = None, compare_times: int=10, also_return_previous_text: bool = False) -> str | tuple[str, str]:
        """
        1. first, we do search based on input_text, if we could not found it, we search for input_text[len()//2:], we search half of the input_text, the second one.
        2. If we found one, we save that input_text keyword and [index-sub_text_length//2, index+sub_text_length//2], we keep doing the search for compare_times times. Then we could use all sub_string from input_text to do a compare for those text windows, we will only return the one that has the highest similarity number.

        if also_return_previous_text == True, we return (previous_text, following_text)
        """
        input_text = input_text.lower()
        real_text_source_data = text_source_data
        text_source_data = text_source_data.lower()

        def normal_next_code_finding(input_text: str, start_index: int = 0) -> tuple[int, int]:
            """
            This will return the start and end index of the target_text
            """
            if (input_text.strip() == ""):
                return 0, 0

            found_start_index = text_source_data.find(input_text, start_index)
            if found_start_index == -1:
                # didn't found
                input_text = input_text[len(input_text)//2+1:]
                #input_text = input_text[1:]
                return normal_next_code_finding(input_text=input_text)
            else:
                start = found_start_index
                end = found_start_index + len(input_text)
                return start, end

        def fuzz_search(a_input_text: str, how_long_the_context_is: int, compare_times: int) -> str:
            start_index, end_index = normal_next_code_finding(input_text=a_input_text, start_index=0)
            if start_index == 0 and end_index == 0:
                if also_return_previous_text == True:
                    return "", ""
                else:
                    return ""

            target_level = end_index - start_index
            result_start_index_list = []
            result_end_index_list = []
            result_start_index_list.append(start_index)
            result_end_index_list.append(end_index)
            for _ in range(compare_times):
                a_input_text = text_source_data[start_index: end_index]
                start_index, end_index = normal_next_code_finding(input_text=a_input_text, start_index=end_index)
                if start_index == 0 and end_index == 0:
                    break

                current_level = end_index - start_index
                if current_level != target_level:
                    break

                result_start_index_list.append(start_index)
                result_end_index_list.append(end_index)
                if len(result_end_index_list) >= compare_times:
                    break

            global_input_sub_string_list = string_.get_all_sub_string(text=input_text) #it uses the global input_text
            previous_context_text_list = []
            for index, _ in enumerate(result_end_index_list):
                previous_context_text_list.append(
                    #text_source_data[result_start_index_list[index]-len(input_text)*2:result_start_index_list[index]]
                    text_source_data[result_end_index_list[index]-how_long_the_context_is:result_end_index_list[index]]
                )
            #print(previous_context_text_list)
            #print(input_text)
            previous, current, next = string_.get_fuzz_match_text_from_text_list(input_text="", text_list=previous_context_text_list, input_sub_string_list=global_input_sub_string_list, quick_mode=False)
            if current == "":
                if also_return_previous_text == True:
                    return "", ""
                else:
                    return ""
            else:
                the_target_index = previous_context_text_list.index(current)
                #print(the_target_index)
                real_index = result_end_index_list[the_target_index]
                previous_text = real_text_source_data[real_index - how_long_the_context_is:real_index]
                next_text = real_text_source_data[real_index: real_index + how_long_the_context_is]
                if also_return_previous_text == True:
                    return previous_text, next_text
                else:
                    return next_text

        return fuzz_search(a_input_text=input_text, how_long_the_context_is=how_long_the_text_you_want_to_get, compare_times=compare_times)

    def fuzz_text_to_text_transforming(self, input_text: str, example_input_text: str, example_output_text: str, levels: int = 4) -> str:
        """
        input_text: My name is god.
        example_input_text: My name is yingshaoxo.
        example_output_text: Hi, yingshaoxo.

        It should return "Hi, god."

        In context_based chat, the source text data before current input_text is the example_input_text (include current input), the data after current input_text is the example_output_text.
        """
        """
        If no quick_mode, we should use regex + sub_string based text transformer, but if we use quick_mode, we simply have to split text by using space, then use regex transformer after that. (In the end, I use words_pattern_dict to find pattens)

        If you want to do the transforming as much as possible, you should make a replace loop, do transforming for new sentence over and over again until you can't find any repeated word between input and output. (You have to make cache dict to make sure you do not do repeat replacement)

        If you stand in a global level, you could even make a RLU cache to save all regex rule, so that you can skip this function to do a direct replacement.

        yingshaoxo's words: text transforming is all about pattern/rule extracting and applying.
        """
        words_pattern_dict = self.get_global_string_word_based_corrector_dict_by_using_yingshaoxo_method(source_text_data = example_input_text, levels = levels)
        words_pattern_dict = words_pattern_dict[levels]
        #print(words_pattern_dict)
        for key, value in words_pattern_dict.items():
            if value not in example_output_text:
                continue

            key_list = key.split('☺')
            key_list = [re.escape(one) for one in key_list]
            new_key = f"(.*?)".join(key_list)

            result = re.search(new_key, input_text, flags=re.DOTALL)
            if result == None:
                continue

            a_input_variable = result.group(1)
            #print(a_input_variable)
            example_output_text = example_output_text.replace(value, a_input_variable)

        return example_output_text.strip()

    def get_text_to_text_hard_coding_transforming_dict(self, input_text_list: list[str], output_text_list: list[str]) -> dict[str, str]:
        yingshaoxo_text_transformer = Yingshaoxo_Text_Transformer()
        return yingshaoxo_text_transformer.get_regex_expression_dict_from_input_and_output_list(input_text_list, output_text_list)

    def text_to_text_hard_coding_transforming(self, input_text: str, the_string_dict: dict[str, str], recursive: bool = False):
        """
        1. Just think the whole transforming process as doing the search in a Q table.
        2. You use a patten filter to check the input_text, "I love you", 3 elements as a window, then you use this patten to do a search in the Q table, you found ["I hate you", "I trust you", "I hate you"], it seems like 'hate' has higher chance to be in the middle of that sentence.
        3. Or, you can simply think this: For a list of "I * you" patten in dataset, what word has more frequency in the position of *?, Choose the one has higher frequency.
        4. tip 3 is still in [MASK] level. If you want to handle the sentence segment sorting problem, you have to predict the 'move farwrd x characters' and 'move backword x character' information. Which can also be treated like a mask.

        speak of the process speed, use cache.

        this function could be used on 'wrong word correction', 'punctuation adding', 'sub_sentence rewrite'

        for 'summarytion task', get substrings from source_text, then get substrings from target_text, see how many substring shold get removed, get couting of those substrings that should get removed over the whole dataset.
            for the next time, in a new input sentence, we get those substring ranks, simply remove those substring that has higher 'garbage rank number'

        for 'sorting task', get substrings from input_text, then try to use before_context and following_context to do a search in target dataset, get the percentage of start_index/the_whole_length_of_the_sentence.
            do a compare for the substring in the input_text, so you would get a percentage number of weather to move that substring farward or backward.
        """
        yingshaoxo_text_transformer = Yingshaoxo_Text_Transformer()
        if recursive == False:
            result = yingshaoxo_text_transformer.yingshaoxo_regex_expression_based_transformer(
                input_text=input_text,
                regex_expression_dict=the_string_dict
            )
        else:
            result = yingshaoxo_text_transformer.yingshaoxo_regex_expression_based_recursive_transformer(
                input_text=input_text,
                regex_expression_dict=the_string_dict
            )
        return result
        # def _count_how_many_sub_string_in_previous_context(self, start_index: int, input_text: str, how_long_the_text_you_want_to_get: int = 1024):
        #     input_text = input_text.lower()

        #     all_substring_list = []
        #     for index, _ in enumerate(input_text):
        #         for index2, _ in enumerate(input_text[index:]):
        #             index2 = index + index2 + 1
        #             sub_string = input_text[index: index2]
        #             all_substring_list.append(sub_string)
        #     all_substring_list.sort(key=len, reverse=True)
        #     all_substring_list = all_substring_list[:len(all_substring_list)//2]

        #     new_source_text = self.lower_case_text_source_data[start_index-how_long_the_text_you_want_to_get: start_index]
        #     counting = 0
        #     for index, sub_string in enumerate(all_substring_list):
        #         if sub_string in new_source_text:
        #             counting += len(sub_string)
        #     return counting

    def do_text_search(self, input_text: str, text_list: list[str], quick_mode: bool = False) -> tuple[str, str, str]:
        """
        This function returns [previous_text, matched_text, next_text]
        """
        return string_.get_fuzz_match_text_from_text_list(input_text, text_list, quick_mode=quick_mode)


class Yingshaoxo_Computer_Vision():
    def __init__(self):
        import numpy
        self.numpy = numpy

    def get_similarity_of_two_images(self, numpy_image_1: Any, numpy_image_2: Any) -> float:
        """
        return a float between 0 and 1, 1 means equal, 0 means no relate.
        """
        mean1 = self.numpy.mean(numpy_image_1, axis=(0, 1))
        mean2 = self.numpy.mean(numpy_image_2, axis=(0, 1))

        difference = 0.0
        difference += self.numpy.absolute(mean1[0] - mean2[0])
        difference += self.numpy.absolute(mean1[1] - mean2[1])
        difference += self.numpy.absolute(mean1[2] - mean2[2])

        final_difference = ((difference * 100) / (255*3)) / 20
        final_difference = 1 - final_difference
        return final_difference


class Yingshaoxo_Speech_Recognizer():
    """
    If you have a text_to_speech dataset, you could make a reverse coding.
    Use voice similarity to get target voice, then use 1:1 speech_to_text dataset to get the target text.
    """
    def __init__(self, language: str = 'en'):
        # pip install vosk
        # pip install sounddevice
        import queue
        import sys
        import sounddevice
        from vosk import Model, KaldiRecognizer
        from auto_everything.time import Time

        self.queue = queue
        self.sys = sys
        self.sounddevice = sounddevice
        self.time_ = Time()

        if language == "en":
            self.vosk_model = Model(lang="en-us")
        else:
            self.vosk_model = Model(model_name="vosk-model-cn-0.22")

        self.KaldiRecognizer = KaldiRecognizer

        self.microphone_bytes_data_queue = queue.Queue()

    def recognize_following_speech(self, timeout_in_seconds: int | None = None) -> str:
        while self.microphone_bytes_data_queue.empty() == False:
            self.microphone_bytes_data_queue.get_nowait()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=self.sys.stderr)
            self.microphone_bytes_data_queue.put(bytes(indata))

        try:
            device_info = self.sounddevice.query_devices(None, "input")
            samplerate = int(device_info["default_samplerate"]) #type:ignore

            with self.sounddevice.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None,
                    dtype="int16", channels=1, callback=callback):
                rec = self.KaldiRecognizer(self.vosk_model, samplerate)

                start_time = self.time_.get_current_timestamp_in_10_digits_format()
                while True:
                    data = self.microphone_bytes_data_queue.get()
                    if rec.AcceptWaveform(data):
                        text = json.loads(rec.Result())["text"] #type:ignore
                        text = text.replace(" ", "").strip()
                        if len(text) != 0:
                            #print(text)
                            return text
                    else:
                        # print(rec.PartialResult())
                        pass
                    end_time = self.time_.get_current_timestamp_in_10_digits_format()
                    if timeout_in_seconds != None:
                        duration = self.time_.get_datetime_object_from_timestamp(end_time) - self.time_.get_datetime_object_from_timestamp(start_time)
                        if duration.seconds > timeout_in_seconds:
                            return ""
        except Exception as e:
            print(e)
            return ""


class Yingshaoxo_Translator():
    """
    translation is kind of 1:1 task
    if you have a super big dataset, you replace longest sentence first, you'll get 100% accurate translation
    """
    def __init__(self):
        # pip install dl-translate
        import dl_translate
        from auto_everything.language import Language
        self.dl_translate = dl_translate
        self.dl_translate_model = self.dl_translate.TranslationModel(device="auto")
        self.languages = self.dl_translate.lang
        self._language = Language()

    def translate(self, text: str, from_language: Any, to_language: Any, sentence_seperation: bool = False) -> str:
        try:
            text = text.strip()
            if sentence_seperation == True:
                data_list = self._language.seperate_text_to_segments(text=text, ignore_space=True)
                """
                [
                    {
                        "is_punctuation_or_space": true, "text": "?",
                    }, {
                        "is_punctuation_or_space": false, "text": "Yes",
                    },
                ]
                """
                text_list = []
                for segment in data_list:
                    if segment["is_punctuation_or_space"] == False:
                        result = self.dl_translate_model.translate(segment["text"], source=from_language, target=to_language)
                        result = str(result).strip("!\"#$%&'()*+, -./:;<=>?@[\\]^_`{|}~ \n，。！？；：（）［］【】")
                        text_list.append(result)
                    else:
                        text_list.append(segment["text"])
                return "".join(text_list)
            else:
                return self.dl_translate_model.translate(text, source=from_language, target=to_language) #type: ignore
        except Exception as e:
            print(e)
            return text

    def chinese_to_english(self, text: str, sentence_seperation: bool = False):
        return self.translate(text=text, from_language=self.languages.CHINESE, to_language=self.languages.ENGLISH, sentence_seperation=sentence_seperation)

    def english_to_chinese(self, text: str, sentence_seperation: bool = False):
        return self.translate(text=text, from_language=self.languages.ENGLISH, to_language=self.languages.CHINESE, sentence_seperation=sentence_seperation)


class Yingshaoxo_Text_to_Speech():
    """
    TTS hard coding method 2:


    1. Text map to 64k mp3 audio

    2. Use ",." symbol to separate text, so you get less repeated text data

    3. When you got 1GB of data, you get a well functioned TTS

    > You could even use speech recognition to collect audio to text dict data.

    > By using this method, you could get almost 100% accurate TTS for your voice


    #tts #yingshaoxo
    """
    """
    TTS hard coding method, 1:


    Word to Sound directly, but with software to control it's strongth, tune, pause length between words.

    The strongth is actually the relative audio volume between a word, a sentence. (Or audio volume line)

    And the tune will need you to change each word length.

    Audio Line: 40 50 70 100 (volume %, from low to high)

    Audio length: 1 1.8 1 (word relative length, "how are you?")

    Audio pause length: 0.1 0.1 (word pause relative length for "how are you")


    #tts #yingshaoxo
    """
    def __init__(self):
        #pip install TTS
        #sudo apt install ffmpeg                 or          https://github.com/markus-perl/ffmpeg-build-script#:~:text=maintain%20different%20systems.-,Installation,-Quick%20install%20and
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

        from TTS.api import TTS
        self.TTS = TTS

        from auto_everything.terminal import Terminal
        from auto_everything.disk import Disk
        self.terminal = Terminal()
        self.disk = Disk()

        import torch
        use_gpu = True if torch.cuda.is_available() else False
        self.torch = torch
        #pprint(TTS.list_models())

        self.tts_en = TTS("tts_models/en/ljspeech/tacotron2-DDC", gpu=use_gpu)
        # self.tts_en = TTS("tts_models/en/ljspeech/fast_pitch", gpu=use_gpu)
        self.tts_cn = TTS("tts_models/zh-CN/baker/tacotron2-DDC-GST", gpu=use_gpu)

    def _language_splitor(self, text: str):
        language_list = []
        index = 0
        while True:
            temp_string = ""
            if (index >= len(text)):
                break
            char = text[index]
            while ord(char) < 128:
                # english
                char = text[index]
                temp_string += char
                index += 1
                if (index >= len(text)):
                    break
            if (temp_string.strip() != ""):
                temp_string = temp_string[:-1]
                index -= 1
                language_list.append({
                    "language": "en",
                    "text": temp_string
                })

            temp_string = ""
            if (index >= len(text)):
                break
            char = text[index]
            while not ord(char) < 128:
                # chinese 
                char = text[index]
                temp_string += char
                index += 1
                if (index >= len(text)):
                    break
            if (temp_string.strip() != ""):
                temp_string = temp_string[:-1]
                index -= 1
                language_list.append({
                    "language": "cn",
                    "text": temp_string
                })

            if (index+1 >= len(text)):
                break

        if len(language_list) > 0:
            language_list[-1]["text"] += text[-1]

        new_list = []
        for index, one in enumerate(language_list):
            new_text = language_list[index]["text"].strip()
            if len(new_text) > 0:
                new_list.append({
                    'language': one['language'],
                    'text': new_text
                })

        return new_list

    def _speak_it(self, language: str, text: str):
        output_file = os.path.abspath(os.path.join(self.disk.get_a_temp_folder_path(), "output.wav"))
        self.disk.create_a_folder(self.disk.get_directory_path(output_file))

        text = text.strip("!\"#$%&'()*+, -./:;<=>?@[\\]^_`{|}~ \n，。！？；：（）［］【】")
        if (language == "en"):
            tts = self.tts_en
            text += "."
        else:
            tts = self.tts_cn
            text += "。"

        try:
            if tts.speakers == None:
                tts.tts_to_file(text=text, file_path=output_file)
            else:
                tts.tts_to_file(text=text, file_path=output_file, speaker=tts.speakers[0], language=tts.languages[0], speed=2.5) #type:ignore
        except Exception as e:
            print(e)

        self.terminal.run(f"""
        ffplay -autoexit -nodisp "{output_file}"
                """, wait=True)

        self.disk.delete_a_file(output_file)

    def speak_it(self, text: str):
        data_ = self._language_splitor(text)
        for one in data_:
            print(one)
            self._speak_it(language=one["language"], text=one["text"])


class ML():
    def __init__(self):
        self.Yingshaoxo_Text_Preprocessor = Yingshaoxo_Text_Preprocessor
        self.Yingshaoxo_Text_Transformer = Yingshaoxo_Text_Transformer
        self.Yingshaoxo_Text_Generator = Yingshaoxo_Text_Generator
        self.Yingshaoxo_Translator = Yingshaoxo_Translator


if __name__ == "__main__":
    pass


'''
# Yingshaoxo machine learning ideas

## For natual language process
We treat every char as an id or tensor element

In GPU based machine learning algorithm, you will often do things with [23, 32, 34, 54]

But now, it becomes ['a', 'b', 'c', 'd']


### For text summary
For the self attention mechanism, it is using word apperance counting dict. You could think it as a dict, multiple key link to one same value, for all those multiple key string, if a word show up a lot time, it is likely it is important word.
(You can think this as a TV show, for the same envirnoment, if a person only show once, it is not the main character, it is not important. But if a character show a lot times, you can almost see it at any eposide, then it is a important character)

For one sequence or list, If its importance number less than average(half of 'its sequence importance sum'), you remove it


### For translation
long sequence (meaning group) -> long sequence (meaning group)

what you do -> 你干什么
It depends on -> 这取决于

(It depends on) (what you do) -> 这取决于 你干什么

meaning group can be get automatically, all you have to do is count continues_words appearance time. the more time a continuse_words appear, the more likely it is a meaning group

It all can be summaryed as "divide and conquer"


### For question and answer
For context information extraction, you have to use the question. If one sentence of the context should at the bottom of the question, you keep it, otherwise, you remove it

Then, for the other context, you do a simple sort

### For text generation
```
one char predict next char
two char predict next char
...
one word predict next word
two words predict next word
three words predict next word
...
```

when you use it, use it from bottom to top, use longest sequence to predict the next word first.

> the more level you make, the more accurate it would be.

> It is dict based next word generator, so the speed is super quick

> This method was created by yingshaoxo. it only need cpu than gpu. it can beat gpt4 with an old computer if you have big dataset (30GB) and big memory to hold the dict.

### For general AI
```
General AI algorithm:

Natural language -> Python programming language -> Go through CPU -> If it is working, add that sentence to database to add weights to that sentence, if it is not working, minus weights for that sentence -> use words or long sub_string weights to generate more following natural language sentences -> it is a never end loop, but if the storage is about to blow, we need to find a way to do compression and find more way to store data.

Those code are generated in real time. For each response, it generate different algorithm or code. It adopts to any situation.

#yingshaoxo
```
'''
