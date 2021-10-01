subscribers = { }

class Subscriber:
    def __init__(self, cb, sent = None, confirmed = None):
        self.cb = cb
        self.sent = sent
        self.confirmed = confirmed

def subscribe(name, event, cb):
    global subscribers
    if event not in subscribers:
        subscribers[event] = { }
    subscribers[event][name] = Subscriber(cb)
    print("EVT: sub %s to %d" %(name, event))

def publish_to_subscriber(name, event, data):
    if event in subscribers and name in subscribers[event]:
        print("EVT: publish %d to %s" % (event, name))
        sub = subscribers[event][name]
        sub.cb(event, data)
        sub.sent = data

def publish(event, data):
    if event in subscribers:
        for name in subscribers[event].keys():
            publish_to_subscriber(event, name, data)

def confirm(name, event, data):
    if event in subscribers and name in subscribers[event]:
        sub = subscribers[event][name]
        sub.confirmed = data
        if sub.confirmed != sub.sent:
            publish_to_subscriber(event, name, data)
