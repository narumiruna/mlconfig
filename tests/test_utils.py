import os
import tempfile
import unittest

from mlconfig.utils import load_dict, save_dict


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.data = {
            'trainer': {
                'name': 'ImageClassificationTrainer',
                'num_epochs': 20,
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
            },
        }

        self.yaml_path = os.path.join(tempfile.gettempdir(), 'test.yaml')
        self.json_path = os.path.join(tempfile.gettempdir(), 'test.json')

    def test_save_dict(self):
        save_dict(self.data, self.yaml_path)
        save_dict(self.data, self.json_path)

    def test_load_dict(self):
        yaml_data = load_dict(self.yaml_path)
        json_data = load_dict(self.json_path)

        self.assertDictEqual(self.data, yaml_data)
        self.assertDictEqual(self.data, json_data)
        self.assertDictEqual(yaml_data, json_data)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
