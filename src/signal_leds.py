import uasyncio as asyncio
import leds
import mqtt

BOOT_LED = "ONBOARD_LED1"
MQTT_LED = "ONBOARD_LED3"
signal_led_boot_state = None
signal_led_mqtt_state = None


def check_signal_led_boot():
    global signal_led_boot_state
    if signal_led_boot_state == None:
        signal_led_boot_state = True
        leds.set_state_by_name(BOOT_LED, 1)


def check_signal_led_mqtt(state):
    global signal_led_mqtt_state
    if signal_led_mqtt_state != state:
        signal_led_mqtt_state = state
        if state:
            leds.set_state_by_name(MQTT_LED, 1)
        else:
            leds.set_state_by_name(MQTT_LED, 0)


async def action():
    check_signal_led_boot()
    check_signal_led_mqtt(mqtt.is_connected())
    await asyncio.sleep(1)
