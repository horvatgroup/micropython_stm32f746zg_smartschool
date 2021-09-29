import uasyncio as asyncio
import common
import common_pins

on_state_change_cb = None
buttons = []

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


class Button:
    def __init__(self, pin):
        self.input = common.create_input(pin.id)
        self.name = pin.name
        self.state = None

    def check(self):
        state = self.input.value()
        if state != self.state:
            self.state = state
            print("[BUTTONS]: %s -> %d" % (self.name, self.state))
            if on_state_change_cb:
                on_state_change_cb(self.name, self.state)


def register_on_state_change_callback(cb):
    print("[BUTTONS]: register on state change cb")
    global on_state_change_cb
    on_state_change_cb = cb


def init():
    print("[BUTTONS]: init")
    for pin in button_pins:
        buttons.append(Button(pin))
    loop()


def loop():
    for button in buttons:
        button.check()


async def loop_async():
    print("[BUTTONS]: start loop_async")
    bigest = 0
    while True:
        timestamp = common.get_millis()
        loop()
        timeout = common.millis_passed(timestamp)
        if timeout >= 3:
            if timeout > bigest:
                bigest = timeout
            print("[BUTTONS]: timeout warning %d ms with bigest %d" % (timeout, bigest))
        await asyncio.sleep(0)


def test():
    print("[BUTTONS]: test")
    init()
    while True:
        loop()


def test_async():
    print("[BUTTONS]: test_async")
    init()
    asyncio.run(loop_async())
