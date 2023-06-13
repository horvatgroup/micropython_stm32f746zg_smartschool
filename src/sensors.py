import uasyncio as asyncio
import common
import driver_bme680
import common_pins
import driver_bh1750fvi
import driver_mhz19b
import onewire, ds18x20

environment_sensors = []
realtime_sensors = []
on_state_change_cb = None


class Radar:
    def __init__(self, pin, alias):
        self.input_pin = common.create_input(pin)
        self.alias = alias
        self.data = None
        self.dirty = False

    def action(self):
        data = self.input_pin.value()
        if data != self.data:
            self.data = data
            self.dirty = True


class Environment:
    def __init__(self, i2c, alias):
        self.i2c = i2c
        self.alias = alias
        self.sensor = None
        self.data = None
        self.dirty = False
        self.error_msg = None
        self.timestamp = None
        self.timeout = 60 * 1000

    def get_sensor(self):
        if self.sensor is None:
            try:
                self.sensor = driver_bme680.BME680_I2C(self.i2c)
            except Exception as e:
                print("[SENSORS]: ERROR @ %s get_sensor with %s" % (self.alias, e))
                self.error_msg = e
                self.sensor = None
        return self.sensor

    async def action(self):
        if self.get_sensor() is not None:
            try:
                self.data = self.get_sensor().read()
                self.dirty = True
            except Exception as e:
                print("[SENSORS]: ERROR @ %s read with %s" % (self.alias, e))
                self.error_msg = e
                self.sensor = None


class Light:
    def __init__(self, i2c, alias):
        self.i2c = i2c
        self.alias = alias
        self.data = None
        self.dirty = False
        self.error_msg = None
        self.timestamp = None
        self.timeout = 60 * 1000

    async def action(self):
        try:
            self.data = await driver_bh1750fvi.sample(self.i2c)
            self.dirty = True
        except Exception as e:
            print("[SENSORS]: ERROR @ %s with %s" % (self.alias, e))
            self.error_msg = e


class Co2:
    def __init__(self, uart_pin, alias):
        self.uart_pin = uart_pin
        self.uart = common.create_uart(self.uart_pin)
        self.reinit_uart = False
        self.alias = alias
        self.sensor = driver_mhz19b.MHZ19BSensor()
        self.data = None
        self.dirty = False
        self.error_msg = None
        self.timestamp = None
        self.timeout = 60 * 1000

    async def action(self):
        try:
            if self.reinit_uart:
                self.reinit_uart = False
                self.uart.deinit()
                self.uart.init(baudrate=9600)
            self.data = await self.sensor.measure(self.uart)
            if self.data is not None:
                self.dirty = True
            else:
                print("[SENSORS]: ERROR @ %s received None" % (self.alias))
                self.error_msg = "received None"
                self.reinit_uart = True
        except Exception as e:
            print("[SENSORS]: ERROR @ %s read with %s" % (self.alias, e))
            self.error_msg = e
            self.reinit_uart = True

class DsTempReader:
    def __init__(self, ds_pin, alias):
        self.ds_pin = ds_pin
        self.alias = alias
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(self.ds_pin))
        self.data = []
        self.error_msg = None
        self.timestamp = None
        self.timeout = 60 * 1000

    def get_name(self, rom):
        return ''.join(struct.pack('B', x).hex() for x in rom)

    async def action(self):
        try:
            roms = self.ds_sensor.scan()
            self.ds_sensor.convert_temp()
            await asyncio.sleep_ms(750)
            for rom in roms:
                temp = self.ds_sensor.read_temp(rom)
                print(self.get_name(rom), temp)
        except Exception as e:
            print("[SENSORS]: ERROR @ %s read with %s" % (self.alias, e))
            self.error_msg = e


def register_on_state_change_callback(cb):
    global on_state_change_cb
    print("[SENSORS]: register on state change cb")
    on_state_change_cb = cb


def init():
    print("[SENSORS]: init")
    global environment_sensors, realtime_sensors
    s1_i2c = common.create_i2c(common_pins.S1_SCL_BUF_I2C_1.id, common_pins.S1_SDA_BUF_I2C_1.id)
    realtime_sensors.append(Radar(common_pins.S1_RADAR_SIG.id, alias="S1_RADAR"))
    environment_sensors.append(Environment(s1_i2c, alias="S1_ENV"))
    environment_sensors.append(Light(s1_i2c, alias="S1_LIGHT"))
    environment_sensors.append(Co2(common_pins.S1_UART5.id, alias="S1_CO2"))

    s2_i2c = common.create_i2c(common_pins.S2_SCL_BUF_I2C_2.id, common_pins.S2_SDA_BUF_I2C_2.id)
    #realtime_sensors.append(Radar(common_pins.S2_RADAR_SIG.id, alias="S2_RADAR"))
    environment_sensors.append(DsTempReader(common_pins.S2_RADAR_SIG.id, alias="S2_DSTEPM"))
    environment_sensors.append(Environment(s2_i2c, alias="S2_ENV"))
    environment_sensors.append(Light(s2_i2c, alias="S2_LIGHT"))
    environment_sensors.append(Co2(common_pins.S2_UART2.id, alias="S2_CO2"))


async def environment_sensors_action():
    print("[SENSORS]: environment_sensors_action")
    while True:
        for sensor in environment_sensors:
            if sensor.timestamp is None or common.millis_passed(sensor.timestamp) >= sensor.timeout:
                sensor.timestamp = common.get_millis()
                await sensor.action()
                if sensor.dirty:
                    sensor.dirty = False
                    if "_ENV" in sensor.alias:
                        for key in sensor.data:
                            if on_state_change_cb is not None:
                                on_state_change_cb(f"{sensor.alias}_{key}", sensor.data[key])
                    else:
                        if on_state_change_cb is not None:
                            on_state_change_cb(sensor.alias, sensor.data)

                if sensor.error_msg is not None:
                    if on_state_change_cb is not None:
                        on_state_change_cb(f"{sensor.alias}_ERROR", sensor.error_msg)
                    sensor.error_msg = None
            await asyncio.sleep_ms(0)


async def realtime_sensors_action():
    print("[SENSORS]: realtime_sensors_action")
    while True:
        for sensor in realtime_sensors:
            sensor.action()
            if sensor.dirty:
                sensor.dirty = False
                if on_state_change_cb is not None:
                    on_state_change_cb(sensor.alias, sensor.data)
        await asyncio.sleep_ms(0)


def on_data_request(thing):
    print("[SENSORS]: on_data_request[%s][%s]" % (thing.alias, thing.data))
    for sensor in environment_sensors:
        if sensor.alias == thing.alias:
            if thing.data == "request":
                print(f"[SENSORS]: request {sensor.alias} data")
                sensor.timestamp = None
            elif "timeout" in thing.data:
                try:
                    sensor.timeout = int(thing.data.split(" ")[1])
                except Exception as e:
                    print("[SENSORS]: Error: timeout with %s" % (e))


def test_print(alias, data):
    print("[SENSORS]: CB -- alias[%s], data[%s]" % (alias, data))


async def test_add_tasks():
    print("[SENSORS]: test_add_tasks")
    tasks = []
    tasks.append(asyncio.create_task(realtime_sensors_action()))
    tasks.append(asyncio.create_task(environment_sensors_action()))
    for task in tasks:
        await task
        print("[SENSORS]: Error: loop task finished!")


def test_start():
    print("[SENSORS]: test_start")
    init()
    register_on_state_change_callback(test_print)
    asyncio.run(test_add_tasks())
