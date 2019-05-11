class Language():
    def compare_two_sentences(self, sentence1, sentence2):
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


class English(Language):
    """
    This is a class for handling English
    """

    def __init__(self):
        import pyttsx3 as _pyttsx3
        self._speak_engine = _pyttsx3.init()
        self._speak_engine.setProperty('rate', 180)  # 180 words per minute
        self._speak_engine.setProperty('volume', 0.8)

    def text_to_speech(self, text):
        """
        speak accourding to text

        Parameters
        ----------
        text: string
        """
        text = text.strip()
        self._speak_engine.say(text)
        self._speak_engine.runAndWait()


class Chinese(Language):
    """
    This is a class for handling Chinese
    """

    def __init__(self):
        from textrank4zh import TextRank4Keyword, TextRank4Sentence
        self.handler = TextRank4Sentence()
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

    def get_sentences_from_text(self, text):
        """
        return a list of sentences

        Parameters
        ----------
        text: string
        """
        self.handler.analyze(text)
        return self.handler.sentences

    def get_key_sentences_from_text(self, text):
        """
        return a list of key sentence

        Parameters
        ----------
        text: string
        """
        self.handler.analyze(text)
        sentences = [s['sentence'] for s in self.handler.get_key_sentences()]
        return sentences

    def sentence_contracting(self, text):
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
