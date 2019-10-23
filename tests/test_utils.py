import os
import tempfile
import unittest

from mlconfig.utils import isextension, load_dict, save_dict


class TestUtils(unittest.TestCase):

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
        self.yaml_path = os.path.join(self.temp_dir, 'test.yaml')
        self.yml_path = os.path.join(self.temp_dir, 'test.yml')
        self.json_path = os.path.join(self.temp_dir, 'test.json')

    def test_save_and_load_dict(self):
        save_dict(self.data, self.yaml_path)
        save_dict(self.data, self.yml_path)
        save_dict(self.data, self.json_path)

        yaml_data = load_dict(self.yaml_path)
        yml_data = load_dict(self.yml_path)
        json_data = load_dict(self.json_path)

        self.assertDictEqual(self.data, yaml_data)
        self.assertDictEqual(yaml_data, yml_data)
        self.assertDictEqual(yml_data, json_data)

    def test_load_dict_value_error(self):
        with self.assertRaises(ValueError):
            load_dict(os.path.join(self.temp_dir, 'test'))

        with self.assertRaises(ValueError):
            load_dict(os.path.join(self.temp_dir, 'test.py'))

    def test_save_dict_value_error(self):
        with self.assertRaises(ValueError):
            save_dict(self.data, os.path.join(self.temp_dir, 'test'))

        with self.assertRaises(ValueError):
            save_dict(self.data, os.path.join(self.temp_dir, 'test.py'))

    def test_isextension(self):
        self.assertTrue(isextension('test.jpg', '.jpg'))
        self.assertTrue(isextension('test.jpg', ('.jpg',)))
        self.assertTrue(isextension('test.jpg', ('.jpg', '.png')))

        self.assertTrue(isextension('.test.jpg', '.jpg'))
        self.assertTrue(isextension('.test.jpg', ('.jpg',)))
        self.assertTrue(isextension('.test.jpg', ('.jpg', '.png')))

        self.assertFalse(isextension('test', '.jpg'))
        self.assertFalse(isextension('test', ('.jpg',)))
        self.assertFalse(isextension('test', ('.jpg', '.png')))

        self.assertFalse(isextension('', '.jpg'))
        self.assertFalse(isextension('', ('.jpg',)))
        self.assertFalse(isextension('', ('.jpg', '.png')))

        self.assertFalse(isextension('.', '.jpg'))
        self.assertFalse(isextension('.', ('.jpg',)))
        self.assertFalse(isextension('.', ('.jpg', '.png')))
