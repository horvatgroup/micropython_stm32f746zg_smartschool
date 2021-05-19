from common import dump_func, create_input, get_millis, millis_passed
import pins

radar_signal_pin = create_input(pins.S2_RADAR_SIG, True)
radar_signal_state = 0
radar_signal_timestamp = 0

@dump_func()
def init():
    pass

def loop():
    global radar_signal_state, radar_signal_timestamp
    state = radar_signal_pin.value() 
    if state != radar_signal_state:
        radar_signal_state = state
        print("RADAR:[%d] %d" % (state, millis_passed(radar_signal_timestamp)))
        radar_signal_timestamp = get_millis()