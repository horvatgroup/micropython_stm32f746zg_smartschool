from machine import Pin, unique_id
from utime import sleep
from time import ticks_ms
import network
import socket

# dir(machine.Pin.board)
# dir(machine.Pin.cpu)
LED_PINS = ['B0', 'B7', 'B14']
BUTTON_PIN = 'C13'

def get_millis():
    return ticks_ms()

def millis_passed(timestamp):
    return get_millis() - timestamp

def create_led(pin):
    return Pin(pin, Pin.OUT)

def create_button(pin):
    return Pin(pin, Pin.IN, Pin.PULL_DOWN)

leds = []
current_led = 0

for pin in LED_PINS:
    leds.append(create_led(pin))

button = create_button(BUTTON_PIN)
button_state = 0

def toggle_leds():
    print("toggle leds")
    global current_led
    leds[current_led].value(not leds[current_led].value())
    current_led += 1
    if current_led >= len(leds):
        current_led = 0

lan = None
client = None

def test_network():
    print("test network start")
    global lan
    lan = network.LAN()
    lan.active(True)
    lan.ifconfig('dhcp')
    result = lan.ifconfig()
    if result:
        print(result)
    print("test network end")

def http_get(url):
    print("http get start")
    import socket
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
    print("http get end")
    
def on_button_callback(state):
    print("button %s" % (("released", "pressed")[state]))
    if not state:
        return
    toggle_leds()
    http_get('http://micropython.org/ks/test.html')

def check_button():
    global button_state
    state = button.value()
    if state != button_state:
        button_state = state
        on_button_callback(button_state)

test_network()

while True:
    check_button()