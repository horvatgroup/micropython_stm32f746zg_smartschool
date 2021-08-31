import buttons
import mqtt
import sensors
import leds

remote_path = {
    # inputs
    "ONBOARD_BUTTON": "test/button1",
    "B1_SW1": "room1/button1",
    "B1_SW2": "room1/button2",
    "B2_SW1": "room1/button3",
    "B2_SW2": "room1/button4",
    "B3_SW1": "room2/button1",
    "B3_SW2": "room2/button2",
    "B4_SW1": "room2/button3",
    "B4_SW2": "room2/button4",
    # sensors
    "S1_RADAR": "room1/radar",
    "S1_TEMPERATURE": "room1/temperature",
    "S1_PRESSURE": "room1/pressure",
    "S1_GAS": "room1/gas",
    "S1_ALTITUDE": "room1/altitude",
    "S1_HUMIDITY": "room1/humidity",
    "S1_LIGHT": "room1/light",
    "S2_RADAR": "room2/radar",
    "S2_TEMPERATURE": "room2/temperature",
    "S2_PRESSURE": "room2/pressure",
    "S2_GAS": "room2/gas",
    "S2_ALTITUDE": "room2/altitude",
    "S2_HUMIDITY": "room2/humidity",
    "S2_LIGHT": "room2/light",
    # outputs
    "ONBOARD_LED1": "test/led1",
    "ONBOARD_LED2": "test/led2",
    "ONBOARD_LED3": "test/led3",
    "RELAY_1": "room2/relay4",
    "RELAY_2": "room2/relay3",
    "RELAY_3": "room2/relay2",
    "RELAY_4": "room2/relay1",
    "RELAY_5": "room1/relay4",
    "RELAY_6": "room1/relay3",
    "RELAY_7": "room1/relay2",
    "RELAY_8": "room1/relay1",
    "RELAY_9": "room1/relay5",
    "RELAY_10": "room1/relay6",
    "RELAY_11": "room2/relay5",
    "RELAY_12": "room2/relay6",
    "B1_LED1_GB": "room1/button1_led1",
    "B1_LED1_R": "room1/button1_led2",
    "B1_LED2_GB": "room1/button2_led1",
    "B1_LED2_R": "room1/button2_led2",
    "B2_LED1_GB": "room1/button3_led1",
    "B2_LED1_R": "room1/button3_led2",
    "B2_LED2_GB": "room1/button4_led1",
    "B2_LED2_R": "room1/button4_led2",
    "B3_LED1_GB": "room2/button1_led1",
    "B3_LED1_R": "room2/button1_led2",
    "B3_LED2_GB": "room2/button2_led1",
    "B3_LED2_R": "room2/button2_led2",
    "B4_LED1_GB": "room2/button3_led1",
    "B4_LED1_R": "room2/button3_led2",
    "B4_LED2_GB": "room2/button4_led1",
    "B4_LED2_R": "room2/button4_led2",
}


def on_button_state_change_callback(name, state):
    topic = remote_path[name]
    mqtt.send_message(topic, str(state))


def on_sensor_state_change_callback(name, state):
    topic = remote_path[name]
    mqtt.send_message(topic, str(state))


def on_mqtt_message_received_callback(topic, msg):
    name = get_key(topic)
    state = int(msg)
    leds.set_state_by_name(name, state)


def get_key(val):
    for key, value in remote_path.items():
        if val == value:
            return key
    return None


def init():
    buttons.register_on_state_change_callback(on_button_state_change_callback)
    sensors.register_on_state_change_callback(on_sensor_state_change_callback)
    mqtt.register_on_message_received_callback(on_mqtt_message_received_callback)


def test():
    buttons.init()
    sensors.init()
    leds.init()
    mqtt.init()
    init()
    while True:
        buttons.loop()
        sensors.loop()
        mqtt.loop()
