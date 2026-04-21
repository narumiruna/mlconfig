from __future__ import annotations

import copy
import functools
from collections.abc import Callable
from typing import Protocol
from typing import TypeVar
from typing import cast

from omegaconf import DictConfig
from omegaconf import ListConfig
from omegaconf import OmegaConf


class _NamedObject(Protocol):
    __name__: str


_T = TypeVar("_T", bound=_NamedObject)
_InstantiatedT = TypeVar("_InstantiatedT")

_registry: dict[str, object] = {}
_key = "name"


def load(f: str | None = None, obj: object | None = None) -> ListConfig | DictConfig:
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
    if length == 1:
        return configs[0]

    return OmegaConf.merge(*configs)


def register(func_or_cls: _T | str | None = None, name: str | None = None) -> Callable[[_T], _T] | _T:
    r"""Register function or class

    Args:
        func_or_cls: function or class to be registered
        name (str, optional): name of the func_or_cls in registry
    """
    if isinstance(func_or_cls, str) and name is None:
        func_or_cls, name = None, func_or_cls

    def _register(func_or_cls: _T, name: str | None = None) -> _T:
        if name is None:
            name = func_or_cls.__name__

        if name not in _registry:
            _registry[name] = func_or_cls
        else:
            raise ValueError(f"duplicate name {name} found")

        return func_or_cls

    if func_or_cls is None:
        return functools.partial(_register, name=name)

    return _register(cast("_T", func_or_cls), name=name)


def getcls(conf: DictConfig | dict[str, object]) -> object:
    key = conf[_key]

    if not isinstance(key, str):
        raise TypeError(f"key {key} must be a string")

    if key not in _registry:
        raise ValueError(f"key {key} not found in registry")

    return _registry[key]


def instantiate(conf: DictConfig | dict[str, object], *args: object, **kwargs: object) -> object:
    kwargs = copy.deepcopy(kwargs)

    for k, v in conf.items():
        if isinstance(k, str) and k not in kwargs and k != _key:
            kwargs[k] = v

    func_or_cls = getcls(conf)
    if not callable(func_or_cls):
        raise TypeError(f"registered object {func_or_cls} is not callable")

    callable_obj = cast("Callable[..., object]", func_or_cls)
    return callable_obj(*args, **kwargs)


def instantiate_as(
    conf: DictConfig | dict[str, object],
    expected_type: type[_InstantiatedT],
    *args: object,
    **kwargs: object,
) -> _InstantiatedT:
    result = instantiate(conf, *args, **kwargs)
    if not isinstance(result, expected_type):
        actual_name = type(result).__qualname__
        expected_name = expected_type.__qualname__
        raise TypeError(f"instantiated object has type {actual_name}, expected {expected_name}")

    return result


def flatten(data: dict[str, object], prefix: str | None = None, sep: str = ".") -> dict[str, object]:
    d: dict[str, object] = {}

    for key, value in data.items():
        if prefix is not None:
            key = prefix + sep + key

        if isinstance(value, dict):
            nested = cast("dict[str, object]", value)
            d.update(flatten(nested, prefix=key, sep=sep))
            continue

        d[key] = value

    return d
