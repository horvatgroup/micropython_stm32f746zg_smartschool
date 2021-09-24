import uasyncio as asyncio
import common
import buttons
import leds
import sensors
import mqtt
import cli


async def process_time_measure():
    print("[RUNNER]: process_time_measure")
    timestamp = common.get_millis()
    bigest = 0
    while True:
        await asyncio.sleep(0)
        timeout = common.millis_passed(timestamp)
        if timeout >= 3:
            if timeout > bigest:
                bigest = timeout
            print("[RUNNER]: timeout warning %d ms with bigest %d" % (timeout, bigest))
        timestamp = common.get_millis()


def init():
    print("[RUNNER]: init")
    buttons.init()
    leds.init()
    sensors.init()
    print("TUSAM 1")
    mqtt.init()
    print("TUSAM 2")
    cli.init()
    print("TUSAM 3")


async def main():
    print("[RUNNER]: main")
    while True:
        await asyncio.sleep(10)


def run():
    global client
    print("[RUNNER]: run")
    asyncio.create_task(buttons.loop_async())
    asyncio.create_task(leds.loop_async())
    asyncio.create_task(sensors.loop_async())
    asyncio.create_task(mqtt.loop_async())
    asyncio.create_task(cli.loop_async())
    asyncio.create_task(process_time_measure())
    asyncio.run(main())


def test():
    init()
    run()
