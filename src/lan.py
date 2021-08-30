import network
import socket

# https://docs.openmv.io/library/network.LAN.html

mac = ""
eth = None


def set_static_ip():
    print("[LAN]: set static ip")
    eth.ifconfig(('192.168.88.17', '255.255.255.0', '192.168.88.1', '8.8.8.8'))

def check_connection():
    status = eth.status()
    if status == 0:
        print("[LAN]: Link Down")
    if status == 1:
        print("[LAN]: Link Join")
        try:
            eth.active(True)
        except Exception as e:
            print("[LAN]: ERROR %s" % (e))
    elif status == 2:
        print("[LAN]: Link No-IP")
        try:
            eth.ifconfig('dhcp')
        except Exception as e:
            print("[LAN]: ERROR %s" % (e))
            set_static_ip()
    elif status == 3:
        print("[LAN]: Link Up")
        return True
    return False


def status():
    print("[LAN]: status")
    print("mac", mac)
    print("status", eth.status())
    print("active", eth.active())
    print("isconnected", eth.isconnected())
    result = eth.ifconfig()
    if result:
        print(result)


def init():
    print("[LAN]: init")
    global eth, mac
    eth = network.LAN()
    mac = "".join(['{:02X}'.format(x) for x in eth.config('mac')])
    # lan.config(trace=4)
