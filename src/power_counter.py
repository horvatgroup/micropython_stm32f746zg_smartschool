import common
import common_pins
import time

interrupt_pin = None

def on_interrupt(pin):
    print(pin)

def init():
    global interrupt_pin
    interrupt_pin = common.create_interrupt(common_pins.POWER_COUNTER, on_interrupt)

def loop():
    pass

def test():
    init()
    while True:
        loop()
        time.sleep_ms(300)