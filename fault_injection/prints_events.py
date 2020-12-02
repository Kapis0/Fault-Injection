from fault_injection.configuration import Configuration
from fault_injection.schedule import Scheduler
import logging
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    config = Configuration("config.json")
    config.load()
    sched = Scheduler(True)
    sched.load_injections(config.get_injections())
    sched.start()
    sched.join()

        
 #   inj = Injector()
 #   inj.inject(config.get_injections())
