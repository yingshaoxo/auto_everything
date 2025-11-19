# This is probobally the strong AI you are looking for.


class English_Analyzer_And_Executor():
    # It should be eaiser than handle chinese
    # Don't be afraid the first version are stupid, after 9999 version upgrade based on previous work, it can be amazing!
    # This is similar to make a higher level 'python' by yourself. According to 'yingshaoxo_python', it is not that hard.
    pass


class Chinese_Analyzer_And_Executor():
    def __init__(self, input_text):
        self.input_text = input_text.strip()

    def is_it_a_question(self):
        input_text = self.input_text
        if input_text.endswith("?"):
            return True
        if input_text.endswith("？"):
            return True
        if "什么" in input_text:
            return True
        return False

    def quetsion_to_normal_sentence(self):
        # '什么是爱情?' -> '爱情是'
        # '哪里有深爱?' -> 'xxx有深爱' ["'哪里' not in xxx", "len(xxx) >= 3"]
        pass
