import uasyncio as asyncio
import things
import lan

lan_reactivate_counter = 0
lan_reinit_lwip_counter = 0

async def action():
    global lan_reactivate_counter, lan_reinit_lwip_counter
    t = things.get_thing_from_path("lan_testing")
    while True:
        if lan.eth is not None:
            registers = repr(lan.get_registers())
            t.data = f"{registers}, {lan_reinit_lwip_counter}, {lan_reactivate_counter}"
            t.dirty_out = True
            print("[LAN]: registers: ", registers)
        await asyncio.sleep_ms(60000)

def lan_reactivate_add():
    global lan_reactivate_counter
    lan_reactivate_counter += 1

def lan_reinit_lwip_add():
    global lan_reinit_lwip_counter
    lan_reinit_lwip_counter += 1
