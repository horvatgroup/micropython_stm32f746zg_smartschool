import common
import common_pins

interrupt_pin = None
impulses = 0
sent_impulses = 0
IMPULSES_PER_KWH = 500
on_state_change_cb = None
diff_value = 2.2
diff_timeout = 30 * 60000
diff_timestamp = 0


def on_interrupt(pin):
    global impulses, sent_impulses
    if sent_impulses:
        impulses = impulses - sent_impulses
        sent_impulses = 0
    impulses += 1


def init():
    global interrupt_pin, diff_timestamp
    diff_timestamp = common.get_millis()
    interrupt_pin = common.create_interrupt(common_pins.POWER_COUNTER.id, on_interrupt)


def register_on_state_change_callback(cb):
    global on_state_change_cb
    print("[POWER_COUNTER]: register on state change cb")
    on_state_change_cb = cb


def action():
    global diff_timestamp, sent_impulses
    if (impulses / IMPULSES_PER_KWH) >= diff_value or common.millis_passed(diff_timestamp) >= diff_timeout:
        sent_impulses = impulses
        value = sent_impulses / IMPULSES_PER_KWH
        diff_timestamp = common.get_millis()
        print("[POWER_COUNTER]: %f kwh" % (value))
        if on_state_change_cb != None:
            on_state_change_cb("POWER_COUNTER", value)


def test():
    init()
    while True:
        loop()
