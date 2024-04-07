import json, yaml, os


class JsonObject(object):

    def __init__(self, d):
        self.__dict__ = d

    def get(self, k):
        return self.__dict__.get(k)


dir_path = os.path.dirname(os.path.abspath(__file__))
with open(f"{dir_path}/config.yaml") as stream:
    data_yaml = yaml.safe_load(stream)
conf = json.loads(json.dumps(data_yaml), object_hook=JsonObject)
