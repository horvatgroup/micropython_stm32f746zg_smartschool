import uasyncio as asyncio
import things
import lan


async def action():
    t = things.get_thing_from_path("heartbeat")
    counter = 0
    while True:
        t.data = counter
        t.dirty_out = True
        counter += 1
        if lan.eth is not None:
            print("[LAN]: registers: ", lan.get_registers())
        await asyncio.sleep_ms(60000)
