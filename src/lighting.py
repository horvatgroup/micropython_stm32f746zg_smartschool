import things


class Button:
    def __init__(self, thing_button):
        self.thing_button = thing_button
        self.was_pressed = thing_button.state


BUTTON_1 = Button(things.get_thing_from_hw("B4_SW1"))
BUTTON_2 = Button(things.get_thing_from_hw("B4_SW2"))

buttons = [
    BUTTON_1, BUTTON_2
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


def on_button_released(button):
    for sl_pair in lightings:
        if sl_pair.thing_button == button.thing_button:
            things.set_state(sl_pair.thing_activity_light, 0)
            next_state = int(not sl_pair.thing_main_light.state)
            things.set_state(sl_pair.thing_main_light, next_state)
            check_inverted_light(sl_pair)
            break


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
        self.check = False


lightings = (
    Lighting(things.get_thing_from_hw("B4_SW1"),
             things.get_thing_from_hw("RELAY_8"),
             things.get_thing_from_hw("B4_LED1_GB"),
             things.get_thing_from_hw("B4_LED1_R")),
    Lighting(things.get_thing_from_hw("B4_SW2"),
             things.get_thing_from_hw("ONBOARD_LED2"),
             things.get_thing_from_hw("B4_LED2_GB"),
             things.get_thing_from_hw("B4_LED2_R")),
)

# class RelayControl:
#     def __init__(self, relay, enable_button, disable_buttons, enabled_timeout=5000):
#         self.relay = relay
#         self.enable_button = enable_button
#         self.disable_buttons = disable_buttons
#         self.enabled_timeout = enabled_timeout
#         self.check = False
#
#
# blinds_pairs = (RelayControl(things.get_thing_from_hw("ONBOARD_LED1"),
#                              things.get_thing_from_hw("B4_SW1"),
#                              [
#                                  things.get_thing_from_hw("B4_SW1"),
#                                  things.get_thing_from_hw("B4_SW2")
#                              ]),
#                 RelayControl(things.get_thing_from_hw("ONBOARD_LED2"),
#                              things.get_thing_from_hw("B4_SW2"),
#                              [
#                                  things.get_thing_from_hw("B4_SW1"),
#                                  things.get_thing_from_hw("B4_SW2")
#                              ])
#                 )
