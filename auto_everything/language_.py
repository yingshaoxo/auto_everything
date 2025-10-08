class English_Analyzer():
    # It should be eaiser than handle chinese
    # Don't be afraid the first version are stupid, after 999 version upgrade based on previous work, it can be amazing!
    pass


class Chinese_Analyzer():
    def __init__(self, input_text):
        self.input_text = input_text

    def is_question(self):
        input_text = self.input_text
        if input_text.endswith("?"):
            return True
        if input_text.endswith("？"):
            return True
        if input_text.startswith("什么是"):
            return True
        return False
