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


async def run():
    print("[RUNNER]: start loop")
    tasks = []

    tasks.append(asyncio.create_task(common.loop_async("BUTTONS", buttons.action)))
    tasks.append(asyncio.create_task(common.loop_async("LEDS", leds.action)))
    tasks.append(asyncio.create_task(common.loop_async("SENSORS", sensors.action, timeout=11)))
    tasks.append(asyncio.create_task(mqtt.loop_async()))
    tasks.append(asyncio.create_task(common.loop_async("CLI", cli.action)))
    tasks.append(asyncio.create_task(process_time_measure()))
    for task in tasks:
        await task
        print("[RUNNER]: Error: loop task finished!")

def start():
    print("[RUNNER]: run")
    init()
    asyncio.run(run())