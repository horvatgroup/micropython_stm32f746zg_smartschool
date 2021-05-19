import common
import bme680
import pins

radar_signal_pin = None
radar_signal_state = 0
radar_signal_timestamp = 0
env_sensor = None
env_sensor_timestamp = 0
env_sensor_timeout = 3000


def radar_init():
    global radar_signal_pin
    radar_signal_pin = common.create_input(pins.S2_RADAR_SIG)


def env_sensor_init():
    global env_sensor
    env_sensor = bme680.BME680_I2C(common.create_i2c(pins.S2_SCL_BUF, pins.S2_SDA_BUF))


def check_radar():
    global radar_signal_state, radar_signal_timestamp
    state = radar_signal_pin.value()
    if state != radar_signal_state:
        radar_signal_state = state
        print("RADAR:[%d] %d" % (state, common.millis_passed(radar_signal_timestamp)))
        radar_signal_timestamp = common.get_millis()


def check_env():
    if common.millis_passed(env_sensor_timestamp) >= env_sensor_timeout:
        env_sensor_timestamp = common.get_millis()
        print(env_sensor.read())


def init():
    radar_init()
    env_sensor_init()


def loop():
    check_radar()
    check_env()
