import json

import yaml
from collections import Iterable

import os


def isextension(f, ext):
    if not isinstance(ext, Iterable):
        ext = (ext,)

    return os.path.splitext(f)[-1] in ext


def load_json(f):
    with open(f, 'r') as fp:
        return json.load(fp)


def save_json(data, f, **kwargs):
    with open(f, 'w') as fp:
        json.dump(data, fp, **kwargs)


def load_yaml(f):
    with open(f, 'r') as fp:
        return yaml.safe_load(fp)


def save_yaml(data, f, **kwargs):
    with open(f, 'w') as fp:
        yaml.safe_dump(data, stream=fp, **kwargs)
