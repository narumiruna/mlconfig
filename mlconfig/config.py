import functools

from .collections import AttrDict
from .utils import load_json, load_yaml, save_json, save_yaml

_REGISTRY = {}


class Config(AttrDict):

    def save(self, f, **kwargs):
        r"""Save configuration file

        Arguments:
            f (str): the configuration file
        """
        if f.endswith('.yaml'):
            save_yaml(self.to_dict(), f, **kwargs)
        elif f.endswith('.json'):
            save_json(self.to_dict(), f, **kwargs)
        else:
            raise ValueError('file extension should be .yaml or .json')

    def __call__(self, *args, **kwargs):
        new_kwargs = {k: v for k, v in self.items() if k != 'name'}
        new_kwargs.update(kwargs)

        # create object recursively
        for k, v in new_kwargs.items():
            if isinstance(v, self.__class__):
                new_kwargs[k] = v()

        return _REGISTRY[self.name](*args, **new_kwargs)


def _flatten(data, prefix=None, sep='.'):
    d = {}

    for key, value in data.items():
        if prefix is not None:
            key = prefix + sep + key

        if isinstance(value, dict):
            d.update(_flatten(value, prefix=key))

        d[key] = value

    return d


def _replace(data, prefix='$'):
    m = _flatten(data)

    def replace(d):
        for key, value in d.items():
            if isinstance(value, str) and value.startswith(prefix):
                d[key] = m[value.lstrip(prefix)]

            if isinstance(value, dict):
                replace(value)

    replace(data)

    return data


def load(f, replace_values=True):
    r"""Load the configuration file

    Arguments:
        f (str): the configuration file
        replace_values (bool, optional): replace the values with prefix $
    """
    if f.endswith('.yaml'):
        data = load_yaml(f)
    elif f.endswith('.json'):
        data = load_json(f)
    else:
        raise ValueError('file extension should be .yaml or .json')

    if replace_values:
        data = _replace(data)

    config = Config(data)
    config.set_immutable()
    return config


def register(func_or_cls=None, name=None):

    def _register(func_or_cls, name=None):
        if name is None:
            name = func_or_cls.__name__
        _REGISTRY[name] = func_or_cls
        return func_or_cls

    if func_or_cls is None:
        return functools.partial(_register, name=name)

    return _register(func_or_cls, name=name)
