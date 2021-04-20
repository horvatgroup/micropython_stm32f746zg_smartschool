from utime import sleep
from common import create_led, create_button
import network
import socket

lan = None
client = None

def test_network():
    print("test network start")
    global lan
    lan = network.LAN()
    lan.active(True)
    lan.ifconfig('dhcp')
    result = lan.ifconfig()
    if result:
        print(result)
    print("test network end")

def http_get(url):
    print("http get start")
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
    print("http get end")
    
def on_button_callback(state):
    print("button %s" % (("released", "pressed")[state]))
    if not state:
        return
    toggle_leds()
    http_get('http://micropython.org/ks/test.html')

def check_button():
    global button_state
    state = button.value()
    if state != button_state:
        button_state = state
        on_button_callback(button_state)

if __name__ == "__main__":
    test_network()
    while True:
        check_button()