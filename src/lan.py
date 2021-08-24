import network
from lib_umqtt_simple import MQTTClient
import ubinascii
import machine

from common import get_millis, millis_passed, dump_func

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
SERVER = "192.168.88.76"
PORT = 16200

lan = None
client = None

outgoing_messages = []
incoming_messages = []


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


is_active = False
has_ip = False
has_internet = False


def reset():
    global is_active, has_ip, has_internet
    is_active = False
    has_ip = False
    has_internet = False


def set_active():
    global is_active
    print("[LAN]: set active")
    try:
        lan.active(True)
        is_active = True
    except:
        print("[LAN]: ERROR: cant activate network")
        reset()


def get_ip():
    global has_ip
    print("[LAN]: get ip")
    try:
        lan.ifconfig('dhcp')
        has_ip = True
    except:
        print("[LAN]: ERROR: cant get ip")
        reset()


def print_ip():
    print("[LAN]: print ip")
    result = lan.ifconfig()
    if result:
        print(result)

def print_status():
    print("[LAN]: print status")
    print(lan.status())

def check_internet():
    global has_internet
    print("[LAN]: test http get")
    http_get('http://micropython.org/ks/test.html')
    has_internet = True


def check_connection():
    if not is_active:
        set_active()
    if is_active and not has_ip:
        get_ip()
    if is_active and has_ip and not has_internet:
        check_internet()


def init():
    print("[LAN]: init")
    global lan
    lan = network.LAN()


def check():
    print("[LAN]: check connection")
    check_connection()


def loop():
    send_mqtt_uptime()
    try:
        client.check_msg()
    except Exception as e:
        print("client.check_msg error %s" % (e))
        # OSError: -1
