from typing import Any, Callable
from dataclasses import dataclass

import os
import socket
import json
import re
from time import sleep


@dataclass()
class Yingshaoxo_Http_Request():
    context: Any
    host: str
    method: str
    url: str
    url_arguments: dict[str, str]
    headers: dict[str, str]
    payload: str | None


def _handle_socket_request(socket_connection, context, router, handle_get_file_url):
    try:
        host = None
        method = None
        url = None
        url_arguments = dict()
        http_standards = None

        raw_http_request_bytes = socket_connection.recv(1024) # one utf-8 char is 0~4 bytes, that's why for the following code, I times the length by 4 to make sure we receive all data
        raw_http_request = raw_http_request_bytes.decode("utf-8", errors="ignore")
        #print(raw_http_request)
        #print(repr(raw_http_request))

        splits = raw_http_request.strip().split("\n")
        if (len(splits) > 0):
            head_line = splits[0]
            head_line_splits = head_line.split(" ")
            if len(head_line_splits) == 3:
                method, url, http_standards = head_line_splits 
                url_splits = url.split("?")
                if len(url_splits) >= 2:
                    url = url_splits[0]
                    raw_url_arguments = "?".join(url_splits[1:])
                    url_arguments_splits = raw_url_arguments.split("&")
                    for one in url_arguments_splits:
                        if "=" in one:
                            argument_key, argument_value = one.split("=")
                            url_arguments[argument_key] = argument_value
                else:
                    pass

        if (method == None or url == None or http_standards == None):
            print(f"Unkonw http request:\n{raw_http_request}")
            exit()
        else:
            pass

        raw_headers_lines = splits[1:] 
        raw_headers_lines = [line for line in raw_headers_lines if ": " in line]
        headers_dict = {}
        for line in raw_headers_lines:
            header_splits = line.split(": ")
            key = header_splits[0]
            value = ":".join(header_splits[1:])
            headers_dict[key] = value

        content_length = None
        payload = None
        payload_seperator_bytes = b"\r\n\r\n"
        payload_seperator = "\r\n\r\n"
        if "Content-Length" in headers_dict:
            content_length = int(headers_dict["Content-Length"])
        
        if content_length != None:
            # receive the rest of data by using socket receiv
            payload_splits = raw_http_request_bytes.split(payload_seperator_bytes)
            if len(payload_splits) >= 2:
                # already has all headers, need payload
                payload = payload_splits[1]
                if len(payload) >= content_length:
                    pass
                else:
                    payload += socket_connection.recv((content_length)*4-len(payload)+200)
                    payload = payload.decode("utf-8", errors="ignore")
            else:
                # missing some headers, need more data, including payload
                raw_http_request_bytes += socket_connection.recv((content_length)*4+len(raw_http_request_bytes)+200)
                raw_http_request = raw_http_request_bytes.decode("utf-8", errors="ignore")
                payload = raw_http_request_bytes.split(payload_seperator_bytes)[1]
                payload = payload.decode("utf-8", errors="ignore")

        # do the process directly
        splits = raw_http_request.split(payload_seperator)
        header_line_list = splits[0].split("\n")[1:]
        headers_dict = {}
        for line in header_line_list:
            header_splits = line.split(": ")
            key = header_splits[0]
            value = (":".join(header_splits[1:])).strip()
            headers_dict[key] = value
        if "Host" in headers_dict:
            host = headers_dict["Host"]

        print(host, method, url)
        #print(f"headers:\n{headers_dict}")
        #print(f"payload:\n{payload}")
        raw_response = None
        response = f"HTTP/1.1 500 Server error\r\n\r\n".lstrip()

        if handle_get_file_url != None and method == "GET":
            # handle file download request, for example, html, css...
            raw_response = handle_get_file_url(url)

        # if do not need to serve file, or file not exists, then handle others
        if raw_response == None:
            the_request_object = Yingshaoxo_Http_Request(
                context=context,
                host=host,
                method=method,
                url=url,
                url_arguments=url_arguments,
                headers=headers_dict,
                payload=payload
            )
            for route_regex_expression, route_function in reversed(list(router.items())):
                if re.fullmatch(route_regex_expression, url) != None:
                    raw_response = route_function(the_request_object)

        if type(raw_response) == str:
            response = f"""
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *\r\n\r\n{raw_response}
""".strip()
        elif type(raw_response) == dict:
            raw_response = json.dumps(raw_response, indent=4)
            json_length = len(raw_response)
            response = f"""
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: {json_length}
Access-Control-Allow-Origin: *\r\n\r\n{raw_response}
            """.strip()
        elif type(raw_response) == bytes:
            bytes_length = len(raw_response)

            the_content_type = None
            if url.endswith(".html"):
                the_content_type = "text/html"
            elif url.endswith(".css"):
                the_content_type = "text/css"

            if the_content_type != None:
                response = f"""
HTTP/1.1 200 OK
Content-Type: {the_content_type}
Content-Length: {bytes_length}
Access-Control-Allow-Origin: *\r\n\r\n""".lstrip()
            else:
                response = f"""
HTTP/1.1 200 OK
Content-Length: {bytes_length}
Access-Control-Allow-Origin: *\r\n\r\n""".lstrip()
            response = response.encode("utf-8", errors="ignore")
            response += raw_response
        else:
            response = f"HTTP/1.1 500 Server error\r\n\r\nNo router for {url}".strip()

        if type(response) == str:
            response = response.encode("utf-8", errors="ignore")

        socket_connection.sendall(response)
    except Exception as e:
        print(e)
        response = f"HTTP/1.1 200 OK\r\n\r\n{e}".strip()
        response = response.encode("utf-8", errors="ignore")
        socket_connection.sendall(response)
    finally:
        socket_connection.shutdown(1)
        socket_connection.close()
        exit()


def _yingshaoxo_home_handler_example(request: Yingshaoxo_Http_Request) -> dict:
    return {"message": "Hello, world, fight for inner peace."}

def _yingshaoxo_special_handler_example(request: Yingshaoxo_Http_Request) -> dict:
    return "Hello, world, fight for personal freedom."

_yingshaoxo_router_example = {
    r"/freedom": _yingshaoxo_special_handler_example,
    r"(.*?)": _yingshaoxo_home_handler_example,
}


class Yingshaoxo_Http_Server():
    def __init__(self, router: dict[str, Callable[[Yingshaoxo_Http_Request], str|dict]]):
        """
        router: a dict where key is the url regex, value is a function like "def handle_function(request: Yingshaoxo_Http_Request) -> str|dict"
        """
        import multiprocessing
        self._multiprocessing = multiprocessing
        multiprocess_manager = self._multiprocessing.Manager()

        self.context = multiprocess_manager.dict()
        self.router = router

    def start(self, host:str = "0.0.0.0", port:int = 80, html_folder_path: str="", serve_html_under_which_url: str="/"): 
        try:
            handle_get_file_url = None
            if (html_folder_path != ""):
                if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
                    def handle_get_file_url(sub_url: str) -> bytes | None:
                        sub_url = sub_url.strip("/")
                        sub_url = sub_url.lstrip(serve_html_under_which_url)
                        if sub_url == '':
                            sub_url = 'index.html'
                        real_file_path = f"{os.path.join(html_folder_path, sub_url)}"
                        if os.path.exists(real_file_path) and os.path.isfile(real_file_path):
                            with open(real_file_path, mode="rb") as f:
                                the_data = f.read()
                        else:
                            #return b"Resource not found"
                            return None
                        return the_data
                else:
                    print(f"Error: You should give me an absolute html_folder_path than {html_folder_path}")

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port))
            server.listen(1)

            print(f"Service is on http://{host}:{port}")

            process_list = []

            while True:
                socket_connection, addr = server.accept()
                process = self._multiprocessing.Process(target=_handle_socket_request, args=(socket_connection, self.context, self.router, handle_get_file_url))
                process.start()
                process_list.append(process)

                new_process_list = []
                for a_process in process_list:
                    if a_process.is_alive():
                        new_process_list.append(a_process)
                process_list = new_process_list
        except KeyboardInterrupt:
            print("Quit...")
            for a_process in process_list:
                if a_process.is_alive():
                    a_process.terminate()
            server.shutdown(1)
            server.close()
        except Exception as e:
            print(e)
            print("Quit...")
            for a_process in process_list:
                if a_process.is_alive():
                    a_process.terminate()
            server.shutdown(1)
            server.close()
        finally:
            pass


class Yingshaoxo_Threading_Based_Http_Server():
    def __init__(self, router: dict[str, Callable[[Yingshaoxo_Http_Request], str|dict]]):
        """
        router: a dict where key is the url regex, value is a function like "def handle_function(request: Yingshaoxo_Http_Request) -> str|dict"
        """
        from http.server import HTTPServer, BaseHTTPRequestHandler
        from socketserver import ThreadingMixIn
        #import http.server as built_in_http_server
        self._HTTPServer = HTTPServer
        self._BaseHTTPRequestHandler = BaseHTTPRequestHandler
        self._ThreadingMixIn = ThreadingMixIn

        self.context = dict()
        self.router = router

    def _get_headers_dict_from_string(self, headers: str) -> dict:
        dic = {}
        for line in headers.split("\n"):
            if line.startswith(("GET", "POST")):
                continue
            point_index = line.find(":")
            dic[line[:point_index].strip()] = line[point_index+1:].strip()
        return dic

    def start(self, host:str = "0.0.0.0", port: int = 80, html_folder_path: str="", serve_html_under_which_url: str="/"):
        def handle_file_request_url(sub_url: str) -> bytes | None:
            return b'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

        if (html_folder_path != ""):
            if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
                def handle_file_request_url(sub_url: str) -> bytes | None:
                    sub_url = sub_url.strip("/")
                    sub_url = sub_url.lstrip(serve_html_under_which_url)
                    if sub_url == '':
                        sub_url = 'index.html'
                    real_file_path = f"{os.path.join(html_folder_path, sub_url)}"
                    if os.path.exists(real_file_path) and os.path.isfile(real_file_path):
                        with open(real_file_path, mode="rb") as f:
                            the_data = f.read()
                    else:
                        return None
                    return the_data
            else:
                print(f"Error: You should give me an absolute html_folder_path than {html_folder_path}")

        def handle_any_url(method: str, sub_url: str, headers: dict[str, str], payload: dict[str, Any] | None = None) -> tuple[bytes, str | bytes | dict]: 
            #sub_url = sub_url.strip("/")
            #sub_url = sub_url.replace("{identity_name}", "", 1)
            #sub_url = sub_url.strip("/")
            #request_url = sub_url.split("/")[0].strip()

            raw_response = None 

            if method == "GET":
                raw_response = handle_file_request_url(sub_url)

            url_arguments = dict()
            url_splits = sub_url.split("?")
            if len(url_splits) >= 2:
                sub_url = url_splits[0]
                raw_url_arguments = "?".join(url_splits[1:])
                url_arguments_splits = raw_url_arguments.split("&")
                for one in url_arguments_splits:
                    if "=" in one:
                        argument_key, argument_value = one.split("=")
                        url_arguments[argument_key] = argument_value

            the_request_object = Yingshaoxo_Http_Request(
                context=self.context,
                host=headers.get("Host"),
                method=method,
                url=sub_url,
                url_arguments=url_arguments,
                headers=headers,
                payload=payload
            )
            for route_regex_expression, route_function in reversed(list(self.router.items())):
                if re.fullmatch(route_regex_expression, sub_url) != None:
                    raw_response = route_function(the_request_object)

            if raw_response == None:
                raw_response = f"No API url matchs '{sub_url}'"

            raw_type = str
            if type(raw_response) == str:
                raw_response = raw_response.encode("utf-8", errors="ignore")
                raw_type = str
            elif type(raw_response) == dict:
                raw_response = json.dumps(raw_response, indent=4).encode("utf-8", errors="ignore")
                raw_type = dict
            elif type(raw_response) == bytes:
                raw_type = bytes

            return raw_response, raw_type
        
        class WebRequestHandler(self._BaseHTTPRequestHandler):
            def do_GET(self2):
                sub_url = self2.path
                headers = self._get_headers_dict_from_string(self2.headers.as_string())

                self2.send_response(200)

                self2.send_header("Access-Control-Allow-Origin", "*")

                if sub_url.endswith(".html"):
                    self2.send_header("Content-Type", "text/html")
                elif sub_url.endswith(".css"):
                    self2.send_header("Content-Type", "text/css")

                response, raw_type = handle_any_url("GET", sub_url, headers, None)

                self2.end_headers()
                self2.wfile.write(response)

            def do_POST(self2):
                sub_url = self2.path
                headers = self._get_headers_dict_from_string(self2.headers.as_string())

                content_length = headers.get('Content-Length')
                if content_length is None:
                    self2.wfile.write("What you send is not json".encode("utf-8", errors="ignore"))
                    return
                else:
                    content_length = int(content_length)
                
                if content_length == 0:
                    self2.wfile.write("What you send is not json".encode("utf-8", errors="ignore"))
                    return

                request_json_dict = json.loads(self2.rfile.read(content_length))

                self2.send_response(200)
                self2.send_header("Access-Control-Allow-Origin", "*")

                response, raw_type = handle_any_url("POST", sub_url, headers, request_json_dict)
                if raw_type == dict:
                    self2.send_header("Content-Type", "application/json")

                self2.end_headers()
                self2.wfile.write(response)

        class ThreadedHTTPServer(self._ThreadingMixIn, self._HTTPServer):
            pass
        
        # Setting TCP Address
        server_address = (host, port)
        
        # invoking server
        http = ThreadedHTTPServer(server_address, WebRequestHandler)

        print(f"The website is running at: http://127.0.0.1:{port}/")
        
        http.serve_forever()


def run_a_command_with_hot_load(watch_path: str, hotload_command: str):
    """
    watch_path: a folder you want to watch, whenever some of those file get changed, the hotload_command will get re executed
    hotload_command: a bash command to start the server, for example, "python3 main.py"

    You should run this function on a diffirent python file than the hotload_command has.
    """
    import multiprocessing
    from auto_everything.develop import Develop
    from auto_everything.terminal import Terminal
    develop = Develop()
    terminal = Terminal()

    def run_the_process():
        terminal.run(hotload_command, wait=True)

    the_running_process = multiprocessing.Process(target=run_the_process, args=())
    the_running_process.start()

    while True:
        changed = develop.whether_a_folder_has_changed(folder_path=watch_path, type_limiter=[".py", ".html", ".css", ".js"])
        if (changed):
            print("Source code get changed, doing a reloading now...")
            the_running_process.kill()
            while the_running_process.is_alive():
                sleep(1)
            the_running_process = multiprocessing.Process(target=run_the_process, args=())
            the_running_process.start()
        sleep(1)


if __name__ == "__main__":
    #yingshaoxo_http_server = Yingshaoxo_Http_Server(router=_yingshaoxo_router_example)
    yingshaoxo_http_server = Yingshaoxo_Threading_Based_Http_Server(router=_yingshaoxo_router_example)
    yingshaoxo_http_server.start(port=1212, html_folder_path="./")
