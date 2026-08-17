import network
import time

def connect_wifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('http://pornhub.com', '')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")

def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

def set_up_wireless_access_point():
    ssid = 'micro_python_access_point'
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid)
    # why it can't configure static ip? (mac bind to ip)

def set_up_wireless_access_point_with_password(password="12345678"):
    ssid = 'micro_python_access_point'
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA2_PSK)
    ap.active(True)


set_up_wireless_access_point()
while True:
    time.sleep(1)

try:
    connect_wifi()
    print(http_get('http://micropython.org/ks/test.html'))
except Exception as e:
    print(e)

