import unittest
from mlconfig.utils import load_dict


class TestUtils(unittest.TestCase):

    def test_load_dict(self):
        data = {
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

        yaml_path = 'tests/test.yaml'
        json_path = 'tests/test.json'

        yaml_data = load_dict(yaml_path)
        json_data = load_dict(json_path)

        self.assertDictEqual(data, yaml_data)
        self.assertDictEqual(data, json_data)
        self.assertDictEqual(yaml_data, json_data)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
