import unittest
from mlconfig.collections import AttrDict


class TestAttrDict(unittest.TestCase):

    def test_init(self):
        d = AttrDict(a=1, b=2)
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 2)

    def test_flat(self):
        data = {'a': 0, 'b': {'c': 1, 'd': {'e': 2, 'f': 3}}}

        d1 = AttrDict(data).flat()
        d2 = {'a': 0, 'b.c': 1, 'b.d.e': 2, 'b.d.f': 3}

        self.assertDictEqual(d1, d2)

    def test_to_dict(self):
        d = AttrDict()
        d.a = 0
        d.b = 1

        self.assertEqual(d.to_dict(), d)

    def test_immutable(self):
        d = AttrDict()
        d.set_immutable()

        with self.assertRaises(AttributeError):
            d.a = 0

    def test_is_immutable(self):
        d = AttrDict(a=0, b=1)
        self.assertFalse(d.is_immutable())

        d.set_immutable()
        self.assertTrue(d.is_immutable())
