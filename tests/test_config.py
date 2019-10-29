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
