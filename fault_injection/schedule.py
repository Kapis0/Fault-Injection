from queue import PriorityQueue
import random


class Event:
    occur_time = None
    type = None
    parameters = None

    def __init__(self, e_time, e_type, parameters):
        self.occur_time = e_time
        self.type = e_type
        self.parameters = parameters
        random.seed()

    def __lt__(self, other):
        return self.occur_time < other.occur_time

    def __gt__(self, other):
        return self.occur_time > other.occur_time

    def __eq__(self, other):
        return self.occur_time == other.occur_time

    def __ne__(self, other):
        return not self.occur_time == other.occur_time

    def __str__(self):
        return '{"time": ' + str(self.occur_time) + ', "type": "' + self.type + '"}'


class Scheduler:
    injections = None
    events_queue = None

    def load_injections(self, injections):
        self.injections = injections
        self.events_queue = PriorityQueue()
        # events generations
        for injection in injections:
            f_prob = injection["fault_probability"]
            start_time = injection["start_time"]
            interval = injection["time_interval"]
            end_time = injection["end_time"]
            cur_time = start_time
            while cur_time < end_time:
                r = random.random()
                if r < f_prob:
                    e_time = cur_time + interval * random.random()
                    self.events_queue.put(Event(e_time, injection["type"], injection))
                cur_time += interval

    def next_event(self):
        if self.events_queue is None:
            raise Exception("Unloaded Queue")
        else:
            if self.events_queue.empty():
                return None
            else:
                return self.events_queue.get_nowait()
