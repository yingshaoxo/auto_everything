from auto_everything.network import Network
network = Network()

def test_ip_port_forward():
    network.ip_port_forward("127.0.0.1:9998", "127.0.0.1:5551")