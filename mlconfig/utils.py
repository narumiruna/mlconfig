import json
import os
from collections.abc import Sequence

import oyaml as yaml


def isextension(f: str, ext) -> bool:
    if isinstance(ext, str):
        ext = (ext,)

    assert isinstance(ext, Sequence)

    return os.path.splitext(f)[1].strip() in ext


def load_json(f: str) -> dict:
    with open(f, 'r') as fp:
        return json.load(fp)


def save_json(data: dict, f: str, **kwargs) -> None:
    with open(f, 'w') as fp:
        json.dump(data, fp, **kwargs)


def load_yaml(f: str) -> dict:
    with open(f, 'r') as fp:
        return yaml.safe_load(fp)


def save_yaml(data: dict, f: str, **kwargs) -> None:
    with open(f, 'w') as fp:
        yaml.safe_dump(data, stream=fp, **kwargs)


def load_dict(f: str) -> dict:
    if isextension(f, ('.yaml', '.yml')):
        data = load_yaml(f)
    elif isextension(f, '.json'):
        data = load_json(f)
    else:
        raise ValueError('file extension of {} should be .yaml, .yml or .json'.format(f))

    return data


def save_dict(data: dict, f: str, **kwargs) -> None:
    if isextension(f, ('.yaml', '.yml')):
        save_yaml(data, f, **kwargs)
    elif isextension(f, '.json'):
        save_json(data, f, **kwargs)
    else:
        raise ValueError('file extension of {} should be .yaml or .json'.format(f))
