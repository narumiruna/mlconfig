import copy
import functools

from omegaconf import OmegaConf

_REGISTRY = {}
_KEY_OF_FUNC_OR_CLS = 'name'


def load(f=None, obj=None) -> OmegaConf:
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
        raise ValueError('No configuration file or structured object provided.')
    elif length == 1:
        return configs[0]

    return OmegaConf.merge(*configs)


def register(func_or_cls=None, name: str = None):
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

        if name not in _REGISTRY:
            _REGISTRY[name] = func_or_cls
        else:
            raise ValueError('duplicate name {} found'.format(name))

        return func_or_cls

    if func_or_cls is None:
        return functools.partial(_register, name=name)

    return _register(func_or_cls, name=name)


def getcls(conf):
    return _REGISTRY[conf[_KEY_OF_FUNC_OR_CLS]]


def instantiate(conf, *args, **kwargs):
    kwargs = copy.deepcopy(kwargs)

    for k, v in conf.items():
        if k not in kwargs and k != _KEY_OF_FUNC_OR_CLS:
            kwargs[k] = v

    func_or_cls = getcls(conf)

    return func_or_cls(*args, **kwargs)
