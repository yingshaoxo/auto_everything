from style_shop_objects import *

from typing import Any
import json
from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request


class Service_style_shop:
    def get_json_web_token(self, headers: dict[str, str], item: Get_JSON_Web_Token_Request) -> Get_JSON_Web_Token_Response:
        default_response = Get_JSON_Web_Token_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response


def run(service_instance: Service_style_shop, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    def handle_get_url(sub_url: str, headers: dict[str, str]) -> str:
        return 'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> dict | str:
        sub_url = sub_url.strip("/")
        sub_url = sub_url.replace("{identity_name}", "", 1)
        sub_url = sub_url.strip("/")
        request_url = sub_url.split("/")[0].strip()

        if (request_url == ""):
            return f"Request url '{request_url}' is empty"
        elif (request_url == "get_json_web_token"):
            correct_item = Get_JSON_Web_Token_Request().from_dict(item)
            return (service_instance.get_json_web_token(headers, correct_item)).to_dict()

        return f"No API url matchs '{request_url}'"

    def general_handler(request: Yingshaoxo_Http_Request) -> dict | str:
        response = f"No handler for {request.url}"
        if request.method == "GET":
            response = handle_get_url(request.url, request.headers)
        elif request.method == "POST":
            response = handle_post_url(request.url, request.headers, json.loads(request.payload))
        return response

    router = {
        r"(.*)": general_handler,
    }

    yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
    yingshaoxo_http_server.start(host="0.0.0.0", port=int(port), html_folder_path=html_folder_path, serve_html_under_which_url=serve_html_under_which_url)

    
if __name__ == "__main__":
    service_instance = Service_style_shop()
    run(service_instance, port="6060", html_folder_path="/home/yingshaoxo/CS/yingshaoxo.github.io", serve_html_under_which_url="/ok")
