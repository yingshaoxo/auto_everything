from auto_everything.network import Network
network = Network()

from_ip = "0.0.0.0:5277"
to_ip = "22.33.44.55:80"
network.ip_port_forward(from_ip, to_ip)

print("Now if you visit '0.0.0.0:5277', actually you are visiting '22.33.44.55:80'")
