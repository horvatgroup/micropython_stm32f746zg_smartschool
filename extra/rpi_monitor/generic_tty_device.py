#!/usr/bin/env python3

from typing import Optional
import serial
import serial.rs485
import time

def get_millis():
    return round(time.time() * 1000)


def millis_passed(timestamp):
    return get_millis() - timestamp


class GenericTtyDevice():
    def __init__(self, port="/dev/ttyUSB0", baud=115200, rs485=False):
        self.device = None
        self.port = port
        self.baud = baud
        self.rs485 = rs485
        self.single_char_timeout_in_s = 1.0
        self.default_timeout_in_ms = 1000
        self.reconfigure_needed = False

    def connect(self):
        print("[GTD]: connect")
        try:
            if not self.rs485:
                self.device = serial.Serial(port=self.port, baudrate=self.baud, timeout=self.single_char_timeout_in_s)
            else:
                self.device = serial.rs485.RS485(self.port, self.baud, timeout=self.single_char_timeout_in_s)
                self.device.rs485_mode = serial.rs485.RS485Settings(False, True)
            return True
        except Exception as e:
            print("[GTD]: connect failed with %s" % (e))
            return False

    def disconnect(self):
        print("[GTD]: disconnect")
        if self.device and self.device.isOpen():
            self.device.close()
        self.device = None

    def reconfigure(self, port=None, baud=None):
        if port != None:
            print("[GTD]: reconfigure - port[%s] -> port[%s]" % (self.port, port))
            self.port = port
            self.reconfigure_needed = True
        if baud != None:
            print("[GTD]: reconfigure - baud[%s] -> baud[%s]" % (self.baud, baud))
            self.baud = baud
            self.reconfigure_needed = True

    def is_ready(self):
        if self.reconfigure_needed:
            print("[GTD]: is_ready - reconfigure_needed")
            self.reconfigure_needed = False
            self.disconnect()
            return self.connect()
        if self.device == None:
            print("[GTD]: is_ready - device == None")
            self.disconnect()
            return self.connect()
        else:
            return True

    def write_single_hex(self, c):
        self.device.write(bytes([c]))

    def write_hex_list(self, data):
        if self.is_ready():
            try:
                self.device.write(data)
                return True
            except Exception as e:
                print("[GTD]: write failed with %s" % (e))
                self.reconfigure_needed = True
                return False
        else:
            return False

    def write_rc(self):
        self.write_single_hex(ord('\r'))

    def write_nl(self):
        self.write_single_hex(ord('\n'))

    def write_ascii(self, s, write_rc=True, write_nl=False):
        if self.is_ready():
            try:
                for c in s:
                    self.write_single_hex(ord(c))
                if write_rc:
                    self.write_rc()
                if write_nl:
                    self.write_nl()
                return True
            except Exception as e:
                print("[GTD]: write_ascii failed with %s" % (e))
                self.reconfigure_needed = True
                return False
        else:
            return False

    def read_hex_list(self, timeout=None, terminator_list=None, num=None):
        read_data = None
        if self.is_ready():
            try:
                if not timeout:
                    timeout = self.default_timeout_in_ms
                timestamp = get_millis()
                read_data = []
                while True:
                    c = self.device.read()
                    if c != b'':
                        c = int.from_bytes(c, "little")
                        read_data.append(c)
                        if terminator_list != None and len(terminator_list) > 0:
                            if len(read_data) >= len(terminator_list):
                                # print("[GTD]: read matching %s %s" % (str(read_data[len(read_data) - len(terminator_list):]), str(terminator_list)))
                                if read_data[len(read_data) - len(terminator_list):] == terminator_list:
                                    #print("[GTD]: read string match")
                                    break
                    else:
                        if millis_passed(timestamp) >= timeout:
                            print("[GTD]: read timeout")
                            break
                    if num != None and len(read_data) >= num:
                        print("[GTD]: read num match")
                        break
            except Exception as e:
                print("[GTD]: read failed with %s" % (e))
                self.reconfigure_needed = True
        return read_data

    def read_ascii(self, timeout=None, terminator_string=None):
        read_data = None
        try:
            terminator_list = None
            if terminator_string:
                terminator_list = [ord(i) for i in terminator_string]
            read_data = self.read_hex_list(timeout, terminator_list)
            if read_data:
                return "".join([chr(i) for i in read_data])
        except Exception as e:
            print("[GTD]: read_ascii failed with %s" % (e))
            self.reconfigure_needed = True
        return read_data

    def read_byte(self):
        byte = None
        if self.is_ready():
            try:
                byte = self.device.read()
                return byte if byte is not None else None
            except Exception as exception:
                print("read failed with %s" % exception)
                self.reconfigure_needed = True
        return byte

    def read_with_parser(self, parser, timeout_ms: Optional[int] = None, exit_if_no_data=False):
        if timeout_ms is None:
            timeout_ms = self.default_timeout_in_ms
        timestamp = get_millis()
        while True:
            byte = self.read_byte()
            if byte != b'':
                try:
                    result = parser.append_byte(byte[0])
                except Exception as exception:
                    print("read failed with %s" % exception)
                    return None

                if result is not None:
                    return result
                else:
                    if millis_passed(timestamp) >= timeout_ms:
                        print("read timeout")
                        return None
                    else:
                        time.sleep(0.01)
            else:
                if exit_if_no_data is True:
                    return None
                if millis_passed(timestamp) >= timeout_ms:
                    print("read timeout")
                    return None
                else:
                    time.sleep(0.01)

    def write_and_read_hex_list(self, data, timeout=None, terminator_list=None):
        read_data = None
        self.clear_input_buffer()
        if self.write_hex_list(data):
            read_data = self.read_hex_list(timeout, terminator_list)
        return read_data

    def write_and_read_ascii(self, s, write_rc=True, write_nl=False, timeout=None, terminator_string=None):
        read_data = None
        self.clear_input_buffer()
        if self.write_ascii(s, write_rc, write_nl):
            read_data = self.read_ascii(timeout, terminator_string)
        return read_data

    def flush(self):
        if self.is_ready():
            try:
                self.device.flush()
                return True
            except Exception as e:
                print("[GTD]: flush failed with %s" % (e))
                self.reconfigure_needed = True
                return False
        return False

    def clear_input_buffer(self):
        if self.is_ready():
            try:
                self.device.reset_input_buffer()
                return True
            except Exception as e:
                print("[GTD]: clear_input_buffer failed with %s" % (e))
                self.reconfigure_needed = True
                return False
        return False

    def print_hex(self, data):
        if data != None:
            print("[HEX]: %s" % (" ".join([hex(i)[2:].zfill(2) for i in data])))


if __name__ == "__main__":
    import readline
    import rlcompleter
    import code

    s = GenericTtyDevice("/dev/ttyUSB2")

    readline.parse_and_bind("tab: complete")
    code.interact(local=locals())
