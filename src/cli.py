import sys
import uselect
import leds
import buttons
import sensors
import lan

spoll = None
input_buffer = []
loop_cbs = []


def init():
    print("[CLI]: init")
    global spoll
    spoll = uselect.poll()
    spoll.register(sys.stdin, uselect.POLLIN)


def read_from_usb():
    return (sys.stdin.read(1) if spoll.poll(0) else None)


def handle_input(byte):
    global input_buffer
    if byte == "?":
        print("[CLI]: \"%s\"" % ("".join(input_buffer)))
    elif ord(byte) == 10:  # return
        cmd = "".join(input_buffer).split(" ")
        input_buffer = []
        cmd = list(filter(None, cmd))
        if len(cmd) == 0:
            print("[CLI]: buffer empty")
            return None
        return cmd
    elif ord(byte) == 127:  # backspace
        try:
            input_buffer.pop()
        except:
            print("[CLI]: buffer empty")
    else:
        # print(ord(byte))  # debug input
        input_buffer.append(byte)
    return None


class LoopCb:
    def __init__(self, name, cb, state):
        self.name = name
        self.cb = cb
        self.state = state

    def set_state(self, state):
        self.state = state

    def loop(self):
        if self.state:
            self.cb()


def set_loop_cb(name, cb, state):
    print("[CLI]: loop_cb %s %s" % (name, state))
    global loop_cbs
    found = False
    for loop_cb in loop_cbs:
        if loop_cb.name == name:
            found = True
            loop_cb.set_state(state)
    if not found:
        loop_cbs.append(LoopCb(name, cb, state))


def parse_leds(cmd):
    if cmd[1] == "1":
        leds.set_state_by_name("ONBOARD_LED1", int(cmd[2]))
    elif cmd[1] == "2":
        leds.set_state_by_name("ONBOARD_LED2", int(cmd[2]))
    elif cmd[1] == "3":
        leds.set_state_by_name("ONBOARD_LED3", int(cmd[2]))
    elif cmd[1] == "init":
        leds.init()
    elif cmd[1] == "name":
        leds.set_state_by_name(cmd[2], int(cmd[3]))
    else:
        print("[CLI]: \"%s\" not implemented" % (" ".join(cmd)))


def parse_buttons(cmd):
    if cmd[1] == "init":
        buttons.init()
    elif cmd[1] == "loop":
        set_loop_cb("buttons", buttons.loop, int(cmd[2]))
    elif cmd[1] == "cb":
        buttons.register_on_state_change_callback(lambda name, state: print("[CLI]: buttons %s -> %s" % (name, state)))
    else:
        print("[CLI]: \"%s\" not implemented" % (" ".join(cmd)))


def parse_sensors(cmd):
    if cmd[1] == "init":
        sensors.init()
    elif cmd[1] == "loop":
        set_loop_cb("sensors", sensors.loop, int(cmd[2]))
    else:
        print("[CLI]: \"%s\" not implemented" % (" ".join(cmd)))


def parse_lan(cmd):
    if cmd[1] == "init":
        lan.init()
    elif cmd[1] == "check":
        lan.is_connection_ready()
    elif cmd[1] == "status":
        lan.print_status()
    elif cmd[1] == "ping":
        lan.ping()
    elif cmd[1] == "loop":
        set_loop_cb("lan", lan.loop, int(cmd[2]))


def parse_input(cmd):
    if cmd[0] == "leds":
        parse_leds(cmd)
    elif cmd[0] == "buttons":
        parse_buttons(cmd)
    elif cmd[0] == "sensors":
        parse_sensors(cmd)
    elif cmd[0] == "lan":
        parse_lan(cmd)
    else:
        print("[CLI]: \"%s\" not implemented" % (" ".join(cmd)))


def loop():
    bytes = read_from_usb()
    if bytes:
        for byte in bytes:
            cmd = handle_input(byte)
            if cmd:
                parse_input(cmd)
            for loop_cb in loop_cbs:
                loop_cb.loop()


def test():
    print("[CLI]: test")
    init()
    while True:
        loop()
