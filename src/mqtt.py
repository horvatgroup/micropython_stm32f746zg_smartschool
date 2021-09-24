import uasyncio as asyncio
import lan
from lib_mqtt_as import MQTTClient

SERVER = '192.168.88.42'
SUBSCRIBE = None
PUBLISH_PREFIX = None
client = None
outgoing_messages = {}
incoming_messages = {}
on_message_received_cb = None


async def conn_han(client):
    await client.subscribe(SUBSCRIBE, 1)


def on_mqtt_message_received(topic, msg, retained):
    if lan.mac in topic:
        topic = "/".join(topic.split("/")[1:])
    incoming_messages[topic] = msg


def send_message(topic, msg):
    outgoing_messages[topic] = msg


def handle_incoming_messages():
    for topic in incoming_messages.keys():
        msg = incoming_messages[topic]
        print("[MQTT]: received [%s] -> [%s]" % (topic, msg))
        if on_message_received_cb != None:
            on_message_received_cb(topic, msg)
        del incoming_messages[topic]


async def handle_outgoing_messages():
    for topic in outgoing_messages.keys():
        msg = outgoing_messages[topic]
        await client.publish("%s/%s" % (PUBLISH_PREFIX, topic), msg, qos=1)
        print("[MQTT]: sent [%s] -> [%s]" % (topic, msg))
        del outgoing_messages[topic]


def register_on_message_received_callback(cb):
    global on_message_received_cb
    print("[MQTT]: register on message received cb")
    on_message_received_cb = cb


def init():
    print("[MQTT]: init")
    global SUBSCRIBE, PUBLISH_PREFIX
    lan.init()
    SUBSCRIBE = "%s/in/#" % (lan.mac)
    PUBLISH_PREFIX = "%s/out" % (lan.mac)
    MQTTClient.DEBUG = True
    global client
    client = MQTTClient(client_id=lan.mac, subs_cb=on_mqtt_message_received, connect_coro=conn_han, server=SERVER)


async def loop_async():
    print("[MQTT]: loop_async")
    print("[MQTT]: connect to LAN")
    while True:
        if lan.check_link() == True:
            break
        await asyncio.sleep(1)

    print("[MQTT]: connect to MQTT")
    await client.connect()

    print("[MQTT]: handle MQTT")
    while True:
        handle_incoming_messages()
        await handle_outgoing_messages()
        await asyncio.sleep(0)


def test():
    init()
    while True:
        loop()