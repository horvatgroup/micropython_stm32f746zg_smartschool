import uasyncio as asyncio
import lan
from lib_mqtt_as import MQTTClient
import events, eventor

remote_path = {
    # buttons out
    events.ONBOARD_BUTTON: "out/test/button1",
    events.B1_SW1: "out/B4/SW1",
    events.B1_SW2: "out/B4/SW2",
    events.B2_SW1: "out/B3/SW1",
    events.B2_SW2: "out/B3/SW2",
    events.B3_SW1: "out/B2/SW1",
    events.B3_SW2: "out/B2/SW2",
    events.B4_SW1: "out/B1/SW1",
    events.B4_SW2: "out/B1/SW2",
    # sensors out
    events.S1_RADAR: "out/S2/radar",
    events.S1_ENV_TEMPERATURE: "out/S2/env_temperature",
    events.S1_ENV_PRESSURE: "out/S2/env_pressure",
    events.S1_ENV_GAS: "out/S2/env_gas",
    events.S1_ENV_ALTITUDE: "out/S2/env_altitude",
    events.S1_ENV_HUMIDITY: "out/S2/env_humidity",
    events.S1_LIGHT: "out/S2/light",
    events.S1_CO2: "out/S1/co2",
    events.S2_RADAR: "out/S1/radar",
    events.S2_ENV_TEMPERATURE: "out/S1/env_temperature",
    events.S2_ENV_PRESSURE: "out/S1/env_pressure",
    events.S2_ENV_GAS: "out/S1/env_gas",
    events.S2_ENV_ALTITUDE: "out/S1/env_altitude",
    events.S2_ENV_HUMIDITY: "out/S1/env_humidity",
    events.S2_LIGHT: "out/S1/light",
    events.S2_CO2: "out/S2/co2",
    # leds and relays in
    events.ONBOARD_LED1: "in/test/led1",
    events.ONBOARD_LED2: "in/test/led2",
    events.ONBOARD_LED3: "in/test/led3",
    events.R_RELAY_1: "in/R/relay8",
    events.R_RELAY_2: "in/R/relay7",
    events.R_RELAY_3: "in/R/relay6",
    events.R_RELAY_4: "in/R/relay5",
    events.R_RELAY_5: "in/R/relay4",
    events.R_RELAY_6: "in/R/relay3",
    events.R_RELAY_7: "in/R/relay2",
    events.R_RELAY_8: "in/R/relay1",
    events.R_RELAY_9: "in/R/relay9",
    events.R_RELAY_10: "in/R/relay10",
    events.R_RELAY_11: "in/R/relay11",
    events.R_RELAY_12: "in/R/relay12",
    events.B1_LED1_GB: "in/B4/SW1/GB",
    events.B1_LED1_R: "in/B4/SW1/R",
    events.B1_LED2_GB: "in/B4/SW2/GB",
    events.B1_LED2_R: "in/B4/SW2/R",
    events.B2_LED1_GB: "in/B3/SW1/GB",
    events.B2_LED1_R: "in/B3/SW1/R",
    events.B2_LED2_GB: "in/B3/SW2/GB",
    events.B2_LED2_R: "in/B3/SW2/R",
    events.B3_LED1_GB: "in/B2/SW1/GB",
    events.B3_LED1_R: "in/B2/SW1/R",
    events.B3_LED2_GB: "in/B2/SW2/GB",
    events.B3_LED2_R: "in/B2/SW2/R",
    events.B4_LED1_GB: "in/B1/SW1/GB",
    events.B4_LED1_R: "in/B1/SW1/R",
    events.B4_LED2_GB: "in/B1/SW2/GB",
    events.B4_LED2_R: "in/B1/SW2/R",
    # relays confirmation out
    events.R_RELAY_1_OUT: "out/R/relay8",
    events.R_RELAY_2_OUT: "out/R/relay7",
    events.R_RELAY_3_OUT: "out/R/relay6",
    events.R_RELAY_4_OUT: "out/R/relay5",
    events.R_RELAY_5_OUT: "out/R/relay4",
    events.R_RELAY_6_OUT: "out/R/relay3",
    events.R_RELAY_7_OUT: "out/R/relay2",
    events.R_RELAY_8_OUT: "out/R/relay1",
    events.R_RELAY_9_OUT: "out/R/relay9",
    events.R_RELAY_10_OUT: "out/R/relay10",
    events.R_RELAY_11_OUT: "out/R/relay11",
    events.R_RELAY_12_OUT: "out/R/relay12",
}


def get_key(val):
    for key, value in remote_path.items():
        if val == value:
            return key
    return None

DEFAULT_SERVER = '192.168.88.42'
MQTT_IP_FILENAME = "mqtt_ip.txt"
SUBSCRIBE = None
PUBLISH_PREFIX = None
client = None
outgoing_messages = {}
incoming_messages = {}
on_message_received_cb = None

EVENTOR_SUB_NAME = "mqtt"
def get_eventor_name(event):
    return EVENTOR_SUB_NAME + "_" + str(event)

async def conn_han(client):
    await client.subscribe(SUBSCRIBE, 1)


def on_mqtt_message_received(topic, msg, retained):
    topic = topic.decode()
    msg = msg.decode()
    if lan.mac in topic:
        topic = "/".join(topic.split("/")[1:])
    incoming_messages[topic] = msg


def send_message(topic, msg):
    outgoing_messages[topic] = msg


async def handle_incoming_messages():
    for topic in incoming_messages.keys():
        msg = incoming_messages[topic]
        print("[MQTT]: received [%s] -> [%s]" % (topic, msg))
        if on_message_received_cb != None:
            on_message_received_cb(topic, msg)
        del incoming_messages[topic]
        await asyncio.sleep(0)


async def handle_outgoing_messages():
    for topic in outgoing_messages.keys():
        msg = outgoing_messages[topic]
        topic_out = "%s/%s" % (PUBLISH_PREFIX, topic)
        await client.publish(topic_out, msg, qos=1)
        print(topic_out)
        print("[MQTT]: sent [%s] -> [%s]" % (topic, msg))
        del outgoing_messages[topic]
        event = get_key(topic)
        eventor.confirm(get_eventor_name(event), event, msg)
        await asyncio.sleep(0)


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


def on_eventor_event(event, data):
    topic = remote_path[event]
    send_message(topic, str(data))

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

    eventor.subscribe(get_eventor_name(events.B3_SW1), events.B3_SW1, on_eventor_event)
    eventor.subscribe(get_eventor_name(events.B3_SW2), events.B3_SW2, on_eventor_event)



async def loop_async():
    print("[MQTT]: start loop_async")
    print("[MQTT]: connect to LAN")
    while True:
        if lan.check_link() == True:
            break
        await asyncio.sleep(1)

    print("[MQTT]: connect to MQTT")
    await client.connect()

    print("[MQTT]: handle MQTT")
    while True:
        await handle_incoming_messages()
        await handle_outgoing_messages()
        await asyncio.sleep(0)


def test_async():
    print("[MQTT]: test_async")
    init()
    asyncio.run(loop_async())
