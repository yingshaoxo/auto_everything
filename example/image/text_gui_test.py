from auto_everything.disk import Disk
from auto_everything.image import GUI, Container

disk = Disk()

def change_it_back():
    the_text1.text="never give up"

def change_it_again():
    the_text1.text="yingshaoxo"

the_text1 = Container(width=0.5, text="Menu", on_click_function=change_it_back)
the_text2 = Container(width=0.5, text="Back", on_click_function=change_it_again)

def change_it(*args):
    the_text.text="yingshaoxo"
    print("fuck")

root_container = Container(
    height=1.0,
    width=1.0,
    rows=True,
    children=[
        Container(
            height=0.5,
            width=1.0,
            columns=True,
        ),
        Container(
            height=0.5,
            width=1.0,
            columns=True,
            children=[
                the_text1,
                the_text2,
            ]
        ),
    ]
)

def change_resolution(window_height=480, window_width=270):
    if root_container.parent_height == window_height and root_container.parent_width == window_width:
        return False
    root_container.parent_height=window_height
    root_container.parent_width=window_width
    return True

def click_it(y,x):
    root_container.click(y,x)

target_image_path = "./gui.png"
def refresh():
    text_2d_array = root_container.render_as_text()
    text = ""
    for row in text_2d_array:
        text += "".join(row) + "\n"
    print(text)
    image = root_container._convert_2d_text_to_image(text)
    image.save_image_to_file_path(target_image_path)

change_resolution()
refresh()


from auto_everything.http_ import Yingshaoxo_Threading_Based_Http_Server, Yingshaoxo_Http_Request
from time import sleep
import json

#@dataclass()
#class Yingshaoxo_Http_Request():
#    context: Any
#    host: str
#    method: str
#    url: str
#    url_arguments: dict[str, str]
#    headers: dict[str, str]
#    payload: str | None

def change_resolution_handler(request: Yingshaoxo_Http_Request) -> str:
    if request.method != "GET":
        return "We accept click?height=22&width=11 get request"
    height = request.url_arguments.get("height")
    width = request.url_arguments.get("width")
    if height == None or width == None:
        return "You should give me height and width"
    height = int(height)
    width = int(width)
    # change the resolution
    if change_resolution(height, width):
        refresh()

def click_handler(request: Yingshaoxo_Http_Request) -> str:
    if request.method != "GET":
        return "We accept click?y=22&x=11 get request"
    y = request.url_arguments.get("y")
    x = request.url_arguments.get("x")
    if y == None or x == None:
        return "You should give me y and x"
    y = int(y)
    x = int(x)
    # do something
    click_it(y, x)
    refresh()
    return "Hello, world, fight for personal freedom."

router = {
    r"/change_resolution": change_resolution_handler,
    r"/click": click_handler,
    #r"(.*)": home_handler
}

yingshaoxo_http_server = Yingshaoxo_Threading_Based_Http_Server(router=router)
yingshaoxo_http_server.start(host="0.0.0.0", port=1212, html_folder_path="./")
