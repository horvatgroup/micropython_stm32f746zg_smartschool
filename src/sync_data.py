import uasyncio as asyncio
import buttons
import mqtt
import sensors
import leds
import things
import lighting
import power_counter
import version


def on_button_state_change_callback(hw, state):
    thing = things.get_thing_from_hw(hw)
    if thing:
        things.set_state(thing, state, soft=True)
        lighting.check_button_logic()


def on_sensor_state_change_callback(hw, state, sync_out_force_update=False):
    thing = things.get_thing_from_hw(hw)
    if thing:
        things.set_state(thing, state, soft=True, sync_out_force_update=sync_out_force_update)


def on_mqtt_message_received_callback(path, state):
    things.set_in_remote_state(path, state)


async def on_thing_sync_out(thing):
    await mqtt.send_message(thing.out_path, str(thing.out_remote_state))


def on_thing_sync_in(thing):
    leds.set_state_by_name(thing.hw, thing.state)


# TODO: handle this somewhere appropriate
def on_thing_remote_in(thing):
    lighting.check_inverted_lights()
    lighting.handle_external_blinds_control(thing)


def init():
    print("[SYNC]: init")
    things.register_on_remote_in_cb_using_hw("VERSION", version.send_version)
    version.send_version(None)
    buttons.register_on_state_change_callback(on_button_state_change_callback)
    sensors.register_on_state_change_callback(on_sensor_state_change_callback)
    power_counter.register_on_state_change_callback(on_sensor_state_change_callback)
    mqtt.register_on_message_received_callback(on_mqtt_message_received_callback)
    things.register_on_thing_sync_out(on_thing_sync_out)
    things.register_on_thing_sync_in(on_thing_sync_in)


async def sync_things():
    for thing in things.things:
        if thing.out_path and thing.sync_out and mqtt.is_connected():
            await things.sync_out_remote_state(thing)
        await asyncio.sleep(0)
        if thing.in_path and thing.sync_in:
            things.sync_in_remote_state(thing)
        await asyncio.sleep(0)


async def loop_async():
    print("[SYNC]: loop async")
    lighting.check_init_lights()
    while True:
        await sync_things()
        await asyncio.sleep(0)
