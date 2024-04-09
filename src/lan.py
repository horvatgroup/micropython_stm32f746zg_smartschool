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


async def check_link():
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
        dhcp_error = False
        try:
            eth.ifconfig('dhcp')
        except Exception as e:
            print("[LAN]: ERROR %s" % (e))
            dhcp_error = True
        if dhcp_error:
            print("[LAN]: Waiting %d until nekt try" % (_DHCP_TIMEOUT_SLEEP_MS))
            await asyncio.sleep_ms(_DHCP_TIMEOUT_SLEEP_MS)
    elif status == 3:
        print("[LAN]: Link Up")
        return True
    return False

def print_status():
    print(f"[DEBUG] mac[{mac}] active[{eth.active()}] isconnected[{eth.isconnected()}] status[{eth.status()}] ip[{eth.ifconfig()}]")

def get_bit(byteval, idx):
    return int((byteval & (1 << idx)) != 0)

def get_registers():
    bcr = eth.register_bcr()
    bsr = eth.register_bsr()
    cbln = eth.register_cbln()
    scsr = eth.register_scsr()
    return bcr, bsr, cbln, scsr

def print_registers(bcr = None, bsr = None, cbln = None, scsr = None):
    if bcr is not None:
        print(f"[DEBUG] BCR:Soft Reset {get_bit(bcr, 15)}")
        print(f"[DEBUG] BCR:Loopback {get_bit(bcr, 14)}")
        print(f"[DEBUG] BCR:Speed Select {get_bit(bcr, 13)}")
        print(f"[DEBUG] BCR:Auto-Negotiation Enable {get_bit(bcr, 12)}")
        print(f"[DEBUG] BCR:Power Down {get_bit(bcr, 11)}")
        print(f"[DEBUG] BCR:Isolate {get_bit(bcr, 10)}")
        print(f"[DEBUG] BCR:Restart Auto-Negotiate {get_bit(bcr, 9)}")
        print(f"[DEBUG] BCR:Duplex Mode {get_bit(bcr, 8)}")
    if bsr is not None:
        print(f"[DEBUG] BSR:100BASE-T4 {get_bit(bsr, 15)}")
        print(f"[DEBUG] BSR:100BASE-TX Full Duplex {get_bit(bsr, 14)}")
        print(f"[DEBUG] BSR:100BASE-TX Half Duplex {get_bit(bsr, 13)}")
        print(f"[DEBUG] BSR:10BASE-T Full Duplex {get_bit(bsr, 12)}")
        print(f"[DEBUG] BSR:10BASE-T Half Duplex {get_bit(bsr, 11)}")
        print(f"[DEBUG] BSR:100BASE-T2 Full Duplex {get_bit(bsr, 10)}")
        print(f"[DEBUG] BSR:100BASE-T2 Half Duplex {get_bit(bsr, 9)}")
        print(f"[DEBUG] BSR:Extended Status {get_bit(bsr, 8)}")
        print(f"[DEBUG] BSR:Auto-Negotiate Complete {get_bit(bsr, 5)}")
        print(f"[DEBUG] BSR:Remote Fault {get_bit(bsr, 4)}")
        print(f"[DEBUG] BSR:Auto-Negotiate Ability {get_bit(bsr, 3)}")
        print(f"[DEBUG] BSR:Link Status {get_bit(bsr, 2)}")
        print(f"[DEBUG] BSR:Jabber Detect {get_bit(bsr, 1)}")
        print(f"[DEBUG] BSR:Extended Capabilities {get_bit(bsr, 0)}")
    if cbln is not None:
        print(f"[DEBUG] CBLN:Cable Length {get_bit(cbln, 15)}{get_bit(cbln, 14)}{get_bit(cbln, 13)}{get_bit(cbln, 12)}")
    if scsr is not None:
        print(f"[DEBUG] SCSR:Autodone {get_bit(scsr, 12)}")
        print(f"[DEBUG] SCSR:Speed Indication (?bit order) {get_bit(scsr, 4)}{get_bit(scsr, 3)}{get_bit(scsr, 2)}")

def registers():
    bcr, bsr, cbln, scsr = get_registers()
    print_registers(bcr, bsr, cbln, scsr)

def init():
    print("[LAN]: init")
    global eth, mac
    eth = network.LAN()
    mac = "".join(['{:02X}'.format(x) for x in eth.config('mac')])
