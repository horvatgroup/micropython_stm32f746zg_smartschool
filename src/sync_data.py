import buttons
import mqtt
import sensors
import leds
import eventor, events





# def on_sensor_state_change_callback(name, state):
#     topic = remote_path[name]
#     mqtt.send_message(topic, str(state))
#
#
# def on_mqtt_message_received_callback(topic, msg):
#     try:
#         name = get_key(topic)
#         state = int(msg)
#         leds.set_state_by_name(name, state)
#     except Exception as e:
#         print("[SYNC_DATA]: message not implemented with %s" % (e))
#




def init():
    pass
    # sensors.register_on_state_change_callback(on_sensor_state_change_callback)
    # mqtt.register_on_message_received_callback(on_mqtt_message_received_callback)
