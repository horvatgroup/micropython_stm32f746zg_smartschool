import network
import socket

# https://docs.openmv.io/library/network.LAN.html

mac = ""
eth = None


def set_static_ip():
    print("[LAN]: set static ip")
    eth.ifconfig(('192.168.88.17', '255.255.255.0', '192.168.88.1', '8.8.8.8'))


def is_connection_ready():
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
        return check_connection_with_gateway()
    return False


def check_connection_with_gateway():
    print("[LAN]: test connection with gateway")
    gateway = eth.ifconfig()[2]
    try:
        addr = socket.getaddrinfo(gateway, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.close()
        return True
    except Exception as e:
        print("[LAN]: ERROR %s" % e)
        return False


def http_get(url):
    print("[LAN]: http get [%s]" % (url))
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()


def check_internet():
    print("[LAN]: check internet")
    http_get('http://micropython.org/ks/test.html')


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


def loop():
    pass
