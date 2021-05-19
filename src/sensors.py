import common
import bme680
import pins
import bh1750fvi

radar_signal_pin = None
radar_signal_state = 0
radar_signal_timestamp = 0
i2c = None
env_sensor = None
env_sensor_timestamp = 0
env_sensor_timeout = 3000
light_sensor_timestamp = 0
light_sensor_timeout = 5000


def radar_init():
    global radar_signal_pin
    radar_signal_pin = common.create_input(pins.S2_RADAR_SIG)


def env_sensor_init():
    global env_sensor
    env_sensor = bme680.BME680_I2C(i2c)
    
def light_sensor_init():
    pass


def check_radar():
    global radar_signal_state, radar_signal_timestamp
    state = radar_signal_pin.value()
    if state != radar_signal_state:
        radar_signal_state = state
        print("RADAR:[%d] %d" % (state, common.millis_passed(radar_signal_timestamp)))
        radar_signal_timestamp = common.get_millis()


def check_env():
    global env_sensor_timestamp
    if common.millis_passed(env_sensor_timestamp) >= env_sensor_timeout:
        env_sensor_timestamp = common.get_millis()
        print(env_sensor.read())


def check_light_sensor():
    global light_sensor_timestamp
    if common.millis_passed(light_sensor_timestamp) >= light_sensor_timeout:
        light_sensor_timestamp = common.get_millis()
        result = bh1750fvi.sample(i2c) # in lux
        print("Light sensor: %f" % (result))
    

def init():
    global i2c
    i2c = common.create_i2c(pins.S2_SCL_BUF, pins.S2_SDA_BUF)
    print("I2C devices:")
    for device in i2c.scan():
        print("  0x%02X" % (device))
    radar_init()
    env_sensor_init()
    light_sensor_init()


def loop():
    check_radar()
    check_env()
    check_light_sensor()
