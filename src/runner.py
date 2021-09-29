import uasyncio as asyncio
import common
import buttons
import leds
import sensors
import mqtt
import cli


async def process_time_measure():
    print("[RUNNER]: start process_time_measure")
    timestamp = common.get_millis()
    bigest = 0
    while True:
        await asyncio.sleep(0)
        timeout = common.millis_passed(timestamp)
        if timeout >= 20:
            if timeout > bigest:
                bigest = timeout
            print("[RUNNER]: timeout warning %d ms with bigest %d" % (timeout, bigest))
        timestamp = common.get_millis()


def init():
    print("[RUNNER]: init")
    buttons.init()
    leds.init()
    sensors.init()
    mqtt.init()
    cli.init()


async def loop():
    print("[RUNNER]: start loop")
    while True:
        await asyncio.sleep(10)


def run():
    print("[RUNNER]: run")
    init()
    global client
    asyncio.create_task(buttons.loop_async())
    asyncio.create_task(leds.loop_async())
    asyncio.create_task(sensors.loop_async())
    asyncio.create_task(mqtt.loop_async())
    asyncio.create_task(cli.loop_async())
    asyncio.create_task(process_time_measure())
    asyncio.run(loop())