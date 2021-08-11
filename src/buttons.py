import common
import common_pins


class Button:
    def __init__(self, pin):
        self.input = common.create_input(pin.id)
        self.name = pin.name
        self.state = None

    def check(self):
        state = self.input.value()
        if state != self.state:
            self.state = state
            print("State change for %s to %d" % (self.name, self.state))


button_pins = [common_pins.ONBOARD_BUTTON,
               common_pins.B1_SW1,
               common_pins.B1_SW2,
               common_pins.B2_SW1,
               common_pins.B2_SW2,
               common_pins.B3_SW1,
               common_pins.B3_SW2,
               common_pins.B4_SW1,
               common_pins.B4_SW2
               ]

buttons = []


def init():
    for pin in button_pins:
        buttons.append(Button(pin))


def loop():
    for button in buttons:
        button.check()


def test():
    init()
    while True:
        loop()
