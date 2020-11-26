import os
import json
from random import random

myjsonfile = open('config.json', 'r')
data = myjsonfile.read()
obj = json.loads(data)
glo = obj['globals']
fut = glo['fail_futex']
usr = obj['user_activity']
injs = obj['injections']
par2 = [injs[0].get("parameters")]
par3 = [injs[1].get("parameters")]
BYTE_2 = par2[0].get("bytes")
COUNT_2 = par2[0].get("count")
SEEK_2 = par2[0].get("seek")

list_event = []
#iterator = iter(list_event)
NAME_DEV = "/dev/sdb1"
NAME_DIR = "/mnt"
NAME_DIR1 = "dir1"
DEV_ZERO = "/dev/zero"
DEV_RANDOM = "/dev/urandom"
PATH = os.path.join(NAME_DIR, NAME_DIR1) #/mnt/dir1

class Partition:

    def __init__(self, dev, dir, path):
        self.dev = dev
        self.dir = dir
        self.path = path

    def __repr__(self):
        return "\n{} --> {}".format(self.dev, self.dir)

    def create_files(self):
        for item in range(0, usr[0].get("tasks")):
            with open("" + self.dir + "/file{}.txt".format(item), "w") as file:
                file.write("This is file {}\n".format(item))
        print("\n*** Creation of the " + str(usr[0].get("tasks")) + " files ***")

    def create_directory(self):
        print("\n *** Directory creation *** ")
        os.mkdir(self.path)

    def unmounting(self):
        print("\n*** Unmounting the partition ***")
        os.system("umount " + str(self.dev))

    def mounting(self):
        print("\n*** Mounting "+ self.dev +" in " + self.dir + " ***")
        os.system("mount " + self.dev + " " + self.dir)

    def formatting(self):
        print("\n*** Partition formatting ***")
        os.system("mkfs.ext4 " + self.dev)

    def filesystem_check(self):
        os.system("e2fsck " + self.dev)

class Event:

    #cont = 0
    def __init__(self, name, id):
        self.name = name
        self.id = id
        #Event.cont += 1

    def __repr__(self):
        return "\n{} --> {}".format(self.name, self.id)

    def to_string(self):
        return f"{self.id}"

class Injection:

    def __init__(self, fileIN, fileOUT, bs, count, seek):
        self.fileIN = fileIN
        self.fileOUT = fileOUT
        self.bs = bs
        self.count = count
        self.seek = seek

    def __repr__(self):
        return "\n{} --> {} with {} {} {}".format(self.fileIN, self.fileOUT, self.bs, self.count, self.seek)

    def injection_superblock(self):
        print("\n*** Loading Fault injection ***")
        os.system("dd if=" + self.fileIN +" of=" + self.fileOUT + " bs=" + str(self.bs) +" count=" + str(self.count) + " seek=" + str(self.seek) +"")


if __name__ == '__main__':

    p = Partition(NAME_DEV, NAME_DIR, PATH)

    if glo.get("user_activity") == True and fut[0].get("fail_futex") == 1:
        ev0 = Event(usr[0].get("type"), usr[0].get("id"))
        p.unmounting()
        p.mounting()
        p.create_files()
        print(ev0)

    if glo.get("user_activity") == True and fut[1].get("fail_futex") == 1:
        ev1 = Event(usr[1].get("type"), usr[1].get("id"))
        p.unmounting()
        p.mounting()
        p.create_directory()
        print(ev1)

    if fut[2].get("fail_futex") == 1:
        ev2 = Event(injs[0].get("type"), injs[0].get("id"))
        list_event.append(ev2.to_string())
        print(ev2)

    if fut[3].get("fail_futex") == 1:
        ev3 = Event(injs[1].get("type"), injs[1].get("id"))
        list_event.append(ev3.to_string())
        print(ev3)


    while True:
        try:
            num = int((input("\nChoose an injection's type\n1. Superblock\n2. I-node\n3. Block\n")))
            break
        except ValueError:
            print("\nInvalid input")

    if num == 1:
        r = input("\n Do you want inject random? {y,n} ")

        if r == "y":
            try:
                list_event.remove(ev3.to_string())
                list_event.insert(0, ev3.to_string())
            except ValueError:
                pass

        if r == "n":
            try:
                list_event.remove(ev2.to_string())
                list_event.insert(0, ev2.to_string())
            except ValueError:
                pass

    while len(list_event) != 0:
        if list_event[0] == ev2.to_string():
            #if next(iterator) == str(ev2.to_string()):
            fault = Injection(DEV_ZERO, NAME_DEV, BYTE_2, COUNT_2, SEEK_2)
            p.unmounting()
            p.mounting()
            fault.injection_superblock()
            p.unmounting()
            p.mounting()
            risp = input("\n***** Mounting failed? {y,n} ")
            if (risp == "y"):
                risp2 = input("\n***** Run e2fsck? {y,n} ")
                if (risp2 == "y"):
                    p.filesystem_check()
            list_event.remove(ev2.to_string())

        elif list_event[0] == ev3.to_string():
            #if next(iterator) == str(ev3.to_string()):
            print("Iniezione Random")
            list_event.remove(ev3.to_string())
            #print(list_event)





