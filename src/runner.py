import buttons
import lib_lan
import sync_data
import buttons

def init():
    buttons.init()


def loop():
    while True:
        buttons.loop()


def run():
    init()
    loop()
