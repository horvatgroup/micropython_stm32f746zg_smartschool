import uasyncio as asyncio
import things
import lan

async def action():
    t = things.get_thing_from_path("lan_testing")
    while True:
        if lan.eth is not None:
            registers = repr(lan.get_registers)
            t.data = registers
            t.dirty_out = True
            print("[LAN]: registers: ", registers)
        await asyncio.sleep_ms(60000)
