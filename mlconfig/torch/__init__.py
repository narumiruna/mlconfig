import functools

import mlconfig

try:
    from torch import optim
except ImportError:
    print('Failed to import torch.')


def _register_classes(module, superclass, prefix=None, sep='.'):
    for name in dir(module):
        attr = getattr(module, name)

        if isinstance(attr, type) and issubclass(attr, superclass):
            if attr is superclass:
                continue

            if prefix is not None:
                name = prefix + sep + name

            mlconfig.register(attr, name=name)


register_torch_optimizers = functools.partial(
    _register_classes,
    module=optim,
    superclass=optim.Optimizer,
)

register_torch_schedulers = functools.partial(
    _register_classes,
    module=optim.lr_scheduler,
    superclass=optim.lr_scheduler._LRScheduler,
)
