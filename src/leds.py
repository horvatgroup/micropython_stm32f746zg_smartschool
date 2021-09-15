#!/bin/bash

import common
import common_pins
import time


class Led:
    def __init__(self, id, name, active_high=False):
        self.output = common.create_output(id)
        self.active_high = active_high
        self.set_state(0)
        self.name = name

    def set_state(self, state):
        if self.active_high:
            if state:
                self.output.off()
            else:
                self.output.on()
        else:
            if state:
                self.output.on()
            else:
                self.output.off()


relay_pins = [
    common_pins.RELAY_8,
    common_pins.RELAY_7,
    common_pins.RELAY_6,
    common_pins.RELAY_5,
    common_pins.RELAY_4,
    common_pins.RELAY_3,
    common_pins.RELAY_2,
    common_pins.RELAY_1,
    common_pins.RELAY_9,
    common_pins.RELAY_10,
    common_pins.RELAY_11,
    common_pins.RELAY_12
]
led_pins = [
    common_pins.ONBOARD_LED1,
    common_pins.ONBOARD_LED2,
    common_pins.ONBOARD_LED3,
    common_pins.B4_LED1_GB,
    common_pins.B4_LED1_R,
    common_pins.B4_LED2_GB,
    common_pins.B4_LED2_R,
    common_pins.B3_LED1_GB,
    common_pins.B3_LED1_R,
    common_pins.B3_LED2_GB,
    common_pins.B3_LED2_R,
    common_pins.B2_LED1_GB,
    common_pins.B2_LED1_R,
    common_pins.B2_LED2_GB,
    common_pins.B2_LED2_R,
    common_pins.B1_LED1_GB,
    common_pins.B1_LED1_R,
    common_pins.B1_LED2_GB,
    common_pins.B1_LED2_R
]

relays = []
leds = []


def init_relays():
    for pin in relay_pins:
        relays.append(Led(pin.id, pin.name))


def init_leds():
    for pin in led_pins:
        if "ONBOARD" in pin.name:
            leds.append(Led(pin.id, pin.name))
        else:
            leds.append(Led(pin.id, pin.name, True))


def init():
    print("[LEDS]: init")
    init_relays()
    init_leds()


def loop():
    pass


def test():
    print("[LEDS]: test")
    init()
    loop()


def test_relays():
    global relays
    relays = []
    init_relays()
    for relay in relays:
        print("[LEDS]: testing %s" % (relay.name))
        relay.set_state(1)
        time.sleep_ms(1000)
        relay.set_state(0)
        time.sleep_ms(1000)


def test_leds():
    global leds
    leds = []
    init_leds()
    for led in leds:
        print("[LEDS]: testing %s" % (led.name))
        led.set_state(1)
        time.sleep_ms(1000)
        led.set_state(0)
        time.sleep_ms(1000)


def set_state_by_name(name, state):
    print("[LEDS]: set_state_by_name(%s, %s)" % (name, state))
    for relay in relays:
        if relay.name == name:
            relay.set_state(state)
    for led in leds:
        if led.name == name:
            led.set_state(state)
