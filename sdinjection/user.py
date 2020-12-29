import os
from sdinjections.utils import Path

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

        if activity["type"] == "CREATE_FILES":
            p = Path(PARENT_DIR)
            p.create_files(PARENT_DIR, activity["tasks"])

        elif activity["type"] == "CREATE_DIR":
            p_dir = Path(PATH_DIR1)
            p_dir.remove_directory(PATH_DIR1)
            p_dir.create_directory(PATH_DIR1)
            p_dir.create_files(PATH_DIR1, activity["tasks"])

    @staticmethod
    def __simulate(activity):
        if activity["type"] == "CREATE_FILES":
            print('User Activity: ' + activity["type"] + 'parameters:', PARENT_DIR)

        elif activity["type"] == "CREATE_DIR":
            print('User Activity: ' + activity["type"] + 'parameters:', PATH_DIR1)
