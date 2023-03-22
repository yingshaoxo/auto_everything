import ipaddress
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
    net = Network()
    # result = net.download(
    #     "https://github.com/yingshaoxo/My-books/raw/master/Tools.py",
    #     "~/.auto_everything/hi.txt",
    # )
    # print(result)

    text_info = net.get_text_record_by_using_domain_url("https://gmail.com/")
    print(text_info)