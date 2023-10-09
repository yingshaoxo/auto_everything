from auto_everything.http import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request


def home_handler_example(request: Yingshaoxo_Http_Request) -> dict:
    return {"message": "Hello, world, fight for inner peace."}

def special_handler_example(request: Yingshaoxo_Http_Request) -> str:
    return "Hello, world, fight for personal freedom."


router_example = {
    r"(.*)": home_handler_example,
    r"/freedom": special_handler_example
}


yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router_example)
yingshaoxo_http_server.start(host="0.0.0.0", port=1212)
