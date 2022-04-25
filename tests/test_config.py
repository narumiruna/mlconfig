import os
import tempfile
import unittest

import mlconfig
from mlconfig.config import Config


@mlconfig.register
class AddOperator(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.data = {
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
        self.temp_dir = tempfile.gettempdir()

    def test_save_and_load_config(self):
        c1 = Config(self.data)
        f = os.path.join(self.temp_dir, 'test_save.yaml')
        c1.save(f)

        c2 = mlconfig.load(f)
        self.assertDictEqual(c1.to_dict(), c2.to_dict())

    def test_instantiate(self):
        a = 1
        b = 2
        config = Config(name='AddOperator', a=a, b=b)

        obj = config.instantiate()
        self.assertEqual(obj.add(), a + b)

    def test_call(self):
        a = 1
        b = 2
        config = Config(name='AddOperator', a=a, b=b)

        obj = config()
        self.assertEqual(obj.add(), a + b)

    def test_merge(self):
        c1 = Config(a=1, b=2)
        c2 = Config(b=3, c=4)

        c1.merge(c2, allow_new_key=True)
        self.assertDictEqual(c1.to_dict(), dict(a=1, b=3, c=4))

    def test_merge_allow_new_key(self):
        c1 = Config(a=1, b=2)
        c2 = Config(b=3, c=4)

        with self.assertRaises(ValueError):
            c1.merge(c2, allow_new_key=False)

    def test_variable_expansion(self):
        data = self.data.copy()
        data['num_classes'] = 50
        data['model']['num_classes'] = '$num_classes'

        data['prefix'] = '/usr/share'
        data['dataset']['root'] = '$prefix/data'

        data['output'] = '$prefix/${model.name}'

        config = mlconfig.load(data)
        self.assertEqual(config['model']['num_classes'], 50)
        self.assertEqual(config['dataset']['root'], '/usr/share/data')
        self.assertEqual(config['output'], '/usr/share/LeNet')
