from fault_injection.configuration import Configuration
from fault_injection.injector import Injector
from fault_injection.schedule import Scheduler

if __name__ == "__main__":
    config = Configuration("config.json")
    config.load()
    sched = Scheduler()
    sched.load_injections(config.get_injections())

    ev = sched.next_event()
    while ev is not None:
        print(ev)
        ev = sched.next_event()
        
    inj = Injector()
    inj.inject(config.get_injections())
