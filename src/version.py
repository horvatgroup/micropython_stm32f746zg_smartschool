VERSION = 1.2


def req_version(thing):
    print("[VER] req_version %s" % (str(thing.data)))
    thing.data = VERSION
    thing.dirty_out = True
