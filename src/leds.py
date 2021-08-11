#!/bin/bash

import common
import common_pins
import time


class Led:
    def __init__(self, id, name):
        self.output = common.create_output(id)
        self.output.off()
        self.name = name


relay_pins = [
    common_pins.RELAY_1,
    common_pins.RELAY_2,
    common_pins.RELAY_3,
    common_pins.RELAY_4,
    common_pins.RELAY_5,
    common_pins.RELAY_6,
    common_pins.RELAY_7,
    common_pins.RELAY_8,
    common_pins.RELAY_9,
    common_pins.RELAY_10,
    common_pins.RELAY_11,
    common_pins.RELAY_12
]
led_pins = [
    common_pins.ONBOARD_LED1,
    common_pins.ONBOARD_LED2,
    common_pins.ONBOARD_LED3,
    common_pins.B1_LED1_GB,
    common_pins.B1_LED1_R,
    common_pins.B1_LED2_GB,
    common_pins.B1_LED2_R,
    common_pins.B2_LED1_GB,
    common_pins.B2_LED1_R,
    common_pins.B2_LED2_GB,
    common_pins.B2_LED2_R,
    common_pins.B3_LED1_GB,
    common_pins.B3_LED1_R,
    common_pins.B3_LED2_GB,
    common_pins.B3_LED2_R,
    common_pins.B4_LED1_GB,
    common_pins.B4_LED1_R,
    common_pins.B4_LED2_GB,
    common_pins.B4_LED2_R
]

relays = []
leds = []


def init_relays():
    for pin in relay_pins:
        relays.append(Led(pin.id, pin.name))


def init_leds():
    for pin in led_pins:
        leds.append(Led(pin.id, pin.name))


def init():
    init_relays()
    init_leds()


def loop():
    pass


def test():
    init()
    loop()


def test_relays():
    global relays
    relays = []
    init_relays()
    for relay in relays:
        print("Testing %s" % (relay.name))
        relay.output.on()
        time.sleep_ms(1000)
        relay.output.off()
        time.sleep_ms(1000)


def test_leds():
    global leds
    leds = []
    init_leds()
    for led in leds:
        print("Testing %s" % (led.name))
        led.output.on()
        time.sleep_ms(1000)
        led.output.off()
        time.sleep_ms(1000)
