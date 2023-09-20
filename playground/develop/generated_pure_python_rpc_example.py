from typing import Any
import http.server as http_server
import json
import os
import multiprocessing
from time import sleep

#from .style_shop_objects import *
from style_shop_objects import *


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


def get_headers_dict_from_string(headers: str) -> dict:
    dic = {}
    for line in headers.split("\n"):
        if line.startswith(("GET", "POST")):
            continue
        point_index = line.find(":")
        dic[line[:point_index].strip()] = line[point_index+1:].strip()
    return dic


def run(service_instance: Service_style_shop, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    # allow_origins=['*'],
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],

    def handle_get_url(sub_url: str, headers: dict[str, str]) -> bytes:
        return b'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    if (html_folder_path != ""):
        if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
            def handle_get_url(sub_url: str, headers: dict[str, str]) -> bytes:
                sub_url = sub_url.strip("/")
                sub_url = sub_url.lstrip(serve_html_under_which_url)
                if sub_url == '':
                    sub_url = 'index.html'
                real_file_path = f"{os.path.join(html_folder_path, sub_url)}"
                if os.path.exists(real_file_path) and os.path.isfile(real_file_path):
                    with open(real_file_path, mode="rb") as f:
                        the_data = f.read()
                else:
                    return b"Resource not found"
                return the_data

            print(f"The website is running at: http://127.0.0.1:{port}/")
        else:
            print(f"Error: You should give me an absolute html_folder_path than {html_folder_path}")

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> str:
        sub_url = sub_url.strip("/")
        request_url = sub_url.split("/")[0].strip()

        if (request_url == ""):
            return f"Request url '{request_url}' is empty"
        elif (request_url == "get_json_web_token"):
            correct_item = Get_JSON_Web_Token_Request().from_dict(item)
            return json.dumps((service_instance.get_json_web_token(headers, correct_item)).to_dict())

        return f"No API url matchs '{request_url}'"
    
    class WebRequestHandler(http_server.BaseHTTPRequestHandler):
        def do_GET(self):
            sub_url = self.path
            headers = get_headers_dict_from_string(self.headers.as_string())

            self.send_response(200)

            self.send_header("Access-Control-Allow-Origin", "*")

            if sub_url.endswith(".html"):
                self.send_header("Content-Type", "text/html")
            elif sub_url.endswith(".css"):
                self.send_header("Content-Type", "text/css")

            response = handle_get_url(sub_url, headers)

            self.end_headers()
            self.wfile.write(response)

        def do_POST(self):
            sub_url = self.path
            headers = get_headers_dict_from_string(self.headers.as_string())

            content_length = headers.get('Content-Length')
            if content_length is None:
                self.wfile.write("What you send is not json".encode("utf-8"))
                return
            else:
                content_length = int(content_length)
            
            if content_length == 0:
                self.wfile.write("What you send is not json".encode("utf-8"))
                return

            request_json_dict = json.loads(self.rfile.read(content_length))

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = handle_post_url(sub_url, headers, request_json_dict)

            self.wfile.write(response.encode("utf-8"))

    
    # Creating Server
    ServerClass  = http_server.HTTPServer
    
    # Setting TCP Address
    server_address = ('0.0.0.0', int(port))
    
    # invoking server
    http = ServerClass(server_address, WebRequestHandler)
    
    http.serve_forever()


def run_with_hot_load(watch_path: str, service_instance: Service_style_shop, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    from auto_everything.develop import Develop
    develop = Develop()

    the_running_process = multiprocessing.Process(target=run, args=(service_instance, port, html_folder_path, serve_html_under_which_url))
    the_running_process.start()

    while True:
        changed = develop.whether_a_folder_has_changed(folder_path=watch_path, type_limiter=[".py", ".html", ".css", ".js"])
        if (changed):
            print("Source code get changed, doing a reloading now...")
            the_running_process.kill()
            while the_running_process.is_alive():
                sleep(1)
            the_running_process = multiprocessing.Process(target=run, args=(service_instance, port, html_folder_path, serve_html_under_which_url))
            the_running_process.start()
        sleep(1)


if __name__ == "__main__":
    service_instance = Service_style_shop()
    #def run(service_instance: Service_style_shop, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    run(service_instance, port="6060", html_folder_path="/home/yingshaoxo/CS/yingshaoxo.github.io", serve_html_under_which_url="/ok")