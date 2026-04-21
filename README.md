# mlconfig

`mlconfig` is a lightweight configuration loader and object instantiation helper built on top of
[OmegaConf](https://omegaconf.readthedocs.io/). It is useful when a Python project needs YAML-based
configuration, interpolation, and a small registry for constructing functions or classes from config.

## Requirements

- Python >=3.12
- OmegaConf >=2.3.0

## Installation

```shell
pip install mlconfig
```

## Example

The example below uses the files in [`example/conf.yaml`](example/conf.yaml) and
[`example/main.py`](example/main.py).

```yaml
num_classes: 50

model:
  name: LeNet
  num_classes: ${num_classes}

optimizer:
  name: Adam
  lr: 1.e-3
  weight_decay: 1.e-4
```

```python
from torch import Tensor
from torch import nn
from torch import optim

from mlconfig import instantiate
from mlconfig import instantiate_as
from mlconfig import load
from mlconfig import register

register(optim.Adam)


@register
class LeNet(nn.Module):
    def __init__(self, num_classes: int) -> None:
        super().__init__()
        self.num_classes = num_classes

        self.features = nn.Sequential(
            nn.Conv2d(1, 6, 5, bias=False),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(6, 16, 5, bias=False),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )

        self.classifier = nn.Sequential(
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 84),
            nn.ReLU(inplace=True),
            nn.Linear(84, self.num_classes),
        )

    def forward(self, x: Tensor) -> Tensor:
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)


def main() -> None:
    config = load("conf.yaml")

    model = instantiate_as(config.model, nn.Module)
    optimizer = instantiate(config.optimizer, model.parameters())
    print(optimizer)


if __name__ == "__main__":
    main()
```

## Core API

### `load`

Load an OmegaConf configuration from a file, a structured object, or both. When both are provided, the
file configuration overrides the structured object.

```python
from mlconfig import load

config = load("conf.yaml")
config_from_object = load(obj={"model": {"name": "LeNet", "num_classes": 10}})
merged = load("conf.yaml", obj={"num_classes": 10})
```

### `register`

Register a function or class so it can be referenced by the `name` field in a config mapping.

```python
from mlconfig import register


@register
class Model:
    pass


@register("custom_factory")
def build_model():
    return Model()


register(Model, name="AnotherModel")
```

Duplicate names raise `ValueError`.

### `instantiate`

Instantiate the registered function or class named by `conf["name"]`. Remaining config fields are passed
as keyword arguments. Explicit `*args` and `**kwargs` are also supported, and explicit keyword arguments
override config values.

```python
from mlconfig import instantiate

model = instantiate({"name": "Model"})
optimizer = instantiate(config.optimizer, model.parameters(), lr=1e-4)
```

### `instantiate_as`

Instantiate an object and verify that the result is an instance of the expected type.

```python
from torch import nn
from mlconfig import instantiate_as

model = instantiate_as(config.model, nn.Module)
```

If the result has a different type, `instantiate_as` raises `TypeError`.

### `getcls`

Return the registered function or class referenced by `conf["name"]`.

```python
from mlconfig import getcls

cls = getcls({"name": "Model"})
```

Unknown names raise `ValueError`; non-string names raise `TypeError`.

### `flatten`

Flatten nested dictionaries into a single dictionary with dot-separated keys.

```python
from mlconfig import flatten

flat = flatten({"train": {"batch_size": 64}})
assert flat == {"train.batch_size": 64}

flat = flatten({"train": {"batch_size": 64}}, sep="/")
assert flat == {"train/batch_size": 64}
```

## PyTorch Helpers

`mlconfig.torch` includes helpers for registering PyTorch optimizer and scheduler classes.

```python
from mlconfig.torch import register_torch_optimizers
from mlconfig.torch import register_torch_schedulers

register_torch_optimizers()
register_torch_schedulers(prefix="scheduler")
```

After registration, optimizers can be instantiated by class name, such as `Adam`. Scheduler names use the
provided prefix when one is passed, such as `scheduler.StepLR`.

## Development

```shell
uv run pytest -v -s --cov=src tests
uv run ruff check .
uv run ty check .
```

## License

`mlconfig` is distributed under the [MIT License](LICENSE).
