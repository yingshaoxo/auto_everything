from auto_everything.http_ import Yingshaoxo_Threading_Based_Http_Server, Yingshaoxo_Http_Request
from time import sleep

"""
@dataclass()
class Yingshaoxo_Http_Request():
    context: Any
    host: str
    method: str
    url: str
    url_arguments: dict[str, str]
    headers: dict[str, str]
    payload: str | None
"""


def home_handler(request: Yingshaoxo_Http_Request) -> dict:
    return {"message": "Hello, world, fight for inner peace."}

def special_handler(request: Yingshaoxo_Http_Request) -> str:
    sleep(30)
    return "Hello, world, fight for personal freedom."


router = {
    r"/freedom": special_handler,
    r"(.*)": home_handler
}


yingshaoxo_http_server = Yingshaoxo_Threading_Based_Http_Server(router=router)
yingshaoxo_http_server.start(host="0.0.0.0", port=1212)
#yingshaoxo_http_server.start(host = "0.0.0.0", port = 80, html_folder_path = "./", serve_html_under_which_url = "/") # remove (.*) url match if you use folder serving
