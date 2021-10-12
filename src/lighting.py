import things


class Lighting:
    def __init__(self, thing_button, thing_main_light, thing_inverted_light, thing_activity_light):
        self.thing_button = thing_button
        self.thing_main_light = thing_main_light
        self.thing_inverted_light = thing_inverted_light
        self.thing_activity_light = thing_activity_light


lighting_pairs = (
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


def check_button_logic():
    for sl_pair in lighting_pairs:
        things.set_state(sl_pair.thing_activity_light, sl_pair.thing_button.state)
        if sl_pair.thing_button.state:
            next_state = int(not sl_pair.thing_main_light.state)
            things.set_state(sl_pair.thing_main_light, next_state)
            things.set_state(sl_pair.thing_inverted_light, 0)
        else:
            inverted_next_state = int(not sl_pair.thing_main_light.state)
            things.set_state(sl_pair.thing_inverted_light, inverted_next_state)
