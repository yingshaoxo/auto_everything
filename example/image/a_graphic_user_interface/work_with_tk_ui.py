from auto_everything.image_ import Container

content_container = Container(text="Hi you.\n\nHere should have an application list that you can click to open.")
def handle_tab_click(tab_name):
    if tab_name == "Files":
        content_container.text="Files view\n\nWhere you can modify files on your disk."
    elif tab_name == "Browser":
        content_container.text="Browser view\n\nWhere you can visit websites."
    elif tab_name == "Terminal":
        content_container.text="Terminal view\n\nWhere you can use command lines."

root_container = Container(
    height=1.0,
    width=1.0,
    rows=True,
    children=[
        Container(
            height=0.1,
            width=1.0,
            columns=True,
            children=[
                Container(
                    width=0.33,
                    text="Files",
                    color=[255,0,0,255],
                    on_click_function=lambda *x: handle_tab_click("Files")
                ),
                Container(
                    width=0.33,
                    text="Browser",
                    color=[0,255,0,255],
                    on_click_function=lambda *x: handle_tab_click("Browser")
                ),
                Container(
                    width=0.33,
                    text="Terminal",
                    color=[0,0,255,255],
                    on_click_function=lambda *x: handle_tab_click("Terminal")
                ),
            ]
        ),
        Container(
            height=0.9,
            width=1.0,
            rows=True,
            color=[245,25,211,255],
            children=[
                content_container
            ]
        ),
    ]
)

def yingshaoxo_image_init(window_height=480, window_width=270):
    if root_container.parent_height == window_height and root_container.parent_width == window_width:
        return False
    root_container.parent_height=window_height
    root_container.parent_width=window_width
    return True

try:
    import tkinter as tk
except Exception as e:
    print(e)
    import Tkinter as tk

class Point_Drawer:
    def __init__(self, root_window, height=480, width=270):
        self.root_window = root_window
        self.root_window.title("a_native_python_window")

        self.canvas = tk.Canvas(root_window, width=width, height=height, bg='white', highlightthickness=0)
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self._on_canvas_click)
        self.click_callback_function = lambda y,x: None

    def draw_point(self, y, x, color_rgba):
        r, g, b, a = color_rgba
        hex_color = '#{r:02x}{g:02x}{b:02x}'.format(r=r,g=g,b=b)
        #self.canvas.create_oval(x-1, y-1, x+1, y+1, fill=hex_color, outline=hex_color, width=0)
        self.canvas.create_rectangle(x-1, y-1, x+1, y+1, fill=hex_color, outline=hex_color, width=0)

    def set_click_callback(self, click_callback_function):
        # when the UI get click, it should call self.click_callback_function(y, x)
        self.click_callback_function = click_callback_function

    def _on_canvas_click(self, event):
        y, x = event.y, event.x
        if self.click_callback_function:
            self.click_callback_function(y, x)

    def center_window(self):
        x = int((self.root_window.winfo_screenwidth() - self.root_window.winfo_reqwidth()) / 2 - 100)
        y = int((self.root_window.winfo_screenheight() - self.root_window.winfo_reqheight()) / 2 - 100)
        self.root_window.geometry("+{}+{}".format(x, y))

def re_render():
    image = root_container.render()
    for y, row in enumerate(image.raw_data):

        for x, color in enumerate(row):
            point_drawer.draw_point(y, x, color)

if __name__ == "__main__":
    root_window = tk.Tk()
    point_drawer = Point_Drawer(root_window)
    point_drawer.center_window()

    yingshaoxo_image_init()
    re_render()

    def click_it(y, x):
        print("clicked: ", y, x)
        root_container.click(y, x)
        re_render()
    point_drawer.set_click_callback(click_it)

    root_window.mainloop()
