import uasyncio as asyncio
import common
import buttons
import leds
import sensors
import mqtt
import cli
import sync_data
import signal_leds
import lighting
import power_counter


async def process_time_measure(timeout=20):
    print("[RUNNER]: start process_time_measure")
    timestamp = common.get_millis()
    bigest = 0
    while True:
        await asyncio.sleep(0)
        timepassed = common.millis_passed(timestamp)
        if timepassed >= timeout:
            if timepassed > bigest:
                bigest = timepassed
            print("[RUNNER]: timeout warning %d ms with bigest %d" % (timepassed, bigest))
        timestamp = common.get_millis()


def init():
    print("[RUNNER]: init")
    buttons.init()
    leds.init()
    sensors.init()
    power_counter.init()
    mqtt.init()
    cli.init()
    sync_data.init()


async def add_tasks():
    print("[RUNNER]: add_tasks")
    tasks = []
    tasks.append(asyncio.create_task(sync_data.loop_async()))
    tasks.append(asyncio.create_task(common.loop_async("BUTTONS", buttons.action)))
    tasks.append(asyncio.create_task(common.loop_async("LEDS", leds.action)))
    tasks.append(asyncio.create_task(sensors.realtime_sensors_action()))
    tasks.append(asyncio.create_task(sensors.environment_sensors_action()))
    tasks.append(asyncio.create_task(common.loop_async("POWER_COUNTER", power_counter.action)))
    tasks.append(asyncio.create_task(mqtt.loop_async()))
    tasks.append(asyncio.create_task(common.loop_async("CLI", cli.action)))
    tasks.append(asyncio.create_task(signal_leds.action()))
    tasks.append(asyncio.create_task(lighting.action()))
    tasks.append(asyncio.create_task(process_time_measure()))
    for task in tasks:
        await task
    print("[RUNNER]: Error: loop task finished!")


def start():
    print("[RUNNER]: start")
    init()
    asyncio.run(add_tasks())
