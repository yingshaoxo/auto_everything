from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request


def home_handler(request: Yingshaoxo_Http_Request) -> dict:
    return {"message": "Hello, world, fight for inner peace."}

def special_handler(request: Yingshaoxo_Http_Request) -> str:
    return "Hello, world, fight for personal freedom."


router = {
    r"/freedom": special_handler
    r"(.*)": home_handler,
}


yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
yingshaoxo_http_server.start(host="0.0.0.0", port=1212)
