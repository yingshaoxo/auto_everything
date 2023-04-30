from auto_everything.network import Network
network = Network()

def test_ip_port_forward():
    network.ip_port_forward("127.0.0.1:9998", "127.0.0.1:5551")

def test_download_function():
    network.download("https://www.learndatasci.com/solutions/python-move-file/", "/home/yingshaoxo/CS/auto_everything/blackhole/index.html")
    network.download("https://raw.githubusercontent.com/yingshaoxo/gopython/main/README.md", "/home/yingshaoxo/CS/auto_everything/blackhole/readme.md")