import common

local_data_out = {}
remote_data_out = {}
local_data_in = {}
remote_data_in = {}

send_data_out_callback = None
send_data_in_callback = None

remote_path = {
    # inputs
    "ONBOARD_BUTTON": "/test/button1",
    "B1_SW1": "/room1/button1",
    "B1_SW2": "/room1/button2",
    "B2_SW1": "/room1/button3",
    "B2_SW2": "/room1/button4",
    "B3_SW1": "/room2/button1",
    "B3_SW2": "/room2/button2",
    "B4_SW1": "/room2/button3",
    "B4_SW2": "/room2/button4",
    # sensors
    "S1_radar": "/room1/radar",
    "S1_temperature": "/room1/temperature",
    "S1_pressure": "/room1/pressure",
    "S1_gas": "/room1/gas",
    "S1_altitude": "/room1/altitude",
    "S1_humidity": "/room1/humidity",
    "S1_light": "/room1/light",
    "S2_radar": "/room2/radar",
    "S2_temperature": "/room2/temperature",
    "S2_pressure": "/room2/pressure",
    "S2_gas": "/room2/gas",
    "S2_altitude": "/room2/altitude",
    "S2_humidity": "/room2/humidity",
    "S2_light": "/room2/light",
    # outputs
    "ONBOARD_LED1": "/test/led1",
    "ONBOARD_LED2": "/test/led2",
    "ONBOARD_LED3": "/test/led3",
    "RELAY_1": "/room2/relay4",
    "RELAY_2": "/room2/relay3",
    "RELAY_3": "/room2/relay2",
    "RELAY_4": "/room2/relay1",
    "RELAY_5": "/room1/relay4",
    "RELAY_6": "/room1/relay3",
    "RELAY_7": "/room1/relay2",
    "RELAY_8": "/room1/relay1",
    "RELAY_9": "/room1/relay5",
    "RELAY_10": "/room1/relay6",
    "RELAY_11": "/room2/relay5",
    "RELAY_12": "/room2/relay6",
    "B1_LED1_GB": "/room1/button1_led1",
    "B1_LED1_R": "/room1/button1_led2",
    "B1_LED2_GB": "/room1/button2_led1",
    "B1_LED2_R": "/room1/button2_led2",
    "B2_LED1_GB": "/room1/button3_led1",
    "B2_LED1_R": "/room1/button3_led2",
    "B2_LED2_GB": "/room1/button4_led1",
    "B2_LED2_R": "/room1/button4_led2",
    "B3_LED1_GB": "/room2/button1_led1",
    "B3_LED1_R": "/room2/button1_led2",
    "B3_LED2_GB": "/room2/button2_led1",
    "B3_LED2_R": "/room2/button2_led2",
    "B4_LED1_GB": "/room2/button3_led1",
    "B4_LED1_R": "/room2/button3_led2",
    "B4_LED2_GB": "/room2/button4_led1",
    "B4_LED2_R": "/room2/button4_led2",
}


def get_key(val):
    for key, value in remote_path.items():
        if val == value:
            return key
    return None


@common.dump_func(showarg=True)
def set_local_data_out(name, value):
    local_data_out[name] = value


def sync_data_out():
    for key in local_data_out:
        local_value = local_data_out[key]
        remote_value = remote_data_out.get(key, None)
        if local_value != remote_value:
            remote_data_out[key] = local_value
            path = remote_path[key]
            print(path, local_value)
            if send_data_out_callback != None:
                send_data_out_callback(key, local_value)


def set_remote_data_in(path, value):
    key = get_key(value)
    if key != None:
        remote_data_in[key] = value
    else:
        print("key %s not found" % (key))


def sync_data_in():
    for key in remote_data_in:
        remote_value = remote_data_in[key]
        local_value = local_data_in.get(key, None)
        if remote_value != local_value:
            local_data_in[key] = remote_value
            print(remote_path[key], remote_value)
            if send_data_in_callback != None:
                send_data_in_callback(key, remote_value)


def init():
    pass


def loop():
    sync_data_out()
    sync_data_in()


def test():
    init()
    while True:
        loop()


def register_send_data_out_callback(cb):
    global send_data_out_callback
    send_data_out_callback = cb


def register_send_data_in_callback(cb):
    global send_data_in_callback
    send_data_in_callback = cb
