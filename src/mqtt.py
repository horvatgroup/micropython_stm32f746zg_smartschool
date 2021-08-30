import lan
from lib_umqtt_simple import MQTTClient
import common

MQTT_SERVER = "192.168.88.32"
MQTT_PORT = 1883
outgoing_messages = {}
incoming_messages = {}
outgoing_messages_confirmation = {}
mqtt_client = None
mqtt_connected = False
timestamp = 0


def on_mqtt_message_received(topic_encoded, msg_encoded):
    topic = topic_encoded.decode()
    if lan.mac in topic:
        topic = "/".join(topic.split("/")[1:])
    msg = msg_encoded.decode()
    if topic in outgoing_messages_confirmation and msg == outgoing_messages_confirmation[topic]:
        print("[MQTT]: received confirmation [%s] -> [%s]" % (topic, msg))
        del outgoing_messages_confirmation[topic]
    else:
        incoming_messages[topic] = msg


def send_message(topic, msg):
    outgoing_messages[topic] = msg


def init():
    print("[MQTT]: init")
    lan.init()
    global mqtt_client
    mqtt_client = MQTTClient(client_id=lan.mac, server=MQTT_SERVER, port=MQTT_PORT)
    mqtt_client.set_callback(on_mqtt_message_received)


def is_connection_ready():
    try:
        mqtt_client.ping()
        tsstart = common.get_millis()
        while True:
            if mqtt_client.check_msg() == 0xd0:
                return True
            if common.millis_passed(tsstart) >= 1000:
                return False
    except Exception as e:
        print("[MQTT]: ERROR cant ping %s" % (e))
        return False


def loop():
    global timestamp, mqtt_connected
    if timestamp != 0 and common.millis_passed(timestamp) < 1000:
        return
    else:
        timestamp = 0

    if mqtt_connected and is_connection_ready():
        mqtt_client.check_msg()
        for topic in incoming_messages.keys():
            msg = incoming_messages[topic]
            print("[MQTT]: received [%s] -> [%s]" % (topic, msg))
            del incoming_messages[topic]
        for topic in outgoing_messages.keys():
            msg = outgoing_messages[topic]
            try:
                mqtt_client.publish("%s/%s".encode() % (lan.mac, topic), msg.encode())
                print("[MQTT]: sent [%s] -> [%s]" % (topic, msg))
                outgoing_messages_confirmation[topic] = msg
                del outgoing_messages[topic]
            except Exception as e:
                print("[MQTT]: ERROR cant send [%s] -> [%s] with %s" % (topic, msg, e))
    else:
        mqtt_connected = False
        try:
            mqtt_client.disconnect()
        except Exception as e:
            print("[MQTT]: ERROR cant disconnect %s" % (e))
        if lan.check_connection():
            try:
                print("[MQTT]: connecting")
                mqtt_client.connect()
                print("[MQTT]: connected, subscribing")
                mqtt_client.subscribe("%s/#".encode() % (lan.mac))
                print("[MQTT]: subscribed")
                mqtt_connected = True
            except Exception as e:
                print("[MQTT]: ERROR cant connect %s" % (e))
        else:
            print("[MQTT]: WAITING for connection ready")
            timestamp = common.get_millis()


def test():
    init()
    while True:
        loop()
