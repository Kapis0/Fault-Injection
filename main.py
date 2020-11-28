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

DEV_USB = "/dev/sdb1"
DEV_ZERO = "/dev/zero"
DEV_RANDOM = "/dev/urandom"

PARENT_DIR = "/mnt"
DIR1 = "dir1"
FILE0 = "file0.txt"
LOST_FOUND = "lost+found"
PATH_DIR1 = os.path.join(PARENT_DIR, DIR1)  # /mnt/dir1
PATH_LOST = os.path.join(PARENT_DIR, LOST_FOUND)  # /mnt/lost+found
PATH_FILE0 = os.path.join(PARENT_DIR, FILE0)  # /mnt/file0.txt


class Device:

    def __init__(self, dev):
        self.dev = dev

    def unmounting(self):
        print("\n*** Unmounting the partition ***")
        os.system("umount " + str(self.dev))

    def formatting(self):
        print("\n*** Partition formatting ***")
        os.system("mkfs.ext4 " + self.dev)

    def filesystem_check(self):
        os.system("e2fsck " + self.dev)


class Path:

    def __init__(self, path):
        self.path = path

    def create_files(self, path):
        for item in range(0, usr[0].get("tasks")):
            with open("" + path + "/file{}.txt".format(item), "w") as file:
                file.write("This is file {}\n".format(item))
        print("\n*** Creation of the " + str(usr[0].get("tasks")) + " files ***")

    def remove_files(self):
        for item in range(0, usr[0].get("tasks")):
            with open("" + self.path + "/file{}.txt".format(item), "r"):
                os.remove("" + self.path + "/file{}.txt".format(item))
        print("\n*** Removing files ***")

    def create_directory(self, path):
        print("\n *** Directory created *** ")
        os.mkdir(path)

    def remove_directory(self, path):
        print("\n *** Directory removed ***")
        os.system("rm -rf " + path)

    def show_content(self, path):
        print("\n *** Show the directory's content ***")
        os.system("ls -l " + path)


class Partition(Device, Path):

    def __init__(self, dev, path):
        Device.__init__(self, dev)
        Path.__init__(self, path)

    def mounting(self):
        print("\n*** Mounting " + self.dev + " in " + self.path + " ***")
        os.system("mount " + self.dev + " " + self.path)

    def umount_mount(self):
        Device.unmounting(self)
        Partition.mounting(self)


class Inode(Device):

    def __init__(self, dev, inode):
        Device.__init__(self, dev)
        self.inode = inode

    def clean_inode(self):
        os.system("debugfs -R 'clri <" + str(self.inode) + ">' " + self.dev + " -w")

    def stat_inode(self):
        os.system("debugfs -R 'stat <" + str(self.inode) + ">' " + self.dev + "|grep '(0)'")

    def modify_inode(self):
        os.system("debugfs -R 'mi <" + str(self.inode) + ">' " + self.dev + " -w")


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


class InjectionS(Partition):

    def __init__(self, dev, path, file_in, file_out, bs, count, seek):
        Partition.__init__(self, dev, path)
        self.file_in = file_in
        self.file_out = file_out
        self.bs = bs
        self.count = count
        self.seek = seek

    def __repr__(self):
        return "\n{} --> {} with {} {} {}".format(self.file_in, self.file_out, self.bs, self.count, self.seek)

    def dd_injection(self):
        print("\n*** Loading Fault injection ***")
        os.system("dd if=" + self.file_in + " of=" + self.file_out +
                  " bs=" + str(self.bs) + " count=" + str(self.count) + " seek=" + str(self.seek) + "")

    def injection_superblock(self):
        Partition.umount_mount(self)
        InjectionS.dd_injection(self)
        Partition.umount_mount(self)
        ans_mount = input("\n***** Mounting failed? {y,n} ")
        if ans_mount == "y":
            ans_e2fsck = input("\n***** Run e2fsck? {y,n} ")
            if ans_e2fsck == "y":
                Partition.filesystem_check(self)


class InjectionID(Inode, Partition):

    def __init__(self, dev, path, inode, directory, lost_found):
        Inode.__init__(self, dev, inode)
        Partition.__init__(self, dev, path)
        self.directory = directory
        self.lost_found = lost_found

    def injection_inode(self):
        Partition.umount_mount(self)
        Partition.remove_directory(self, self.lost_found)
        Partition.create_files(self, self.directory)
        Inode.clean_inode(self)
        Partition.umount_mount(self)
        Partition.show_content(self, self.path)  # dovrebbe chiedere di fare pulizia
        Partition.unmounting(self)
        ans_e2fsck = input("\n***** Run e2fsck? {y,n} ")
        if ans_e2fsck == "y":
            Partition.filesystem_check(self)
        Partition.mounting(self)
        Partition.show_content(self, self.lost_found)

    def injection_directblock(self):
        Partition.umount_mount(self)
        os.system("cat /mnt/file0.txt /mnt/file1.txt")
        Inode.stat_inode(self)
        Inode.modify_inode(self)  # L'utente qui deve inserire un indirizzo in più in Direct block 0 o 5
        Partition.umount_mount(self)
        os.system("cat /mnt/file0.txt /mnt/file1.txt")


if __name__ == '__main__':

    p = Partition(DEV_USB, PARENT_DIR)
    p_dir1 = Partition(DEV_USB, PATH_DIR1)

    if glo.get("user_activity") is True and fut[0].get("fail_futex") == 1:
        ev0 = Event(usr[0].get("type"), usr[0].get("id"))
        p.umount_mount()
        p.remove_files()
        p.create_files(PARENT_DIR)
        INODE_FILE = os.stat(PATH_FILE0).st_ino
        print(ev0)

    if glo.get("user_activity") is True and fut[1].get("fail_futex") == 1:
        ev1 = Event(usr[1].get("type"), usr[1].get("id"))
        p.umount_mount()
        p_dir1.remove_directory(PATH_DIR1)
        p_dir1.create_directory(PATH_DIR1)
        INODE_DIR1 = os.stat(PATH_DIR1).st_ino
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
            num = int((input("\nChoose an injection's type\n1. Superblock\n2. I-node\n3. Direct Block\n")))
            break
        except ValueError:
            print("\nInvalid input")

    if num == 1:

        r = input("\n Do you want inject random? {y,n} ")
        if r == "y":
            list_event.remove(ev3.to_string())
            list_event.insert(0, ev3.to_string())
        if r == "n":
            list_event.remove(ev2.to_string())
            list_event.insert(0, ev2.to_string())

    if num == 2:

        list_event.remove(ev4.to_string())
        list_event.insert(0, ev4.to_string())

    if num == 3:

        list_event.remove(ev5.to_string())
        list_event.insert(0, ev5.to_string())


    while len(list_event) != 0:
        if fut[2].get("fail_futex") == 1:
            if list_event[0] == ev2.to_string():
                print("\n *** Injection into all bytes of the supeblock")
                fault = InjectionS(DEV_USB, PARENT_DIR, DEV_ZERO, DEV_USB, BYTE_ALL, COUNT, SEEK)
                fault.injection_superblock()
                list_event.remove(ev2.to_string())

        if fut[3].get("fail_futex") == 1:
            if list_event[0] == ev3.to_string():
                print("\n *** Random injection of " + str(BYTE_RAND) + " bytes")
                fault_rand = InjectionS(DEV_USB, PARENT_DIR, DEV_ZERO, DEV_USB, BYTE_RAND, COUNT, SEEK)
                fault_rand.injection_superblock()
                list_event.remove(ev3.to_string())

        if glo.get("user_activity") is True and fut[0].get("fail_futex") == 1 and fut[1].get("fail_futex") == 1 and fut[4].get("fail_futex") == 1:
            if list_event[0] == ev4.to_string():
                print("*** I-node injection ***")
                fault_inode = InjectionID(DEV_USB, PARENT_DIR, INODE_DIR1, PATH_DIR1, PATH_LOST)
                fault_inode.injection_inode()
                list_event.remove(ev4.to_string())

        if glo.get("user_activity") is True and fut[0].get("fail_futex") == 1 and fut[5].get("fail_futex") == 1:
            if list_event[0] == ev5.to_string():
                fault_directblock = InjectionID(DEV_USB, PARENT_DIR, INODE_FILE, None, None)
                fault_directblock.injection_directblock()
                list_event.remove(ev5.to_string())


