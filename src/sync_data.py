import buttons
import mqtt
import sensors
import leds

remote_path = {
    # inputs
    "ONBOARD_BUTTON": "out/test/button1",
    "B1_SW1": "out/B4/SW1",
    "B1_SW2": "out/B4/SW2",
    "B2_SW1": "out/B3/SW1",
    "B2_SW2": "out/B3/SW2",
    "B3_SW1": "out/B2/SW1",
    "B3_SW2": "out/B2/SW2",
    "B4_SW1": "out/B1/SW1",
    "B4_SW2": "out/B1/SW2",
    # sensors
    "S1_RADAR": "out/S2/radar",
    "S1_TEMPERATURE": "out/S2/temperature",
    "S1_PRESSURE": "out/S2/pressure",
    "S1_GAS": "out/S2/gas",
    "S1_ALTITUDE": "out/S2/altitude",
    "S1_HUMIDITY": "out/S2/humidity",
    "S1_LIGHT": "out/S2/light",
    "S1_CO2": "out/S1/co2",
    "S2_RADAR": "out/S1/radar",
    "S2_TEMPERATURE": "out/S1/temperature",
    "S2_PRESSURE": "out/S1/pressure",
    "S2_GAS": "out/S1/gas",
    "S2_ALTITUDE": "out/S1/altitude",
    "S2_HUMIDITY": "out/S1/humidity",
    "S2_LIGHT": "out/S1/light",
    "S2_CO2": "out/S2/co2",
    # outputs
    "ONBOARD_LED1": "in/test/led1",
    "ONBOARD_LED2": "in/test/led2",
    "ONBOARD_LED3": "in/test/led3",
    "RELAY_1": "in/R/relay8",
    "RELAY_2": "in/R/relay7",
    "RELAY_3": "in/R/relay6",
    "RELAY_4": "in/R/relay5",
    "RELAY_5": "in/R/relay4",
    "RELAY_6": "in/R/relay3",
    "RELAY_7": "in/R/relay2",
    "RELAY_8": "in/R/relay1",
    "RELAY_9": "in/R/relay9",
    "RELAY_10": "in/R/relay10",
    "RELAY_11": "in/R/relay11",
    "RELAY_12": "in/R/relay12",
    "B1_LED1_GB": "in/B4/SW1/GB",
    "B1_LED1_R": "in/B4/SW1/R",
    "B1_LED2_GB": "in/B4/SW2/GB",
    "B1_LED2_R": "in/B4/SW2/R",
    "B2_LED1_GB": "in/B3/SW1/GB",
    "B2_LED1_R": "in/B3/SW1/R",
    "B2_LED2_GB": "in/B3/SW2/GB",
    "B2_LED2_R": "in/B3/SW2/R",
    "B3_LED1_GB": "in/B2/SW1/GB",
    "B3_LED1_R": "in/B2/SW1/R",
    "B3_LED2_GB": "in/B2/SW2/GB",
    "B3_LED2_R": "in/B2/SW2/R",
    "B4_LED1_GB": "in/B1/SW1/GB",
    "B4_LED1_R": "in/B1/SW1/R",
    "B4_LED2_GB": "in/B1/SW2/GB",
    "B4_LED2_R": "in/B1/SW2/R",
    "RELAY_1_OUT": "out/R/relay8",
    "RELAY_2_OUT": "out/R/relay7",
    "RELAY_3_OUT": "out/R/relay6",
    "RELAY_4_OUT": "out/R/relay5",
    "RELAY_5_OUT": "out/R/relay4",
    "RELAY_6_OUT": "out/R/relay3",
    "RELAY_7_OUT": "out/R/relay2",
    "RELAY_8_OUT": "out/R/relay1",
    "RELAY_9_OUT": "out/R/relay9",
    "RELAY_10_OUT": "out/R/relay10",
    "RELAY_11_OUT": "out/R/relay11",
    "RELAY_12_OUT": "out/R/relay12",
}


def on_button_state_change_callback(name, state):
    topic = remote_path[name]
    mqtt.send_message(topic, str(state))
    if (name == "B1_SW1" and state == 1):
        leds.set_state_by_name("RELAY_1", 1)
    elif (name == "B1_SW2" and state == 1):
        leds.set_state_by_name("RELAY_2", 0)


def on_sensor_state_change_callback(name, state):
    topic = remote_path[name]
    mqtt.send_message(topic, str(state))


def on_mqtt_message_received_callback(topic, msg):
    try:
        name = get_key(topic)
        state = int(msg)
        leds.set_state_by_name(name, state)
    except Exception as e:
        print("[SYNC_DATA]: message not implemented with %s" % (e))


def get_key(val):
    for key, value in remote_path.items():
        if val == value:
            return key
    return None


def init():
    buttons.register_on_state_change_callback(on_button_state_change_callback)
    sensors.register_on_state_change_callback(on_sensor_state_change_callback)
    mqtt.register_on_message_received_callback(on_mqtt_message_received_callback)