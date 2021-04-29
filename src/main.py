from common import dump_func, create_led, create_button, get_millis, millis_passed
from peripherals import register_button_callback_function, check_button
import network
from umqtt_simple import MQTTClient
import ubinascii
import machine

#testing
# sudo systemctl start mosquitto
# mosquitto_sub -t "led"
# mosquitto_pub -h 192.168.88.75 -t "foo_topic" -m "bok"

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
SERVER = "soldier.cloudmqtt.com"
PORT = 16200
USER = "exrkeina"
PASSWORD = "2zUqpbUBMZGY"
TOPIC = b"micropython/uptime"
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
    client = MQTTClient(client_id=CLIENT_ID, server=SERVER, port=PORT, user=USER, password=PASSWORD)
    client.connect()
    client.set_callback(sub_cb)
    client.subscribe(b"micropython/led")
    #TODO: handle
    # OSError: [Errno 104] ECONNRESET
    # client.disconnect()


def on_button_callback(state):
    client.publish(TOPIC, "toggle %s".encode() % (state))

timestamp = 0

def send_mqtt_uptime():
    global timestamp
    if (millis_passed(timestamp) > 30000):
        timestamp = get_millis()
        print("uptime %d" % (timestamp))
        client.publish(TOPIC, "uptime %d".encode() % (timestamp))
        

if __name__ == "__main__":
    test_network()
    http_get('http://micropython.org/ks/test.html')
    test_mqtt()
    register_button_callback_function(on_button_callback)
    while True:
        check_button()
        send_mqtt_uptime()
        try:
            client.check_msg()
        except Exception as e:
            print("client.check_msg error %s" % (e))
            #OSError: -1