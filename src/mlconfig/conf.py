from __future__ import annotations

import copy
import functools
from typing import Any

from omegaconf import DictConfig
from omegaconf import ListConfig
from omegaconf import OmegaConf

_registry = {}
_key = "name"


def load(f: str | None = None, obj: Any | None = None) -> ListConfig | DictConfig:
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


def register(func_or_cls: Any = None, name: str | None = None) -> Any:
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
            raise ValueError(f"duplicate name {name} found")

        return func_or_cls

    if func_or_cls is None:
        return functools.partial(_register, name=name)

    return _register(func_or_cls, name=name)


def getcls(conf: DictConfig) -> Any:
    key = conf[_key]

    if not isinstance(key, str):
        raise ValueError(f"key {key} must be a string")

    if key not in _registry:
        raise ValueError(f"key {key} not found in registry")

    return _registry[conf[_key]]


def instantiate(conf: DictConfig, *args: Any, **kwargs: Any) -> Any:
    kwargs = copy.deepcopy(kwargs)

    for k, v in conf.items():
        if isinstance(k, str) and k not in kwargs and k != _key:
            kwargs[k] = v

    func_or_cls = getcls(conf)

    return func_or_cls(*args, **kwargs)


def flatten(data: dict[str, Any], prefix: str | None = None, sep: str = ".") -> dict[str, Any]:
    d = {}

    for key, value in data.items():
        if prefix is not None:
            key = prefix + sep + key

        if isinstance(value, dict):
            d.update(flatten(value, prefix=key, sep=sep))
            continue

        d[key] = value

    return d
