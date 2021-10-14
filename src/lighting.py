import uasyncio as asyncio
import things
import common


class Button:
    def __init__(self, thing_button):
        self.thing_button = thing_button
        self.was_pressed = thing_button.state


buttons = [
    Button(things.get_thing_from_hw("B1_SW1")),
    Button(things.get_thing_from_hw("B1_SW2")),
    Button(things.get_thing_from_hw("B2_SW1")),
    Button(things.get_thing_from_hw("B2_SW2")),
    Button(things.get_thing_from_hw("B3_SW1")),
    Button(things.get_thing_from_hw("B3_SW2")),
    Button(things.get_thing_from_hw("B4_SW1")),
    Button(things.get_thing_from_hw("B4_SW2")),
]


def check_button_logic():
    for button in buttons:
        if button.thing_button.state:
            if not button.was_pressed:
                button.was_pressed = True
                on_button_pressed(button)
        elif not button.thing_button.state:
            if button.was_pressed:
                button.was_pressed = False
                on_button_released(button)


def on_button_pressed(button):
    for sl_pair in lightings:
        if sl_pair.thing_button == button.thing_button:
            things.set_state(sl_pair.thing_inverted_light, 0)
            things.set_state(sl_pair.thing_activity_light, 1)
            break
    for bl_group in blinds_pairs:
        for bl_pair in bl_group:
            if bl_pair.enable_button == button.thing_button:
                things.set_state(bl_pair.idle_light, 0)
                things.set_state(bl_pair.pressed_light, 1)


def on_button_released(button):
    for sl_pair in lightings:
        if sl_pair.thing_button == button.thing_button:
            things.set_state(sl_pair.thing_activity_light, 0)
            next_state = int(not sl_pair.thing_main_light.state)
            things.set_state(sl_pair.thing_main_light, next_state)
            check_inverted_light(sl_pair)
            break
    for bl_group in blinds_pairs:
        for bl_pair in bl_group:
            if bl_pair.enable_button == button.thing_button:
                things.set_state(bl_pair.idle_light, 1)
                things.set_state(bl_pair.pressed_light, 0)
        button_action = False
        for bl_pair in bl_group:
            if not button_action and button.thing_button in bl_pair.disable_buttons and bl_pair.relay.state:
                things.set_state(bl_pair.relay, 0)
                bl_pair.timestamp = 0
                button_action = True
        if not button_action:
            for bl_pair in bl_group:
                if not button_action and button.thing_button == bl_pair.enable_button and not bl_pair.relay.state:
                    things.set_state(bl_pair.relay, 1)
                    bl_pair.timestamp = common.get_millis()
                    button_action = True



def check_init_lights():
    check_inverted_lights()
    for bl_group in blinds_pairs:
        for bl_pair in bl_group:
            things.set_state(bl_pair.idle_light, 1)
            things.set_state(bl_pair.pressed_light, 0)


def check_inverted_light(sl_pair):
    if not sl_pair.thing_button.state:
        inverted_next_state = int(not sl_pair.thing_main_light.state)
        things.set_state(sl_pair.thing_inverted_light, inverted_next_state)


def check_inverted_lights():
    for sl_pair in lightings:
        check_inverted_light(sl_pair)


class Lighting:
    def __init__(self, thing_button, thing_main_light, thing_inverted_light, thing_activity_light):
        self.thing_button = thing_button
        self.thing_main_light = thing_main_light
        self.thing_inverted_light = thing_inverted_light
        self.thing_activity_light = thing_activity_light


lightings = [
    Lighting(thing_button=things.get_thing_from_hw("B4_SW1"),
             thing_main_light=things.get_thing_from_hw("RELAY_8"),
             thing_inverted_light=things.get_thing_from_hw("B4_LED1_GB"),
             thing_activity_light=things.get_thing_from_hw("B4_LED1_R")),
    Lighting(thing_button=things.get_thing_from_hw("B4_SW2"),
             thing_main_light=things.get_thing_from_hw("RELAY_7"),
             thing_inverted_light=things.get_thing_from_hw("B4_LED2_GB"),
             thing_activity_light=things.get_thing_from_hw("B4_LED2_R")),
    Lighting(thing_button=things.get_thing_from_hw("B3_SW1"),
             thing_main_light=things.get_thing_from_hw("RELAY_6"),
             thing_inverted_light=things.get_thing_from_hw("B3_LED1_GB"),
             thing_activity_light=things.get_thing_from_hw("B3_LED1_R")),
    #Lighting(thing_button=things.get_thing_from_hw("B3_SW2"),
    #         thing_main_light=things.get_thing_from_hw("RELAY_5"),
    #         thing_inverted_light=things.get_thing_from_hw("B3_LED2_GB"),
    #         thing_activity_light=things.get_thing_from_hw("B3_LED2_R")),
]


class RelayControl:
    def __init__(self, relay, idle_light, pressed_light, enable_button, disable_buttons, enabled_timeout=5000):
        self.relay = relay
        self.idle_light = idle_light
        self.pressed_light = pressed_light
        self.enable_button = enable_button
        self.disable_buttons = disable_buttons
        self.enabled_timeout = enabled_timeout
        self.timestamp = 0


blinds_pairs = [
    [
        RelayControl(relay=things.get_thing_from_hw("RELAY_4"),
                     idle_light=things.get_thing_from_hw("B2_LED1_GB"),
                     pressed_light=things.get_thing_from_hw("B2_LED1_R"),
                     enable_button=things.get_thing_from_hw("B2_SW1"),
                     disable_buttons=[
                         things.get_thing_from_hw("B2_SW1"),
                         things.get_thing_from_hw("B2_SW2")
                     ]),
        RelayControl(relay=things.get_thing_from_hw("RELAY_3"),
                     idle_light=things.get_thing_from_hw("B2_LED2_GB"),
                     pressed_light=things.get_thing_from_hw("B2_LED2_R"),
                     enable_button=things.get_thing_from_hw("B2_SW2"),
                     disable_buttons=[
                         things.get_thing_from_hw("B2_SW1"),
                         things.get_thing_from_hw("B2_SW2")
                     ])
    ],
    [
        RelayControl(relay=things.get_thing_from_hw("RELAY_2"),
                     idle_light=things.get_thing_from_hw("B1_LED1_GB"),
                     pressed_light=things.get_thing_from_hw("B1_LED1_R"),
                     enable_button=things.get_thing_from_hw("B1_SW1"),
                     disable_buttons=[
                         things.get_thing_from_hw("B1_SW1"),
                         things.get_thing_from_hw("B1_SW2")
                     ]),
        RelayControl(relay=things.get_thing_from_hw("RELAY_1"),
                     idle_light=things.get_thing_from_hw("B1_LED2_GB"),
                     pressed_light=things.get_thing_from_hw("B1_LED2_R"),
                     enable_button=things.get_thing_from_hw("B1_SW2"),
                     disable_buttons=[
                         things.get_thing_from_hw("B1_SW1"),
                         things.get_thing_from_hw("B1_SW2")
                     ])
    ]
]


def check_blinds_timeouts():
    for bl_group in blinds_pairs:
        for bl_pair in bl_group:
            if bl_pair.relay.state and common.millis_passed(bl_pair.timestamp) >= bl_pair.enabled_timeout:
                things.set_state(bl_pair.relay, 0)
                bl_pair.timestamp = 0


def handle_external_blinds_control(thing):
    for bl_group in blinds_pairs:
        for bl_pair in bl_group:
            if bl_pair.relay == thing:
                if bl_pair.relay.state:
                    bl_pair.timestamp = common.get_millis()
                else:
                    bl_pair.timestamp = 0


async def action():
    while True:
        check_blinds_timeouts()
        await asyncio.sleep(1)
