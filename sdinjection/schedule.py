from queue import PriorityQueue
import random
from sdinjection.injector import Injector
from sdinjection.user import  User
import threading
import time
import logging

class Event:
    occur_time = None
    e_type = None
    parameters = None

    def __init__(self, e_time, e_type, parameters):
        self.occur_time = e_time
        self.e_type = e_type
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
        return '{"time": ' + str(self.occur_time) + ', "type": "' + self.e_type + '"}'


class Scheduler(threading.Thread):
    injections = None
    events_queue = None
    current_time = 0
    simulation = False

    def __init__(self, simulation=False):
        threading.Thread.__init__(self)
        self.simulation = simulation

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

    def next_injection(self):
        Injector.inject(self.next_event().parameters, self.simulation)

    def sched_injections_nowait(self):
        while not self.events_queue.empty():
            self.next_injection()

    def run(self):
        while not self.events_queue.empty():
            event = self.next_event()
            logging.info("next event " + event.e_type + " in " +
                         str(event.occur_time - self.current_time) + " seconds")
            time. sleep(event.occur_time - self.current_time)
            Injector.inject(event.parameters, self.simulation)
            self.current_time = event.occur_time
            logging.info("now is " + str(self.current_time))


class Scheduler_User(threading.Thread):

    activities = None
    events_queue = None
    current_time = 0
    simulation = False

    def __init__(self, simulation=False):
        threading.Thread.__init__(self)
        self.simulation = simulation

    def load_user_activity(self, activities):
        self.activities = activities
        self.events_queue = PriorityQueue()
        # user activity events generations
        for activity in activities:
            start_time = activity["start_time"]
            end_time = activity["end_time"]
            cur_time = start_time
            self.events_queue.put(Event(cur_time, activity["type"], activity))
            cur_time += end_time

    def next_event(self):
        if self.events_queue is None:
            raise Exception("Unloaded Queue")
        else:
            if self.events_queue.empty():
                return None
            else:
                return self.events_queue.get_nowait()

    def next_user_activity(self):
        User.activity(self.next_event().parameters, self.simulation)

    def sched_user_activity_nowait(self):
        while not self.events_queue.empty():
            self.next_user_activity()

    def run_usr(self):
        while not self.events_queue.empty():
            event = self.next_event()
            logging.info("next event " + event.e_type + " in " +
                         str(event.occur_time - self.current_time) + " seconds")
            time.sleep(event.occur_time - self.current_time)
            User.activity(event.parameters, self.simulation)
            self.current_time = event.occur_time
            logging.info("now is " + str(self.current_time))
