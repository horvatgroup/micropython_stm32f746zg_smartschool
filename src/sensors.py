import uasyncio as asyncio
import common
import driver_bme680
import common_pins
import driver_bh1750fvi
import driver_mhz19b

sensors = []
on_state_change_cb = None


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
                self.on_change({"RADAR": data})

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
        self.data['TEMPERATURE'] = 0.0
        self.data['PRESSURE'] = 0.0
        self.data['GAS'] = 0
        self.data['ALTITUDE'] = 0.0
        self.data['HUMIDITY'] = 0.0
        self.diff = {}
        self.diff['TEMPERATURE'] = 1.0
        self.diff['PRESSURE'] = 0.1
        self.diff['GAS'] = 1
        self.diff['ALTITUDE'] = 0.1
        self.diff['HUMIDITY'] = 0.1
        self.disable_error_print = False

    def get_sensor(self):
        if self.sensor != None:
            return self.sensor
        else:
            try:
                self.sensor = driver_bme680.BME680_I2C(self.i2c)
                return self.sensor
            except Exception as e:
                if not self.disable_error_print:
                    print("[SENSORS]: ERROR @ Environment get_sensor with %s" % (e))
                    self.disable_error_print = True
                self.sensor = None
                return None

    def read(self):
        if self.get_sensor() != None:
            try:
                data = self.get_sensor().read()
                self.disable_error_print = False
                for key in data:
                    diff = abs(data[key] - self.data[key])
                    if diff != 0 and diff > self.diff[key]:
                        self.data[key] = data[key]
                        if self.on_change:
                            self.on_change({key: self.data[key]})
            except Exception as e:
                print("[SENSORS]: ERROR @ Environment read with %s" % (e))
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
        self.disable_error_print = False

    def read(self):
        try:
            data = driver_bh1750fvi.sample(self.i2c)
            self.disable_error_print = False
            diff = abs(data - self.data)
            if diff != 0 and diff > self.diff:
                self.data = data
                if self.on_change:
                    self.on_change({"LIGHT": self.data})
        except Exception as e:
            if not self.disable_error_print:
                print("[SENSORS]: ERROR @ Light with %s" % (e))
                self.disable_error_print = True

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
        self.disable_error_print = False

    def get_sensor(self):
        if self.sensor != None:
            return self.sensor
        else:
            try:
                self.sensor = driver_mhz19b.MHZ19BSensor(self.uart)
                return self.sensor
            except Exception as e:
                print("[SENSORS]: ERROR @ Co2 get_sensor with %s" % (e))
                self.sensor = None
                return None

    def read(self):
        if self.get_sensor() != None:
            try:
                data = self.get_sensor().measure()
                self.disable_error_print = False
                if data:
                    diff = abs(data - self.data)
                    if diff != 0 and diff > self.diff:
                        self.data = data
                        if self.on_change:
                            self.on_change({"CO2": self.data})
            except Exception as e:
                if not self.disable_error_print:
                    print("[SENSORS]: ERROR @ Co2 read with %s" % (e))
                    self.disable_error_print = True
                self.sensor = None

    def loop(self):
        if common.millis_passed(self.timestamp) >= self.timeout:
            self.timestamp = common.get_millis()
            self.read()

    def is_available(self):
        return True


def publish_results(sensor_board, data):
    print("[SENSORS]: %s -> %s" % (sensor_board, str(data)))
    if on_state_change_cb != None:
        for d in data:
            topic = "%s_%s" % (sensor_board, d)
            on_state_change_cb(topic, data[d])


def register_on_state_change_callback(cb):
    global on_state_change_cb
    print("[SENSORS]: register on state change cb")
    on_state_change_cb = cb


def init():
    print("[SENSORS]: init")
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

    action()


def action():
    for sensor in sensors:
        sensor.loop()


def test():
    print("[SENSORS]: test")
    init()
    while True:
        action()


def test_async():
    print("[SENSORS]: test_async")
    init()
    asyncio.run(common.loop_async("SENSORS", action))
