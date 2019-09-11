import yaml


def load_yaml(f):
    with open(f, 'r') as fp:
        return yaml.safe_load(fp)


def save_yaml(data, f):
    with open(f, 'w') as fp:
        yaml.safe_dump(data, stream=fp)
