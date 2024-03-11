from project.models.Event import Event
from project.models.PC import PC
from project.models.TransmissionLine import TransmissionLine
import queue
import random

debug = True


def generate_message():
    message = ""
    for i in range(random.randint(10, 15)):  # 46 - 1500
        message += str(random.randint(0, 1))
    return message


class Simulator:
    timemul = 100000000
    time = []
    events = queue.PriorityQueue()
    PCs = []
    transmission_line = None
    delta = 5
    current_time = 0.0

    def start(self):
        self.transmission_line = TransmissionLine
        self.setup_pcs()
        self.transmission_line.PCs = self.PCs
        self.generate_events()
        isFirst = True
        while self.events.empty() is False:
            event = self.events.get()

            event_finish_time = event.event_time + event.duration  # start + obliczony czas z dlugosci wiadomosci
            if debug:
                print(f"{25 * '*'} Proba wyslania wyslania pakietu {25 * '*'}")
                print(f"czas eventu: {event.event_time}")
                print(f"zablokowana do: {self.transmission_line.time_to_free}")
                print(f"{50 * '*'}")
            if self.transmission_line.time_to_free < event.event_time:
                if debug:
                    print("wysylam")
                if isFirst:
                    self.time.append(event.event_time)
                    isFirst = False
                response = self.handle_event(event)
                if response:
                    duration = self.timemul * len(response[3]) / 80000000
                    new_event = Event(event_finish_time, response[0], response[1], response[3], duration, response[2])
                    self.repeat_event_with_delta(new_event)
                self.transmission_line.time_to_free = event_finish_time
                self.time.append(event_finish_time)
            else:
                self.repeat_event_with_delta(event)

    def setup_pcs(self):
        self.PCs.append(PC("AAA", self.transmission_line))
        self.PCs.append(PC("BBB", self.transmission_line))
        self.PCs.append(PC("CCC", self.transmission_line))
        self.PCs.append(PC("DDD", self.transmission_line))

    def handle_event(self, event):
        for pc in self.PCs:
            if pc.mac_address == event.src:
                return pc.send_packet(event.dest, event.event_type, event.message)

    def generate_events(self):
        for i in range(5):
            src = random.choice(self.PCs).mac_address
            dest = random.choice(self.PCs).mac_address
            while src == dest:
                dest = random.choice(self.PCs).mac_address
            message = generate_message()
            delay = round(random.uniform(0.1, 1.0), 1)
            event_time = self.current_time + delay
            duration = self.timemul * len(message) / 80000000
            print(event_time, src, dest, message, duration)
            event_type = "MESSAGE"
            self.events.put(Event(event_time, src, dest, message, duration, event_type))

    def repeat_event_with_delta(self, event):
        self.events.put(Event(event.event_time + self.delta, event.src, event.dest, event.message, event.duration,
                              event.event_type))


simulation = Simulator()
simulation.start()

print("\nSENT MESSAGES:")
print(simulation.transmission_line.line_MESSAGE)
print("ACK:")
print(simulation.transmission_line.line_ACK)
print("NACK:")
print(simulation.transmission_line.line_NACK)
print("TIMELINE")
print(simulation.time)
