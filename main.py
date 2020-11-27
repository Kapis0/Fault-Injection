import os
import json
import random

# READ JSON
myjsonfile = open('config.json', 'r')
data = myjsonfile.read()
obj = json.loads(data)
glo = obj['globals']
fut = glo['fail_futex']
usr = obj['user_activity']
injs = obj['injections']
par2 = [injs[0].get("parameters")]
par3 = [injs[1].get("parameters")]
BYTE_ALL = par2[0].get("bytes")
BYTE_RAND = random.choice(par3[0].get("bytes"))
COUNT = par2[0].get("count")
SEEK = par2[0].get("seek")

list_event = []
# iterator = iter(list_event)
NAME_DEV = "/dev/sdb1"
DEV_ZERO = "/dev/zero"
DEV_RANDOM = "/dev/urandom"

NAME_DIR = "/mnt"
NAME_DIR1 = "dir1"
NAME_FILE0 = "file0.txt"
LOST_FOUND = "lost+found"
PATH = os.path.join(NAME_DIR, NAME_DIR1)  # /mnt/dir1
PATH_LOST = os.path.join(NAME_DIR, LOST_FOUND)  # /mnt/lost+found
PATH_FILE = os.path.join(NAME_DIR, NAME_FILE0) # /mnt/file0.txt

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

    def elimina_file(self):
        for item in range(0, usr[0].get("tasks")):
            with open("" + self.dir + "/file{}.txt".format(item), "r"):
                os.remove("" + self.dir + "/file{}.txt".format(item))
        print("\n*** Removing files ***")

    def create_directory(self):
        print("\n *** Directory created *** ")
        os.mkdir(self.path)

    def remove_directory(self):
        print("\n *** Directory removed ***")
        os.system("rm -rf " + self.path)

    def show_content(self):
        print("\n *** Show the directory's content ***")
        os.system("ls -l " + self.path)

    def unmounting(self):
        print("\n*** Unmounting the partition ***")
        os.system("umount " + str(self.dev))

    def mounting(self):
        print("\n*** Mounting " + self.dev + " in " + self.dir + " ***")
        os.system("mount " + self.dev + " " + self.dir)

    def formatting(self):
        print("\n*** Partition formatting ***")
        os.system("mkfs.ext4 " + self.dev)

    def filesystem_check(self):
        os.system("e2fsck " + self.dev)


class Event:

    # cont = 0
    def __init__(self, name, id):
        self.name = name
        self.id = id
        # Event.cont += 1

    def __repr__(self):
        return "\n{} --> {}".format(self.name, self.id)

    def to_string(self):
        return f"{self.id}"


class Injection:

    def __init__(self, file_in, file_out, bs, count, seek):
        self.file_in = file_in
        self.file_out = file_out
        self.bs = bs
        self.count = count
        self.seek = seek

    def __repr__(self):
        return "\n{} --> {} with {} {} {}".format(self.file_in, self.file_out, self.bs, self.count, self.seek)

    def injection_superblock(self):
        print("\n*** Loading Fault injection ***")
        os.system("dd if=" + self.file_in + " of=" + self.file_out +
                  " bs=" + str(self.bs) + " count=" + str(self.count) + " seek=" + str(self.seek) + "")


class Inode:

    def __init__(self, dev, inode):
        self.dev = dev
        self.inode = inode

    def clean_inode(self):
        os.system("debugfs -R 'clri <" + str(self.inode) + ">' " + self.dev + " -w")

    def stat_inode(self):
        os.system("debugfs -R 'stat <" + str(self.inode) + ">' " + self.dev + "|grep '(0)'")

    def modify_inode(self):
        os.system("debugfs -R 'mi <" + str(self.inode) + ">' " + self.dev + " -w")

if __name__ == '__main__':

    p = Partition(NAME_DEV, NAME_DIR, PATH)

    if glo.get("user_activity") is True and fut[0].get("fail_futex") == 1:
        ev0 = Event(usr[0].get("type"), usr[0].get("id"))
        p.unmounting()
        p.mounting()
        p.elimina_file()
        p.create_files()
        INODE_FILE = os.stat(PATH_FILE).st_ino
        print(ev0)

    if glo.get("user_activity") is True and fut[1].get("fail_futex") == 1:
        ev1 = Event(usr[1].get("type"), usr[1].get("id"))
        p.unmounting()
        p.mounting()
        p.remove_directory()
        p.create_directory()
        INODE_DIR1 = os.stat(PATH).st_ino
        print(ev1)

    if fut[2].get("fail_futex") == 1:
        ev2 = Event(injs[0].get("type"), injs[0].get("id"))
        list_event.append(ev2.to_string())
        print(ev2)

    if fut[3].get("fail_futex") == 1:
        ev3 = Event(injs[1].get("type"), injs[1].get("id"))
        list_event.append(ev3.to_string())
        print(ev3)

    if fut[4].get("fail_futex") == 1:
        ev4 = Event(injs[2].get("type"), injs[2].get("id"))
        list_event.append(ev4.to_string())
        print(ev4)

    if fut[5].get("fail_futex") == 1:
        ev5 = Event(injs[3].get("type"), injs[3].get("id"))
        list_event.append(ev5.to_string())
        print(ev5)

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

    if num == 2:
        try:
            list_event.remove(ev4.to_string())
            list_event.insert(0, ev4.to_string())
        except ValueError:
            pass

    if num == 3:
        try:
            list_event.remove(ev5.to_string())
            list_event.insert(0, ev5.to_string())
        except ValueError:
            pass

    while len(list_event) != 0:
        if fut[2].get("fail_futex") == 1:
            if list_event[0] == ev2.to_string():
                # if next(iterator) == str(ev2.to_string()):
                fault = Injection(DEV_ZERO, NAME_DEV, BYTE_ALL, COUNT, SEEK)
                p.unmounting()
                p.mounting()
                fault.injection_superblock()
                p.unmounting()
                p.mounting()
                risp = input("\n***** Mounting failed? {y,n} ")
                if risp == "y":
                    risp2 = input("\n***** Run e2fsck? {y,n} ")
                    if risp2 == "y":
                        p.filesystem_check()
                list_event.remove(ev2.to_string())

        if fut[3].get("fail_futex") == 1:
            if list_event[0] == ev3.to_string():
                # if next(iterator) == str(ev3.to_string()):
                print("\n *** Random injection of " + str(BYTE_RAND) + " bytes")
                fault_rand = Injection(DEV_ZERO, NAME_DEV, BYTE_RAND, COUNT, SEEK)
                p.unmounting()
                p.mounting()
                fault_rand.injection_superblock()
                p.unmounting()
                p.mounting()
                risp = input("\n***** Mounting failed? {y,n} ")
                if risp == "y":
                    risp2 = input("\n***** Run e2fsck? {y,n} ")
                    if risp2 == "y":
                        p.filesystem_check()
                list_event.remove(ev3.to_string())
                # print(list_event)

        if glo.get("user_activity") is True and fut[0].get("fail_futex") == 1 and fut[1].get("fail_futex") == 1 and fut[4].get("fail_futex") == 1:
            if list_event[0] == ev4.to_string():
                print("I-node injection")
                p_lost = Partition(NAME_DEV, NAME_DIR, PATH_LOST)
                p_path = Partition(NAME_DEV, PATH, PATH)
                i = Inode(NAME_DEV, INODE_DIR1)

                p.unmounting()
                p.mounting()
                p_lost.remove_directory()
                p_path.create_files()
                i.clean_inode()
                p.unmounting()
                p.mounting()
                p.show_content()  # dovrebbe chiedere di fare pulizia
                p.unmounting()
                risp2 = input("\n***** Run e2fsck? {y,n} ")
                if risp2 == "y":
                    p.filesystem_check()
                p.mounting()
                p_lost.show_content()
                list_event.remove(ev4.to_string())
        else:
            print("\n*** CREATE DIR AND CREATE FILES NOT ABILITED ***")

        if glo.get("user_activity") is True and fut[0].get("fail_futex") == 1 and fut[5].get("fail_futex") == 1:
            if list_event[0] == ev5.to_string():
                i2 = Inode(NAME_DEV, INODE_FILE)
                p.unmounting()
                p.mounting()
                os.system("cat /mnt/file0.txt /mnt/file1.txt")
                i2.stat_inode()
                i2.modify_inode() # L'utente qui deve inserire un indirizzo in più in Direct block 0 o 5
                p.unmounting()
                p.mounting()
                os.system("cat /mnt/file0.txt /mnt/file1.txt")
                list_event.remove(ev5.to_string())
        else:
            print("\n*** CREATE FILES NOT ABILITED ***")

