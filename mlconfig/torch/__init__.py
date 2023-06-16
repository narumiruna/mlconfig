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

            mlconfig.conf(attr, name=name)


def get_lr_scheduler_class():
    # PyTorch 2.0 renamed LRScheduler to _LRScheduler
    name = 'LRScheduler' if hasattr(optim.lr_scheduler, 'LRScheduler') else '_LRScheduler'
    return getattr(optim.lr_scheduler, name)


register_torch_optimizers = functools.partial(
    _register_classes,
    module=optim,
    superclass=optim.Optimizer,
)

register_torch_schedulers = functools.partial(
    _register_classes,
    module=optim.lr_scheduler,
    superclass=get_lr_scheduler_class(),
)
