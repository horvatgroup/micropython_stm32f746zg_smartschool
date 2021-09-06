import common
import common_pins
import time
import mutex

interrupt_pin = None
state = 0
kwh = 0
impulses = 0
IMPULSES_PER_KWH = 800
measure_timeout = 60*1000
measure_timestamp = 0
lock = mutex.Mutex()
queue = []

def on_interrupt(pin):
    global impulses, kwh, measure_timestamp
    impulses += 1
    if (impulses == IMPULSES_PER_KWH):
        kwh += 1
        impulses = 0

    now = common.get_millis()
    time = now - measure_timestamp
    if time >= measure_timeout:
        if lock.test():
            measure_timestamp = now
            value = total_kwh()
            kwh = 0
            impulses = 0
            queue.append((time, value))
            lock.release()


def init():
    global interrupt_pin, measure_timestamp
    measure_timestamp = common.get_millis()
    interrupt_pin = common.create_interrupt(common_pins.POWER_COUNTER.id, on_interrupt)


def total_kwh():
    return kwh + impulses / IMPULSES_PER_KWH


def loop():
    with lock:
        if len(queue) > 0:
            time, value = queue.pop(0)
            print("[POWER_COUNTER]: %f kwh in %d ms" % (value, time))


def test():
    init()
    while True:
        loop()
        time.sleep_ms(30000)