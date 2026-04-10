import json


def read_lock(path="mypm.lock"):
    with open(path) as f:
        return json.load(f)