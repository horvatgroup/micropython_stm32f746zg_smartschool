import uasyncio as asyncio
import buttons
import mqtt
import sensors
import leds


class Device:
    def __init__(self, hw, in_path=None, out_path=None):
        self.hw = hw
        self.in_path = in_path
        self.out_path = out_path
        self.out_remote_state = None
        self.in_remote_state = None
        self.state = None


devices = (
    # inputs
    Device("ONBOARD_BUTTON", out_path="out/test/button1"),
    Device("B1_SW1", out_path="out/B4/SW1"),
    Device("B1_SW2", out_path="out/B4/SW2"),
    Device("B2_SW1", out_path="out/B3/SW1"),
    Device("B2_SW2", out_path="out/B3/SW2"),
    Device("B3_SW1", out_path="out/B2/SW1"),
    Device("B3_SW2", out_path="out/B2/SW2"),
    Device("B4_SW1", out_path="out/B1/SW1"),
    Device("B4_SW2", out_path="out/B1/SW2"),
    # sensors
    Device("S1_RADAR", out_path="out/S2/radar"),
    Device("S1_TEMPERATURE", out_path="out/S2/temperature"),
    Device("S1_PRESSURE", out_path="out/S2/pressure"),
    Device("S1_GAS", out_path="out/S2/gas"),
    Device("S1_ALTITUDE", out_path="out/S2/altitude"),
    Device("S1_HUMIDITY", out_path="out/S2/humidity"),
    Device("S1_LIGHT", out_path="out/S2/light"),
    Device("S1_CO2", out_path="out/S1/co2"),
    Device("S2_RADAR", out_path="out/S1/radar"),
    Device("S2_TEMPERATURE", out_path="out/S1/temperature"),
    Device("S2_PRESSURE", out_path="out/S1/pressure"),
    Device("S2_GAS", out_path="out/S1/gas"),
    Device("S2_ALTITUDE", out_path="out/S1/altitude"),
    Device("S2_HUMIDITY", out_path="out/S1/humidity"),
    Device("S2_LIGHT", out_path="out/S1/light"),
    Device("S2_CO2", out_path="out/S2/co2"),
    # outputs
    Device("ONBOARD_LED1", in_path="in/test/led1", out_path="out/test/led1"),
    Device("ONBOARD_LED2", in_path="in/test/led2", out_path="out/test/led2"),
    Device("ONBOARD_LED3", in_path="in/test/led3", out_path="out/test/led3"),
    Device("RELAY_1", in_path="in/R/relay8", out_path="out/R/relay8"),
    Device("RELAY_2", in_path="in/R/relay7", out_path="out/R/relay7"),
    Device("RELAY_3", in_path="in/R/relay6", out_path="out/R/relay6"),
    Device("RELAY_4", in_path="in/R/relay5", out_path="out/R/relay5"),
    Device("RELAY_5", in_path="in/R/relay4", out_path="out/R/relay4"),
    Device("RELAY_6", in_path="in/R/relay3", out_path="out/R/relay3"),
    Device("RELAY_7", in_path="in/R/relay2", out_path="out/R/relay2"),
    Device("RELAY_8", in_path="in/R/relay1", out_path="out/R/relay1"),
    Device("RELAY_9", in_path="in/R/relay9", out_path="out/R/relay9"),
    Device("RELAY_10", in_path="in/R/relay10", out_path="out/R/relay10"),
    Device("RELAY_11", in_path="in/R/relay11", out_path="out/R/relay11"),
    Device("RELAY_12", in_path="in/R/relay12", out_path="out/R/relay12"),
    Device("B1_LED1_GB", in_path="in/B4/SW1/GB", out_path="out/B4/SW1/GB"),
    Device("B1_LED1_R", in_path="in/B4/SW1/R", out_path="out/B4/SW1/R"),
    Device("B1_LED2_GB", in_path="in/B4/SW2/GB", out_path="out/B4/SW2/GB"),
    Device("B1_LED2_R", in_path="in/B4/SW2/R", out_path="out/B4/SW2/R"),
    Device("B2_LED1_GB", in_path="in/B3/SW1/GB", out_path="out/B3/SW1/GB"),
    Device("B2_LED1_R", in_path="in/B3/SW1/R", out_path="out/B3/SW1/R"),
    Device("B2_LED2_GB", in_path="in/B3/SW2/GB", out_path="out/B3/SW2/GB"),
    Device("B2_LED2_R", in_path="in/B3/SW2/R", out_path="out/B3/SW2/R"),
    Device("B3_LED1_GB", in_path="in/B2/SW1/GB", out_path="out/B2/SW1/GB"),
    Device("B3_LED1_R", in_path="in/B2/SW1/R", out_path="out/B2/SW1/R"),
    Device("B3_LED2_GB", in_path="in/B2/SW2/GB", out_path="out/B2/SW2/GB"),
    Device("B3_LED2_R", in_path="in/B2/SW2/R", out_path="out/B2/SW2/R"),
    Device("B4_LED1_GB", in_path="in/B1/SW1/GB", out_path="out/B1/SW1/GB"),
    Device("B4_LED1_R", in_path="in/B1/SW1/R", out_path="out/B1/SW1/R"),
    Device("B4_LED2_GB", in_path="in/B1/SW2/GB", out_path="out/B1/SW2/GB"),
    Device("B4_LED2_R", in_path="in/B1/SW2/R", out_path="out/B1/SW2/R"),
)


def activity_light_logic(hw, state):
    #print("activity_light_logic", hw, state)
    led = get_device_from_hw(hw)
    optimised_led_change(led, state)


def toggle_light_logic(hw, first_time=False):
    #print("toggle_light_logic", hw, first_time)
    device = get_device_from_hw(hw)
    if first_time:
        fliped_state = 0
    else:
        fliped_state = not device.state
    optimised_led_change(device, fliped_state)


def check_button_logic(hw, state, first_time=False):
    #print("check_button_logic", hw, state, first_time)
    device = get_device_from_hw(hw)
    if device.hw == "B4_SW1":
        activity_light_logic("B4_LED1_R", state)
        if not state:
            toggle_light_logic("RELAY_8", first_time)
        flip_light_logic("RELAY_8", "B4_LED1_R")
    elif device.hw == "B4_SW2":
        activity_light_logic("B4_LED2_R", state)
        if not state:
            toggle_light_logic("ONBOARD_LED2", first_time)
        flip_light_logic("ONBOARD_LED2", "B4_LED2_R")


def flip_light_logic(hw, inative_hw = None):
    #print("flip_light_logic", hw, inative_hw)
    if hw == "RELAY_8":
        linked_light = get_device_from_hw("RELAY_8")
        switch_light = get_device_from_hw("B4_LED1_GB")
        inactive = get_device_from_hw(inative_hw)
        if inactive and inactive.state:
            optimised_led_change(switch_light, 0)
        else:
            optimised_led_change(switch_light, int(not linked_light.state))

    elif hw == "ONBOARD_LED2":
        linked_light = get_device_from_hw("ONBOARD_LED2")
        switch_light = get_device_from_hw("B4_LED2_GB")
        optimised_led_change(switch_light, not linked_light.state)
        inactive = get_device_from_hw(inative_hw)
        if inactive and inactive.state:
            optimised_led_change(switch_light, 0)
        else:
            optimised_led_change(switch_light, int(not linked_light.state))

def optimised_led_change(device, state):
    #print("optimised_led_change", device.hw, state)
    device.in_remote_state = state
    device.state = state
    device.state = device.state
    leds.set_state_by_name(device.hw, state)


def on_button_state_change_callback(hw, state):
    #print("on_button_state_change_callback", hw, state)
    device = get_device_from_hw(hw)
    first_time = device.state == None
    if device:
        device.state = state
    check_button_logic(hw, state, first_time)


def on_sensor_state_change_callback(hw, state):
    device = get_device_from_hw(hw)
    if device:
        device.state = state


def on_mqtt_message_received_callback(path, state):
    device = get_device_from_path(path)
    try:
        device.in_remote_state = int(state)
    except Exception as e:
        print("[SYNC]: ERROR probably not implemented with %s" % (e))


def get_device_from_hw(hw):
    for device in devices:
        if device.hw == hw:
            return device
    return None


def get_device_from_path(path):
    for device in devices:
        if device.in_path == path or device.out_path == path:
            return device
    return None


def set_boot_led():
    leds.set_state_by_name("ONBOARD_LED1", 1)


mqtt_led_state = None


def set_mqtt_led(state):
    global mqtt_led_state
    if mqtt_led_state != state:
        mqtt_led_state = state
        if state:
            leds.set_state_by_name("ONBOARD_LED3", 1)
        else:
            leds.set_state_by_name("ONBOARD_LED3", 0)


def info_leds_logic():
    set_mqtt_led(mqtt.is_connected())


def buttons_lights_logic():
    pass


def init():
    print("[SYNC]: init")
    buttons.register_on_state_change_callback(on_button_state_change_callback)
    sensors.register_on_state_change_callback(on_sensor_state_change_callback)
    mqtt.register_on_message_received_callback(on_mqtt_message_received_callback)


async def loop_async():
    print("[SYNC]: loop async")
    set_boot_led()
    while True:
        info_leds_logic()
        await asyncio.sleep(0)
        buttons_lights_logic()
        await asyncio.sleep(0)
        for device in devices:
            if device.out_path and mqtt.is_connected():
                if device.state != device.out_remote_state and device.state != None:
                    device.out_remote_state = device.state
                    await mqtt.send_message(device.out_path, str(device.out_remote_state))
            await asyncio.sleep(0)
            if device.in_path:
                if device.in_remote_state != device.state and device.in_remote_state != None:
                    device.state = device.in_remote_state
                    leds.set_state_by_name(device.hw, device.in_remote_state)
                    if device.out_path:
                        device.state = device.state
                    flip_light_logic(device.hw)
            await asyncio.sleep(0)
