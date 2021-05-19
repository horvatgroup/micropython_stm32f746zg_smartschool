from machine import Pin
from time import ticks_ms


def get_millis():
    return ticks_ms()


def millis_passed(timestamp):
    return get_millis() - timestamp


def dump_func(pexit=False, timing=False, showarg=False):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            enter_string = "%s.%s <enter>" % (f.__globals__['__name__'], f.__name__)
            pexit_local = False
            if showarg:
                enter_string += ", <args[%s%s]>" % (args, kwargs)
            print(enter_string)
            if timing:
                pexit_local = True
                timestamp = get_millis()
            response = f(*args, **kwargs)
            exit_string = "%s <exit>" % (f.__name__)
            if timing:
                exit_string += ", <time[%d]>" % (millis_passed(timestamp))
            if pexit or pexit_local:
                print(exit_string)
            return response
        return wrapped
    return inner_decorator


def print_available_pins():
    print(dir(Pin.board))
    print(dir(Pin.cpu))


def create_output(pin):
    return Pin(pin, Pin.OUT)


def create_input(pin, pullup=None):
    if pullup == None:
        return Pin(pin, Pin.IN, None)
    if pullup:
        return Pin(pin, Pin.IN, Pin.PULL_UP)
    else:
        return Pin(pin, Pin.IN, Pin.PULL_DOWN)

