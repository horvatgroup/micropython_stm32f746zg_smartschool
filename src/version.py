import things

VERSION = 1.2


def send_version(msg):
    print("[VER] get_version %s" % (str(msg)))
    things.set_state_using_hw("VERSION", VERSION, sync_out_force_update=True)
