import uasyncio as asyncio
import sensors
import power_counter
import mqtt
import version
import phy_interface


class Thing:
    def __init__(self, path=None, alias=None, ignore_duplicates_out=False, ignore_duplicates_in=False, cb_out=None, cb_in=None):
        self.path = path
        self.alias = alias
        self.ignore_duplicates_out = ignore_duplicates_out
        self.ignore_duplicates_in = ignore_duplicates_in
        self.data = None
        self.dirty_out = False
        self.dirty_in = False
        self.cb_out = cb_out
        self.cb_in = cb_in


things = (
    # sensors
    Thing("S2/radar", alias="S1_RADAR", cb_in=sensors.on_data_request),
    Thing("S2/env", alias="S1_ENV", cb_in=sensors.on_data_request),
    Thing("S2/env/error", alias="S1_ENV_ERROR", cb_in=sensors.on_data_request),
    Thing("S2/env/temperature", alias="S1_ENV_TEMPERATURE"),
    Thing("S2/env/pressure", alias="S1_ENV_PRESSURE"),
    Thing("S2/env/gas", alias="S1_ENV_GAS"),
    Thing("S2/env/altitude", alias="S1_ENV_ALTITUDE"),
    Thing("S2/env/humidity", alias="S1_ENV_HUMIDITY"),
    Thing("S2/light", alias="S1_LIGHT", cb_in=sensors.on_data_request),
    Thing("S2/light/error", alias="S1_LIGHT_ERROR", cb_in=sensors.on_data_request),
    Thing("S2/co2", alias="S1_CO2", cb_in=sensors.on_data_request),
    Thing("S2/co2/error", alias="S1_CO2_ERROR", cb_in=sensors.on_data_request),
    Thing("S1/radar", alias="S2_RADAR", cb_in=sensors.on_data_request),
    Thing("S1/env", alias="S2_ENV", cb_in=sensors.on_data_request),
    Thing("S1/env/error", alias="S2_ENV_ERROR", cb_in=sensors.on_data_request),
    Thing("S1/env/temperature", alias="S2_ENV_TEMPERATURE"),
    Thing("S1/env/pressure", alias="S2_ENV_PRESSURE"),
    Thing("S1/env/gas", alias="S2_ENV_GAS"),
    Thing("S1/env/altitude", alias="S2_ENV_ALTITUDE"),
    Thing("S1/env/humidity", alias="S2_ENV_HUMIDITY"),
    Thing("S1/light", alias="S2_LIGHT", cb_in=sensors.on_data_request),
    Thing("S1/light/error", alias="S2_LIGHT_ERROR", cb_in=sensors.on_data_request),
    Thing("S1/co2", alias="S2_CO2", cb_in=sensors.on_data_request),
    Thing("S1/co2/error", alias="S2_CO2_ERROR", cb_in=sensors.on_data_request),
    Thing("power_counter", alias="POWER_COUNTER", cb_in=sensors.on_data_request),
    # phy outputs
    Thing("test/led1"),
    Thing("test/led2"),
    Thing("test/led3"),
    Thing("R/relay8"),
    Thing("R/relay7"),
    Thing("R/relay6"),
    Thing("R/relay5"),
    Thing("R/relay4"),
    Thing("R/relay3"),
    Thing("R/relay2"),
    Thing("R/relay1"),
    Thing("R/relay9"),
    Thing("R/relay10"),
    Thing("R/relay11"),
    Thing("R/relay12"),
    Thing("B4/SW1/GB"),
    Thing("B4/SW1/R"),
    Thing("B4/SW2/GB"),
    Thing("B4/SW2/R"),
    Thing("B3/SW1/GB"),
    Thing("B3/SW1/R"),
    Thing("B3/SW2/GB"),
    Thing("B3/SW2/R"),
    Thing("B2/SW1/GB"),
    Thing("B2/SW1/R"),
    Thing("B2/SW2/GB"),
    Thing("B2/SW2/R"),
    Thing("B1/SW1/GB"),
    Thing("B1/SW1/R"),
    Thing("B1/SW2/GB"),
    Thing("B1/SW2/R"),
    # logic
    Thing("version", cb_in=version.req_version),
    Thing("lights/1/1", cb_in=phy_interface.on_data_received),
    Thing("lights/1/2", cb_in=phy_interface.on_data_received),
    Thing("lights/2/1", cb_in=phy_interface.on_data_received),
    Thing("rollo/1", cb_in=phy_interface.on_data_received),
    Thing("rollo/2", cb_in=phy_interface.on_data_received),
)


def get_thing_from_path(path):
    for thing in things:
        if path == thing.path:
            return thing
    return None


def get_thing_from_alias(alias):
    for thing in things:
        if alias == thing.alias:
            return thing
    return None


def send_msg_req(t, data):
    if t.ignore_duplicates_out:
        if data != t.data:
            t.dirty_out = True
    else:
        t.dirty_out = True
    t.data = data


def on_sensor_state_change_callback(alias, data):
    t = get_thing_from_alias(alias)
    if t is not None:
        send_msg_req(t, data)


def on_mqtt_message_received_callback(path, msg):
    t = get_thing_from_path(path)
    if t is not None:
        if t.ignore_duplicates_in:
            if msg != t.data:
                t.dirty_in = True
        else:
            t.dirty_in = True
        t.data = msg


def init():
    print("[THINGS]: init")
    sensors.register_on_state_change_callback(on_sensor_state_change_callback)
    power_counter.register_on_state_change_callback(on_sensor_state_change_callback)
    mqtt.register_on_message_received_callback(on_mqtt_message_received_callback)


async def handle_msg_reqs():
    for t in things:
        if t.dirty_out:
            t.dirty_out = False
            if t.cb_out is not None:
                t.cb_out(t)
            await mqtt.send_message(t.path, str(t.data))
        if t.dirty_in:
            t.dirty_in = False
            if t.cb_in is not None:
                t.cb_in(t)


async def loop_async():
    print("[SYNC]: loop async")
    while True:
        await handle_msg_reqs()
        await asyncio.sleep(0)
