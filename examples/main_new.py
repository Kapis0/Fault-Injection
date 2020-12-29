import argparse
import logging
from sdinjection.configuration import Configuration
from sdinjection.utils import Device, Path
from sdinjection.schedule import Scheduler, Scheduler_User


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(description='sd injection')
    parser.add_argument('config_file', metavar='CONFIG_FILE', type=str, default="config.json",
                        help='the configuration file')
    parser.add_argument('device', metavar='DEVICE', type=str, default="/dev/sdb1",
                        help='device or partition')
    parser.add_argument('path', metavar='PATH', type=str, default="/mnt",
                        help='mounting point')
    args = parser.parse_args()
    
    logging.info(' Using configuration file: {} '.format(args.config_file))
    logging.info(' Using device: {} '.format(args.device))
    logging.info(' Using mounting point: {} '.format(args.path))


    # Usa il modulo configuration per leggere il file config.json
    conf = Configuration(args.config_file)
    conf.load()

    dev = Device(args.device)
    path = Path(args.path)

    # Monta la partizione
    dev.mount(args.path)

    # Crea gli scheduler
    # Carica gli eventi
    # Fai partire gli eventi

    usr = Scheduler_User()
    usr.load_user_activity(conf.get_user_activities())
    usr.start()
    usr.join()
    usr.sched_user_activity_nowait()

    sched = Scheduler()
    sched.load_injections(conf.get_injections())
    sched.start()
    sched.join()
    sched.sched_injections_nowait() 


    # smonta/monta la partizione
    dev.umount_mount()
    # esegui  e2fsck se il montaggio non è andato a buon fine
    ans_e2fsck = input("\n***** Mounting failed? {y,n} ")
    if ans_e2fsck == "y":
        dev.filesystem_check() 
    pass
