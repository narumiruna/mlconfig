import unittest
from mlconfig.collections import AttrDict


class TestAttrDict(unittest.TestCase):

    def test_init(self):
        d = AttrDict(a=1, b=2)
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 2)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
