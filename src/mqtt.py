import uasyncio as asyncio
import lan
from lib_mqtt_as import MQTTClient

DEFAULT_SERVER = '10.200.60.60'
MQTT_IP_FILENAME = "mqtt_ip.txt"
SUBSCRIBE = None
PUBLISH_PREFIX = None
client = None
on_message_received_cb = None


async def conn_han(client):
    await client.subscribe(SUBSCRIBE, 1)


def on_mqtt_message_received(topic, msg, retained):
    topic = topic.decode()
    msg = msg.decode()
    if lan.mac in topic:
        topic = "/".join(topic.split("/")[1:])
    print("[MQTT]: received [%s] -> [%s]" % (topic, msg))
    if on_message_received_cb != None:
        on_message_received_cb(topic, msg)


async def send_message(topic, msg):
    topic_out = "%s/%s" % (PUBLISH_PREFIX, topic)
    print("[MQTT]: sent [%s] -> [%s]" % (topic, msg))
    await client.publish(topic_out, msg, qos=1)


def register_on_message_received_callback(cb):
    global on_message_received_cb
    print("[MQTT]: register on message received cb")
    on_message_received_cb = cb


def write_ip_to_flash(ip):
    print("[MQTT]: ip write to file %s" % (ip))
    f = open(MQTT_IP_FILENAME, 'w')
    f.write(ip)
    f.close()


def read_ip_from_flash():
    try:
        f = open(MQTT_IP_FILENAME)
        ip = f.read()
        f.close()
        print("[MQTT]: ip read from file %s" % (ip))
        return ip
    except:
        print("[MQTT]: no ip found using default %s" % (DEFAULT_SERVER))
        return None


def is_connected():
    return client.is_connected()


def init():
    print("[MQTT]: init")
    global SUBSCRIBE, PUBLISH_PREFIX
    lan.init()
    SUBSCRIBE = "%s/in/#" % (lan.mac)
    PUBLISH_PREFIX = "%s" % (lan.mac)
    MQTTClient.DEBUG = True
    global client
    ip = read_ip_from_flash()
    if not ip:
        ip = DEFAULT_SERVER
    client = MQTTClient(client_id=lan.mac, subs_cb=on_mqtt_message_received, connect_coro=conn_han, server=ip)


async def loop_async():
    print("[MQTT]: start loop_async")
    while True:
        try:
            print("[MQTT]: connect to LAN")
            while True:
                if lan.check_link() == True:
                    break
                await asyncio.sleep(1)

            print("[MQTT]: connect to MQTT")
            await client.connect()
            while True:
                await asyncio.sleep(10)
        except Exception as e:
            print("[MQTT]: error connect with %s" % (e))
            await asyncio.sleep(10)


def test_async():
    print("[MQTT]: test_async")
    init()
    asyncio.run(loop_async())
