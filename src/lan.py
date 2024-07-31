from micropython import const
import network
import uasyncio as asyncio

# https://docs.openmv.io/library/network.LAN.html
# https://github.com/EchoDel/hardware_projects/blob/main/micropython/micropython-async-master/v2/sock_nonblock.py
# https://github.com/peterhinch/micropython-mqtt/blob/master/mqtt_as/mqtt_as.py
# https://github.com/microhomie/microhomie/blob/master/lib/mqtt_as.py
# https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py
# https://github.com/fizista/micropython-umqtt.simple2/blob/master/src/umqtt/simple2.py

_DHCP_TIMEOUT_SLEEP_MS = const(30 * 60 * 1000)

mac = ""
eth = None
activated = False
reinit_lwip = False

def check_link():
    global activated, reinit_lwip
    link_status = eth.status()
    if link_status == 0:
        print("[LAN]: lan cable not connected")
    else:
        if not activated:
            print("[LAN]: activating")
            eth.active(False)
            eth.active(True)
            activated = True
        else:
            if reinit_lwip:
                print("[LAN]: reinit lwip")
                eth.reinit_lwip()
                reinit_lwip = False
            else:
                return True
    return False

def print_status():
    print(f"[DEBUG] mac[{mac}] active[{eth.active()}] isconnected[{eth.isconnected()}] status[{eth.status()}] ip[{eth.ifconfig()}]")

def get_bit(byteval, idx):
    return int((byteval & (1 << idx)) != 0)

def get_link_status():
    bsr = eth.register_bsr()
    return bool(get_bit(bsr, 2))

def request_reactivate():
    print("[LAN]: require reactivate")
    global activated
    activated = False

def init():
    print("[LAN]: init")
    global eth, mac
    eth = network.LAN()
    mac = "".join(['{:02X}'.format(x) for x in eth.config('mac')])
