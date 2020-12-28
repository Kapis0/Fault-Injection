import os
from sdinjection.utils import Partition

DEV_USB = "/dev/sdb1"
PARENT_DIR = "/mnt"
DIR1 = "dir1"
PATH_DIR1 = os.path.join(PARENT_DIR, DIR1)  # /mnt/dir1


class User:

    @staticmethod
    def activity(activity, simulation=False):
        if not simulation:
            User.__real_user_activity(activity)
        else:
            User.__simulate(activity)

    @staticmethod
    def __real_user_activity(activity):

        p = Partition(DEV_USB, PARENT_DIR)
        p_dir = Partition(DEV_USB, PATH_DIR1)

        if activity["type"] == "CREATE_FILES":
            p.umount_mount()
            p.create_files(PARENT_DIR)

        elif activity["type"] == "CREATE_DIR":
            p.umount_mount()
            p_dir.remove_directory(PATH_DIR1)
            p_dir.create_directory(PATH_DIR1)
            p_dir.create_files(PATH_DIR1)

    @staticmethod
    def __simulate(activity):
        if activity["type"] == "CREATE_FILES":
            print('User Activity: ' + activity["type"] + 'parameters:', DEV_USB, PARENT_DIR)

        elif activity["type"] == "CREATE_DIR":
            print('User Activity: ' + activity["type"] + 'parameters:', DEV_USB, PATH_DIR1)
