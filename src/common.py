from machine import Pin
from time import ticks_ms


def get_millis():
    return ticks_ms()


def millis_passed(timestamp):
    return get_millis() - timestamp


def dump_func(exit=False, timing=False):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            enter_string = "%s enter" % (f.__name__)
            print(enter_string)
            if timing: timestamp = get_millis() 
            response = f(*args, **kwargs)
            exit_string = "%s exit" % (f.__name__)
            if timing: exit_string += ", time[%d]" % (millis_passed(timestamp)) 
            if exit:
                print(exit_string)
            return response
        return wrapped
    return inner_decorator


def print_available_pins():
    print(dir(Pin.board))
    print(dir(Pin.cpu))


def create_led(pin):
    return Pin(pin, Pin.OUT)


def create_button(pin):
    return Pin(pin, Pin.IN, Pin.PULL_DOWN)
