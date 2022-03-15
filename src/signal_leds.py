import uasyncio as asyncio
import leds
import mqtt


# boot_led = things.get_thing_from_hw("ONBOARD_LED1")
# mqtt_led = things.get_thing_from_hw("ONBOARD_LED3")


def check_signal_led_boot():
    # things.set_state(boot_led, 1)
    pass


def check_signal_led_mqtt(state):
    # things.set_state(mqtt_led, int(state))
    pass


async def action():
    while True:
        check_signal_led_boot()
        check_signal_led_mqtt(mqtt.is_connected())
        await asyncio.sleep(1)
