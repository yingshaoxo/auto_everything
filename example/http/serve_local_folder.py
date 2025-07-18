from auto_everything.http_ import Yingshaoxo_Threading_Based_Http_Server, Yingshaoxo_Http_Request
import os

"""
@dataclass()
class Yingshaoxo_Http_Request():
    context: Any
    host: str
    method: str
    url: str
    url_arguments: dict[str, str]
    headers: dict[str, str]
    payload: dict[str, str] | None
"""

def home_handler(request):
    print(request)
    try:
        real_file_path = "." + request.url
        if os.path.isdir(real_file_path):
            files = os.listdir("." + request.url)

            if "index.html" not in files:
                folders = [file for file in files if "." not in file]
                files = [file for file in files if "." in file]

                folders.sort()
                files.sort()

                all_list = folders + files
                new_request_url = request.url.strip("/")
                if new_request_url != "":
                    new_request_url = "/" + new_request_url

                new_all_list = []
                for file in all_list:
                    target_path = new_request_url + "/" + file
                    if os.path.isdir("." + target_path):
                        target_path += "/"
                        new_all_list.append('<a href="{the_path}">{file}</a>'.format(the_path=target_path, file=file))
                    else:
                        new_all_list.append('<a href="{the_path}">{file}</a>'.format(the_path=target_path, file=file))
                all_list = new_all_list

                html_code = "<br>".join(all_list)
                html_code = '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + html_code
            else:
                with open(os.path.join(real_file_path, "index.html"), "r") as f:
                    html_code = f.read()

            return html_code
        else:
            with open(real_file_path, "rb") as f:
                bytes_data = f.read()
            return bytes_data
    except Exception as e:
        return str(e)

def special_handler(request: Yingshaoxo_Http_Request):
    return "Hello, world, fight for personal freedom."

router = {
    r"/__yingshaoxo__": special_handler,
    r"(.*)": home_handler
}

yingshaoxo_http_server = Yingshaoxo_Threading_Based_Http_Server(router=router)
yingshaoxo_http_server.start(host = "0.0.0.0", port = 9999)
# If you see utf-8 character broken, you may need to use "Yingshaoxo_Http_Server"
