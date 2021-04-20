from common import create_led, create_button

LED_PINS = ['B0', 'B7', 'B14']
BUTTON_PIN = 'C13'

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

def on_button_callback(state):
    print("button %s" % (("released", "pressed")[state]))
    if not state:
        return
    toggle_leds()

def check_button():
    global button_state
    state = button.value()
    if state != button_state:
        button_state = state
        on_button_callback(button_state)