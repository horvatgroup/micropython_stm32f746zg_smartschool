from machine import Pin
from time import ticks_ms

def get_millis():
    return ticks_ms()

def millis_passed(timestamp):
    return get_millis() - timestamp
  
def print_available_pins():
    print(dir(Pin.board))
    print(dir(Pin.cpu))

def create_led(pin):
    return Pin(pin, Pin.OUT)

def create_button(pin):
    return Pin(pin, Pin.IN, Pin.PULL_DOWN)