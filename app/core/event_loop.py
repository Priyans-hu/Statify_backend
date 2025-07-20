event_loop = None

def set_event_loop(loop):
    global event_loop
    event_loop = loop

def get_event_loop():
    return event_loop
