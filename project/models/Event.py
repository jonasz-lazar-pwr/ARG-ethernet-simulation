class Event:
    event_time = None
    src = None
    dest = None
    message = None
    duration = None
    event_type = None

    def __lt__(self, other):
        return self.event_time < other.event_time

    def __init__(self, event_time, src, dest, message, duration, event_type):
        self.event_time = event_time
        self.src = src
        self.dest = dest
        self.message = message
        self.duration = duration
        self.event_type = event_type
