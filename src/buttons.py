import uasyncio as asyncio
import common
import common_pins
import eventor, events

on_state_change_cb = None
buttons = []

button_pins = {
    events.ONBOARD_BUTTON: common_pins.ONBOARD_BUTTON,
    events.B1_SW1: common_pins.B1_SW1,
    events.B1_SW2: common_pins.B1_SW2,
    events.B2_SW1: common_pins.B2_SW1,
    events.B2_SW2: common_pins.B2_SW2,
    events.B3_SW1: common_pins.B3_SW1,
    events.B3_SW2: common_pins.B3_SW2,
    events.B4_SW1: common_pins.B4_SW1,
    events.B4_SW2: common_pins.B4_SW2,
}

class Button:
    def __init__(self, pin, event):
        self.input = common.create_input(pin.id)
        self.event = event
        self.name = pin.name
        self.state = None

    def check(self):
        state = self.input.value()
        if state != self.state:
            self.state = state
            eventor.publish(self.event, self.state)
            print("[BUTTONS]: %s -> %d" % (self.name, self.state))


def init():
    print("[BUTTONS]: init")
    for event, pin in button_pins.items():
        buttons.append(Button(pin, event))


def action():
    for button in buttons:
        button.check()


def test():
    print("[BUTTONS]: test")
    init()
    while True:
        action()


def test_async():
    print("[BUTTONS]: test_async")
    init()
    asyncio.run(common.loop_async("BUTTONS", action))
