import os
import random
from sdinjection.main import InjectionS, InjectionID
import logging



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


class Injector:


    @staticmethod
    def inject(injection, simulation=False):
        if not simulation:
            Injector.__real_injection(injection)
        else:
            Injector.__simulate(injection)

    @staticmethod
    def __simulate(injection):
        if injection["type"] == "super_block_corruption":
            print ('Injecting: ' + injection["type"] + 'parameters:',DEV_USB, PARENT_DIR, DEV_ZERO, DEV_USB,
                   injection["parameters"]["bytes"], injection["parameters"]["count"], injection["parameters"]["seek"])


        elif injection["type"] == "super_block_corruption_random":
            print(injection["type"], DEV_USB, PARENT_DIR, DEV_ZERO, DEV_USB,
                  random.choice(injection["parameters"]["bytes"]),
                  injection["parameters"]["count"], injection["parameters"]["seek"])

        elif injection["type"] == "i-node_corruption":
            try:
                INODE_DIR1 = os.stat(PATH_DIR1).st_ino
            except:
                logging.warning("File Not Found")
                INODE_DIR1 = None
            print(injection["type"] , DEV_USB, PARENT_DIR, INODE_DIR1, PATH_DIR1, PATH_LOST)

        elif injection["type"] == "direct_block_corruption":
            try:
                INODE_FILE = os.stat(PATH_FILE0)
            except:
                logging.warning("File Not Found")
                INODE_FILE = None

            print(injection["type"], DEV_USB, PARENT_DIR, INODE_FILE, None, None)


    @staticmethod
    def __real_injection(injection):

        if injection["type"] == "super_block_corruption":
            fault = InjectionS(DEV_USB, PARENT_DIR, DEV_ZERO, DEV_USB, injection["parameters"]["bytes"],
                               injection["parameters"]["count"], injection["parameters"]["seek"])
            fault.injection_superblock()
        elif injection["type"] == "super_block_corruption_random":
            fault_rand = InjectionS(DEV_USB, PARENT_DIR, DEV_ZERO, DEV_USB,
                                    random.choice(injection["parameters"]["bytes"]),
                                    injection["parameters"]["count"], injection["parameters"]["seek"])
            fault_rand.injection_superblock()
        elif injection["type"] == "i-node_corruption":
            INODE_DIR1 = os.stat(PATH_DIR1).st_ino
            fault_inode = InjectionID(DEV_USB, PARENT_DIR, INODE_DIR1, PATH_DIR1, PATH_LOST)
            fault_inode.injection_inode()
        elif injection["type"] == "direct_block_corruption":
            INODE_FILE = os.stat(PATH_FILE0).st_ino
            fault_directblock = InjectionID(DEV_USB, PARENT_DIR, INODE_FILE, None, None)
            fault_directblock.injection_directblock()
