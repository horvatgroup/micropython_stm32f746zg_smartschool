import common
import bme680
import pins
import bh1750fvi
import mhz19b

sensors = []


class Radar:
    def __init__(self, pin, timeout=3000, on_change=None):
        self.input = common.create_input(pin)
        self.timestamp = 0
        self.timeout = timeout
        self.on_change = on_change
        self.data = 2 # data is binary

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
        self.sensor = bme680.BME680_I2C(i2c)
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

    def read(self):
        data = self.sensor.read()
        for key in data:
            diff = abs(data[key] - self.data[key])
            if diff != 0 and diff > self.diff[key]:
                self.data[key] = data[key]
                if self.on_change:
                    self.on_change({key: self.data[key]})

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
        data = bh1750fvi.sample(self.i2c)
        diff = abs(data - self.data)
        if diff != 0 and diff > self.diff:
            self.data = data
            if self.on_change:
                self.on_change({"light": self.data})

    def loop(self):
        if common.millis_passed(self.timestamp) >= self.timeout:
            self.timestamp = common.get_millis()
            self.read()


class Co2:
    def __init__(self, uart, timeout=3000, on_change=None):
        self.sensor = mhz19b.MHZ19BSensor(uart)
        self.timestamp = 0
        self.timeout = timeout
        self.on_change = on_change
        self.data = 0
        self.diff = 1

    def read(self):
        data = self.sensor.measure()
        if data:
            diff = abs(data - self.data)
            if diff != 0 and diff > self.diff:
                self.data = data
                if self.on_change:
                    self.on_change({"co2": self.data})

    def loop(self):
        if common.millis_passed(self.timestamp) >= self.timeout:
            self.timestamp = common.get_millis()
            self.read()


class SignalLed:
    def __init__(self, pin, timeout=3000, default_state=False):
        self.output = common.create_output(pin)
        self.output.value(False)
        self.timestamp = 0
        self.timeout = timeout

    def set_state(self, state):
        self.output = state

    def loop(self):
        if common.millis_passed(self.timestamp) >= self.timeout:
            self.timestamp = common.get_millis()
            self.output.value(not self.output.value())


def init():
    global sensors
    s1_i2c = common.create_i2c(pins.S1_SCL_BUF_I2C_1, pins.S1_SDA_BUF_I2C_1)
    #s1_uart = common.create_uart(pins.S1_UART5)
    #sensors.append(Radar(pins.S1_RADAR_SIG, on_change=lambda x: print("S1:", x)))
    #sensors.append(Environment(s1_i2c, on_change=lambda x: print("S1:", x)))
    #sensors.append(Light(s1_i2c, on_change=lambda x: print("S1:", x)))
    #sensors.append(Co2(s1_uart, on_change=lambda x: print("S1:", x)))
    sensors.append(SignalLed(pins.S1_SIGNAL_LED))

    #s2_i2c = common.create_i2c(pins.S2_SCL_BUF_I2C_2, pins.S2_SDA_BUF_I2C_2)
    #s2_uart = common.create_uart(pins.S2_UART2)
    #sensors.append(Radar(pins.S2_RADAR_SIG, on_change=lambda x: print("S2:", x)))
    #sensors.append(Environment(s2_i2c, on_change=lambda x: print("S2:", x)))
    #sensors.append(Light(s2_i2c, on_change=lambda x: print("S2:", x)))
    #sensors.append(Co2(s2_uart, on_change=lambda x: print("S2:", x)))
    #sensors.append(SignalLed(pins.S2_SIGNAL_LED))


def loop():
    for sensor in sensors:
        sensor.loop()
        
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