from typing import Any
import re


class Language():
    def compare_two_sentences(self, sentence1: str, sentence2: str) -> float:
        """
        return similarity, from `0.0` to `1.0`

        Parameters
        ----------
        sentence1: string

        sentence2: string
        """
        from difflib import SequenceMatcher
        ratio = SequenceMatcher(None, sentence1, sentence2).ratio()
        return ratio

    def seperate_text_to_segments(self, text: str, ignore_space: bool = True) -> list[dict[str, Any]]:
        """
        It returns a list of dict.
        For example:
            [
                {
                    "is_punctuation_or_space": true,
                    "text": "?",
                },
                {
                    "is_punctuation_or_space": false,
                    "text": "Yes",
                },
            ]
        """
        if ignore_space == True:
            all_result = re.findall(r"((?:\w* *)*)(\W*)", text, flags=re.MULTILINE)
        else:
            all_result = re.findall(r"(\w*)(\W*)", text, flags=re.MULTILINE)
        final_result = []
        for one in all_result:
            words = one[0]
            puctuation = one[1]
            if len(words) > 0:
                item = {
                    "is_punctuation_or_space": False,
                    "text": words
                }
                final_result.append(item)
            if len(puctuation) > 0:
                item = {
                    "is_punctuation_or_space": True,
                    "text": puctuation
                }
                final_result.append(item)
        return final_result
    

class English(Language):
    """
    This is a class for handling English
    """

    def __init__(self):
        from summa.summarizer import summarize
        from summa.keywords import keywords
        self._keywords = keywords
        self._summarize = summarize

    def text_to_speech(self, text):
        """
        speak accourding to text

        Parameters
        ----------
        text: string
        """
        import pyttsx3 as _pyttsx3
        self._speak_engine = _pyttsx3.init()
        self._speak_engine.setProperty('rate', 180)  # 180 words per minute
        self._speak_engine.setProperty('volume', 0.8)

        text = text.strip()
        self._speak_engine.say(text)
        self._speak_engine.runAndWait()
    
    def get_key_words(self, input_text: str) -> list[str]:
        return self._keywords(input_text) #type: ignore

    def get_sentences_from_text(self, text) -> list[str]:
        """
        return a list of sentences

        Parameters
        ----------
        text: string
        """
        from nltk import tokenize
        return tokenize.sent_tokenize(text)

    def get_key_sentences_from_text(self, text: str, reduce_ratio: float = 0.5, return_list: bool = True) -> list[str] | str:
        """
        return a list of key sentence

        Parameters
        ----------
        text: string
        reduce_ratio: float

        """
        if return_list:
            return self._summarize(text, split=True, ratio=reduce_ratio) #type: ignore
        else:
            return self._summarize(text, split=False, ratio=reduce_ratio) #type: ignore


class Chinese(Language):
    """
    This is a class for handling Chinese
    """

    def __init__(self):
        from textrank4zh import TextRank4Keyword, TextRank4Sentence
        self.sentence_handler = TextRank4Sentence()
        self.keywords_handler = TextRank4Keyword()

        import jieba as jieba
        self.jieba = jieba

    def get_text_from_docx(self, docx_path):
        """
        return text content of a docx file

        Parameters
        ----------
        docx_path: string
        """
        from docx import Document
        doc = Document(docx_path)
        text_list = []
        for paragraph in doc.paragraphs:
            text_list.append(paragraph.text)
        return '\n'.join(text_list)

    def get_key_words(self, input_text: str) -> list[str]:
        words = []
        for item in self.keywords_handler.get_keywords(20, word_min_len=1):
            words.append(item.word)
        return words

    def get_sentences_from_text(self, text) -> list[str]:
        """
        return a list of sentences

        Parameters
        ----------
        text: string
        """
        self.sentence_handler.analyze(text)
        return self.sentence_handler.sentences #type: ignore

    def get_key_sentences_from_text(self, text) -> list[str]:
        """
        return a list of key sentence

        Parameters
        ----------
        text: string
        """
        self.sentence_handler.analyze(text)
        sentences = [s['sentence'] for s in self.sentence_handler.get_key_sentences()]
        return sentences

    def sentence_contracting(self, text: str) -> str:
        """
        return a contracted sentence

        Parameters
        ----------
        text: string
        """
        text = text.strip()

        import jieba.posseg as pseg
        words = pseg.cut(text)
        result = []
        for word, flag in words:
            if word == "能":
                print(flag)
            if flag in ['n', 'nr', 'ns', 'v', 'r', 'p', 'r1']:
                result.append(word)
        return ''.join(result)

    def split_words_from_sentence(self, sentence):
        """
        return a list of words cut from sentence 

        Parameters
        ----------
        sentence: string
        """
        return list(self.jieba.cut(sentence))


if __name__ == "__main__":
    chinese = Chinese()
    sentence = "他穿着一件大翻领上带着道道滚边的海军服。"
    r = chinese.split_words_from_sentence(sentence)
    print(sentence)
    print(r)
    print("what i would say: 他穿着一件 大翻领上带着道道滚边的 海军服。")
