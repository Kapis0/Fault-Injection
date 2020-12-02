import os
import json
import random
from fault_injection.fault import InjectionS, InjectionID
from fault_injection.schedule import Event, Scheduler

# READ JSON
JSON_FILE = open('config.json', 'r')

# PARSE
OBJECT = json.loads(JSON_FILE.read())

# SUPERBLOCK PARAMETERS
BYTE_ALL = OBJECT["injections"][0]["parameters"]["bytes"]
BYTE_RAND = random.choice(OBJECT["injections"][1]["parameters"]["bytes"])
COUNT = OBJECT["injections"][0]["parameters"]["count"]
SEEK = OBJECT["injections"][0]["parameters"]["seek"]

# DEVICE
DEV_USB = "/dev/sdb1"
DEV_ZERO = "/dev/zero"
DEV_RANDOM = "/dev/urandom"

# DIRECTORY AND PATH
PARENT_DIR = "/mnt"
DIR1 = "dir1"
FILE0 = "file0.txt"
LOST_FOUND = "lost+found"
PATH_DIR1 = os.path.join(PARENT_DIR, DIR1)  # /mnt/dir1
PATH_LOST = os.path.join(PARENT_DIR, LOST_FOUND)  # /mnt/lost+found
PATH_FILE0 = os.path.join(PARENT_DIR, FILE0)  # /mnt/file0.txt


class Injector(Event):

    def __init__(self):
        Event.__init__(self, self.occur_time, self.type, self.parameters)

    injections = None

    def inject(self, injections):

        self.injections = injections

        for injection in injections:
            self.type = injection["type"]

            if self.type == "super_block_corruption":
                fault = InjectionS(DEV_USB, PARENT_DIR, DEV_ZERO, DEV_USB, BYTE_ALL, COUNT, SEEK)
                fault.injection_superblock()
            if self.type == "super_block_corruption_random":
                fault_rand = InjectionS(DEV_USB, PARENT_DIR, DEV_ZERO, DEV_USB, BYTE_RAND, COUNT, SEEK)
                fault_rand.injection_superblock()
            if self.type == "i-node_corruption":
                INODE_DIR1 = os.stat(PATH_DIR1).st_ino
                fault_inode = InjectionID(DEV_USB, PARENT_DIR, INODE_DIR1, PATH_DIR1, PATH_LOST)
                fault_inode.injection_inode()
            if self.type == "direct_block_corruption":
                INODE_FILE = os.stat(PATH_FILE0).st_ino
                fault_directblock = InjectionID(DEV_USB, PARENT_DIR, INODE_FILE, None, None)
                fault_directblock.injection_directblock()



            
