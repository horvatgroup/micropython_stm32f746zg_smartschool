import peripherals
import lan
import sensors


def on_button_callback(state):
    pass


if __name__ == "__main__":
    peripherals.register_button_callback_function(on_button_callback)
    sensors.init()
    # lan.init()
    while True:
        peripherals.loop()
        sensors.loop()
        # lan.loop()
