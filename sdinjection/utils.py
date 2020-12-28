import os


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

    def create_files(self, path, files):
        for item in files:
            with open("" + path + "/file{}.txt".format(item), "w") as file:
                file.write("This is file {}\n".format(item))
        print("\n*** Creation of the " + str(files) + " files ***")

    def remove_files(self, path, files ):
        for item in  files:
            with open("" + path + "/file{}.txt".format(item), "r"):
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