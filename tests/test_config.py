import unittest
import mlconfig


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
        d = {'name': 'AddOperator', 'a': a, 'b': b}
        config = mlconfig.Config(d)

        obj = mlconfig.create_object(config)
        self.assertEqual(obj.add(), a + b)
