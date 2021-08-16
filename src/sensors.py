import common
import driver_bme680
import common_pins
import driver_bh1750fvi
import driver_mhz19b
import sync_data

sensors = []


class Radar:
    def __init__(self, pin, timeout=3000, on_change=None):
        self.input = common.create_input(pin)
        self.timestamp = 0
        self.timeout = timeout
        self.on_change = on_change
        self.data = 2  # data is binary

    def read(self):
        data = self.input.value()
        if data != self.data:
            self.data = data
            if self.on_change:
                self.on_change({"radar": data})

    def loop(self):
        if common.millis_passed(self.timestamp) >= self.timeout:
            self.timestamp = common.get_millis()
            self.read()


class Environment:
    def __init__(self, i2c, timeout=3000, on_change=None):
        self.i2c = i2c
        self.sensor = None
        self.timestamp = 0
        self.timeout = timeout
        self.on_change = on_change
        self.data = {}
        self.data['temperature'] = 0.0
        self.data['pressure'] = 0.0
        self.data['gas'] = 0
        self.data['altitude'] = 0.0
        self.data['humidity'] = 0.0
        self.diff = {}
        self.diff['temperature'] = 1.0
        self.diff['pressure'] = 0.1
        self.diff['gas'] = 1
        self.diff['altitude'] = 0.1
        self.diff['humidity'] = 0.1

    def get_sensor(self):
        if self.sensor != None:
            return self.sensor
        else:
            try:
                self.sensor = driver_bme680.BME680_I2C(self.i2c)
                return self.sensor
            except:
                self.sensor = None
                return None

    def read(self):
        if self.get_sensor() != None:
            try:
                data = self.get_sensor().read()
                for key in data:
                    diff = abs(data[key] - self.data[key])
                    if diff != 0 and diff > self.diff[key]:
                        self.data[key] = data[key]
                        if self.on_change:
                            self.on_change({key: self.data[key]})
            except:
                self.sensor = None

    def loop(self):
        if common.millis_passed(self.timestamp) >= self.timeout:
            self.timestamp = common.get_millis()
            self.read()


class Light:
    def __init__(self, i2c, timeout=3000, on_change=None):
        self.i2c = i2c
        self.timestamp = 0
        self.timeout = timeout
        self.on_change = on_change
        self.data = 0
        self.diff = 1

    def read(self):
        try:
            data = driver_bh1750fvi.sample(self.i2c)
            diff = abs(data - self.data)
            if diff != 0 and diff > self.diff:
                self.data = data
                if self.on_change:
                    self.on_change({"light": self.data})
        except:
            pass

    def loop(self):
        if common.millis_passed(self.timestamp) >= self.timeout:
            self.timestamp = common.get_millis()
            self.read()


class Co2:
    def __init__(self, uart, timeout=3000, on_change=None):
        self.uart = uart
        self.sensor = None
        self.timestamp = 0
        self.timeout = timeout
        self.on_change = on_change
        self.data = 0
        self.diff = 1

    def get_sensor(self):
        if self.sensor != None:
            return self.sensor
        else:
            try:
                self.sensor = driver_mhz19b.MHZ19BSensor(self.uart)
                return self.sensor
            except:
                self.sensor = None
                return None

    def read(self):
        if self.get_sensor() != None:
            try:
                data = self.get_sensor().measure()
                if data:
                    diff = abs(data - self.data)
                    if diff != 0 and diff > self.diff:
                        self.data = data
                        if self.on_change:
                            self.on_change({"co2": self.data})
            except:
                self.sensor = None

    def loop(self):
        if common.millis_passed(self.timestamp) >= self.timeout:
            self.timestamp = common.get_millis()
            self.read()

    def is_available(self):
        return True


def publish_results(sensor_board, data):
    print("%s: %s" % (sensor_board, str(data)))
    for key in data:
        sync_data_name = sensor_board + "_" + key
        sync_data_value = data[key]
        sync_data.set_local_data_out(sync_data_name, sync_data_value)


def init():
    global sensors
    s1_i2c = common.create_i2c(common_pins.S1_SCL_BUF_I2C_1.id, common_pins.S1_SDA_BUF_I2C_1.id)
    s1_uart = common.create_uart(common_pins.S1_UART5.id)
    sensors.append(Radar(common_pins.S1_RADAR_SIG.id, on_change=lambda x: publish_results("S1", x)))
    sensors.append(Environment(s1_i2c, on_change=lambda x: publish_results("S1", x)))
    sensors.append(Light(s1_i2c, on_change=lambda x: publish_results("S1", x)))
    sensors.append(Co2(s1_uart, on_change=lambda x: publish_results("S1", x)))

    s2_i2c = common.create_i2c(common_pins.S2_SCL_BUF_I2C_2.id, common_pins.S2_SDA_BUF_I2C_2.id)
    s2_uart = common.create_uart(common_pins.S2_UART2.id)
    sensors.append(Radar(common_pins.S2_RADAR_SIG.id, on_change=lambda x: publish_results("S2", x)))
    sensors.append(Environment(s2_i2c, on_change=lambda x: publish_results("S2", x)))
    sensors.append(Light(s2_i2c, on_change=lambda x: publish_results("S2", x)))
    sensors.append(Co2(s2_uart, on_change=lambda x: publish_results("S2", x)))


def loop():
    for sensor in sensors:
        sensor.loop()


def test():
    init()
    while True:
        loop()

# S1: {'radar': 1}
# S1: {'temperature': 26.88586}
# S1: {'pressure': 996.904}
# S1: {'gas': 101219}
# S1: {'altitude': 136.9887}
# S1: {'humidity': 30.71368}
# S1: {'light': 50}

# S2: {'radar': 1}
# S2: {'temperature': 34.75129}
# S2: {'pressure': 997.032}
# S2: {'gas': 131553}
# S2: {'altitude': 135.9106}
# S2: {'humidity': 27.13816}
# S2: {'light': 10}
# S2: {'co2': 1478}
