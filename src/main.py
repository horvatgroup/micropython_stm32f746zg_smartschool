from common import dump_func, create_led, create_button
from peripherals import register_button_callback_function, check_button
import network
from umqtt_simple import MQTTClient
import ubinascii, machine

SERVER = "192.168.88.75"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"led"
lan = None
client = None

@dump_func(timing=True)
def test_network():
    global lan
    lan = network.LAN()
    lan.active(True)
    # TODO: handle exception
    # OSError: timeout waiting for DHCP to get IP address
    lan.ifconfig('dhcp')
    result = lan.ifconfig()
    if result:
        print(result)


@dump_func(timing=True, showarg=True)
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

@dump_func(timing=True)
def test_mqtt():
    global client
    client = MQTTClient(CLIENT_ID, SERVER)
    client.connect()
    #TODO: handle
    #OSError: [Errno 104] ECONNRESET
    print("Connected to %s, waiting for button presses" % SERVER)
    client.publish(TOPIC, b"toggle")
    client.disconnect()

def on_button_callback(state):
    if state:
        http_get('http://micropython.org/ks/test.html')
        test_mqtt()


if __name__ == "__main__":
    test_network()
    register_button_callback_function(on_button_callback)
    while True:
        check_button()
