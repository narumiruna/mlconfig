import os
from tempfile import gettempdir

import pytest

import mlconfig
from mlconfig.config import Config


@mlconfig.register
class AddOperator(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b


@pytest.fixture
def raw_config():
    return {
        'num_classes': 50,
        'root': '/path/to/repo',
        'output': '$root/${model.name}',
        'trainer': {
            'name': 'ImageClassificationTrainer',
            'num_epochs': 20
        },
        'dataset': {
            'name': 'MNISTDataloader',
            'root': '$root/data',
            'batch_size': 256,
            'num_workers': 0
        },
        'model': {
            'name': 'LeNet',
            'num_classes': '$num_classes'
        },
        'optimizer': {
            'name': 'Adam',
            'lr': 1e-3
        },
        'scheduler': {
            'name': 'StepLR',
            'step_size': 10,
            'gamma': 0.1
        }
    }


def test_config_save_and_load(raw_config):
    c1 = mlconfig.load(raw_config)
    f = os.path.join(gettempdir(), 'test_save.yaml')
    c1.save(f)

    c2 = mlconfig.load(f)
    assert c1.to_dict() == c2.to_dict()


def test_config_instantiate():
    a = 1
    b = 2
    config = Config(name='AddOperator', a=a, b=b)

    obj = config.instantiate()
    assert obj.add() == a + b


def test_config_call():
    a = 1
    b = 2
    config = Config(name='AddOperator', a=a, b=b)

    obj = config()
    assert obj.add() == a + b


def test_config_merge():
    c1 = Config(a=1, b=2)
    c2 = Config(b=3, c=4)

    c1.merge(c2, allow_new_key=True)
    assert c1.to_dict() == dict(a=1, b=3, c=4)


def test_config_merge_allow_new_key():
    c1 = Config(a=1, b=2)
    c2 = Config(b=3, c=4)

    with pytest.raises(ValueError):
        c1.merge(c2, allow_new_key=False)


def test_variable_expansion(raw_config):
    config = mlconfig.load(raw_config)

    assert config['dataset']['root'] == f'{config.root}/data'
    assert config['output'] == f'{config.root}/{config.model.name}'
