class A_Keyboard():
    def __init__(self):
        self.char_height = 16
        self.char_width = 8

        self.text = """
    1 2 3 4 5 6 7 8 9 0    
    q w e r t y u i o p    
     a s d f g h j k l     
      z x c v b n m        
       _!:;\"'?.,%#        
     <>{}[]()=+-*/@$&|^    
""".strip("\n")

        self.lines = self.text.split("\n")

        def handle_char_output_function(char):
            pass
            #print("pressed:", char)
        self.handle_char_output_function = handle_char_output_function

    def render_as_text(self):
        return self.text

    def handle_touch_function(self, y, x):
        text_y = int(y/self.char_height)
        text_x = int(x/self.char_width)
        try:
            a_char = self.lines[text_y][text_x]
            self.handle_char_output_function(a_char)
            return a_char
        except Exception as e:
            print(e)
            return "None"
