from time import sleep, time

class Terminal_App():
    def __init__(self, height=320, width=240):
        self.height = height
        self.width = width
        self.text = "Hi"
        self.text += "\n\ncontent_view has height and width of:\n"
        self.text += "{height}, {width}".format(height=height, width=width)

    def render_as_text(self):
        return self.text

    def handle_touch_function(self, y, x):
        print("sub_app_click:", y, x)
        self.text = "y:{}, x:{}".format(y, x)
