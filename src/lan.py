import network
from lib_umqtt_simple import MQTTClient
import ubinascii
import machine
import socket

# https://docs.openmv.io/library/network.LAN.html

from common import get_millis, millis_passed, dump_func

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
SERVER = "192.168.88.76"
PORT = 1883

mac = ""
lan = None
client = None

outgoing_messages = []
incoming_messages = []


def http_get(url):
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


def test_connection_with_gateway():
    print("[LAN]: test connection with gateway")
    gateway = lan.ifconfig()[2]
    try:
        addr = socket.getaddrinfo(gateway, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.close()
        return True
    except Exception as e:
        print("[LAN]: ERROR %s" % e)
        return False


def sub_cb(topic, msg):
    print("[LAN]: mqtt sub %s, %s " % (topic, msg))


@dump_func(timing=True)
def test_mqtt():
    global client
    client = MQTTClient(client_id=CLIENT_ID, server=SERVER, port=PORT)
    client.connect()
    client.set_callback(sub_cb)
    client.subscribe(b"micropython/led")
    # TODO: handle
    # OSError: [Errno 104] ECONNRESET
    # client.disconnect()


def send_mqtt_uptime():
    global timestamp
    if (millis_passed(timestamp) > 30000):
        timestamp = get_millis()
        print("uptime %d" % (timestamp))
        client.publish(TOPIC, "uptime %d".encode() % (timestamp))


def set_static_ip():
    print("[LAN]: set static ip")
    lan.ifconfig(('192.168.88.17', '255.255.255.0', '192.168.88.1', '8.8.8.8'))


def print_status():
    print("[LAN]: print status")
    print("mac", mac)
    print("status", lan.status())
    print("active", lan.active())
    print("isconnected", lan.isconnected())
    result = lan.ifconfig()
    if result:
        print(result)


def ping():
    uping.ping('192.168.88.1')


# Check internet connectivity by sending DNS lookup to Google's 8.8.8.8
def check_internet():
    print("[LAN]: check_internet")
    http_get('http://micropython.org/ks/test.html')


def is_connection_ready():
    status = lan.status()
    if status == 0:
        print("[LAN]: Link Down")
    if status == 1:
        print("[LAN]: Link Join")
        try:
            lan.active(True)
        except Exception as e:
            print("[LAN]: ERROR %s" % (e))
    elif status == 2:
        print("[LAN]: Link No-IP")
        try:
            lan.ifconfig('dhcp')
        except Exception as e:
            print("[LAN]: ERROR %s" % (e))
            set_static_ip()
    elif status == 3:
        print("[LAN]: Link Up")
        return test_connection_with_gateway()
    return False


def init():
    print("[LAN]: init")
    global lan, mac
    lan = network.LAN()
    mac = "".join(['{:02X}'.format(x) for x in lan.config('mac')])
    # lan.config(trace=4)


def check():
    print("[LAN]: check connection")
    is_connection_ready()


def loop():
    send_mqtt_uptime()
    try:
        client.check_msg()
    except Exception as e:
        print("client.check_msg error %s" % (e))
        # OSError: -1
