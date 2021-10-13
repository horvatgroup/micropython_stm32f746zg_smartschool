import things


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

blinds_pairs = ()


def check_inverted_light(sl_pair):
    if not sl_pair.thing_button.state:
        inverted_next_state = int(not sl_pair.thing_main_light.state)
        things.set_state(sl_pair.thing_inverted_light, inverted_next_state)


def check_inverted_lights():
    for sl_pair in lightings:
        check_inverted_light(sl_pair)


def check_button_logic():
    for sl_pair in lightings:
        if sl_pair.thing_button.state:
            things.set_state(sl_pair.thing_inverted_light, 0)
            things.set_state(sl_pair.thing_activity_light, 1)
            sl_pair.check = True
        elif not sl_pair.thing_button.state and sl_pair.check:
            sl_pair.check = False
            things.set_state(sl_pair.thing_activity_light, 0)
            next_state = int(not sl_pair.thing_main_light.state)
            things.set_state(sl_pair.thing_main_light, next_state)
            check_inverted_light(sl_pair)
