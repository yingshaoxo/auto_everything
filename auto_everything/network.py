import ipaddress
from typing import Any
from auto_everything.disk import Disk
from pathlib import Path
import os
import http.client as httplib

from auto_everything.base import Terminal, OS

t = Terminal(debug=True)
os_ = OS()
disk = Disk()


class Network:
    """
    I use this module to handle network stuff.
    """

    def __init__(self):
        assert "not found" not in t.run_command(
            "wget"
        ), """
'wget' is required for this module to work
You can install it with `sudo apt install wget`"""  

    def ip_port_forward(self, from_ip_port: str, to_ip_port: str):
        import socket
        import threading

        def handle(buffer: Any, direction: Any, src_address: Any, src_port: Any, dst_address: Any, dst_port: Any):
            '''
            intercept the data flows between local port and the target port
            '''
            # if direction:
            #     print(f"{src_address, src_port} -> {dst_address, dst_port} {len(buffer)} bytes")
            # else:
            #     print(f"{src_address, src_port} <- {dst_address, dst_port} {len(buffer)} bytes")
            return buffer

        def transfer(src: Any, dst: Any, direction: Any):
            src_address, src_port = src.getsockname()
            dst_address, dst_port = dst.getsockname()
            while True:
                try:
                    buffer = src.recv(4096)
                    if len(buffer) > 0:
                        dst.send(handle(buffer, direction, src_address, src_port, dst_address, dst_port))
                except Exception as e:
                    print("error: ", repr(e))
                    break
            # logging.warning(f"Closing connect {src_address, src_port}! ")
            src.close()
            # logging.warning(f"Closing connect {dst_address, dst_port}! ")
            dst.close()

        def server(local_host: Any, local_port: Any, remote_host: Any, remote_port: Any):
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((local_host, local_port))
            server_socket.listen(0x40)
            # logging.info(f"Server started {local_host, local_port}")
            # logging.info(f"Connect to {local_host, local_port} to get the content of {remote_host, remote_port}")
            while True:
                src_socket, src_address = server_socket.accept()
                # logging.info(f"[Establishing] {src_address} -> {local_host, local_port} -> ? -> {remote_host, remote_port}")
                try:
                    dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    dst_socket.connect((remote_host, remote_port))
                    # logging.info(f"[OK] {src_address} -> {local_host, local_port} -> {dst_socket.getsockname()} -> {remote_host, remote_port}")
                    s = threading.Thread(target=transfer, args=(dst_socket, src_socket, False))
                    r = threading.Thread(target=transfer, args=(src_socket, dst_socket, True))
                    s.start()
                    r.start()
                except Exception as e:
                    # logging.error(repr(e))
                    print("error: ", repr(e))

        from_ = from_ip_port.split(":")
        to_ = to_ip_port.split(":")
        server(local_host=from_[0], local_port=int(from_[1]), remote_host=to_[0], remote_port=int(to_[1]))

    def available(self, timeout: int = 1):
        conn = httplib.HTTPConnection("www.google.com", timeout=timeout)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except:
            conn.close()
            return False

    def download(self, url: str, target: str, size: str = "0B") -> bool:
        """
        Download a file from internet.

        Parameters
        ----------
        url: string
            the download link of a file
        target: string
            the local disk file path where the file would be saved to
        size: string
            do a simple check for the file. like '12KB' or '20MB'

        Returns
        -------
        bool
            return `false` if the specified size less than the file we downloaded
        """
        target_path_object = Path(target).expanduser().absolute()

        directory = target_path_object.parent
        target = str(target_path_object)
        assert os.path.exists(
            directory), f"target directory '{directory}' is not exits"
        t.run(f"wget {url} -O {target}")

        number = int("".join([i for i in list(size) if i.isdigit()]))
        unit = size.replace(str(number), "")
        assert unit in [
            "B",
            "KB",
            "MB",
        ], f"number={number}, unit={unit}\nsize error, it should be 700B, 5KB, 40MB and so on."
        the_file_size = disk.get_file_size(target, unit)
        if the_file_size != None and the_file_size > number:
            return True
        else:
            return False

    def get_mail_exchanger_record_by_using_base_domain_url(self, url: str) -> tuple[list[str], list[str]]:
        """
        Get mx record list by using a base domain.

        Parameters
        ----------
        url: string
            something like `gmail.com`

        Returns
        -------
        tuple(list[str], list[str])
            one is the record list without base domain, another one is the record list with base domain
        """
        url = url.removeprefix("http://")
        url = url.removeprefix("https://")
        url = url.removesuffix("/")
        result = t.run_command(f"dig {url} mx +short")
        result_list1 = [one.split(" ")[1] for one in result.strip().split("\n") if one.strip() != ""]
        result_list2 = [one.split(" ")[1]+url for one in result.strip().split("\n") if one.strip() != ""]
        return result_list1, result_list2
    
    def get_domain_to_ip_record_by_using_domain_url(self, url: str) -> list[str]:
        """
        Get IP address list by using a domain url.

        Parameters
        ----------
        url: string
            something like `alt4.gmail-smtp-in.l.google.com.`

        Returns
        -------
        list[string]
        """
        url = url.removeprefix("http://")
        url = url.removeprefix("https://")
        url = url.removesuffix("/")
        result = t.run_command(f"dig {url} a +short")
        return [one.strip() for one in result.strip().split("\n") if one.strip() != ""]

    def get_text_record_by_using_domain_url(self, url: str) -> list[str]:
        """
        Get text record list by using a domain url.

        Parameters
        ----------
        url: string
            something like `gmail.com`

        Returns
        -------
        list[string]
        """
        url = url.removeprefix("http://")
        url = url.removeprefix("https://")
        url = url.removesuffix("/")
        result = t.run_command(f"dig {url} txt +short")
        return [one.strip('" \n') for one in result.strip().split("\n") if one.strip('" \n') != ""]

    def check_if_an_ip_in_an_ip_network(self, ip: str, ip_network: str) -> bool:
        """
        check_if_an_ip_in_an_ip_network

        Parameters
        ----------
        ip: string
            something like `127.0.0.1`
        ip_network: string
            something like `127.0.0.0/24`

        Returns
        -------
        bool
        """
        an_address = ipaddress.ip_address(ip)
        a_network = ipaddress.ip_network(ip_network)
        return an_address in a_network


if __name__ == "__main__":
    network = Network()
    # result = net.download(
    #     "https://github.com/yingshaoxo/My-books/raw/master/Tools.py",
    #     "~/.auto_everything/hi.txt",
    # )
    # print(result)

    # text_info = net.get_text_record_by_using_domain_url("https://gmail.com/")
    # print(text_info)

    network.ip_port_forward("127.0.0.1:9998", "127.0.0.1:5551")