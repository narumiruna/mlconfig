import copy
import functools
from typing import Any
from typing import Optional
from typing import Union

from omegaconf import DictConfig
from omegaconf import ListConfig
from omegaconf import OmegaConf

_registry = {}
_key = "name"


def load(f: Optional[str] = None, obj: Optional[Any] = None) -> Union[ListConfig, DictConfig]:
    """Load configuration file or structured object.
    If both are provided, then the configuration from file
    will override the configuration from structured object.

    Args:
        f (str, optional): Path to configuration file
        obj (object, optional): Structured object to load

    Returns:
        OmegaConf: OmegaConf object
    """
    configs = []

    if obj is not None:
        configs.append(OmegaConf.structured(obj))

    if f is not None:
        configs.append(OmegaConf.load(f))

    length = len(configs)
    if length == 0:
        raise ValueError("No configuration file or structured object provided.")
    elif length == 1:
        return configs[0]

    return OmegaConf.merge(*configs)


def register(func_or_cls=None, name: Optional[str] = None):
    r"""Register function or class

    Args:
        func_or_cls: function or class to be registered
        name (str, optional): name of the func_or_cls in registry
    """
    if isinstance(func_or_cls, str) and name is None:
        func_or_cls, name = None, func_or_cls

    def _register(func_or_cls, name=None):
        if name is None:
            name = func_or_cls.__name__

        if name not in _registry:
            _registry[name] = func_or_cls
        else:
            raise ValueError("duplicate name {} found".format(name))

        return func_or_cls

    if func_or_cls is None:
        return functools.partial(_register, name=name)

    return _register(func_or_cls, name=name)


def getcls(conf):
    return _registry[conf[_key]]


def instantiate(conf, *args, **kwargs):
    kwargs = copy.deepcopy(kwargs)

    for k, v in conf.items():
        if k not in kwargs and k != _key:
            kwargs[k] = v

    func_or_cls = getcls(conf)

    return func_or_cls(*args, **kwargs)


def flatten(data: dict, prefix: Optional[str] = None, sep: str = ".") -> dict:
    d = {}

    for key, value in data.items():
        if prefix is not None:
            key = prefix + sep + key

        if isinstance(value, dict):
            d.update(flatten(value, prefix=key))
            continue

        d[key] = value

    return d
