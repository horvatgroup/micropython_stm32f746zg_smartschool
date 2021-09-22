from mqtt_as import MQTTClient
import uasyncio as asyncio
import lan

SERVER = '192.168.88.32'
client = None


def callback(topic, msg, retained):
    print((topic, msg, retained))


async def conn_han(client):
    await client.subscribe('foo_topic', 1)


async def main(client):
    await client.connect()
    n = 0
    while True:
        await asyncio.sleep(5)
        print('publish', n)
        # If WiFi is down the following will pause for the duration.
        await client.publish('result', '{}'.format(n), qos=1)
        n += 1


def init():
    global client
    lan.init()
    MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    client = MQTTClient(client_id=lan.mac, subs_cb=callback, connect_coro=conn_han, server=SERVER)


def run():
    asyncio.run(main(client))
