from common import dump_func, create_led, create_button
from peripherals import register_button_callback_function, check_button
import network
from umqtt_simple import MQTTClient
import ubinascii
import machine

#testing
# sudo systemctl start mosquitto
# mosquitto_sub -t "led"
# mosquitto_pub -h 192.168.88.75 -t "foo_topic" -m "bok"

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


def sub_cb(topic, msg):
    print((topic, msg))


@dump_func(timing=True)
def test_mqtt():
    global client
    client = MQTTClient(CLIENT_ID, SERVER)
    client.connect()
    client.set_callback(sub_cb)
    client.subscribe(b"foo_topic")
    #TODO: handle
    # OSError: [Errno 104] ECONNRESET
    # client.disconnect()


def on_button_callback(state):
    client.publish(TOPIC, "toggle %s".encode() % (state))


if __name__ == "__main__":
    test_network()
    http_get('http://micropython.org/ks/test.html')
    test_mqtt()
    register_button_callback_function(on_button_callback)
    while True:
        check_button()
        client.check_msg()