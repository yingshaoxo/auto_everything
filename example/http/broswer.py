"""
Should use Yingshaoxo_Http_Client as the http client, use image module GUI as front_end
"""

from auto_everything.http_ import Yingshaoxo_Http_Client
yingshaoxo_http_client = Yingshaoxo_Http_Client()

print(yingshaoxo_http_client.post("http://127.0.0.1:1212/post", {"hi": "you"}))
