from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request

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
    return "Hello, world, fight for personal freedom."

def utf8_handler(request: Yingshaoxo_Http_Request) -> str:
    #return {"ok": "今天你反抗了吗？"}
    return "今天你反抗了吗？"

router = {
    r"/fight": utf8_handler,
    r"/freedom": special_handler,
    r"(.*)": home_handler
}


yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
yingshaoxo_http_server.start(host="0.0.0.0", port=1212)
#yingshaoxo_http_server.start(host = "0.0.0.0", port = 80, html_folder_path = "./", serve_html_under_which_url = "/") # remove (.*) url match if you use folder serving
