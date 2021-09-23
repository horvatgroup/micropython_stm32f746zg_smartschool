import uasyncio as asyncio

import common
import buttons
import leds
import sensors
import lan
from mqtt_as import MQTTClient
import cli

SERVER = '192.168.88.42'
client = None


def callback(topic, msg, retained):
    print((topic, msg, retained))


async def conn_han(client):
    await client.subscribe('foo_topic', 1)


async def process_time_measure():
    print("[RUNNERAS]: start_task process_time_measure")
    timestamp = common.get_millis()
    bigest = 0
    while True:
        await asyncio.sleep(0)
        timeout = common.millis_passed(timestamp)
        if timeout >= 3:
            if timeout > bigest:
                bigest = timeout
            print("[RUNNERAS]: timeout warning %d ms with bigest %d" % (timeout, bigest))
        timestamp = common.get_millis()


async def mqtt_handler(client):
    print("[RUNNERAS]: start_task mqtt_handler")
    # connect to lan
    print("[RUNNERAS]: connect to LAN")
    while True:
        if lan.check_link() == True:
            break
        await asyncio.sleep(1)
    # connect to mqtt
    print("[RUNNERAS]: connect to MQTT")
    await client.connect()

    # handle MQTT
    print("[RUNNERAS]: handle to MQTT")
    n = 0
    while True:
        await asyncio.sleep(5)
        print('[RUNNERAS]: publish', n)
        # If WiFi is down the following will pause for the duration.
        await client.publish('result', '{}'.format(n), qos=1)
        n += 1


def init():
    print("[RUNNERAS]: init")
    buttons.init()
    leds.init()
    #sensors.init()
    lan.init()
    MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    global client
    client = MQTTClient(client_id=lan.mac, subs_cb=callback, connect_coro=conn_han, server=SERVER)
    cli.init()


async def buttons_handler():
    print("[RUNNERAS]: start_task buttons_handler")
    while True:
        buttons.loop()
        await asyncio.sleep(0)


async def leds_handler():
    print("[RUNNERAS]: start_task leds_handler")
    while True:
        leds.loop()
        await asyncio.sleep(0)


async def sensors_handler():
    print("[RUNNERAS]: start_task sensors_handler")
    while True:
        sensors.loop()
        await asyncio.sleep(0)


async def cli_handler():
    print("[RUNNERAS]: start_task cli_handler")
    while True:
        cli.loop()
        await asyncio.sleep(0)


async def main():
    print("[RUNNERAS]: start_task main")
    while True:
        await asyncio.sleep(10)


def run():
    global client
    print("[RUNNERAS]: run")
    asyncio.create_task(buttons_handler())
    asyncio.create_task(leds_handler())
    #asyncio.create_task(sensors_handler())
    asyncio.create_task(mqtt_handler(client))
    asyncio.create_task(cli_handler())
    asyncio.create_task(process_time_measure())
    asyncio.run(main())


def test():
    init()
    run()
