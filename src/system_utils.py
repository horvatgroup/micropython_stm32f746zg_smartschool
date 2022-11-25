import sys
import machine


def req_reset(thing):
    print("req_reset %s" % (str(thing.data)))
    if thing.data == "soft":
        sys.exit()
    elif thing.data == "hard":
        machine.reset()
