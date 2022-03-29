import uasyncio as asyncio
import buttons
import leds


class Light:
    def __init__(self, button, main_light, inverted_light, activity_light):
        self.button = button
        self.main_light = main_light
        self.inverted_light = inverted_light
        self.activity_light = activity_light
        self.state = None


lights = {
    "lights/1/1": Light("B4_SW1", "RELAY_11", "B4_LED1_GB", "B4_LED1_R"),
    "lights/1/2": Light("B4_SW2", "RELAY_12", "B4_LED2_GB", "B4_LED2_R"),
    "lights/2/1": Light("B3_SW1", "RELAY_6", "B3_LED1_GB", "B3_LED1_R")
}


def get_light_from_alias(alias):
    light = None
    for key in lights:
        if lights[key].button == alias:
            light = lights[key]
    return light


def on_button_state_change_callback(alias, data):
    light = get_light_from_alias(alias)
    if light is not None:
        if data:
            leds.set_state_by_name(light.activity_light, 0)
            leds.set_state_by_name(light.inverted_light, 1)
        else:
            leds.set_state_by_name(light.inverted_light, 0)
            set_lights(light, int(not (light.state)))


def on_data_received(thing):
    light = lights.get(thing.path)
    if light is not None:
        state = int(thing.data) if thing.data in ("0", "1") else None
        if state is not None:
            set_lights(light, state)


def set_lights(light, state):
    light.state = state
    leds.set_state_by_name(light.main_light, state)
    leds.set_state_by_name(light.activity_light, int(not (state)))


def init():
    buttons.register_on_state_change_callback(on_button_state_change_callback)
    for key in lights:
        set_lights(lights[key], 0)


async def action():
    while True:
        # check_blinds_timeouts()
        await asyncio.sleep(1)
