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

    def test_create_object(self):
        a = 1
        b = 2
        config = Config(name='AddOperator', a=a, b=b)

        obj = config.create_object()
        self.assertEqual(obj.add(), a + b)

    def test_call(self):
        a = 1
        b = 2
        config = Config(name='AddOperator', a=a, b=b)

        obj = config()
        self.assertEqual(obj.add(), a + b)

    def test_merge_config(self):
        c1 = Config(a=1, b=2)
        c2 = Config(b=3, c=4)

        c1.merge_config(c2, allow_new_key=True)
        self.assertDictEqual(c1.to_dict(), dict(a=1, b=3, c=4))

    def test_merge_config_allow_new_key(self):
        c1 = Config(a=1, b=2)
        c2 = Config(b=3, c=4)

        with self.assertRaises(ValueError):
            c1.merge_config(c2, allow_new_key=False)

    def test_instantiate(self):
        a = 1
        b = 2
        config = Config(name='AddOperator', a=a, b=b)

        obj = mlconfig.instantiate(config)
        self.assertEqual(obj.add(), a + b)
