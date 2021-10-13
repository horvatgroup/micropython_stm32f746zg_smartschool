class Thing:
    def __init__(self, hw, in_path=None, out_path=None, sync_in=True, sync_out=True):
        self.hw = hw
        self.in_path = in_path
        self.out_path = out_path
        self.out_remote_state = None
        self.in_remote_state = None
        self.state = None
        self.sync_in = sync_in
        self.sync_out = sync_out


things = (
    # inputs
    Thing("ONBOARD_BUTTON", out_path="out/test/button1"),
    Thing("B1_SW1", out_path="out/B4/SW1", sync_out=False),
    Thing("B1_SW2", out_path="out/B4/SW2", sync_out=False),
    Thing("B2_SW1", out_path="out/B3/SW1", sync_out=False),
    Thing("B2_SW2", out_path="out/B3/SW2", sync_out=False),
    Thing("B3_SW1", out_path="out/B2/SW1", sync_out=False),
    Thing("B3_SW2", out_path="out/B2/SW2", sync_out=False),
    Thing("B4_SW1", out_path="out/B1/SW1", sync_out=False),
    Thing("B4_SW2", out_path="out/B1/SW2", sync_out=False),
    # sensors
    Thing("S1_RADAR", out_path="out/S2/radar"),
    Thing("S1_ENV_TEMPERATURE", out_path="out/S2/env_temperature"),
    Thing("S1_ENV_PRESSURE", out_path="out/S2/env_pressure"),
    Thing("S1_ENV_GAS", out_path="out/S2/env_gas"),
    Thing("S1_ENV_ALTITUDE", out_path="out/S2/env_altitude"),
    Thing("S1_ENV_HUMIDITY", out_path="out/S2/env_humidity"),
    Thing("S1_LIGHT", out_path="out/S2/light"),
    Thing("S1_CO2", out_path="out/S2/co2"),
    Thing("S2_RADAR", out_path="out/S1/radar"),
    Thing("S2_ENV_TEMPERATURE", out_path="out/S1/env_temperature"),
    Thing("S2_ENV_PRESSURE", out_path="out/S1/env_pressure"),
    Thing("S2_ENV_GAS", out_path="out/S1/env_gas"),
    Thing("S2_ENV_ALTITUDE", out_path="out/S1/env_altitude"),
    Thing("S2_ENV_HUMIDITY", out_path="out/S1/env_humidity"),
    Thing("S2_LIGHT", out_path="out/S1/light"),
    Thing("S2_CO2", out_path="out/S1/co2"),
    # outputs
    Thing("ONBOARD_LED1", in_path="in/test/led1", out_path="out/test/led1", sync_out=False),
    Thing("ONBOARD_LED2", in_path="in/test/led2", out_path="out/test/led2"),
    Thing("ONBOARD_LED3", in_path="in/test/led3", out_path="out/test/led3", sync_out=False),
    Thing("RELAY_1", in_path="in/R/relay8", out_path="out/R/relay8"),
    Thing("RELAY_2", in_path="in/R/relay7", out_path="out/R/relay7"),
    Thing("RELAY_3", in_path="in/R/relay6", out_path="out/R/relay6"),
    Thing("RELAY_4", in_path="in/R/relay5", out_path="out/R/relay5"),
    Thing("RELAY_5", in_path="in/R/relay4", out_path="out/R/relay4"),
    Thing("RELAY_6", in_path="in/R/relay3", out_path="out/R/relay3"),
    Thing("RELAY_7", in_path="in/R/relay2", out_path="out/R/relay2"),
    Thing("RELAY_8", in_path="in/R/relay1", out_path="out/R/relay1"),
    Thing("RELAY_9", in_path="in/R/relay9", out_path="out/R/relay9"),
    Thing("RELAY_10", in_path="in/R/relay10", out_path="out/R/relay10"),
    Thing("RELAY_11", in_path="in/R/relay11", out_path="out/R/relay11"),
    Thing("RELAY_12", in_path="in/R/relay12", out_path="out/R/relay12"),
    Thing("B1_LED1_GB", in_path="in/B4/SW1/GB", out_path="out/B4/SW1/GB", sync_out=False),
    Thing("B1_LED1_R", in_path="in/B4/SW1/R", out_path="out/B4/SW1/R", sync_out=False),
    Thing("B1_LED2_GB", in_path="in/B4/SW2/GB", out_path="out/B4/SW2/GB", sync_out=False),
    Thing("B1_LED2_R", in_path="in/B4/SW2/R", out_path="out/B4/SW2/R", sync_out=False),
    Thing("B2_LED1_GB", in_path="in/B3/SW1/GB", out_path="out/B3/SW1/GB", sync_out=False),
    Thing("B2_LED1_R", in_path="in/B3/SW1/R", out_path="out/B3/SW1/R", sync_out=False),
    Thing("B2_LED2_GB", in_path="in/B3/SW2/GB", out_path="out/B3/SW2/GB", sync_out=False),
    Thing("B2_LED2_R", in_path="in/B3/SW2/R", out_path="out/B3/SW2/R", sync_out=False),
    Thing("B3_LED1_GB", in_path="in/B2/SW1/GB", out_path="out/B2/SW1/GB", sync_out=False),
    Thing("B3_LED1_R", in_path="in/B2/SW1/R", out_path="out/B2/SW1/R", sync_out=False),
    Thing("B3_LED2_GB", in_path="in/B2/SW2/GB", out_path="out/B2/SW2/GB", sync_out=False),
    Thing("B3_LED2_R", in_path="in/B2/SW2/R", out_path="out/B2/SW2/R", sync_out=False),
    Thing("B4_LED1_GB", in_path="in/B1/SW1/GB", out_path="out/B1/SW1/GB", sync_out=False),
    Thing("B4_LED1_R", in_path="in/B1/SW1/R", out_path="out/B1/SW1/R", sync_out=False),
    Thing("B4_LED2_GB", in_path="in/B1/SW2/GB", out_path="out/B1/SW2/GB", sync_out=False),
    Thing("B4_LED2_R", in_path="in/B1/SW2/R", out_path="out/B1/SW2/R", sync_out=False),
)

on_thing_sync_out = None
on_thing_sync_in = None
on_thing_remote_in = None


def get_thing_from_hw(hw):
    for thing in things:
        if thing.hw == hw:
            return thing
    return None


def get_thing_from_path(path):
    for thing in things:
        if thing.in_path == path or thing.out_path == path:
            return thing
    return None


def set_state(thing, state, soft=False):
    if thing.state != state:
        print("[THING]: set_state hw=%s, state=%s, soft=%s" % (thing.hw, state, soft))
        thing.state = state
        thing.in_remote_state = state
        if not soft:
            if on_thing_sync_in != None:
                on_thing_sync_in(thing)


def set_in_remote_state(path, state):
    print("[THING]: set_in_remote_state path=%s, state=%s" % (path, state))
    thing = get_thing_from_path(path)
    if thing:
        try:
            thing.in_remote_state = int(state)
        except Exception as e:
            print("[THING]: ERROR probably not implemented with %s" % (e))


def sync_in_remote_state(thing):
    if thing.in_remote_state != None and thing.in_remote_state != thing.state:
        set_state(thing, thing.in_remote_state)
        if on_thing_remote_in != None:
            on_thing_remote_in(thing)


async def sync_out_remote_state(thing):
    if thing.state != None and thing.state != thing.out_remote_state:
        thing.out_remote_state = thing.state
        if on_thing_sync_out != None:
            await on_thing_sync_out(thing)


def register_on_thing_sync_out(func):
    print("[THING]: register_on_thing_sync_out")
    global on_thing_sync_out
    on_thing_sync_out = func


def register_on_thing_sync_in(func):
    print("[THING]: register_on_thing_sync_in")
    global on_thing_sync_in
    on_thing_sync_in = func


def register_on_thing_remote_in(func):
    print("[THING]: register_on_thing_remote_in")
    global on_thing_remote_in
    on_thing_remote_in = func
