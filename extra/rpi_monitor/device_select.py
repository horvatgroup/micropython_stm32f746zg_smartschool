#!/usr/bin/env python

from generic_tty_device import GenericTtyDevice
import time


class R4D3B16():
    FUNCTION_CONTROL_INSTRUCTION = 0x06
    FUNCTION_READ_STATUS = 0x03
    CMD_TURN_ON = 0x01
    CMD_SHUT_DOWN = 0x02
    STARTING_REGISTER_ADDRESS = 0x0001

    CONTROL_INSTRUCTION_RESPONSE_LEN = 8
    READ_STATUS_RESPONSE_LEN = 7

    DELAY = 0
    OPEN = 1
    CLOSED = 2
    NUM_OF_CHANNELS = 8

    def __init__(self, port="/dev/ttyUSB0"):
        self.gtd = GenericTtyDevice(port=port, baud=9600, rs485=True)

    # legacy call
    def connect(self):
        return True

    # legacy call
    def disconnect(self):
        pass

    def get_check_sum(self, data):
        data = bytearray(data)
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for i in range(8):
                if ((crc & 1) != 0):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return [crc >> 0 & 0xff, crc >> 8 & 0xff]

    def get_address_channel_from_index(self, index):
        index = index - 1
        address = int(index / self.NUM_OF_CHANNELS) + 1
        channel = index % self.NUM_OF_CHANNELS + 1
        return address, channel

    def generate_control_instruction(self, cmd, index):
        packet = []
        address, channel = self.get_address_channel_from_index(index)
        packet.append(address)
        packet.append(self.FUNCTION_CONTROL_INSTRUCTION)
        packet.append((channel & 0xff00) >> 8)
        packet.append(channel & 0x00ff)
        packet.append(cmd)
        packet.append(self.DELAY)
        check_sum = self.get_check_sum(packet)
        packet.append(check_sum[0])
        packet.append(check_sum[1])
        return packet

    def generate_read_status(self, index):
        packet = []
        address, channel = self.get_address_channel_from_index(index)
        packet.append(address)
        packet.append(self.FUNCTION_READ_STATUS)
        packet.append((channel & 0xff00) >> 8)
        packet.append(channel & 0x00ff)
        packet.append((self.STARTING_REGISTER_ADDRESS & 0xff00) >> 8)
        packet.append(self.STARTING_REGISTER_ADDRESS & 0x00ff)
        check_sum = self.get_check_sum(packet)
        packet.append(check_sum[0])
        packet.append(check_sum[1])
        return packet

    def set_relay_on(self, index):
        packet = self.generate_control_instruction(self.CMD_TURN_ON, index)
        self.gtd.write_hex_list(packet)
        read_packet = self.gtd.read_hex_list(num=self.CONTROL_INSTRUCTION_RESPONSE_LEN)
        if read_packet is not None and len(read_packet) == self.CONTROL_INSTRUCTION_RESPONSE_LEN:
            crc = read_packet[-2:]
            expected_crc = self.get_check_sum(read_packet[:-2])
            if expected_crc == crc:
                address = read_packet[0]
                function = read_packet[1]
                channel = (read_packet[2] << 8) + read_packet[3]
                state = read_packet[4]
                expected_address, expected_channel = self.get_address_channel_from_index(index)
                if address == expected_address and function == self.FUNCTION_CONTROL_INSTRUCTION and channel == expected_channel:
                    return state == self.OPEN
        print("set_relay_on: wrong result, data is not the same")
        self.gtd.print_hex(packet)
        self.gtd.print_hex(read_packet)
        return False

    def set_relay_off(self, index):
        packet = self.generate_control_instruction(self.CMD_SHUT_DOWN, index)
        self.gtd.write_hex_list(packet)
        read_packet = self.gtd.read_hex_list(num=self.CONTROL_INSTRUCTION_RESPONSE_LEN)
        if read_packet is not None and len(read_packet) == self.CONTROL_INSTRUCTION_RESPONSE_LEN:
            crc = read_packet[-2:]
            expected_crc = self.get_check_sum(read_packet[:-2])
            if expected_crc == crc:
                address = read_packet[0]
                function = read_packet[1]
                channel = (read_packet[2] << 8) + read_packet[3]
                state = read_packet[4]
                expected_address, expected_channel = self.get_address_channel_from_index(index)
                if address == expected_address and function == self.FUNCTION_CONTROL_INSTRUCTION and channel == expected_channel:
                    return state == self.CLOSED
        print("set_relay_off: wrong result, data is not the same")
        self.gtd.print_hex(packet)
        self.gtd.print_hex(read_packet)
        return False

    def get_relay_state(self, index):
        packet = self.generate_read_status(index)
        self.gtd.write_hex_list(packet)
        read_packet = self.gtd.read_hex_list(num=self.READ_STATUS_RESPONSE_LEN)
        if read_packet is not None and len(read_packet) == self.READ_STATUS_RESPONSE_LEN:
            crc = read_packet[-2:]
            expected_crc = self.get_check_sum(read_packet[:-2])
            if expected_crc == crc:
                address = read_packet[0]
                function = read_packet[1]
                data_len = read_packet[2]
                relay_status = (read_packet[3] << 8) + read_packet[4]
                expected_address, expected_channel = self.get_address_channel_from_index(index)
                if address == expected_address and function == self.FUNCTION_READ_STATUS and data_len == 2:
                    return relay_status
        print("get_relay_state: can't parse")
        self.gtd.print_hex(read_packet)
        return None

    def is_responsive(self):
        state = self.get_relay_state(0x01)
        return state is not None

    def single_ring(self, index, doorbell_panel_address, delay=1):
        res_on = self.set_relay_on(index)
        time.sleep(delay)
        res_off = self.set_relay_off(index)
        return res_on and res_off

    def set_relay(self, index, state):
        if state:
            self.set_relay_on(index)
        else:
            self.set_relay_off(index)

    CHANNEL_USB_GND = 4
    CHANNEL_USB_VCC = 3
    CHANNEL_USB_SIG1 = 2
    CHANNEL_USB_SIG2 = 1
    CHANNEL_GPIO_GND = 8
    CHANNEL_GPIO_VCC = 7
    CHANNEL_GPIO_SIG1 = 6
    CHANNEL_GPIO_SIG2 = 5

    def set_power_usb(self, state):
        self.set_relay(self.CHANNEL_USB_GND, state)
        self.set_relay(self.CHANNEL_USB_VCC, state)

    def set_power_gpio(self, state):
        self.set_relay(self.CHANNEL_GPIO_GND, state)
        self.set_relay(self.CHANNEL_GPIO_VCC, state)

    def set_data_usb(self, state):
        self.set_relay(self.CHANNEL_USB_SIG1, state)
        self.set_relay(self.CHANNEL_USB_SIG2, state)

    def set_data_gpio(self, state):
        self.set_relay(self.CHANNEL_GPIO_SIG1, state)
        self.set_relay(self.CHANNEL_GPIO_SIG2, state)

    def set_usb(self):
        self.set_data_gpio(False)
        self.set_power_gpio(False)
        time.sleep(3)
        self.set_data_usb(True)
        self.set_power_usb(True)

    def set_gpio(self):
        self.set_data_usb(False)
        self.set_power_usb(False)
        time.sleep(3)
        self.set_data_gpio(True)
        self.set_power_gpio(True)

    def set_off(self):
        self.set_data_gpio(False)
        self.set_power_gpio(False)
        self.set_data_usb(False)
        self.set_power_usb(False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        import readline
        import rlcompleter
        import code

        rb = R4D3B16()

        readline.parse_and_bind("tab: complete")
        code.interact(local=locals())
    else:
        rb = R4D3B16()
        if sys.argv[1] == "usb":
            rb.set_usb()
        elif sys.argv[1] == "gpio":
            rb.set_gpio()
        elif sys.argv[1] == "off":
            rb.set_off()
