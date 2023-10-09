from typing import Any, Callable
from dataclasses import dataclass

import socket
import multiprocessing
import json
import re
from time import sleep


multiprocess_manager = multiprocessing.Manager()


@dataclass()
class Yingshaoxo_Http_Request():
    context: multiprocess_manager.dict
    host: str
    method: str
    url: str
    url_arguments: dict[str, str]
    headers: dict[str, str]
    payload: str | None


def _handle_socket_request(socket_connection, context, router):
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
        response = f"HTTP/1.1 500 Server error\r\n\r\n"

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
            response = f"HTTP/1.1 200 OK\r\n\r\n{raw_response}"
        elif type(raw_response) == dict:
            raw_response = json.dumps(raw_response, indent=4)
            json_length = len(raw_response)
            response = f"""
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: {json_length}

{raw_response}
            """
        else:
            response = f"HTTP/1.1 500 Server error\r\n\r\nNo router for {url}"

        socket_connection.sendall(response.encode("utf-8", errors="ignore"))
    except Exception as e:
        print(e)
        response = f"HTTP/1.1 200 OK\r\n\r\n{e}"
        socket_connection.sendall(response.encode("utf-8", errors="ignore"))
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
        self.context = multiprocess_manager.dict()
        self.router = router

    def start(self, host:str = "0.0.0.0", port:int = 80): 
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port))
            server.listen(1)

            print(f"Service is on http://{host}:{port}")

            process_list = []

            while True:
                socket_connection, addr = server.accept()
                process = multiprocessing.Process(target=_handle_socket_request, args=(socket_connection, self.context, self.router))
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
        finally:
            pass


if __name__ == "__main__":
    yingshaoxo_http_server = Yingshaoxo_Http_Server(router=_yingshaoxo_router_example)
    yingshaoxo_http_server.start(port=1212)
