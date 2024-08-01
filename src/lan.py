from micropython import const
import network
import uasyncio as asyncio

# https://docs.openmv.io/library/network.LAN.html
# https://github.com/EchoDel/hardware_projects/blob/main/micropython/micropython-async-master/v2/sock_nonblock.py
# https://github.com/peterhinch/micropython-mqtt/blob/master/mqtt_as/mqtt_as.py
# https://github.com/microhomie/microhomie/blob/master/lib/mqtt_as.py
# https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py
# https://github.com/fizista/micropython-umqtt.simple2/blob/master/src/umqtt/simple2.py

mac = ""
eth = None
activated = False
reboot_requested = False

def check_link():
    global activated
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
            return True
    return False

def print_status():
    print(f"[DEBUG] mac[{mac}] active[{eth.active()}] isconnected[{eth.isconnected()}] status[{eth.status()}] ip[{eth.ifconfig()}]")

def request_reactivate():
    print("[LAN]: request reactivate")
    global activated
    activated = False

def request_reboot():
    print("[LAN]: request reboot")
    global reboot_requested
    reboot_requested = True

def init():
    print("[LAN]: init")
    global eth, mac
    eth = network.LAN()
    mac = "".join(['{:02X}'.format(x) for x in eth.config('mac')])
