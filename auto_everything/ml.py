import random
from auto_everything.disk import Disk
from auto_everything.io import IO
from auto_everything.language import Language
disk = Disk()
io_ = IO()
language = Language()


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


class SpeechToText():
    pass
    # https://tfhub.dev/silero/silero-stt/en/1


class Yingshaoxo_Text_Generator():
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
    """
    def __init__(self, input_txt_folder_path: str):
        self.input_txt_folder_path = input_txt_folder_path

        self.text_source_data = ""
        files = disk.get_files(self.input_txt_folder_path, recursive=True, type_limiter=[".txt"])
        for file in files:
            self.text_source_data += io_.read(file)
            self.local_case_text_source_data = self.text_source_data.lower()
    
    @staticmethod
    def get_random_text_deriation_from_source_text(source_text: str) -> str:
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
        return final_random_text
    
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

        new_source_text = self.local_case_text_source_data[start_index-how_long_the_text_you_want_to_get: start_index]
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
            found = self.local_case_text_source_data.find(input_text, search_start_index)
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
                #print("Using fuzz searching...")
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
                        found = self.local_case_text_source_data.find(sub_string, search_start_index)
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

    def search_and_get_following_text_in_a_exact_way(self, input_text: str, quick_mode: bool = False, how_long_the_text_you_want_to_get: int = 1024) -> str:
        context, following_text = self.search_and_get_following_text(input_text=input_text, quick_mode=quick_mode, use_fuzz_search=True, how_long_the_text_you_want_to_get=how_long_the_text_you_want_to_get)
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
                print(f"last_input_sentence: {last_input_sentence}")
                break
        
        similarity_list = []
        for index, one_target in enumerate(context_splits):
            if one_target ["is_punctuation_or_space"] == False:
                one_sentence = one_target["text"]
                similarity = language.compare_two_sentences(one_sentence, last_input_sentence)
                similarity_list.append({
                    "similarity": similarity,
                    "start_index": index
                })
        
        similarity_list.sort(key=lambda item: item["similarity"], reverse=True)

        the_seperator_index = similarity_list[0]["start_index"]

        for index, one in enumerate(context_splits[the_seperator_index:]):
            if one["is_punctuation_or_space"] == False:
                the_seperator_index += index
                break

        return "".join([one["text"] for one in context_splits[the_seperator_index:]])


if __name__ == "__main__":
    pass
