# mlconfig

## Installation

```shell
$ pip install mlconfig
```

## Usage

config.yaml
```yaml
num_classes: 50

model:
  name: LeNet
  num_classes: $num_classes

optimizer:
  name: Adam
  lr: 1.e-3
  weight_decay: 1.e-4

...
```

main.py
```python
import mlconfig
from torch import nn, optim
from torchvision import models

mlconfig.register(optim.Adam)


@mlconfig.register
class LeNet(nn.Module):

    def __init__(self, num_classes):
        super(LeNet, self).__init__()
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

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def main():
    config = mlconfig.load('config.yaml')

    model = config.model()
    optimizer = config.optimizer(model.parameters())
    ...

if __name__ == '__main__':
    main()
```