import time

class MHZ19BSensor:
    def __init__(self, uart):
        self.uart = uart

    # measure CO2
    def measure(self):
        # send a read command to the sensor
        self.uart.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')

        # a little delay to let the sensor measure CO2 and send the data back
        # time.sleep(1)  # in seconds

        # read and validate the data
        buf = self.uart.read(9)
        if self.is_valid(buf):
            co2 = buf[2] * 256 + buf[3]

            return co2
        return None

    # check data returned by the sensor
    def is_valid(self, buf):
        if buf is None or buf[0] != 0xFF or buf[1] != 0x86:
            return False
        i = 1
        checksum = 0x00
        while i < 8:
            checksum += buf[i] % 256
            i += 1
        checksum = ~checksum & 0xFF
        checksum += 1
        return checksum == buf[8]
