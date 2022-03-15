import uasyncio as asyncio
import common
import driver_bme680
import common_pins
import driver_bh1750fvi
import driver_mhz19b

environment_sensors = []
realtime_sensors = []
on_state_change_cb = None


def get_diff(first, second):
    if (first >= 0 and second >= 0) or (first < 0 and second < 0):
        return abs(first - second)
    else:
        return abs(first) + abs(second)


class Radar:
    def __init__(self, pin, timeout=3, on_change=None, name="RADAR", sensor_board=""):
        self.input = common.create_input(pin)
        self.biggest = 0
        self.on_change = on_change
        self.name = name
        self.sensor_board = sensor_board
        self.data = -1  # data is binary
        self.timeout = timeout

    def read(self):
        data = self.input.value()
        if data != self.data:
            self.data = data
            if self.on_change:
                self.on_change(self.get_name(), data)

    def loop(self):
        self.read()

    def get_name(self):
        if self.sensor_board:
            return "%s_%s" % (self.sensor_board, self.name)
        else:
            return self.name


class Environment:
    def __init__(self, i2c, timeout=3, on_change=None, name="ENV", sensor_board=""):
        self.i2c = i2c
        self.sensor = None
        self.biggest = 0
        self.on_change = on_change
        self.name = name
        self.sensor_board = sensor_board
        self.data = {}
        self.data['TEMPERATURE'] = 0
        self.data['PRESSURE'] = 0
        self.data['GAS'] = 0
        self.data['ALTITUDE'] = 0
        self.data['HUMIDITY'] = 0
        self.diff = {}
        self.diff['TEMPERATURE'] = 0.5
        self.diff['PRESSURE'] = 3.0
        self.diff['GAS'] = 5000
        self.diff['ALTITUDE'] = 100.0
        self.diff['HUMIDITY'] = 3.0
        self.disable_error_print = False
        self.diff_timeout = 120 * 60000
        self.diff_timestamp = {}
        self.diff_timestamp['TEMPERATURE'] = 0
        self.diff_timestamp['PRESSURE'] = 0
        self.diff_timestamp['GAS'] = 0
        self.diff_timestamp['ALTITUDE'] = 0
        self.diff_timestamp['HUMIDITY'] = 0
        self.timeout = timeout

    def get_sensor(self):
        if self.sensor != None:
            return self.sensor
        else:
            try:
                self.sensor = driver_bme680.BME680_I2C(self.i2c)
                return self.sensor
            except Exception as e:
                if not self.disable_error_print:
                    print("[SENSORS]: ERROR @ %s get_sensor with %s" % (self.get_name(), e))
                    self.disable_error_print = True
                self.sensor = None
                return None

    def read(self):
        if self.get_sensor() != None:
            try:
                data = self.get_sensor().read()
                self.disable_error_print = False
                for key in data:
                    force_send = self.diff_timestamp[key] == 0 or (common.millis_passed(self.diff_timestamp[key]) >= self.diff_timeout)
                    diff = get_diff(data[key], self.data[key])
                    if (diff != 0 and diff > self.diff[key]) or force_send:
                        self.data[key] = data[key]
                        self.diff_timestamp[key] = common.get_millis()
                        if self.on_change:
                            self.on_change("%s_%s" % (self.get_name(), key), self.data[key])
            except Exception as e:
                print("[SENSORS]: ERROR @ %s read with %s" % (self.get_name(), e))
                self.sensor = None

    def loop(self):
        self.read()

    def get_name(self):
        if self.sensor_board:
            return "%s_%s" % (self.sensor_board, self.name)
        else:
            return self.name


class Light:
    def __init__(self, i2c, timeout=3, on_change=None, name="LIGHT", sensor_board=""):
        self.i2c = i2c
        self.timeout = timeout
        self.biggest = 0
        self.on_change = on_change
        self.name = name
        self.sensor_board = sensor_board
        self.data = 0
        self.diff = 50
        self.disable_error_print = False
        self.diff_timeout = 120 * 60000
        self.diff_timestamp = 0

    def read(self):
        try:
            data = driver_bh1750fvi.sample(self.i2c)
            self.disable_error_print = False
            force_send = self.diff_timestamp == 0 or (common.millis_passed(self.diff_timestamp) >= self.diff_timeout)
            diff = get_diff(data, self.data)
            if (diff != 0 and diff > self.diff) or force_send:
                self.data = data
                self.diff_timestamp = common.get_millis()
                if self.on_change:
                    self.on_change(self.get_name(), self.data)
        except Exception as e:
            if not self.disable_error_print:
                print("[SENSORS]: ERROR @ %s with %s" % (self.get_name(), e))
                self.disable_error_print = True

    def loop(self):
        self.read()

    def get_name(self):
        if self.sensor_board:
            return "%s_%s" % (self.sensor_board, self.name)
        else:
            return self.name


class Co2:
    def __init__(self, uart, timeout=3, on_change=None, name="CO2", sensor_board=""):
        self.uart = uart
        self.sensor = None
        self.timeout = timeout
        self.biggest = 0
        self.on_change = on_change
        self.name = name
        self.sensor_board = sensor_board
        self.data = 0
        self.diff = 100
        self.disable_error_print = False
        self.diff_timeout = 120 * 60000
        self.diff_timestamp = 0

    def get_sensor(self):
        if self.sensor != None:
            return self.sensor
        else:
            try:
                self.sensor = driver_mhz19b.MHZ19BSensor(self.uart)
                return self.sensor
            except Exception as e:
                print("[SENSORS]: ERROR @ %s get_sensor with %s" % (self.get_name(), e))
                self.sensor = None
                return None

    def read(self):
        if self.get_sensor() != None:
            try:
                data = self.get_sensor().measure()
                self.disable_error_print = False
                if data:
                    force_send = self.diff_timestamp == 0 or (common.millis_passed(self.diff_timestamp) >= self.diff_timeout)
                    diff = get_diff(data, self.data)
                    if (diff != 0 and diff > self.diff) or force_send:
                        self.data = data
                        self.diff_timestamp = common.get_millis()
                        if self.on_change:
                            self.on_change(self.get_name(), self.data)
            except Exception as e:
                if not self.disable_error_print:
                    print("[SENSORS]: ERROR @ %s read with %s" % (self.get_name(), e))
                    self.disable_error_print = True
                self.sensor = None

    def loop(self):
        self.read()

    def is_available(self):
        return True

    def get_name(self):
        if self.sensor_board:
            return "%s_%s" % (self.sensor_board, self.name)
        else:
            return self.name


def publish_results(name, data):
    print("[SENSORS]: %s -> %s" % (name, str(data)))
    if on_state_change_cb != None:
        on_state_change_cb(name, data)


def register_on_state_change_callback(cb):
    global on_state_change_cb
    print("[SENSORS]: register on state change cb")
    on_state_change_cb = cb


def init():
    print("[SENSORS]: init")
    global environment_sensors, realtime_sensors
    s1_i2c = common.create_i2c(common_pins.S1_SCL_BUF_I2C_1.id, common_pins.S1_SDA_BUF_I2C_1.id)
    s1_uart = common.create_uart(common_pins.S1_UART5.id)
    realtime_sensors.append(Radar(common_pins.S1_RADAR_SIG.id, on_change=lambda x, y: publish_results(x, y), sensor_board="S1"))
    environment_sensors.append(Environment(s1_i2c, on_change=lambda x, y: publish_results(x, y), sensor_board="S1"))
    environment_sensors.append(Light(s1_i2c, on_change=lambda x, y: publish_results(x, y), sensor_board="S1"))
    environment_sensors.append(Co2(s1_uart, on_change=lambda x, y: publish_results(x, y), sensor_board="S1"))

    s2_i2c = common.create_i2c(common_pins.S2_SCL_BUF_I2C_2.id, common_pins.S2_SDA_BUF_I2C_2.id)
    s2_uart = common.create_uart(common_pins.S2_UART2.id)
    realtime_sensors.append(Radar(common_pins.S2_RADAR_SIG.id, on_change=lambda x, y: publish_results(x, y), sensor_board="S2"))
    environment_sensors.append(Environment(s2_i2c, on_change=lambda x, y: publish_results(x, y), sensor_board="S2"))
    environment_sensors.append(Light(s2_i2c, on_change=lambda x, y: publish_results(x, y), sensor_board="S2"))
    environment_sensors.append(Co2(s2_uart, on_change=lambda x, y: publish_results(x, y), sensor_board="S2"))


async def environment_sensors_action():
    print("[SENSORS]: environment_sensors_action")
    while True:
        for sensor in environment_sensors:
            timestamp = common.get_millis()
            sensor.loop()
            timepassed = common.millis_passed(timestamp)
            if timepassed >= sensor.timeout:
                if timepassed > sensor.biggest:
                    sensor.biggest = timepassed
                print("[%s]: timeout warning %d ms with biggest %d" % (sensor.get_name(), timepassed, sensor.biggest))
            await asyncio.sleep(0)
        await asyncio.sleep(60)


async def realtime_sensors_action():
    print("[SENSORS]: realtime_sensors_action")
    while True:
        for sensor in realtime_sensors:
            timestamp = common.get_millis()
            sensor.loop()
            timepassed = common.millis_passed(timestamp)
            if timepassed >= sensor.timeout:
                if timepassed > sensor.biggest:
                    sensor.biggest = timepassed
                print("[%s]: timeout warning %d ms with biggest %d" % (sensor.get_name(), timepassed, sensor.biggest))
            await asyncio.sleep(0)


async def test_add_tasks():
    print("[SENSORS]: test_add_tasks")
    tasks = []
    tasks.append(asyncio.create_task(realtime_sensors_action()))
    tasks.append(asyncio.create_task(environment_sensors_action()))
    for task in tasks:
        await task
        print("[RUNNER]: Error: loop task finished!")


def test_start():
    print("[RUNNER]: test_start")
    init()
    asyncio.run(test_add_tasks())
