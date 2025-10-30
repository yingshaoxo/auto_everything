# This is probobally the strong AI you are looking for.


class English_Analyzer_And_Executor():
    # It should be eaiser than handle chinese
    # Don't be afraid the first version are stupid, after 9999 version upgrade based on previous work, it can be amazing!
    # This is similar to make a higher level 'python' by yourself. According to 'yingshaoxo_python', it is not that hard.
    pass


class Chinese_Analyzer_And_Executor():
    def __init__(self, input_text):
        self.input_text = input_text

    def is_it_a_question(self):
        input_text = self.input_text
        if input_text.endswith("?"):
            return True
        if input_text.endswith("？"):
            return True
        if input_text.startswith("什么是"):
            return True
        if input_text.startswith("What is"):
            return True
        return False
