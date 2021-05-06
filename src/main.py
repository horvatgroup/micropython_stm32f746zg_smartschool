from common import dump_func, create_led, create_button, get_millis, millis_passed
from peripherals import register_button_callback_function, check_button
import lan


def on_button_callback(state):
    pass


if __name__ == "__main__":
    register_button_callback_function(on_button_callback)
    lan.init()
    while True:
        check_button()
        lan.loop()
