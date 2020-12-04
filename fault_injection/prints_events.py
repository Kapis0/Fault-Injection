from fault_injection.configuration import Configuration
from fault_injection.schedule import Scheduler, Scheduler_User
import logging

logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    config = Configuration("config.json")
    config.load()

    usr = Scheduler_User()
    usr.load_user_activity(config.get_user_activities())
    usr.start()
    usr.join()
    usr.sched_user_activity_nowait()

    sched = Scheduler()
    sched.load_injections(config.get_injections())
    sched.start()
    sched.join()
    sched.sched_injections_nowait()



