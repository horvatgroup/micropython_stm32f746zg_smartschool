import network
import usocket
import uselect
import time

# https://docs.openmv.io/library/network.LAN.html

mac = ""
eth = None


def check_connection_with_gateway():
    # around 400ms
    print("[LAN]: test connection with gateway")
    gateway = eth.ifconfig()[2]
    write_data = 'GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % ('', gateway)
    read_data = 'HTTP/1.0 200 OK\r\n'
    return check_socket_write_and_read(gateway, 80, write_data.encode(), read_data.encode())


def check_link():
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


def check_socket_write_and_read(ip, port, write_data=b"", read_data=b""):
    addr = usocket.getaddrinfo(ip, port)[0][-1]
    s = usocket.socket()
    s.setblocking(False)
    try:
        s.connect(addr)
        print("connect done")
    except OSError as e:
        print("connect", e)

    p = uselect.poll()
    p.register(s, uselect.POLLOUT | uselect.POLLIN)
    status_write = None
    status_read = None

    try:
        if p.poll(-1)[0][1] & uselect.POLLOUT:
            s.send(write_data)
            status_write = True
        else:
            print("[LAN]: ERROR socket not writable")
            status_write = False
    except Exception as e:
        print("[LAN]: ERROR write %s" % (e))
        status_write = False

    if read_data == "":
        p.unregister(s)
        s.close()
        s = None
        return status_write

    for i in range(10):
        try:
            if p.poll(-1)[0][1] & uselect.POLLIN:
                print(p.poll(-1))
                data = s.recv(len(read_data))
                print(data)
                if data == read_data:
                    status_read = True
                    break
            else:
                print("[LAN]: ERROR socket not readable")
                status_read = False
        except Exception as e:
            print("[LAN]: ERROR read %s" % (e))
            status_read = False
        time.sleep_ms(100)

    p.unregister(s)
    s.close()
    s = None
    return status_write and status_read
