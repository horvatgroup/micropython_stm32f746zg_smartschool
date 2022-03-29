import uasyncio as asyncio
import common
import buttons
import leds


class Light:
    def __init__(self, alias, button, main_light, inverted_light, activity_light):
        self.alias = alias
        self.button = button
        self.main_light = main_light
        self.inverted_light = inverted_light
        self.activity_light = activity_light
        self.state = None


class Rollo:
    def __init__(self, alias, relay_up, relay_down, button_up, button_down, idle_light_up, idle_light_down, pressed_light_up, pressed_light_down):
        self.alias = alias
        self.relay_up = relay_up
        self.relay_down = relay_down
        self.button_up = button_up
        self.button_down = button_down
        self.idle_light_up = idle_light_up
        self.idle_light_down = idle_light_down
        self.pressed_light_up = pressed_light_up
        self.pressed_light_down = pressed_light_down
        self.active_up = False
        self.active_down = False
        self.timestamp = None
        self.timeout = 10000
        self.percent = None
        self.requested_percent = None


class Co2Alarm:
    def __init__(self, alias, light1, light2):
        self.alias = alias
        self.light1 = light1
        self.light2 = light2
        self.active = False


lights = {
    "lights/1/1": Light("lights/1/1", "B4_SW1", "RELAY_11", "B4_LED1_GB", "B4_LED1_R"),
    "lights/1/2": Light("lights/1/2", "B4_SW2", "RELAY_12", "B4_LED2_GB", "B4_LED2_R"),
    "lights/2/1": Light("lights/2/1", "B3_SW1", "RELAY_6", "B3_LED1_GB", "B3_LED1_R")
}

rollos = {
    "rollo/1": Rollo("rollo/1", "RELAY_4", "RELAY_3", "B2_SW1", "B2_SW2", "B2_LED1_GB", "B2_LED2_GB", "B2_LED1_R", "B2_LED2_R"),
    "rollo/2": Rollo("rollo/2", "RELAY_2", "RELAY_1", "B1_SW1", "B1_SW2", "B1_LED1_GB", "B1_LED2_GB", "B1_LED1_R", "B1_LED2_R")
}

co2alarm = {
    "co2_alarm/1": Co2Alarm("co2_alarm/1", "B2_LED1_R", "B2_LED2_R"),
    "co2_alarm/2": Co2Alarm("co2_alarm/2", "B1_LED1_R", "B1_LED2_R")
}


def get_light_from_alias(alias):
    light = None
    for key in lights:
        if lights[key].button == alias:
            light = lights[key]
    return light


def get_rollo_from_alias(alias) -> Rollo:
    rollo = None
    for key in rollos:
        if alias == rollos[key].button_up or alias == rollos[key].button_down:
            rollo = rollos[key]
    return rollo


def on_button_state_change_callback(alias, data):
    light = get_light_from_alias(alias)
    if light is not None:
        if data:
            leds.set_state_by_name(light.activity_light, 0)
            leds.set_state_by_name(light.inverted_light, 1)
        else:
            leds.set_state_by_name(light.inverted_light, 0)
            set_lights(light, int(not (light.state)))
    rollo = get_rollo_from_alias(alias)
    if rollo is not None:
        if rollo.button_up == alias:
            if data:
                leds.set_state_by_name(rollo.idle_light_up, 0)
                leds.set_state_by_name(rollo.pressed_light_up, 1)
            else:
                if rollo.active_up or rollo.active_down:
                    set_rollos(rollo, "STOP")
                else:
                    set_rollos(rollo, "UP")
        elif rollo.button_down == alias:
            if data:
                leds.set_state_by_name(rollo.idle_light_down, 0)
                leds.set_state_by_name(rollo.pressed_light_down, 1)
            else:
                if rollo.active_up or rollo.active_down:
                    set_rollos(rollo, "STOP")
                else:
                    set_rollos(rollo, "DOWN")


def on_data_received(thing):
    light = lights.get(thing.path)
    if light is not None:
        state = int(thing.data) if thing.data in ("0", "1") else None
        if state is not None:
            set_lights(light, state)
    rollo = rollos.get(thing.path)
    if rollo is not None:
        set_rollos(rollo, thing.data)


def set_lights(light, state):
    print("[PHY]: set_lights[%s], data[%s]" % (light.alias, state))
    light.state = state
    leds.set_state_by_name(light.main_light, state)
    leds.set_state_by_name(light.activity_light, int(not (state)))


def set_rollos(rollo, data):
    print("[PHY]: set_rollos[%s], data[%s]" % (rollo.alias, data))
    if data in (100, "100", "UP"):
        leds.set_state_by_name(rollo.pressed_light_up, 0)
        leds.set_state_by_name(rollo.idle_light_up, 1)
        if rollo.active_down:
            leds.set_state_by_name(rollo.relay_down, 0)
            rollo.active_down = False
        leds.set_state_by_name(rollo.relay_up, 1)
        rollo.active_up = True
        rollo.timestamp = common.get_millis()
    elif data in (0, "0", "DOWN"):
        leds.set_state_by_name(rollo.pressed_light_down, 0)
        leds.set_state_by_name(rollo.idle_light_down, 1)
        if rollo.active_up:
            leds.set_state_by_name(rollo.relay_up, 0)
            rollo.active_up = False
        leds.set_state_by_name(rollo.relay_down, 1)
        rollo.active_down = True
        rollo.timestamp = common.get_millis()
    elif data == "STOP":
        leds.set_state_by_name(rollo.pressed_light_up, 0)
        leds.set_state_by_name(rollo.idle_light_up, 1)
        leds.set_state_by_name(rollo.pressed_light_down, 0)
        leds.set_state_by_name(rollo.idle_light_down, 1)
        leds.set_state_by_name(rollo.relay_up, 0)
        rollo.active_up = False
        leds.set_state_by_name(rollo.relay_down, 0)
        rollo.active_down = False
        rollo.timestamp = None
    else:
        try:
            percent = int(data)
        except Exception as e:
            print("[PHY]: ERROR with %s" % (e))


def check_rollos_timeout():
    for key in rollos:
        rollo = rollos[key]
        if rollo.active_up or rollo.active_down:
            if common.millis_passed(rollo.timestamp) >= rollo.timeout:
                set_rollos(rollo, "STOP")


def init():
    print("[PHY]: init")
    buttons.register_on_state_change_callback(on_button_state_change_callback)
    for key in lights:
        set_lights(lights[key], 0)
    for key in rollos:
        set_rollos(rollos[key], "STOP")


async def action():
    while True:
        check_rollos_timeout()
        await asyncio.sleep(1)
