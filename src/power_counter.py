import common
import common_pins
import time

interrupt_pin = None
state = 0
kwh = 0
impulses = 0
IMPULSES_PER_KWH = 500
on_state_change_cb = None
diff_value = 2.2
diff_timeout = 30 * 60000
diff_timestamp = 0


def total_kwh():
    return kwh + impulses / IMPULSES_PER_KWH


def on_interrupt(pin):
    global impulses, kwh
    impulses += 1
    if (impulses == IMPULSES_PER_KWH):
        kwh += 1
        impulses = 0


def init():
    global interrupt_pin, diff_timestamp
    diff_timestamp = common.get_millis()
    interrupt_pin = common.create_interrupt(common_pins.POWER_COUNTER.id, on_interrupt)


def register_on_state_change_callback(cb):
    global on_state_change_cb
    print("[POWER_COUNTER]: register on state change cb")
    on_state_change_cb = cb


def action():
    global diff_timestamp
    if total_kwh() >= diff_value or common.millis_passed(diff_timestamp) >= diff_timeout:
        value = total_kwh()
        kwh = 0
        impulses = 0
        diff_timestamp = common.get_millis()
        print("[POWER_COUNTER]: %f kwh" % (value))
        if on_state_change_cb != None:
            on_state_change_cb("POWER_COUNTER", value)


def test():
    init()
    while True:
        loop()
