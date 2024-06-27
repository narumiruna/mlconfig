from torch import nn
from torch import optim

from mlconfig import instantiate
from mlconfig import load
from mlconfig import register

register(optim.Adam)


@register
class LeNet(nn.Module):
    def __init__(self, num_classes):
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

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def main():
    config = load("conf.yaml")

    model = instantiate(config.model)
    optimizer = instantiate(config.optimizer, model.parameters())
    print(optimizer)


if __name__ == "__main__":
    main()
