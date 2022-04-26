import os
from tempfile import gettempdir

import pytest

from mlconfig.utils import isextension
from mlconfig.utils import load_dict
from mlconfig.utils import save_dict


@pytest.fixture
def raw_config():
    return {
        'trainer': {
            'name': 'ImageClassificationTrainer',
            'num_epochs': 20
        },
        'dataset': {
            'name': 'MNISTDataloader',
            'root': 'data',
            'batch_size': 256,
            'num_workers': 0
        },
        'model': {
            'name': 'LeNet'
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


def test_utils_save_and_load_dict(raw_config):
    yaml_path = os.path.join(gettempdir(), 'test.yaml')
    yml_path = os.path.join(gettempdir(), 'test.yml')
    json_path = os.path.join(gettempdir(), 'test.json')

    save_dict(raw_config, yaml_path)
    save_dict(raw_config, yml_path)
    save_dict(raw_config, json_path)

    yaml_data = load_dict(yaml_path)
    yml_data = load_dict(yml_path)
    json_data = load_dict(json_path)

    assert raw_config == yaml_data
    assert yaml_data == yml_data
    assert yml_data == json_data


def test_utils_load_dict_value_error():
    with pytest.raises(ValueError):
        load_dict(os.path.join(gettempdir(), 'test'))

    with pytest.raises(ValueError):
        load_dict(os.path.join(gettempdir(), 'test.py'))


def test_utils_save_dict_value_error(raw_config):
    with pytest.raises(ValueError):
        save_dict(raw_config, os.path.join(gettempdir(), 'test'))

    with pytest.raises(ValueError):
        save_dict(raw_config, os.path.join(gettempdir(), 'test.py'))


def test_utils_isextension():
    assert isextension('test.jpg', '.jpg')
    assert isextension('test.jpg', ('.jpg',))
    assert isextension('test.jpg', ('.jpg', '.png'))

    assert isextension('.test.jpg', '.jpg')
    assert isextension('.test.jpg', ('.jpg',))
    assert isextension('.test.jpg', ('.jpg', '.png'))

    assert not isextension('test', '.jpg')
    assert not isextension('test', ('.jpg',))
    assert not isextension('test', ('.jpg', '.png'))

    assert not isextension('', '.jpg')
    assert not isextension('', ('.jpg',))
    assert not isextension('', ('.jpg', '.png'))

    assert not isextension('.', '.jpg')
    assert not isextension('.', ('.jpg',))
    assert not isextension('.', ('.jpg', '.png'))
