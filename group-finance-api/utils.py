import json


def obj_dict(obj):
    return obj.__dict__


def list_json(list):
    json_string = json.dumps(list, default=obj_dict)
