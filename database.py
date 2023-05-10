import json


class DataBase:

    def load(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def save(self, s_dict, filename):
        with open(filename, 'w') as f:
            json.dump(s_dict, f, indent=3)
