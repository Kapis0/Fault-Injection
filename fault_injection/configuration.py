import json


class Configuration:
    config_file = None
    jsonObject = None

    def __init__(self, filename):
        self.config_file = filename

    def load(self):
        if self.config_file is not None:
            fp = open(self.config_file)
            self.jsonObject = json.load(fp)
        else:
            raise Exception("Config File Not Initialized")

    def get_injections(self):
        if self.jsonObject is None:
            self.load()

        fail_futex = {}
        for futex in self.jsonObject["globals"]['fail_futex']:
            fail_futex[futex['id']] = futex['fail_futex']

        injections = []
        for injection in self.jsonObject["injections"]:
            if fail_futex[injection['id']] == 1:
                injections.append(injection)
        return injections

    def get_user_activities(self):
        if self.jsonObject is None:
            self.load()

        fail_futex = {}
        for futex in self.jsonObject["globals"]['fail_futex']:
            fail_futex[futex['id']] = futex['fail_futex']

        user_activities = []
        for activity in self.jsonObject["user_activity"]:
            if fail_futex[activity['id']] == 1:
                user_activities.append(activity)
        return user_activities
